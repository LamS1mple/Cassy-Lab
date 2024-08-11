import tkinter as tk
from tkinter import ttk

def update_value(val):
    voltage_value.set(f"UA1 = {float(val):.2f} V")

root = tk.Tk()
root.title("Voltage Display")

# Scale for voltage adjustment
scale_frame = ttk.Frame(root, padding="10")
scale_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

scale = tk.Scale(scale_frame, from_=-10, to=10, orient=tk.HORIZONTAL, length=300,
                 tickinterval=1, resolution=0.01, showvalue=False, command=update_value)
scale.set(0)
scale.grid(row=0, column=0)

# Label to show the current voltage
voltage_value = tk.StringVar()
voltage_value.set("UA1 = 0.00 V")

voltage_label = ttk.Label(scale_frame, textvariable=voltage_value, font=("Arial", 16))
voltage_label.grid(row=1, column=0, pady=10)

root.mainloop()
