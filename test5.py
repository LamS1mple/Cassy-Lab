import matplotlib.pyplot as plt
import numpy as np

# Tạo dữ liệu ví dụ ban đầu
x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()
line, = ax.plot(x, y, 'o-', label='sin(x)')

# Biến để lưu trữ trạng thái click
start_index = None
highlighted_line = None

# Sự kiện khi nhấn chuột
def on_press(event):
    global start_index
    if event.inaxes != ax:
        return
    
    # Lưu lại vị trí x bắt đầu
    start_index = np.argmin(np.abs(x - event.xdata))
    print(f"Bắt đầu tại: {start_index}")

# Sự kiện khi di chuyển chuột
def on_motion(event):
    global highlighted_line
    if event.inaxes != ax or start_index is None:
        return
    
    # Xóa đoạn màu được tô trước đó nếu có
    if highlighted_line:
        highlighted_line.remove()
    
    # Xác định vị trí hiện tại
    current_index = np.argmin(np.abs(x - event.xdata))
    
    # Vẽ đoạn màu mới
    if current_index > start_index:
        highlighted_line, = ax.plot(x[start_index:current_index+1], y[start_index:current_index+1], color='red', linewidth=2)
    
    fig.canvas.draw()

# Sự kiện khi thả chuột
def on_release(event):
    global start_index, highlighted_line
    if event.inaxes != ax or start_index is None:
        return
    
    # Xác định vị trí kết thúc
    end_index = np.argmin(np.abs(x - event.xdata))
    
    # Tô màu đoạn từ start_index đến end_index
    if end_index >= start_index:
        highlighted_line, = ax.plot(x[start_index:end_index+1], y[start_index:end_index+1], color='red', linewidth=2)
    
    # Vẽ lại biểu đồ
    fig.canvas.draw()
    
    # Reset trạng thái
    start_index = None

# Kết nối sự kiện với biểu đồ
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)

plt.show()
