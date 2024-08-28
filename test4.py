import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.optimize import curve_fit
import tkinter as tk

def fitStraightLine(x, a, b):
    return a * x + b

def plot_with_tkinter(xFit, yFit):
    # Tạo cửa sổ tkinter
    root = tk.Tk()
    root.title("Đồ Thị Đường Thẳng Fit")

    # Tạo đối tượng Figure
    fig, ax = plt.subplots()

    try:
        # Cung cấp giá trị khởi tạo cho các tham số (a và b)
        initial_guess = [1, 0]  # Giá trị khởi tạo cho a và b
        popt, pcov = curve_fit(fitStraightLine, xFit, yFit, p0=initial_guess)
        a, b = popt
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
        return

    # Vẽ dữ liệu gốc
    ax.scatter(xFit, yFit, label='Dữ liệu')

    # Vẽ đường thẳng fit
    x_range = np.linspace(min(xFit), max(xFit), 100)
    ax.plot(x_range, fitStraightLine(x_range, *popt), color='red', label='Hàm đường thẳng fit')

    ax.legend()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Đường Thẳng Fit')

    # Nhúng Figure vào tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Tạo nút để đóng cửa sổ
    button_quit = tk.Button(master=root, text="Thoát", command=root.quit)
    button_quit.pack(side=tk.BOTTOM)

    # Chạy vòng lặp chính của tkinter
    root.mainloop()

# Dữ liệu mẫu
x = np.linspace(0, 10, 20)
y = 2 * x + 1 + np.random.normal(0, 1, x.shape)

plot_with_tkinter(x, y)
