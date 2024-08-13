import tkinter as tk
from tkinter import ttk

def create_gui():
    root = tk.Tk()
    root.title("Quantity Settings")

    # Select Quantity
    tk.Label(root, text="Select Quantity:").grid(row=0, column=0, padx=10, pady=5)
    quantity_combo = ttk.Combobox(root, values=[1, 2, 3, 4, 5])
    quantity_combo.grid(row=0, column=1, padx=10, pady=5)
    quantity_combo.current(1)

    # Buttons for New Quantity and Delete Quantity
    tk.Button(root, text="New Quantity").grid(row=0, column=2, padx=10, pady=5)
    tk.Button(root, text="Delete Quantity").grid(row=0, column=3, padx=10, pady=5)

    # Properties frame
    prop_frame = tk.LabelFrame(root, text="Properties", padx=10, pady=10)
    prop_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

    # Parameter or Formula
    tk.Radiobutton(prop_frame, text="Parameter (Manual Entry in Table or Here) =", value=1).grid(row=0, column=0, sticky='w')
    param_entry = tk.Entry(prop_frame)
    param_entry.grid(row=0, column=1, padx=5)

    tk.Radiobutton(prop_frame, text="Formula (time,date,n,t,UA1,f1) =", value=2).grid(row=1, column=0, sticky='w')
    formula_entry = tk.Entry(prop_frame)
    formula_entry.grid(row=1, column=1, padx=5)

    # Checkboxes for different options
    tk.Checkbutton(prop_frame, text="Derivation over Time from").grid(row=2, column=0, sticky='w')
    tk.Checkbutton(prop_frame, text="Integral over Time from").grid(row=3, column=0, sticky='w')
    tk.Checkbutton(prop_frame, text="Mean Value over").grid(row=4, column=0, sticky='w')
    mean_value_entry = tk.Entry(prop_frame, width=5)
    mean_value_entry.grid(row=4, column=1, sticky='w', padx=5)
    tk.Label(prop_frame, text="s from").grid(row=4, column=2, sticky='w')
    tk.Checkbutton(prop_frame, text="Fast Fourier Transformation from").grid(row=5, column=0, sticky='w')

    # Additional fields (Symbol, Unit, From, To, Decimal Places)
    tk.Label(prop_frame, text="Symbol:").grid(row=6, column=0, sticky='w')
    symbol_entry = tk.Entry(prop_frame, width=5)
    symbol_entry.grid(row=6, column=1, sticky='w', padx=5)

    tk.Label(prop_frame, text="Unit:").grid(row=6, column=2, sticky='w')
    unit_entry = tk.Entry(prop_frame, width=5)
    unit_entry.grid(row=6, column=3, sticky='w', padx=5)

    tk.Label(prop_frame, text="From:").grid(row=7, column=0, sticky='w')
    from_entry = tk.Entry(prop_frame, width=5)
    from_entry.grid(row=7, column=1, sticky='w', padx=5)

    tk.Label(prop_frame, text="To:").grid(row=7, column=2, sticky='w')
    to_entry = tk.Entry(prop_frame, width=5)
    to_entry.grid(row=7, column=3, sticky='w', padx=5)

    tk.Label(prop_frame, text="Decimal Places:").grid(row=8, column=0, sticky='w')
    decimal_entry = tk.Entry(prop_frame, width=5)
    decimal_entry.grid(row=8, column=1, sticky='w', padx=5)

    root.mainloop()

create_gui()
