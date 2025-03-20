import psutil
import time
import numpy as np
from sklearn.linear_model import LinearRegression
from collections import deque

# Store last 10 values for prediction
cpu_history = deque(maxlen=10)
memory_history = deque(maxlen=10)
disk_history = deque(maxlen=10)

# Define threshold values
CPU_THRESHOLD = 80  # Alert if CPU usage > 80%
MEMORY_THRESHOLD = 75  # Alert if memory usage > 75%
DISK_THRESHOLD = 90  # Alert if disk usage > 90%

while True:
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    net_io = psutil.net_io_counters()

    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_info.percent}%")
    print(f"Disk Usage: {disk_usage.percent}%")
    print(f"Network Sent: {net_io.bytes_sent / (1024 * 1024):.2f} MB")
    print(f"Network Received: {net_io.bytes_recv / (1024 * 1024):.2f} MB")

    # Store data in history
    cpu_history.append(cpu_usage)
    memory_history.append(memory_info.percent)
    disk_history.append(disk_usage.percent)

    # Detect bottlenecks
    if cpu_usage > CPU_THRESHOLD:
        print("⚠️ High CPU Usage! Consider closing unnecessary applications.")

    if memory_info.percent > MEMORY_THRESHOLD:
        print("⚠️ High Memory Usage! Try freeing up RAM or closing heavy processes.")

    if disk_usage.percent > DISK_THRESHOLD:
        print("⚠️ High Disk Usage! Check for large files or background processes.")

    # Predict future values if we have enough data
    if len(cpu_history) == 10:
        def predict_next(values):
            X = np.array(range(10)).reshape(-1, 1)
            y = np.array(values)
            model = LinearRegression().fit(X, y)
            return model.predict([[10]])[0]

        predicted_cpu = predict_next(cpu_history)
        predicted_memory = predict_next(memory_history)
        predicted_disk = predict_next(disk_history)

        print(f"🔮 Predicted Next CPU Usage: {predicted_cpu:.2f}%")
        print(f"🔮 Predicted Next Memory Usage: {predicted_memory:.2f}%")
        print(f"🔮 Predicted Next Disk Usage: {predicted_disk:.2f}%")

    print("\n" + "-"*40 + "\n")
    time.sleep(3)
