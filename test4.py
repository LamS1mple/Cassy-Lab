import tkinter as tk
from tkinter import ttk

def correct_action():
    print("Correct button clicked")

def delete_action():
    print("Delete button clicked")

def help_action():
    print("Help button clicked")

def close_action():
    root.destroy()

root = tk.Tk()
root.title("Sensor Input Settings")

# Frame for the main content
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Input A1 label and display
ttk.Label(frame, text="Input A1:").grid(row=0, column=0, sticky=tk.W)
ttk.Label(frame, text="No Sensor Box").grid(row=0, column=1, sticky=tk.W)

# Quantity dropdown
ttk.Label(frame, text="Quantity:").grid(row=1, column=0, sticky=tk.W)
quantity = ttk.Combobox(frame, values=["Voltage UA1"])
quantity.set("Voltage UA1")
quantity.grid(row=1, column=1, sticky=(tk.W, tk.E))

# Meas. Range dropdown
ttk.Label(frame, text="Meas. Range:").grid(row=2, column=0, sticky=tk.W)
meas_range = ttk.Combobox(frame, values=["-10 V .. 10 V"])
meas_range.set("-10 V .. 10 V")
meas_range.grid(row=2, column=1, sticky=(tk.W, tk.E))

# Record Measured Values section
record_frame = ttk.Labelframe(frame, text="Record Measured Values", padding="10")
record_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))

value_type = tk.StringVar(value="Instantaneous")

tk.Radiobutton(record_frame, text="Instantaneous Values", variable=value_type, value="Instantaneous").grid(row=0, column=0, sticky=tk.W)
tk.Radiobutton(record_frame, text="Averaged Values", variable=value_type, value="Averaged").grid(row=1, column=0, sticky=tk.W)

avg_time_label = ttk.Label(record_frame, text="100 ms")
avg_time_label.grid(row=1, column=1, sticky=tk.W)

tk.Radiobutton(record_frame, text="RMS Values (cos φ)", variable=value_type, value="RMS").grid(row=2, column=0, sticky=tk.W)

# Zero Point section
zero_point_frame = ttk.Labelframe(frame, text="Zero Point", padding="10")
zero_point_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))

zero_point = tk.StringVar(value="Middle")

tk.Radiobutton(zero_point_frame, text="Left", variable=zero_point, value="Left").grid(row=0, column=0, sticky=tk.W)
tk.Radiobutton(zero_point_frame, text="Middle", variable=zero_point, value="Middle").grid(row=0, column=1, sticky=tk.W)
tk.Radiobutton(zero_point_frame, text="Right", variable=zero_point, value="Right").grid(row=0, column=2, sticky=tk.W)

# Buttons
button_frame = ttk.Frame(frame)
button_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.E, tk.W))

ttk.Button(button_frame, text="Correct", command=correct_action).grid(row=0, column=0, sticky=tk.W)
ttk.Button(button_frame, text="Help", command=help_action).grid(row=0, column=1, sticky=tk.W)
ttk.Button(button_frame, text="Delete", command=delete_action).grid(row=0, column=2, sticky=tk.W)
ttk.Button(button_frame, text="Close", command=close_action).grid(row=0, column=3, sticky=tk.W)

root.mainloop()
