from pathlib import Path
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import json
import os
MALICIOUS = "results/holl/MALICIOUS-outcomes-n5/2025-03-22T21-55"
GENTLE_GLOBAL = "results/sas/GENTLE-outcomes-n5-d30"
STRONG_GLOBAL = "results/holl/STRONG-outcomes-n5/glob"
UNCOR_DEPOL = "results/sas/UNCOR_DEPOL-outcomes-n5-d30"
DEPOL = "results/sas/DEPOL-outcomes-n5-d30"
plots_folder = "results/plots"


colorful = True
threshold_values = ([1, 0.10, 0.08, 0.05])
folder = MALICIOUS

noise_type = folder.split('/')[2].split('-')[0]

if noise_type in ["MALICIOUS", "GENTLE", "STRONG"] :
    sampled_circuits = "gospel/cluster/sampled_circuits.holl.txt"
else :
    sampled_circuits = "gospel/cluster/sampled_circuits.sas.txt"
d = 100
s = 100


# delta = 0.15
# delta = 0
delta = 0.5-1/np.e

bqp_error=0.4
with Path(sampled_circuits).open() as f:
    circuits = json.load(f)

def find_correct_value(circuit_name):
    with Path("circuits/table.json").open() as f:
        table = json.load(f)
        # return 1 if yes instance
        # return 0 else (no instance, as circuits are already filtered)
        # print(table[circuit_name])
        return(int(table[circuit_name] > 1-bqp_error))
    
def find_prob(circuit_name):
    with Path("circuits/table.json").open() as f:
        table = json.load(f)
        return(table[circuit_name])


files_dict = {}
for file in os.listdir(folder):
    file_path=os.path.join(folder, file)
    if ".json" in file_path and "raw" not in file_path:
        prob = float(file.split(".json")[0].split("p")[1])
        files_dict[prob] = file_path
    
p_values = np.array(sorted(list([float(i) for i in files_dict.keys()])))
if noise_type == "UNCOR_DEPOL":
    p_values = p_values[:-1]
elif noise_type == "DEPOL":
    p_values = p_values[:-1]
print(p_values)

def get_harold_table():
    harold_table = pd.DataFrame()
    harold_table.index = circuits
    harold_table["Sampling p(meas = 1)"] = [find_prob(circuit_name=circuit) for circuit in harold_table.index]
    return harold_table

def get_failure_rate(threshold_values:list[float]):
    harold_table = get_harold_table()

    plot_data = pd.DataFrame()
    plot_data.index = p_values
    average_wrong_decisions_list = []
    proportion_failed_instances_dict = {w:[] for w in threshold_values}
    test_round_failure_list = []

    # harold_table = pd.DataFrame()
    for prob in p_values:
        file_path = files_dict[prob]
        with open(file_path, 'r') as file:
            json_data = json.load(file)

        # Convert JSON data to DataFrame
        df = pd.DataFrame.from_dict(json_data, orient='index')

        # Recording test round failure rate
        test_round_failure_rate = df["n_failed_trap_rounds"].mean()/s
        test_round_failure_list.append(test_round_failure_rate)
        
        # Recording failed instances (number of wrong decisions, and number of wrongly-decided instances after majority vote)
        df["bqp_error"] = [find_prob(circuit) for circuit in df.index]
        df["expected_outcome"] = [find_correct_value(circuit) for circuit in df.index]
        df["majority vote outcome"] = df["outcome_sum"].apply(lambda s : int(s>d/2))

        # This lambda returns the number of bad decisions for `circuit` if the number of `1` obtained is `s`.
        test_lambda = lambda s, circuit : (d-s) if find_correct_value(circuit_name=circuit) else s
        wrong_decisions = [test_lambda(s=df.loc[circuit]["outcome_sum"], circuit=circuit)/d for circuit in df.index]
        average_wrong_decisions = sum(wrong_decisions)/len(circuits)
        average_wrong_decisions_list.append(average_wrong_decisions)

        print(f"p={prob} gave on average {average_wrong_decisions*d}% wrong decisions")
        harold_table[f"# wrong decisions p{prob}"] = wrong_decisions
        # df["outcome_sum"].apply(lambda s: s if find_correct_value(circuit_name=) else (d-s))

        # print(harold_table)
        for w in (threshold_values):
            proportion_wrong_outcomes = len(df[(df['majority vote outcome'] != df["expected_outcome"]) 
                                               & (df["n_failed_trap_rounds"] < w*s)
                                               & (abs(df["bqp_error"]-0.5 >= delta))
                                               ])
            accepted_instances =  df[(df["n_failed_trap_rounds"] < w*s)]
            filtered_accepted_instances = df[
                (abs(df["bqp_error"]-0.5 >= delta))
                & (df["n_failed_trap_rounds"] < w*s)
                ]
            if len(filtered_accepted_instances) != 0:
                # proportion = proportion_wrong_outcomes/len(circuits)
                proportion = proportion_wrong_outcomes/len(filtered_accepted_instances)
            else:
                proportion = None
            proportion_failed_instances_dict[w].append(proportion)
            # proportion_failed_instances_dict[w].append(proportion_wrong_outcomes/len(df[
            #     (abs(df["bqp_error"]-0.5 >= delta))
            #     & (df["n_failed_trap_rounds"] < w*s)
            #     ]))

            print(f"w={w}, p={prob} => {proportion_wrong_outcomes} instances /100 gave more than 50% wrong decisions")
            if proportion_wrong_outcomes != 0:
                print("Incorrect decision dataframe")
                print(df[df['majority vote outcome'] != df["expected_outcome"]])
                print("#######")

        df.to_csv(f"{folder}/summary-p{prob}.csv")
        # print("Too fragile instances")
        # print(df[(df['bqp_error'] > 0.3) & (df['bqp_error'] < 0.7)])
    
    plot_data["Average wrong decisions"] = average_wrong_decisions_list

    for w in threshold_values:
        plot_data[f"Proportion of failed instances (w={w})"] = proportion_failed_instances_dict[w]
    plot_data["Test round failure rate"] = test_round_failure_list

    return plot_data, harold_table



colors_list = [
    ("red", "white"),
    ("orange", "lightsalmon"),
    ("green", "lightgreen"),
    ("blue", "lightblue"),
]
colors = {threshold_values[i]:colors_list[i] for i in range(len(threshold_values))}

# colors = {1: 'green', 0.08: 'blue', 0.15: 'red', 0.25: 'orange'}
# zone_colors = {1: 'lightgreen', 0.08: 'lightblue', 0.15: 'lightcoral', 0.25: 'lightsalmon'}

boundary_lines = sorted(threshold_values)  # Ensure correct order

plot_data, harold_table = get_failure_rate(threshold_values=threshold_values)
harold_table.to_csv(f"{folder}/final-summary.csv")
plot_data.to_csv(f"{folder}/final-summary-wrong_decisions.csv")





plt.figure()
# plt.title(f"Proportion of corrupted instances accepted according to threshold $\omega$, $|c|<{round(0.5-delta, 3)}$, {noise_type}")
plt.xlabel('$p_{err}$')
plt.ylim(0, 1)
if noise_type in ["MALICIOUS", "GENTLE", "STRONG"] :
    plt.xlim(0, 1)

# Coloring horizontal zones
opacity = 0.5  # Adjust opacity here
for i in range(len(boundary_lines)):
    lower = boundary_lines[i - 1] if i > 0 else 0  # Start from 0
    upper = boundary_lines[i]
    if colorful:
        plt.axhspan(lower, upper, color=colors[upper][1], alpha=opacity, edgecolor='black', linewidth=1)
    else:
        plt.axhspan(lower, upper, color="white", alpha=opacity, edgecolor='black', linewidth=1)

prob_values = np.array([min(t*2, 1) for t in threshold_values])

if colorful:
    # Adding hatched regions
    for i in range(len(boundary_lines)):
        lower = boundary_lines[i - 1] if i > 0 else 0
        upper = boundary_lines[i]

        if upper == threshold_values[3]:
            plt.fill_between(prob_values, lower, upper, where=(prob_values >= 0.1), 
                            facecolor='none', hatch='/', edgecolor='black', linewidth=1)
        elif upper == threshold_values[2]:
            plt.fill_between(prob_values, lower, upper, where=(prob_values >= 0.16), 
                            facecolor='none', hatch='\\', edgecolor='black', linewidth=1)
        elif upper == threshold_values[1]:
            plt.fill_between(prob_values, lower, upper, where=(prob_values >= 0.2), 
                            facecolor='none', hatch='/', edgecolor='black', linewidth=1)
        # elif upper == 1:  # Hatch the entire zone
        #     plt.fill_between(p_values, lower, upper, 
        #                     facecolor='none', hatch='\\', edgecolor='gray', linewidth=0)

# Scatter plots
for w in threshold_values:
    plt.scatter(p_values, plot_data[f"Proportion of failed instances (w={w})"], 
                label=f"$\omega={w}$", marker="o", color=colors[w][0])

plt.scatter(p_values, plot_data["Test round failure rate"], 
            label="Proportion of failed test rounds", marker="*", color='black')

plt.gcf().set_size_inches(10, 6)
plt.legend()
plt.savefig(plots_folder + "/" + noise_type + ".pdf", bbox_inches='tight')
plt.show()




# filename = "wrong-decisions-prob.csv"

# # Open the file for writing
# with open(filename, mode="w", newline="") as file:
#     writer = csv.writer(file)
    
#     # Write header row
#     writer.writerow(["Threshold"] + p_values)
    
#     # Compute and write failure rates
#     for t in threshold_values:
#         proportion_wrong_outcomes_dict = get_failure_rate(t)
#         comp_failure_rates = [proportion_wrong_outcomes_dict[prob] for prob in p_values]
#         print(comp_failure_rates)
#         writer.writerow([t] + comp_failure_rates)

# print(f"Data saved to {filename}")

readmefile = folder + "/README.md"
with open(readmefile, "w") as file:
    if noise_type in ["MALICIOUS", "GENTLE", "STRONG"]:
        content = """
These results have been generated in lines with the following settings:

```
git checkout 629616845598b2c8b932a9014798d0b6989caede
rm -rf circuits
python -m gospel.sampling_circuits.sampling_circuits --ncircuits 1000 --nqubits 5 --depth 30 --p-gate 0.5 --p-cnot 0.25 --p-cnot-flip 0.5 --p-rx 0.5 --seed 1729 --target circuits
git checkout sim-verif
mv gospel/cluster/sampled_circuits.txt gospel/cluster/sampled_circuits.tmp.txt 
cp gospel/cluster/sampled_circuits.holl.txt gospel/cluster/sampled_circuits.txt
    ```
"""
    else:
        content ="""
These results have been generated in lines with the following settings:
```
git checkout 143645c8cedcd2c0e14dd58e991b610ad7385d7a
rm -rf circuits
python -m gospel.sampling_circuits.sampling_circuits --ncircuits 1000 --nqubits 5 --depth 30 --p-gate 0.5 --p-cnot 0.25 --p-cnot-flip 0.5 --p-rx 0.5 --seed 1729 --target circuits
git checkout sim-verif
mv gospel/cluster/sampled_circuits.txt gospel/cluster/sampled_circuits.tmp.txt 
cp gospel/cluster/sampled_circuits.sas.txt gospel/cluster/sampled_circuits.txt
```
"""

    file.write(content)