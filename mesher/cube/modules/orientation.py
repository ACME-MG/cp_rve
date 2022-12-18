"""
 Title:         Orientation
 Description:   For exporting orientation information
 Author:        Janzen Choi

"""

# Libraries
import pyvista as pv
import numpy as np

# Exports the orientations based on the centroid of voxel clusters (i.e., grains)
def export_orientations(stats_path, exodus_path, export_path, tess_length):
    
    # Read the grain statistics from the tessellation
    stats_file = open(stats_path, "r") # (x, y, z, phi_1, Phi, phi_2)
    tess_grains = []
    for row in stats_file.readlines():
        row_list = row.replace("\n", "").split(",")
        row_list = [float(val) for val in row_list]
        tess_grains.append({
            "x":        round(row_list[0], 2),
            "y":        round(row_list[1], 2),
            "z":        round(row_list[2], 2),
            "phi_1":    row_list[3],
            "Phi":      row_list[4],
            "phi_2":    row_list[5],
        })
    stats_file.close()

    # Read in exodus mesh
    all_blocks = pv.read(exodus_path)[0]
    bounds = all_blocks.bounds
    bounds = [[bounds[0], bounds[1]], [bounds[2], bounds[3]], [bounds[4], bounds[5]]]
    
    # Extract the grain statistics from the mesh
    mesh_grains = []
    for block in all_blocks:
        centroid = list(block.center_of_mass())
        centroid = [(centroid[i]-bounds[i][0])/(bounds[i][1]-bounds[i][0])*tess_length for i in range(3)]
        mesh_grains.append({
            "x":        round(centroid[2], 2),
            "y":        round(centroid[1], 2),
            "z":        round(centroid[0], 2),
            "grain":    {}, # allocated tess_grain
            "error":    1000000, # error of allocation
        })

    # Allocate mesh grains to tessellation grains
    for mesh_grain in mesh_grains:
        for tess_grain in tess_grains:
            error = sum([(mesh_grain[i] - tess_grain[i])**2 for i in ["x", "y", "z"]])**(1/2)
            if error < mesh_grain["error"]:
                mesh_grain["error"] = error
                mesh_grain["grain"] = tess_grain

    # Write allocated orientations
    export_file = open(export_path, "w+") # (phi1, Phi, phi2)
    for mesh_grain in mesh_grains:
        phi_1   = mesh_grain["grain"]["phi_1"]
        Phi     = mesh_grain["grain"]["Phi"]
        phi_2   = mesh_grain["grain"]["phi_2"]
        export_file.write(f"{phi_1},{Phi},{phi_2}\n")
    export_file.close()

    # Print conclusion
    average_error = round(np.average([mesh_grain["error"] for mesh_grain in mesh_grains]), 2)
    print(f"Allocated orientations to {len(mesh_grains)} grains")
    print(f"Average euclidean distance error is {average_error}/{tess_length}")