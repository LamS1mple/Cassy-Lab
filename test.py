import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import numpy as np
import matplotlib.animation as animation

# Khởi tạo cửa sổ Tkinter
window = tk.Tk()
window.title("Biểu đồ thời gian thực trong Tkinter")

# Tạo figure và axes cho biểu đồ
fig, ax = plt.subplots()
x_data, y_data = [], []

# Thiết lập giới hạn ban đầu cho trục x và y
ax.set_xlim(0, 10)
ax.set_ylim(-1, 1)

# Vẽ đường biểu đồ ban đầu
line, = ax.plot([], [], lw=2)

# Hàm khởi tạo dữ liệu biểu đồ
def init():
    line.set_data([], [])
    return line,

# Hàm cập nhật dữ liệu cho biểu đồ theo thời gian thực
def update(frame):
    x_data.append(frame)
    y_data.append(np.sin(frame))  # Hàm sin của giá trị frame

    line.set_data(x_data, y_data)

    # Nếu x_data vượt quá giới hạn, cập nhật giới hạn của trục x
    if frame > 10:
        ax.set_xlim(frame - 10, frame)
    
    return line,

# Thiết lập animation để cập nhật biểu đồ mỗi 100ms
ani = animation.FuncAnimation(fig, update, frames=np.linspace(0, 20, 200), init_func=init, blit=True, interval=100, repeat=False)

# Tạo canvas để hiển thị biểu đồ trong cửa sổ Tkinter
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Tạo thanh công cụ tương tác
toolbar = NavigationToolbar2Tk(canvas, window)
toolbar.update()
toolbar.pack(side=tk.TOP, fill=tk.X)

# Khởi chạy ứng dụng Tkinter
window.mainloop()
