import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import subprocess
import threading
import time

class CommandScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Command Scheduler")
        self.root.resizable(False, False)
        self.is_running = False
        self.thread = None
        self.execution_count = 0

        # Generate icons
        self.play_icon = self.generate_play_icon(24)
        self.stop_icon = self.generate_stop_icon(24)
        app_icon = self.generate_play_icon(32)

        # Set application icon
        root.iconphoto(False, app_icon)

        # Configure grid layout
        root.grid_columnconfigure(0, weight=1, uniform="buttons")
        root.grid_columnconfigure(1, weight=1, uniform="buttons")

        # Top frame: frequency input and execution count
        top_frame = tk.Frame(root)
        top_frame.grid(row=0, column=0, columnspan=2, sticky='ew', padx=10, pady=5)
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=0)
        top_frame.grid_columnconfigure(2, weight=1)

        tk.Label(top_frame, text="Interval (minutes):").grid(row=0, column=0, sticky='w')
        self.interval_entry = tk.Entry(top_frame, width=10)
        self.interval_entry.grid(row=0, column=1, padx=(5, 10))

        self.execution_label = tk.Label(top_frame, text="Executions: 0")
        self.execution_label.grid(row=0, column=2, sticky='e')

        # Command input section
        tk.Label(root, text="Shell Command:").grid(row=1, column=0, sticky='w', padx=10, pady=(10, 0))

        self.command_text = tk.Text(root, height=4, width=34)
        self.command_text.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10))

        # Action buttons
        self.start_button = tk.Button(
            root, image=self.play_icon, command=self.start_execution, padx=10
        )
        self.start_button.grid(row=3, column=0, pady=15, padx=(10, 5), sticky='ew')

        self.stop_button = tk.Button(
            root, image=self.stop_icon, command=self.stop_execution, state='disabled', padx=10
        )
        self.stop_button.grid(row=3, column=1, pady=15, padx=(5, 10), sticky='ew')

    def generate_play_icon(self, size):
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        margin = size // 4
        points = [(margin, margin), (margin, size - margin), (size - margin, size // 2)]
        draw.polygon(points, fill="green")
        return ImageTk.PhotoImage(img)

    def generate_stop_icon(self, size):
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        margin = size // 4
        draw.rectangle(
            [margin, margin, size - margin, size - margin],
            fill="red"
        )
        return ImageTk.PhotoImage(img)

    def execute_command_periodically(self, interval_minutes, command):
        while self.is_running:
            subprocess.Popen(command, shell=True)
            self.execution_count += 1
            self.execution_label.config(text=f"Executions: {self.execution_count}")
            for _ in range(interval_minutes * 60):
                if not self.is_running:
                    return
                time.sleep(1)

    def start_execution(self):
        try:
            interval = int(self.interval_entry.get())
            command = self.command_text.get("1.0", tk.END).strip()
            if not command:
                messagebox.showerror("Input Error", "Please provide a command to execute.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Interval must be a valid number.")
            return

        self.execution_count = 0
        self.execution_label.config(text="Executions: 0")
        self.is_running = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')

        self.thread = threading.Thread(
            target=self.execute_command_periodically,
            args=(interval, command),
            daemon=True
        )
        self.thread.start()

    def stop_execution(self):
        self.is_running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = CommandScheduler(root)
    root.mainloop()
