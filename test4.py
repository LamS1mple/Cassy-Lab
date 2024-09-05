import tkinter as tk
from tkinter import Toplevel

def open_custom_dialog():
    dialog = Toplevel(root)
    dialog.title("Custom Dialog")
    
    # Set this window as a transient window (child of the main window)
    dialog.transient(root)
    
    # Optional: Disable the window from being minimized separately
    dialog.grab_set()
    
    label = tk.Label(dialog, text="This is a custom dialog")
    label.pack(pady=10, padx=10)

    button = tk.Button(dialog, text="Close", command=dialog.destroy)
    button.pack(pady=5)

root = tk.Tk()
root.title("Main Application")

button = tk.Button(root, text="Open Dialog", command=open_custom_dialog)
button.pack(pady=20)

root.mainloop()
