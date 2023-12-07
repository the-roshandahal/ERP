import tkinter as tk
import subprocess
import os

def start_django():
    global start_button, stop_button, open_browser_button
    start_button.destroy()

    django_path = r"E:\Github Files\ERP"  # Change to your Django project path
    subprocess.Popen(["cmd", "/c", f"cd /d {django_path} && start /b python manage.py runserver"])

    stop_button = tk.Button(root, text="Stop Program", command=stop_django)
    stop_button.pack(pady=10)

    open_browser_button = tk.Button(root, text="Open Browser", command=open_browser)
    open_browser_button.pack(pady=10)

def stop_django():
    global start_button, stop_button, open_browser_button
    subprocess.run(["taskkill", "/im", "python.exe", "/f"])
    stop_button.destroy()
    open_browser_button.destroy()
    
    start_button = tk.Button(root, text="Start Program", command=start_django)
    start_button.pack(pady=10)

def open_browser():
    os.system("start http://127.0.0.1:8000/")

root = tk.Tk()
root.title("ERP")

# Increase height and width
root.geometry("500x400")

start_button = tk.Button(root, text="Start Program", command=start_django)
start_button.pack(pady=10)

root.mainloop()