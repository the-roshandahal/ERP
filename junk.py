import time
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk  # Added for progress bar
import subprocess
import os
import webbrowser
import threading  # Added for threading
import chardet  # Added for detecting file encoding

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        return result['encoding']

def start_django():
    global start_button, stop_button, open_browser_button, install_requirements_button
    start_button.destroy()
    install_requirements_button.destroy()

    django_path = r"E:\Github Files\ERP"  # Change to your Django project path
    
    # Start Django server in the foreground
    django_command = f"cd /d {django_path} && python manage.py runserver"
    subprocess.Popen(django_command, shell=True)

    # Wait for Django server to start
    time.sleep(2)
    messages_text.insert(tk.END, "Server Started Successfully\n")

    stop_button = tk.Button(root, text="Stop Program", command=stop_django)
    stop_button.pack(pady=10)

    open_browser_button = tk.Button(root, text="Open Browser", command=open_browser)
    open_browser_button.pack(pady=10)

def stop_django():
    global stop_button, open_browser_button, install_requirements_button, start_button
    subprocess.run(["taskkill", "/im", "python.exe", "/f"])
    stop_button.destroy()
    open_browser_button.destroy()

    start_button = tk.Button(root, text="Start Program", command=start_django)
    start_button.pack(pady=10)
    install_requirements_button = tk.Button(root, text="Install Requirements", command=install_requirements)
    install_requirements_button.pack(pady=10)
    messages_text.insert(tk.END, "Server Closed  Successfully\n")

def open_browser():
    webbrowser.open("http://127.0.0.1:8000/")

def install_requirements():
    global install_requirements_button, messages_text, start_button

    django_path = r"E:\Github Files\ERP"  # Change to your Django project path
    requirements_path = os.path.join(django_path, "requirements.txt")

    try:
        # Change the current working directory
        os.chdir(django_path)

        messages_text.insert(tk.END, "Installing Libraries...\n")

        # Disable the install button during installation
        install_requirements_button.destroy()

        # Create a progress bar
        progress = ttk.Progressbar(root, mode="indeterminate")
        progress.pack(pady=10)
        progress.start()

        # Function to execute installation in a separate thread
        def install():
            try:
                encoding = detect_encoding(requirements_path)
                with open(requirements_path, 'r', encoding=encoding) as file:
                    requirements = file.read().splitlines()

                for req in requirements:
                    req = req.strip()
                    if req:  # Skip empty lines
                        messages_text.insert(tk.END, f"Installing {req} -- ")
                        subprocess.Popen(["pip", "install", req], shell=True).wait()
                        messages_text.insert(tk.END, "Completed\n")

                messagebox.showinfo("Installation", "Requirements installed successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Error installing requirements: {e}")

            # Enable the start button and destroy the progress bar after installation
            start_button = tk.Button(root, text="Start Program", command=start_django)
            start_button.pack(pady=10)
            progress.stop()
            progress.destroy()

        # Start a new thread for the installation
        threading.Thread(target=install).start()

    except FileNotFoundError:
        messagebox.showerror("Error", "pip command not found. Make sure it's installed and in the system PATH.")

    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")

# Create the main window
root = tk.Tk()
root.title("ERP")

# Increase height and width
root.geometry("600x400")

# Add text widget to display messages
messages_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15)
messages_text.pack(pady=10)

# Add button to install requirements
install_requirements_button = tk.Button(root, text="Install Requirements", command=install_requirements)
install_requirements_button.pack(pady=10)

# Add button to start the program
start_button = tk.Button(root, text="Start Program", command=start_django)
start_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()