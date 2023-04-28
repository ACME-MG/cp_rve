def get_real_times(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
    timestamp_list = []
    for line in lines:
        line_list = line.replace("\n", "").split(" ")
        if "results_ELMTS_0" in line_list[0]:
            timestamp_list.append(float(line_list[1]))
    min_timestamp = min(timestamp_list)
    timestamp_diff = [timestamp-min_timestamp for timestamp in timestamp_list]
    return timestamp_diff

def get_sim_times(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
    sim_time_list = []
    for i in range(len(lines)-1):
        line_list = lines[i+1].replace("\n", "").split(",")
        sim_time_list.append(float(line_list[0]))
    return sim_time_list

def normalise(real_times, sim_times, threshold):
    real_times = [real_time for real_time in real_times if real_time <= threshold]
    sim_times = sim_times[:len(real_times)]
    return real_times, sim_times

import matplotlib.pyplot as plt
old_real_times = get_real_times("old_500_24_s1.txt")
old_sim_times = get_sim_times("old_500_24_s1.csv")
old_time_steps = list(range(len(old_sim_times)))
old_real_times, old_sim_times = normalise(old_real_times, old_sim_times, 60000)

new_real_times = get_real_times("new_500_24_s1.txt")
new_sim_times = get_sim_times("new_500_24_s1.csv")
new_time_steps = list(range(len(new_sim_times)))
new_real_times, new_sim_times = normalise(new_real_times, new_sim_times, 60000)

plt.scatter(old_real_times, old_sim_times)
plt.scatter(new_real_times, new_sim_times)
plt.legend(["old", "new"])
plt.xlabel("Real Time")
plt.ylabel("Simulation Time")
plt.savefig("plot.png")