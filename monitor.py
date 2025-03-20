
'''
import psutil
import time

while True:
    cpu_usage = psutil.cpu_percent(interval=1)  # CPU usage in %
    memory_info = psutil.virtual_memory()  # Memory usage details

    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_info.percent}%\n")

    time.sleep(1)  # Wait 1 second before refreshing


    #to run the code: python3 monitor.py



import psutil
import time

while True:
    cpu_usage = psutil.cpu_percent(interval=1)  # CPU usage
    memory_info = psutil.virtual_memory()  # Memory usage
    disk_usage = psutil.disk_usage('/')  # Disk usage
    net_io = psutil.net_io_counters()  # Network activity

    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_info.percent}%")
    print(f"Disk Usage: {disk_usage.percent}%")
    print(f"Network Sent: {net_io.bytes_sent / (1024 * 1024):.2f} MB")
    print(f"Network Received: {net_io.bytes_recv / (1024 * 1024):.2f} MB\n")

    time.sleep(1)  # Wait 1 second before refreshing

'''

import psutil
import time

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

    print("\nTop 5 Processes (by CPU usage):")
    process_list = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            cpu_percent = proc.info['cpu_percent']
            if cpu_percent is None:  
                cpu_percent = 0.0  # Set None values to 0.0
            process_list.append((proc.info['pid'], proc.info['name'], cpu_percent))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue  

    # Sort processes by CPU usage in descending order
    for pid, name, cpu in sorted(process_list, key=lambda x: x[2], reverse=True)[:5]:
        print(f"PID: {pid}, Name: {name}, CPU: {cpu}%")

    print("\n" + "-"*40 + "\n")
    time.sleep(3)
