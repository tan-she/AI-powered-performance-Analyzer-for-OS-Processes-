import psutil
import numpy as np
import tkinter as tk
from sklearn.linear_model import LinearRegression
from collections import deque
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

# Store last 20 values for better visualization
cpu_history = deque(maxlen=20)
memory_history = deque(maxlen=20)
disk_history = deque(maxlen=20)

# Define thresholds for color coding
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 75
DISK_THRESHOLD = 90

# Create GUI window
root = tk.Tk()
root.title("AI-Powered Performance Analyzer")
root.geometry("700x500")

# Labels for system usage
tk.Label(root, text="System Performance Monitor", font=("Arial", 14, "bold")).pack(pady=5)

cpu_label = tk.Label(root, text="CPU Usage: ", font=("Arial", 12))
cpu_label.pack()
cpu_bar = ttk.Progressbar(root, length=300, mode="determinate")
cpu_bar.pack()

memory_label = tk.Label(root, text="Memory Usage: ", font=("Arial", 12))
memory_label.pack()
memory_bar = ttk.Progressbar(root, length=300, mode="determinate")
memory_bar.pack()

disk_label = tk.Label(root, text="Disk Usage: ", font=("Arial", 12))
disk_label.pack()
disk_bar = ttk.Progressbar(root, length=300, mode="determinate")
disk_bar.pack()

prediction_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="blue")
prediction_label.pack()

# Create a Matplotlib figure for real-time graph
fig = Figure(figsize=(6, 2), dpi=100)
ax = fig.add_subplot(111)
ax.set_title("CPU Usage Over Time")
ax.set_ylim(0, 100)  # CPU usage is between 0-100%
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("CPU Usage (%)")
ax.grid(True)

line, = ax.plot([], [], "r-", label="CPU Usage")
ax.legend(loc="upper right")

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Function to update system stats
def update_monitor():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    # Update labels and progress bars
    cpu_label.config(text=f"CPU Usage: {cpu_usage:.1f}%")
    memory_label.config(text=f"Memory Usage: {memory_usage:.1f}%")
    disk_label.config(text=f"Disk Usage: {disk_usage:.1f}%")

    cpu_bar["value"] = cpu_usage
    memory_bar["value"] = memory_usage
    disk_bar["value"] = disk_usage

    # Change bar color based on thresholds
    cpu_color = "green" if cpu_usage < 50 else "orange" if cpu_usage < CPU_THRESHOLD else "red"
    memory_color = "green" if memory_usage < 50 else "orange" if memory_usage < MEMORY_THRESHOLD else "red"
    disk_color = "green" if disk_usage < 50 else "orange" if disk_usage < DISK_THRESHOLD else "red"

    cpu_label.config(fg=cpu_color)
    memory_label.config(fg=memory_color)
    disk_label.config(fg=disk_color)

    # Store data
    cpu_history.append(cpu_usage)
    memory_history.append(memory_usage)
    disk_history.append(disk_usage)

    # Predict future CPU usage using AI
    if len(cpu_history) >= 10:
        def predict_next(values):
            X = np.array(range(len(values))).reshape(-1, 1)
            y = np.array(values)
            model = LinearRegression().fit(X, y)
            return model.predict([[len(values)]])[0]

        predicted_cpu = predict_next(cpu_history)
        predicted_memory = predict_next(memory_history)
        predicted_disk = predict_next(disk_history)

        prediction_label.config(text=f"🔮 Predicted CPU: {predicted_cpu:.2f}%, Memory: {predicted_memory:.2f}%, Disk: {predicted_disk:.2f}%", fg="yellow")

    # Update graph
    line.set_xdata(range(len(cpu_history)))
    line.set_ydata(cpu_history)
    ax.set_xlim(0, len(cpu_history))
    canvas.draw()

    # Refresh data every 2 seconds
    root.after(2000, update_monitor)

# Start monitoring
update_monitor()
root.mainloop()
