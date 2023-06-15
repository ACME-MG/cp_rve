from modules.reader import read_csv
csv_dict = read_csv("input/a617_stats.csv")
print(csv_dict.keys())
print(csv_dict["sphericity"])