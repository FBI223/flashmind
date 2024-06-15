import sqlite3
import subprocess
import time
from datetime import datetime, timedelta
import os
import sys
from win10toast_click import ToastNotifier

# Redirect stdout and stderr to null
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

# Function to handle notification click
def on_notification_clicked():
    script_path = os.path.join(os.getcwd(), "source.py")  # Use .exe if it's an executable
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    #subprocess.run([script_path], startupinfo=startupinfo)
    subprocess.run(["python", script_path] , startupinfo=startupinfo )

# Function to show notification
def show_notification():
    toaster = ToastNotifier()
    toaster.show_toast(
        "Reminder",
        "Click here to open flashcards!",
        icon_path=os.path.join(os.getcwd() , "images" , "logo.ico"),
        duration=5,
        threaded=True,
        callback_on_click=on_notification_clicked
    )
    # Keep the script running while the notification is active
    while toaster.notification_active():
        time.sleep(0.1)

# Function to get interval from database
def get_interval(cursor):
    query = "SELECT INTERWAL FROM Profile LIMIT 1"
    cursor.execute(query)
    first_row = cursor.fetchone()
    if first_row:
        interwal_baza = first_row[0]
    else:
        interwal_baza = "no reminder"

    interval_mapping = {
        "no reminder": timedelta(days=99999),
        "20s": timedelta(seconds=20),
        "1m": timedelta(minutes=1),
        "5m": timedelta(minutes=5),
        "10m": timedelta(minutes=10),
        "30m": timedelta(minutes=30),
        "1h": timedelta(hours=1),
        "2h": timedelta(hours=2),
        "5h": timedelta(hours=5),
        "12h": timedelta(hours=12),
        "1d": timedelta(days=1),
        "2d": timedelta(days=2),
        "7d": timedelta(days=7)
    }

    return interval_mapping.get(interwal_baza, timedelta(days=99999))

# Function to get the last notification time from database
def get_last_notification_time(cursor):
    query = "SELECT OSTATNIE_POWIADOMIENIE FROM Profile LIMIT 1"
    cursor.execute(query)
    first_row = cursor.fetchone()
    if first_row:
        try:
            return datetime.strptime(first_row[0], "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            return datetime.min  # Return a very old date if the format is incorrect
    else:
        return datetime.now()

def main():
    sciezka = os.path.join(os.getcwd(), "fiszki.db")

    while True:
        db = sqlite3.connect(sciezka)
        cursor = db.cursor()

        last_notification_time = get_last_notification_time(cursor)
        interval = get_interval(cursor)

        if last_notification_time + interval < datetime.now():
            show_notification()
            cursor.execute("UPDATE Profile SET OSTATNIE_POWIADOMIENIE = ?", (datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),))
            db.commit()

        db.close()
        time.sleep(10)  # Delay for 10 seconds

if __name__ == "__main__":
    try:
        main()
    finally:
        # Restore stdout and stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__