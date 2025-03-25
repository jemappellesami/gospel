#!/bin/bash

# rm -rf circuits
# python -m gospel.sampling_circuits.experiments

n_instances=100
bqp_error=0.4
# python -m gospel.cluster.generate_circuit_sample $n_instances $bqp_error

n_comp_run=100
n_test_run=100
n_nodes=$n_instances

echo "Simulations on h-oll circuits"
# Generate circuits and samples from h-oll
# git checkout 629616845598b2c8b932a9014798d0b6989caede
# rm -rf circuits
# python -m gospel.sampling_circuits.sampling_circuits --ncircuits 1000 --nqubits 5 --depth 30 --p-gate 0.5 --p-cnot 0.25 --p-cnot-flip 0.5 --p-rx 0.5 --seed 1729 --target circuits
# git checkout sim-verif
mv gospel/cluster/sampled_circuits.txt gospel/cluster/sampled_circuits.tmp.txt 
cp gospel/cluster/sampled_circuits.holl.txt gospel/cluster/sampled_circuits.txt

# echo "MALICIOUS"
# # Malicious model
# for p_err in 0.1 0.25 0.35 0.45 0.55 0.65 0.75 0.85 0.95; do
#   PORT=24396

# #   # Print p and assigned port
# #   echo "Running with p_err=$p_err, PORT=$PORT"

#   # Run the process in the background locally
#   # python -m gospel.cluster.run_veriphix-malicious $n_comp_run $n_test_run $n_instances $p_err $bqp_error

#   # Run the process in the background on the cluster
#   python -m gospel.cluster.run_veriphix-malicious $n_comp_run $n_test_run $n_instances $p_err $bqp_error --walltime 6 --memory 4 --cores 4 --port $PORT --scale $n_nodes &

# done

# # Gentle Global Noise
# for p_err in 0.05 0.10 0.20 0.30 0.40 0.50 0.60 0.70 0.80 0.90 1.00 ; do
#   PORT=35407

#   # Print p and assigned port
#   echo "Running with p_err=$p_err, PORT=$PORT"

#   # Run the process in the background locally
#   # time python -m gospel.cluster.run_veriphix $n_comp_run $n_test_run $n_instances $p_err $bqp_error --scale 12  

#   # Run the process in the background on the cluster
#   (time python -m gospel.cluster.run_veriphix $n_comp_run $n_test_run $n_instances $p_err $bqp_error --walltime 3 --memory 4 --cores 4 --port $PORT --scale $n_nodes) 2>> exec_times.log

# done

# echo "STRONG GLOBAL NOISE"
# # Strong global noise
# for p_err in 0.5 ; do
#   PORT=24395

#   # Print p and assigned port
#   echo "Running with p_err=$p_err, PORT=$PORT"

#   # Run the process in the background locally
#   #time python -m gospel.cluster.run_veriphix-strong $n_comp_run $n_test_run $n_instances $p_err $bqp_error --scale $n_nodes

#   # Run the process in the background on the cluster
#   nohup python -m gospel.cluster.run_veriphix-strong $n_comp_run $n_test_run $n_instances $p_err $bqp_error --walltime 3 --memory 4 --cores 4 --port $PORT --scale $n_nodes 

# done




echo "Simulations on SAS circuits"
# git checkout 143645c8cedcd2c0e14dd58e991b610ad7385d7a
# rm -rf circuits
# python -m gospel.sampling_circuits.sampling_circuits --ncircuits 1000 --nqubits 5 --depth 30 --p-gate 0.5 --p-cnot 0.25 --p-cnot-flip 0.5 --p-rx 0.5 --seed 1729 --target circuits
# git checkout sim-verif
mv gospel/cluster/sampled_circuits.txt gospel/cluster/sampled_circuits.tmp.txt 
cp gospel/cluster/sampled_circuits.sas.txt gospel/cluster/sampled_circuits.txt

echo "DEPOLARIZING (CORRELATED)"
# Depolarizing
for p_err in 0.0015 0.002 ; do
  PORT=35407

  # Print p and assigned port
  echo "Running with p_err=$p_err, PORT=$PORT"

  # Run the process in the background
  time python -m gospel.cluster.run_veriphix-depol $n_comp_run $n_test_run $n_instances $p_err $bqp_error --walltime 10 --memory 4 --cores 4 --port $PORT --scale $n_nodes &

done

# cp gospel/cluster/sampled_circuits.sas.txt gospel/cluster/sampled_circuits.txt
# echo "DEPOLARIZING (UNCORRELATED)"
# Depolarizing
# for p_err in 0.00005 0.00009 ; do
#   PORT=35407

#   # Print p and assigned port
#   echo "Running with p_err=$p_err, PORT=$PORT"

#   # Run the process in the background
#   time python -m gospel.cluster.run_veriphix-uncorr_depol $n_comp_run $n_test_run $n_instances $p_err $bqp_error --walltime 10 --memory 4 --cores 4 --port $PORT --scale $n_nodes &

# done

# wait  # Ensure all background jobs complete

# echo "All jobs completed!"


# Loaded 100 circuits.
# /home/sabdulsa/miniconda3/envs/gospel/lib/python3.12/site-packages/distributed/node.py:187: UserWarning: Port 35407 is already in use.
# Perhaps you already have a cluster running?
# Hosting the HTTP server on port 43995 instead
#   warnings.warn(
# /home/sabdulsa/miniconda3/envs/gospel/lib/python3.12/site-packages/distributed/node.py:187: UserWarning: Port 35407 is already in use.
# Perhaps you already have a cluster running?
# Hosting the HTTP server on port 39437 instead
#   warnings.warn(
# Loaded 100 circuits.
# Loaded 100 circuits.
# /home/sabdulsa/miniconda3/envs/gospel/lib/python3.12/site-packages/distributed/node.py:187: UserWarning: Port 35407 is already in use.
# Perhaps you already have a cluster running?
# Hosting the HTTP server on port 42813 instead
#   warnings.warn(
# Loaded 100 circuits.