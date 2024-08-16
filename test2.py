import tkinter as tk
from tkinter import ttk

def create_gui():
    root = tk.Tk()
    root.title("Display Settings")

    # Select Display
    tk.Label(root, text="Select Display:").grid(row=0, column=0, padx=10, pady=5)
    display_combo = ttk.Combobox(root, values=["New Display", "Display 1", "Display 2"])
    display_combo.grid(row=0, column=1, padx=10, pady=5)
    display_combo.current(0)

    # Buttons for New Display and Clear Display
    tk.Button(root, text="New Display").grid(row=0, column=2, padx=10, pady=5)
    tk.Button(root, text="Clear Display").grid(row=0, column=3, padx=10, pady=5)

    # X-Axis and Y-Axis
    tk.Label(root, text="X-Axis:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
    x_axis_combo = ttk.Combobox(root, values=["f1", "f2", "f3"])
    x_axis_combo.grid(row=1, column=1, padx=10, pady=5)
    x_axis_combo.current(0)

    tk.Label(root, text="Y-Axes:").grid(row=1, column=2, padx=10, pady=5, sticky='w')
    y_axis_combo = ttk.Combobox(root, values=["f1", "f2", "f3", "Off"])
    y_axis_combo.grid(row=1, column=3, padx=10, pady=5)
    y_axis_combo.current(1)

    # X-Axis Transformation Options
    x_frame = tk.LabelFrame(root, text="X-Axis Transformation")
    x_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
    
    x_var = tk.StringVar(value="x")
    tk.Radiobutton(x_frame, text="x", variable=x_var, value="x").grid(row=0, column=0, sticky='w')
    tk.Radiobutton(x_frame, text="x²", variable=x_var, value="x²").grid(row=1, column=0, sticky='w')
    tk.Radiobutton(x_frame, text="1/x", variable=x_var, value="1/x").grid(row=2, column=0, sticky='w')
    tk.Radiobutton(x_frame, text="1/x²", variable=x_var, value="1/x²").grid(row=3, column=0, sticky='w')
    tk.Radiobutton(x_frame, text="log x", variable=x_var, value="log x").grid(row=4, column=0, sticky='w')

    # Y-Axis Transformation Options
    y_frame = tk.LabelFrame(root, text="Y-Axis Transformation")
    y_frame.grid(row=2, column=2, columnspan=2, padx=10, pady=10, sticky='ew')
    
    y_var = tk.StringVar(value="y")
    tk.Radiobutton(y_frame, text="y", variable=y_var, value="y").grid(row=0, column=0, sticky='w')
    tk.Radiobutton(y_frame, text="y²", variable=y_var, value="y²").grid(row=1, column=0, sticky='w')
    tk.Radiobutton(y_frame, text="1/y", variable=y_var, value="1/y").grid(row=2, column=0, sticky='w')
    tk.Radiobutton(y_frame, text="1/y²", variable=y_var, value="1/y²").grid(row=3, column=0, sticky='w')
    tk.Radiobutton(y_frame, text="log y", variable=y_var, value="log y").grid(row=4, column=0, sticky='w')

    # Additional Options (Polar, Bars)
    tk.Checkbutton(root, text="Polar").grid(row=3, column=0, padx=10, pady=5, sticky='w')
    tk.Checkbutton(root, text="Bars").grid(row=3, column=2, padx=10, pady=5, sticky='w')

    root.mainloop()

create_gui()
