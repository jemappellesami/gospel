from pathlib import Path
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import csv
import json
import os
import pandas as pd


folder = "results/sas/UNCOR_DEPOL-outcomes-n5-d30"
noise_type = "UNCOR DEPOL"
d = 100
s = 100

bqp_error=0.4
with Path("gospel/cluster/sampled_circuits.txt").open() as f:
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
    
p_values = sorted(list([float(i) for i in files_dict.keys()]))
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
        for w in threshold_values:
            proportion_wrong_outcomes = len(df[(df['majority vote outcome'] != df["expected_outcome"]) & (df["n_failed_trap_rounds"] < w*s)])
            proportion_failed_instances_dict[w].append(proportion_wrong_outcomes/len(circuits))

        print(f"p={prob} => {proportion_wrong_outcomes} instances /100 gave more than 50% wrong decisions")
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


threshold_values = [0.1, 0.6, 0.7]
# colors = {1:'red', 0.08:'blue', 0.15:'green'}
plot_data, harold_table = get_failure_rate(threshold_values=threshold_values)
harold_table.to_csv(f"{folder}/final-summary.csv")
plot_data.to_csv(f"{folder}/final-summary-wrong_decisions.csv")

plt.figure()
plt.title(f"Proportion of corrupted instances accepted according to threshold" + ' $w$ ' + f"({noise_type})")
plt.xlabel('$p_{err}$')
# plt.ylabel("Rate")
plt.ylim(0,1)
# plt.scatter(p_values, plot_data["Average wrong decisions"], label="Average rate of wrong decisions")

for w in threshold_values:
    plt.scatter(p_values, plot_data[f"Proportion of failed instances (w={w})"], label=f"w={w}", marker="o")

plt.scatter(p_values, plot_data["Test round failure rate"], label="Proportion of failed test rounds", marker="*", color='black')
plt.legend()
# plt.grid()
plt.show()
plt.savefig(folder + "plot.png")



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
    file.write(content)