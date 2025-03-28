 def end_process(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a process")
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
        self.updateGui()

    def cleanup(self):
        self.running = False
        self.root.destroy()
