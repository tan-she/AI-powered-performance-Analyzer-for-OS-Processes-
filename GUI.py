import psutil
import time
import numpy as np
import tkinter as tk
from sklearn.linear_model import LinearRegression
from collections import deque
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Store last 10 values for predictions
cpu_history = deque(maxlen=10)
memory_history = deque(maxlen=10)
disk_history = deque(maxlen=10)

# Create GUI window
root = tk.Tk()
root.title("AI-Powered Performance Analyzer")
root.geometry("600x400")

# Labels for system usage
cpu_label = tk.Label(root, text="CPU Usage: ", font=("Arial", 12))
cpu_label.pack()
memory_label = tk.Label(root, text="Memory Usage: ", font=("Arial", 12))
memory_label.pack()
disk_label = tk.Label(root, text="Disk Usage: ", font=("Arial", 12))
disk_label.pack()
prediction_label = tk.Label(root, text="", font=("Arial", 12))
prediction_label.pack()

# Create a Matplotlib figure for real-time graph
fig = Figure(figsize=(5, 2), dpi=100)
ax = fig.add_subplot(111)
ax.set_title("CPU Usage Over Time")
ax.set_ylim(0, 100)  # CPU usage is between 0-100%
line, = ax.plot([], [], "r-")

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Function to update system stats
def update_monitor():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    # Update labels
    cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
    memory_label.config(text=f"Memory Usage: {memory_info}%")
    disk_label.config(text=f"Disk Usage: {disk_usage}%")

    # Store data
    cpu_history.append(cpu_usage)
    memory_history.append(memory_info)
    disk_history.append(disk_usage)

    # Predict future CPU usage
    if len(cpu_history) == 10:
        X = np.array(range(10)).reshape(-1, 1)
        y = np.array(cpu_history)
        model = LinearRegression().fit(X, y)
        predicted_cpu = model.predict([[10]])[0]
        prediction_label.config(text=f"🔮 Predicted CPU Usage: {predicted_cpu:.2f}%")

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
