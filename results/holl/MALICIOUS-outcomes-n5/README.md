
These results have been generated in lines with the following settings:

```
git checkout 629616845598b2c8b932a9014798d0b6989caede
rm -rf circuits
python -m gospel.sampling_circuits.sampling_circuits --ncircuits 1000 --nqubits 5 --depth 30 --p-gate 0.5 --p-cnot 0.25 --p-cnot-flip 0.5 --p-rx 0.5 --seed 1729 --target circuits
git checkout sim-verif
mv gospel/cluster/sampled_circuits.txt gospel/cluster/sampled_circuits.tmp.txt 
cp gospel/cluster/sampled_circuits.holl.txt gospel/cluster/sampled_circuits.txt
```
    