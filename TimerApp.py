import tkinter as tk

from interfaces import ITimerApp
import winsound

class TimerApp_points(ITimerApp):
    def __init__(self, root, duration, end_callback):
        self.root = root
        self.duration = duration
        self.time_left = duration
        self.end_callback = end_callback

        self.root.geometry("+10+10")  # Ustawienie okna w górnym lewym rogu
        self.root.overrideredirect(1)  # Usunięcie ramki okna, aby nie można było go przesuwać

        self.label = tk.Label(root, text="", font=("Helvetica", 44))
        self.label.pack(pady=20)

        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            self.label.config(text=time_format)

            # Change color based on the remaining time
            if  ( self.time_left <= self.duration // 2 ) and (self.time_left > 4 ) :
                self.label.config(fg="orange")
            elif self.time_left <= 4 :
                self.label.config(fg="red")
                winsound.Beep(1000, 100)  # Tick sound
            else:
                self.label.config(fg="black")

            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.label.config(text="00:00")
            winsound.MessageBeep(winsound.MB_OK)
            self.end_callback()

    def destroy(self):
        self.root.destroy()

class TimerApp_def(ITimerApp):
    def __init__(self, root, duration, end_callback):
        self.root = root
        self.duration = duration
        self.time_left = duration
        self.end_callback = end_callback

        self.root.geometry("+10+10")  # Ustawienie okna w górnym lewym rogu
        # self.root.overrideredirect(1)  # Usunięcie ramki okna, aby nie można było go przesuwać

        self.label = tk.Label(root, text="", font=("Helvetica", 34))
        self.label.pack(pady=10)

        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            self.label.config(text=time_format)
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.label.config(text="00:00")
            self.end_callback()

    def destroy(self):
        self.root.destroy()


