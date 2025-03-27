import psutil
import numpy as np
import tkinter as tk
from sklearn.linear_model import LinearRegression
from collections import deque
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, messagebox

# Store last 20 values for real-time analysis
cpu_history = deque(maxlen=20)
memory_history = deque(maxlen=20)
disk_history = deque(maxlen=20)

# Define alert thresholds
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 75
DISK_THRESHOLD = 90

# Create Modern Dashboard UI
root = tk.Tk()
root.title("🚀 AI-Powered Performance Analyzer")
root.geometry("1000x700")
root.configure(bg="#121212")  # Dark background

# 🖌 Custom Styling
style = ttk.Style()
style.configure("TFrame", background="#1e1e1e")
style.configure("TLabel", font=("Arial", 12), background="#1e1e1e", foreground="white")
style.configure("TProgressbar", troughcolor="#333", background="orange", thickness=10)

# === Main Title ===
tk.Label(root, text="AI-Powered System Monitor", font=("Arial", 18, "bold"), fg="cyan", bg="#121212").pack(pady=10)

# === System Usage Section ===
frame_system = ttk.Frame(root, padding=10, style="TFrame")
frame_system.pack(pady=10, fill="x")

cpu_label = ttk.Label(frame_system, text="CPU Usage:")
cpu_label.grid(row=0, column=0, sticky="w", padx=5)
cpu_bar = ttk.Progressbar(frame_system, length=300, mode="determinate", style="TProgressbar")
cpu_bar.grid(row=0, column=1, padx=5)

memory_label = ttk.Label(frame_system, text="Memory Usage:")
memory_label.grid(row=1, column=0, sticky="w", padx=5)
memory_bar = ttk.Progressbar(frame_system, length=300, mode="determinate", style="TProgressbar")
memory_bar.grid(row=1, column=1, padx=5)

disk_label = ttk.Label(frame_system, text="Disk Usage:")
disk_label.grid(row=2, column=0, sticky="w", padx=5)
disk_bar = ttk.Progressbar(frame_system, length=300, mode="determinate", style="TProgressbar")
disk_bar.grid(row=2, column=1, padx=5)

# === Alerts & Bottleneck Detection ===
bottleneck_label = tk.Label(root, text="✅ System Running Smoothly", font=("Arial", 12, "bold"), fg="green", bg="#121212")
bottleneck_label.pack(pady=5)

# === AI Forecasting ===
prediction_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="yellow", bg="#121212")
prediction_label.pack()

# === Process List Table ===
frame_processes = ttk.Frame(root, padding=10, style="TFrame")
frame_processes.pack(pady=10, fill="x")

process_label = ttk.Label(frame_processes, text="Top 5 High Resource Apps:")
process_label.pack()

columns = ("Process Name", "CPU Usage (%)", "Memory Usage (%)")
process_table = ttk.Treeview(frame_processes, columns=columns, show="headings", height=5)
process_table.pack(pady=5)

for col in columns:
    process_table.heading(col, text=col)
    process_table.column(col, width=200)

# === Optimization Suggestions ===
optimization_label = ttk.Label(root, text="Optimization Suggestions:", font=("Arial", 12, "bold"))
optimization_label.pack()
optimization_text = tk.Label(root, text="", font=("Arial", 12), fg="lightblue", bg="#121212")
optimization_text.pack()

# === Graph Section ===
fig = Figure(figsize=(6, 2), dpi=100)
ax = fig.add_subplot(111)
ax.set_title("CPU Usage Over Time", color="white")
ax.set_ylim(0, 100)
ax.set_xlabel("Time (seconds)", color="white")
ax.set_ylabel("CPU Usage (%)", color="white")
ax.grid(True, color="gray")

line, = ax.plot([], [], "r-", label="CPU Usage")
ax.legend(loc="upper right")

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# === Bottleneck Alert Function ===
def show_alert(message):
    messagebox.showwarning("⚠ Performance Alert!", message)

# === Bottleneck Detection Function ===
def detect_bottlenecks():
    high_cpu = []
    high_memory = []
    top_processes = []
    alert_triggered = False

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            p_info = proc.info
            cpu_usage = p_info['cpu_percent']
            memory_usage = p_info['memory_percent']

            if cpu_usage is not None and memory_usage is not None:
                top_processes.append((p_info['name'], cpu_usage, memory_usage))

                if cpu_usage > CPU_THRESHOLD:
                    high_cpu.append(f"{p_info['name']} (CPU: {cpu_usage:.1f}%)")
                    alert_triggered = True
                if memory_usage > MEMORY_THRESHOLD:
                    high_memory.append(f"{p_info['name']} (Memory: {memory_usage:.1f}%)")
                    alert_triggered = True

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    top_processes = sorted(top_processes, key=lambda x: (x[1], x[2]), reverse=True)[:5]

    # Update process table
    process_table.delete(*process_table.get_children())
    for p in top_processes:
        process_table.insert("", "end", values=(p[0], f"{p[1]:.1f}%", f"{p[2]:.1f}%"))

    # Show alerts
    bottlenecks = []
    if high_cpu:
        bottlenecks.append("⚠ High CPU: " + ", ".join(high_cpu))
    if high_memory:
        bottlenecks.append("⚠ High Memory: " + ", ".join(high_memory))

    if bottlenecks:
        bottleneck_label.config(text="\n".join(bottlenecks), fg="red")
        if alert_triggered:
            show_alert("\n".join(bottlenecks))
    else:
        bottleneck_label.config(text="✅ System Running Smoothly", fg="green")

# === System Monitoring Function ===
def update_monitor():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    # Update progress bars and labels
    cpu_label.config(text=f"CPU Usage: {cpu_usage:.1f}%")
    memory_label.config(text=f"Memory Usage: {memory_usage:.1f}%")
    disk_label.config(text=f"Disk Usage: {disk_usage:.1f}%")

    cpu_bar["value"] = cpu_usage
    memory_bar["value"] = memory_usage
    disk_bar["value"] = disk_usage

    # Store data
    cpu_history.append(cpu_usage)
    memory_history.append(memory_usage)
    disk_history.append(disk_usage)

    # Run bottleneck detection
    detect_bottlenecks()

    # AI Forecasting
    if len(cpu_history) >= 10:
        def predict_next(values):
            X = np.array(range(len(values))).reshape(-1, 1)
            y = np.array(values)
            model = LinearRegression().fit(X, y)
            return model.predict([[len(values)]])[0]

        predicted_cpu = predict_next(cpu_history)
        predicted_memory = predict_next(memory_history)
        predicted_disk = predict_next(disk_history)

        prediction_label.config(text=f"🔮 Predicted CPU: {predicted_cpu:.2f}%, Memory: {predicted_memory:.2f}%, Disk: {predicted_disk:.2f}%")

    # Update graph
    line.set_xdata(range(len(cpu_history)))
    line.set_ydata(cpu_history)
    ax.set_xlim(0, len(cpu_history))
    canvas.draw()

    root.after(2000, update_monitor)

# Start monitoring
update_monitor()
root.mainloop()
