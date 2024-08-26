import tkinter as tk
from tkinter import ttk

def changeValueComboboxDisplay():
    # Hàm trả về các giá trị để hiển thị trong Combobox
    return ["Option 1", "Option 2", "Option 3"]

def show_selected_value():
    selected_value = x_axis_combo.get()
    status_bar.config(text=f"Giá trị chọn: {selected_value}")

# Khởi tạo cửa sổ Tkinter
window = tk.Tk()
window.title("Lấy giá trị Combobox Example")

# Tạo một frame để chứa Combobox và nút
frameDisplay = ttk.Frame(window)
frameDisplay.pack(padx=10, pady=10)

# Tạo Combobox với giá trị từ changeValueComboboxDisplay và trạng thái readonly
x_axis_combo = ttk.Combobox(frameDisplay, values=changeValueComboboxDisplay(), state='readonly')
x_axis_combo.pack()

# Tạo nút để lấy giá trị của Combobox
button = ttk.Button(frameDisplay, text="Lấy giá trị", command=show_selected_value)
button.pack(pady=10)

# Tạo status bar để hiển thị giá trị chọn
status_bar = ttk.Label(window, text="Giá trị chọn: ", anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

# Khởi chạy ứng dụng Tkinter
window.mainloop()
