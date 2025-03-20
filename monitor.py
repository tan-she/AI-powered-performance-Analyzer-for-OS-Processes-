import psutil
import time
import numpy as np
from sklearn.linear_model import LinearRegression
from collections import deque

# Store the last 10 CPU usage values for prediction
cpu_history = deque(maxlen=10)

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

    # Store CPU usage in history
    cpu_history.append(cpu_usage)

    # Predict future CPU usage if we have enough data
    if len(cpu_history) == 10:
        X = np.array(range(10)).reshape(-1, 1)  # Time steps [0,1,2,...9]
        y = np.array(cpu_history)  # CPU usage values
        model = LinearRegression().fit(X, y)
        predicted_cpu = model.predict([[10]])[0]  # Predict the next CPU usage

        print(f"🔮 Predicted Next CPU Usage: {predicted_cpu:.2f}%")

    print("\n" + "-"*40 + "\n")
    time.sleep(3)
