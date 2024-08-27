import matplotlib.pyplot as plt
import numpy as np

# Dữ liệu mẫu
x = [1, 2, 3, 4]
y = [10, 15, 13, 17]

# Tạo đồ thị
fig, ax = plt.subplots()
sc = ax.scatter(x, y, picker=True)

# Hàm xử lý sự kiện click
def onpick(event):
    # Lấy thông tin điểm được click
    if event.artist != sc:
        return
    ind = event.ind
    if isinstance(ind, (list, np.ndarray)):
        ind = ind[0]
    print(f"Clicked data: x={x[ind]}, y={y[ind]}")

# Kết nối sự kiện click với hàm xử lý
fig.canvas.mpl_connect('pick_event', onpick)

plt.show()
