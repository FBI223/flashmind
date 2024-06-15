# timer_factory.py

from interfaces import ITimerApp
from TimerApp import TimerApp_points
from TimerApp import TimerApp_def

def create_timer(root, duration, end_callback, mode) -> ITimerApp:
    if mode == "points":
        return TimerApp_points(root, duration, end_callback)
    elif mode == "def":
        return TimerApp_def(root, duration, end_callback)
    else:
        raise ValueError("Unknown timer mode")