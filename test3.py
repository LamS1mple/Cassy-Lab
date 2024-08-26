import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import numpy as np

# Khởi tạo cửa sổ Tkinter
window = tk.Tk()
window.title("Cập nhật biểu đồ khi bấm F9")

# Tạo figure và axes cho biểu đồ
fig, ax = plt.subplots()

# Dữ liệu ban đầu
x_data = np.linspace(0, 10, 100)
y_data = np.sin(x_data)

# Vẽ biểu đồ ban đầu
line, = ax.plot(x_data, y_data, lw=2)

# Hàm để cập nhật biểu đồ khi bấm F9
def update_plot(event):
    # Cập nhật dữ liệu y với một chút thay đổi
    global y_data
    y_data = np.sin(x_data + np.random.uniform(-0.1, 0.1))  # Tạo sự thay đổi ngẫu nhiên
    
    # Cập nhật dữ liệu cho đường biểu đồ
    line.set_ydata(y_data)
    
    # Vẽ lại biểu đồ
    canvas.draw()
    
    # Cập nhật thông báo trên status bar
    status_bar.config(text="Biểu đồ đã được cập nhật!")

# Tạo canvas để hiển thị biểu đồ trong cửa sổ Tkinter
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Tạo thanh công cụ tương tác
toolbar = NavigationToolbar2Tk(canvas, window)
toolbar.update()
toolbar.pack(side=tk.TOP, fill=tk.X)

# Tạo status bar để hiển thị trạng thái
status_bar = tk.Label(window, text="Nhấn F9 để cập nhật biểu đồ", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Kết nối sự kiện phím F9 với hàm update_plot
window.bind("<F9>", update_plot)

# Khởi chạy ứng dụng Tkinter
window.mainloop()
