
These results have been generated in lines with the following settings:
```
git checkout 143645c8cedcd2c0e14dd58e991b610ad7385d7a
rm -rf circuits
python -m gospel.sampling_circuits.sampling_circuits --ncircuits 1000 --nqubits 5 --depth 30 --p-gate 0.5 --p-cnot 0.25 --p-cnot-flip 0.5 --p-rx 0.5 --seed 1729 --target circuits
git checkout sim-verif
mv gospel/cluster/sampled_circuits.txt gospel/cluster/sampled_circuits.tmp.txt 
cp gospel/cluster/sampled_circuits.sas.txt gospel/cluster/sampled_circuits.txt
```
