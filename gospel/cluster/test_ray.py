import ray

# Connect to the existing Ray cluster
ray.init(address="auto")


@ray.remote
def compute_task(x):
    import time

    time.sleep(1)  # Simulate work
    return x * x


# Distribute computation across workers
results = ray.get(compute_task.remote(i) for i in range(10))

print("Ray computation results:", results)
