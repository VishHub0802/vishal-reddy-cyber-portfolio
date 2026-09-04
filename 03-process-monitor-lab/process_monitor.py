import os
import psutil
import time
from datetime import datetime

CPU_THRESHOLD = 50
MEM_THRESHOLD = 50
CHECK_INTERVAL = 5
LOG_FILE = "alerts.log"

def log_alert(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def check_processes():
    my_pid = os.getpid()

    for proc in psutil.process_iter(['cpu_percent']):
        pass

    time.sleep(1)

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        info = proc.info

        if info['pid'] == my_pid:
            continue
        if info['name'] == 'System Idle Process':
            continue

        cpu = round(info['cpu_percent'], 1)
        mem = round(info['memory_percent'], 1)

        if cpu >= CPU_THRESHOLD:
            log_alert(f"[HIGH CPU] {info['name']} (pid {info['pid']}) using {cpu}% CPU")

        if mem >= MEM_THRESHOLD:
            log_alert(f"[HIGH MEM] {info['name']} (pid {info['pid']}) using {mem}% memory")

        if info['status'] == 'zombie':
            log_alert(f"[ZOMBIE] {info['name']} (pid {info['pid']}) is a zombie process")



if __name__ == "__main__":
    print(f"Monitoring processes every {CHECK_INTERVAL} seconds. Press Ctrl+C to stop.\n")
    try:
        while True:
            check_processes()
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\nStopped monitoring.")