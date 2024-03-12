import math

def calculate_host_unit(total_memory, monitoring_mode):
    # Convert total memory from bytes to gigabytes
    total_memory_gb = float(math.ceil(total_memory / (1024 * 1024 * 1024)))
    # Define the host unit mapping based on monitoring mode
    if monitoring_mode == "FULL_STACK":
        host_unit = 0.0
        for memory, increment in [(1.6, 0.10), (4.0, 0.25), (8.0, 0.50), (16.0, 1.0)]:
            if memory == 16 and total_memory_gb > memory:
                host_unit = float(math.ceil((total_memory_gb // 16)))
                break
            elif total_memory_gb <= memory:
                host_unit = increment
                break
            else:
                continue
    elif monitoring_mode == "INFRASTRUCTURE":
        # Initialize host unit to 0.03 for memory <= 64 GB
        host_unit = 0.03
        for memory, increment in [(1.6, 0.03), (4.0, 0.075), (8.0, 0.15), (16.0, 0.3),(32.0, 0.6),(48.0, 0.9),(64.0, 1.0)]:
            if(memory == 64 and total_memory_gb > memory):
                host_unit = 1.0
                break
            elif total_memory_gb <= memory:
                host_unit = increment
                break
            else:
                continue
    else:
        return 0.0  # Unknown monitoring mode

    return host_unit