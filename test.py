import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Hệ tọa độ với Matplotlib trong Tkinter")

# Tạo một figure cho matplotlib
fig, ax = plt.subplots()

# Vẽ các đường lưới (grid lines) và thiết lập giới hạn trục
ax.grid(True)
ax.set_xlim(0, 10)
ax.set_ylim(0, 100)

# Tạo canvas để hiển thị biểu đồ trong cửa sổ Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

# Tạo thanh công cụ tương tác
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack()

# Chạy vòng lặp chính
root.mainloop()
