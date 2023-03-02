"""
 Title:         Analyser
 Description:   For analysing the results of the simulation
 Author:        Janzen Choi

"""

# Libraries
import matplotlib.pyplot as plt

# Plots curves from the simulation results
def plot_curves(input_directory, output_path, input_tests, directions):

    # Define the directions
    direction_map = {"x": "xx", "y": "yy", "z": "zz"}
    directions = [direction_map[d] for d in directions]
    num_directions = len(directions)

    # Prepare the plots
    figure, axis = plt.subplots(1, num_directions)
    axes = [axis] if num_directions == 1 else axis
    figure.set_size_inches(5*num_directions+num_directions-1, 5)
    for i in range(num_directions):
        axes[i].set_title(f"Strain {directions[i]} against Time")
        axes[i].set_xlabel("Time (s)")
        axes[i].set_ylabel(f"Strain {directions[i]}")

    # Iterate through files
    for input_test in input_tests:

        # Reads the contents of the file
        input_path = f"{input_directory}/{input_test['file']}"
        file = open(input_path, "r")
        all_lines = file.readlines()
        file.close()

        # Get headers and indexes
        headers = all_lines[0].replace("\n","").split(",")
        time_index = headers.index("time")
        strain_index_list = [headers.index(f"mTE_{d}") for d in directions]

        # Extract data
        time_list = []
        strain_list_list = [[] for _ in range(num_directions)]
        for line in all_lines[1:]:
            line = line.replace("\n", "").split(",")
            time_list.append(float(line[time_index]))
            for i in range(num_directions):
                strain_list_list[i] += [float(line[strain_index_list[i]])]

        # Apply time and strain factors
        time_list = [time*input_test["time_factor"] for time in time_list]
        strain_list_list[i] = [strain*input_test["strain_factor"] for strain in strain_list_list[i]]

        # Plot the data
        for i in range(num_directions):
            axes[i].scatter(time_list, strain_list_list[i], marker="o", linewidth=1)
    
    # Format and save
    for i in range(num_directions):
        axes[i].legend([input_test["file"].replace(".csv", "") for input_test in input_tests])
        axes[i].locator_params(axis='x', nbins=7)
    figure.tight_layout(pad=1.0)
    figure.savefig(output_path)