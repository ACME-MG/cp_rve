"""
 Title:         Visualiser
 Description:   For visualising the results of the simulation
 Author:        Janzen Choi

"""

# Libraries
import matplotlib.pyplot as plt

# Visualises the simulation results
def visualise(input_directory, input_files, output_path):

    # Prepare the plots
    figure, axis = plt.subplots(1, 3)
    figure.set_size_inches(17, 5)
    directions = ["XX", "YY", "ZZ"]
    for i in range(len(directions)):
        axis[i].set_title(f"Strain {directions[i]} against Time")
        axis[i].set_xlabel("Time (s)")
        axis[i].set_ylabel(f"Strain {directions[i]}")

    # Iterate through files
    for input_file in input_files:

        # Reads the contents of the file
        input_path = f"{input_directory}/{input_file}"
        file = open(input_path, "r")
        all_lines = file.readlines()
        file.close()

        # Get headers and indexes
        headers = all_lines[0].replace("\n","").split(",")
        time_index = headers.index("time")
        strain_xx_index = headers.index("mTE_xx")
        strain_yy_index = headers.index("mTE_yy")
        strain_zz_index = headers.index("mTE_zz")

        # Extract data
        time_list, strain_xx_list, strain_yy_list, strain_zz_list = [], [], [], []
        for line in all_lines[1:]:
            line = line.replace("\n", "").split(",")
            time_list.append(float(line[time_index]))
            strain_xx_list.append(float(line[strain_xx_index]))
            strain_yy_list.append(float(line[strain_yy_index]))
            strain_zz_list.append(float(line[strain_zz_index]))

        # Plot the data
        axis[0].scatter(time_list, strain_xx_list, marker="o", linewidth=1)
        axis[1].scatter(time_list, strain_yy_list, marker="o", linewidth=1)
        axis[2].scatter(time_list, strain_zz_list, marker="o", linewidth=1)
    
    # Format and save
    for i in range(3):
        axis[i].legend([input_file.replace(".csv", "") for input_file in input_files])
        axis[i].locator_params(axis='x', nbins=7)
    figure.tight_layout(pad=1.0)
    figure.savefig(output_path)