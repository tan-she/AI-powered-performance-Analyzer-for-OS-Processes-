import psutil
import time

while True:
    cpu_usage = psutil.cpu_percent(interval=1)  # CPU usage in %
    memory_info = psutil.virtual_memory()  # Memory usage details

    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_info.percent}%\n")

    time.sleep(1)  # Wait 1 second before refreshing
