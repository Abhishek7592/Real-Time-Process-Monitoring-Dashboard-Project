import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import threading
import time

class SimpleSystemMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")
        self.root.geometry("750x500")

        self.style = ttk.Style()
        self.style.configure("Red.Horizontal.TProgressbar", foreground='red', background='red')
        self.style.configure("Yellow.Horizontal.TProgressbar", foreground='orange', background='orange')
        self.style.configure("Green.Horizontal.TProgressbar", foreground='green', background='green')

        self.processes = []
        self.running = True

        self.create_widgets()

        threading.Thread(target=self.updateProcesses, daemon=True).start()
        self.updateGui()

    def create_widgets(self):
        mainFrame = ttk.Frame(self.root, padding=10)
        mainFrame.pack(fill=tk.BOTH, expand=True)

        metricsFrame = ttk.LabelFrame(mainFrame, text="System Resources", padding=10)
        metricsFrame.pack(fill=tk.X, pady=5)

        ttk.Label(metricsFrame, text="CPU Usage:").grid(row=0, column=0, sticky="w")
        self.cpuVar = tk.StringVar(value="0%")
        ttk.Label(metricsFrame, textvariable=self.cpuVar).grid(row=0, column=1, sticky="e")
        self.cpuBar = ttk.Progressbar(metricsFrame, length=300, mode='determinate')
        self.cpuBar.grid(row=0, column=2, padx=5, sticky="ew")

        ttk.Label(metricsFrame, text="Memory Usage:").grid(row=1, column=0, sticky="w")
        self.memVar = tk.StringVar(value="0%")
        ttk.Label(metricsFrame, textvariable=self.memVar).grid(row=1, column=1, sticky="e")
        self.memBar = ttk.Progressbar(metricsFrame, length=300, mode='determinate')
        self.memBar.grid(row=1, column=2, padx=5, sticky="ew")

        ttk.Label(metricsFrame, text="Disk Usage:").grid(row=2, column=0, sticky="w")
        self.diskVar = tk.StringVar(value="0%")
        ttk.Label(metricsFrame, textvariable=self.diskVar).grid(row=2, column=1, sticky="e")
        self.diskBar = ttk.Progressbar(metricsFrame, length=300, mode='determinate')
        self.diskBar.grid(row=2, column=2, padx=5, sticky="ew")

        self.tree = ttk.Treeview(mainFrame, columns=('pid', 'name', 'cpu', 'memory'), show='headings')
        self.tree.heading('pid', text='PID')
        self.tree.heading('name', text='Process Name')
        self.tree.heading('cpu', text='CPU %')
        self.tree.heading('memory', text='Memory %')
        self.tree.column('pid', width=80, anchor='center')
        self.tree.column('name', width=250)
        self.tree.column('cpu', width=80, anchor='center')
        self.tree.column('memory', width=80, anchor='center')
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

        btnFrame = ttk.Frame(mainFrame)
        btnFrame.pack(fill=tk.X, pady=5)

        ttk.Button(btnFrame, text="End Process", command=self.end_process).pack(side=tk.LEFT, padx=5)
        ttk.Button(btnFrame, text="Refresh", command=self.refresh).pack(side=tk.LEFT, padx=5)
        ttk.Button(btnFrame, text="CPU Hogs", command=self.find_cpu_hogs).pack(side=tk.LEFT, padx=5)
        ttk.Button(btnFrame, text="Memory Hogs", command=self.find_memory_hogs).pack(side=tk.LEFT, padx=5)
        ttk.Button(btnFrame, text="Exit", command=self.cleanup).pack(side=tk.RIGHT, padx=5)

    def updateProcesses(self):
        while self.running:
            currentProcesses = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    currentProcesses.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu': proc.info['cpu_percent'],
                        'memory': proc.info['memory_percent']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            self.processes = sorted(currentProcesses, key=lambda p: p['cpu'], reverse=True)
            time.sleep(2)

    def updateGui(self):
        if not self.running:
            return

        cpu_usage = psutil.cpu_percent()
        mem_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        self.cpuVar.set(f"{cpu_usage:.1f}%")
        self.memVar.set(f"{mem_usage:.1f}%")
        self.diskVar.set(f"{disk_usage:.1f}%")

        self.updateProgress_bar(self.cpuBar, cpu_usage)
        self.updateProgress_bar(self.memBar, mem_usage)
        self.updateProgress_bar(self.diskBar, disk_usage)

        self.refresh_treeview()

        self.root.after(2000, self.updateGui)

    def updateProgress_bar(self, bar, value):
        bar['value'] = value
        if value > 80:
            bar['style'] = 'Red.Horizontal.TProgressbar'
        elif value > 60:
            bar['style'] = 'Yellow.Horizontal.TProgressbar'
        else:
            bar['style'] = 'Green.Horizontal.TProgressbar'

    def refresh_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for proc in self.processes[:100]:
            self.tree.insert('', 'end', values=(
                proc['pid'],
                proc['name'][:50],
                f"{proc['cpu']:.1f}",
                f"{proc['memory']:.1f}"
            ))

    def end_process(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a process first")
            return

        pid = int(self.tree.item(selected)['values'][0])
        name = self.tree.item(selected)['values'][1]

        try:
            p = psutil.Process(pid)
            response = messagebox.askyesno("Confirm", f"Terminate {name} (PID: {pid})?")
            if response:
                p.terminate()
                messagebox.showinfo("Success", f"Terminated {name} (PID: {pid})")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to terminate process: {e}")

    def refresh(self):
        self.update_gui()

    def find_cpu_hogs(self):
        for item in self.tree.get_children():
            cpu = float(self.tree.item(item)['values'][2])
            if cpu > 30:
                self.tree.tag_configure('cpu_hog', background='#ffdddd')
                self.tree.item(item, tags=('cpu_hog',))

    def find_memory_hogs(self):
        for item in self.tree.get_children():
            memory = float(self.tree.item(item)['values'][3])
            if memory > 10:
                self.tree.tag_configure('mem_hog', background='#ddffdd')
                self.tree.item(item, tags=('mem_hog',))

    def cleanup(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleSystemMonitor(root)
    root.protocol("WM_DELETE_WINDOW", app.cleanup)
    root.mainloop()
