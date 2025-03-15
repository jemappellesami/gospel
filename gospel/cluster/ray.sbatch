#!/bin/bash
#SBATCH --job-name=ray-worker
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=4G
#SBATCH --time=01:00:00
#SBATCH --partition=cpu_devel
#SBATCH --array=0-31

cd gospel
. .venv/bin/activate
ray start --address=10.224.0.2:6379