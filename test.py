import matplotlib.pyplot as plt
import numpy as np

# Tạo dữ liệu ví dụ ban đầu
x = list(np.linspace(0, 10, 100))
y = list(np.sin(x))

fig, ax = plt.subplots()
line, = ax.plot(x, y, 'o-', label='Original Data')

# Biến để lưu trữ các điểm được thêm vào khi di chuyển chuột
added_x = []
added_y = []

# Đồ thị mới sẽ chứa các điểm được thêm vào
new_line, = ax.plot([], [], 'r-o', label='Added Points')

# Sự kiện khi di chuyển chuột
def on_motion(event):
    if event.inaxes != ax:
        return

    # Thêm tọa độ hiện tại vào danh sách các điểm
    x.append(event.xdata)
    y.append(event.ydata)

    # Cập nhật dữ liệu cho đồ thị mới
    line.set_data(x, y)

    # Vẽ lại biểu đồ
    fig.canvas.draw()

# Kết nối sự kiện với biểu đồ
fig.canvas.mpl_connect('motion_notify_event', on_motion)

# Hiển thị chú thích (legend)
ax.legend()

plt.show()
