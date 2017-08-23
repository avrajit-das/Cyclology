from tkinter import *
import time
import threading

from FreeMark.tools.pacer import Pacer


class RemainingTime(Frame):
    """
    GUI element displaying remaining time for a process,
    resembles tkinter's progress bar
    """
    def __init__(self, master=None):
        super().__init__(master)

        # Required GUI elements
        self.remaining_time = IntVar()
        self.description = Label(self, text="Est. time remaining:")
        self.time_label = Label(self, textvariable=self.remaining_time)
        self.unit_label = Label(self, text="Seconds")

        self.pacer = Pacer()

    def set_max(self, _max):
        self.pacer.set_max(_max)

    def start(self):
        """
        Show the element and start the timer
        """
        self.pacer.start()
        self.remaining_time.set(0)  # Set it to 0 till we have the first step
        threading.Thread(target=self._updater).start()
        self.show()

    def step(self):
        """
        Take a step
        """
        self.pacer.step()
        if not self.pacer.running:
            # We're done, hide in shame.
            self.hide()

    def update(self):
        self.remaining_time.set(round(self.pacer.get_estimated_remaining()))

    def _updater(self):
        while self.pacer.running:
            self.update()
            time.sleep(0.5)

    def stop(self):
        self.pacer.reset()
        self.remaining_time.set(0)
        self.hide()

    def hide(self):
        for child in self.winfo_children():
            child.grid_forget()

    def show(self):
        self.description.grid(column=0, row=0)
        self.time_label.grid(column=1, row=0)
        self.unit_label.grid(column=2, row=0)