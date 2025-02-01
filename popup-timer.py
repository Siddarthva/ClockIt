import tkinter as tk
from tkinter import ttk

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Timer")

        self.remaining_time = 0
        self.running = False
        self.paused = False
        self.total_time = 0

        # Input field and labels
        self.entry_label = tk.Label(root, text="Enter time in minutes:")
        self.entry_label.pack(pady=5)

        self.entry = tk.Entry(root)
        self.entry.pack(pady=5)

        # Timer display
        self.timer_label = tk.Label(root, font=("Helvetica", 48), text="00:00")
        self.timer_label.pack(pady=20)

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        # Buttons
        self.start_button = tk.Button(root, text="Start Timer", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.pause_button = tk.Button(root, text="Pause Timer", command=self.pause_timer, state="disabled")
        self.pause_button.pack(pady=5)

        self.reset_button = tk.Button(root, text="Reset Timer", command=self.reset_timer, state="disabled")
        self.reset_button.pack(pady=5)

        self.preset_buttons = tk.Frame(root)
        self.preset_buttons.pack(pady=10)
        for preset in [1, 5, 10]:
            tk.Button(self.preset_buttons, text=f"{preset} min", command=lambda p=preset: self.set_preset(p)).pack(side="left", padx=5)

        # Dark mode toggle
        self.dark_mode_var = tk.BooleanVar()
        self.dark_mode_toggle = tk.Checkbutton(root, text="Dark Mode", variable=self.dark_mode_var, command=self.toggle_dark_mode)
        self.dark_mode_toggle.pack(pady=10)

    def start_timer(self):
        try:
            if not self.running:
                self.remaining_time = int(self.entry.get()) * 60
                self.total_time = self.remaining_time
            self.running = True
            self.paused = False
            self.update_timer()
            self.start_button.config(state="disabled")
            self.pause_button.config(state="normal")
            self.reset_button.config(state="normal")
        except ValueError:
            self.timer_label.config(text="Invalid input!")

    def update_timer(self):
        if self.running and not self.paused:
            if self.remaining_time > 0:
                mins, secs = divmod(self.remaining_time, 60)
                time_format = f"{mins:02d}:{secs:02d}"
                self.timer_label.config(text=time_format)
                self.progress["value"] = (self.total_time - self.remaining_time) / self.total_time * 100
                self.remaining_time -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.timer_label.config(text="Time's up!")
                self.running = False
                self.start_button.config(state="normal")

    def pause_timer(self):
        if self.running:
            self.paused = not self.paused
            if self.paused:
                self.pause_button.config(text="Resume Timer")
            else:
                self.pause_button.config(text="Pause Timer")
                self.update_timer()

    def reset_timer(self):
        self.running = False
        self.paused = False
        self.remaining_time = 0
        self.timer_label.config(text="00:00")
        self.progress["value"] = 0
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")
        self.reset_button.config(state="disabled")

    def set_preset(self, minutes):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(minutes))
        self.start_timer()

    def toggle_dark_mode(self):
        if self.dark_mode_var.get():
            self.root.config(bg="black")
            self.timer_label.config(bg="black", fg="white")
            self.entry_label.config(bg="black", fg="white")
            self.dark_mode_toggle.config(bg="black", fg="white")
        else:
            self.root.config(bg="white")
            self.timer_label.config(bg="white", fg="black")
            self.entry_label.config(bg="white", fg="black")
            self.dark_mode_toggle.config(bg="white", fg="black")


# Create the main window
root = tk.Tk()
app = TimerApp(root)
root.mainloop()
