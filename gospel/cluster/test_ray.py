import pyslurm

# Define job parameters
job_spec = {
    "name": "test_job",
    "nodes": 1,
    "ntasks": 1,
    "time": "00:01:00",
    "partition": "cpu_devel",
    "script": "echo foo",
}

# Submit job
job_id = pyslurm.job().submit_batch_job(job_spec)
print(f"Submitted job ID: {job_id}")
