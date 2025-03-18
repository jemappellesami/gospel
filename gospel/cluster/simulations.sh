#!/bin/bash

rm -rf circuits
python -m gospel.sampling_circuits.experiments

n_comp_run=100
n_test_run=0
n_instances=1000
n_nodes=$n_instances
bqp_error=0.5

for p_err in  0; do
  PORT=24395

  # Print p and assigned port
  echo "Running with p_err=$p_err, PORT=$PORT"

  # Run the process in the background
  time python -m gospel.cluster.run_veriphix $n_comp_run $n_test_run $n_instances $p_err $bqp_error --walltime 3 --memory 4 --cores 4 --port $PORT --scale $n_nodes

done

wait  # Ensure all background jobs complete

echo "All jobs completed!"
