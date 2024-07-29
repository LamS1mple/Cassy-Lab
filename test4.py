import tkinter as tk
from tkinter import PhotoImage

# Khởi tạo cửa sổ chính
window = tk.Tk()
window.title("Custom Cursor Example")

# Tạo một Frame chính với kích thước cố định và màu nền
frame = tk.Frame(window, width=300, height=200, bg='lightblue')
frame.pack_propagate(False)  # Ngăn không cho frame tự động điều chỉnh kích thước
frame.pack()

# Tạo Canvas trong Frame để chứa hình ảnh con trỏ
canvas = tk.Canvas(frame, width=300, height=200, bg='lightblue')
canvas.pack(fill=tk.BOTH, expand=True)

# Tải hình ảnh con trỏ
cursor_image = PhotoImage(file='four-arrows.png')  # Thay đổi đường dẫn hình ảnh con trỏ

# Tạo hình ảnh con trỏ trên Canvas
cursor_id = canvas.create_image(0, 0, image=cursor_image, anchor=tk.NW)
canvas.itemconfig(cursor_id, state=tk.HIDDEN)  # Ẩn hình ảnh con trỏ ngay từ đầu

# Cập nhật vị trí của hình ảnh con trỏ khi di chuyển chuột
def update_cursor_position(event):
    canvas.coords(cursor_id, event.x, event.y)

# Hiển thị con trỏ khi chuột di vào Canvas
def show_cursor(event):
    canvas.itemconfig(cursor_id, state=tk.NORMAL)  # Hiển thị hình ảnh con trỏ
    update_cursor_position(event)

# Ẩn con trỏ khi chuột rời khỏi Canvas
def hide_cursor(event):
    canvas.itemconfig(cursor_id, state=tk.HIDDEN)  # Ẩn hình ảnh con trỏ

# Đặt kiểu con trỏ cho Canvas và Frame
canvas.config(cursor='none')  # Ẩn con trỏ mặc định trên Canvas
frame.config(cursor='none')   # Ẩn con trỏ mặc định trên Frame

# Liên kết sự kiện với các hàm
canvas.bind('<Enter>', show_cursor)
canvas.bind('<Leave>', hide_cursor)
canvas.bind('<Motion>', update_cursor_position)

# Chạy vòng lặp chính của Tkinter
window.mainloop()
