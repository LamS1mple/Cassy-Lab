import tkinter as tk

def show_u1(event):
    label1.config(text="U1")

def show_u2(event):
    label2.config(text="U2")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Vertical Frame Example")

# Tạo frame đầu tiên
frame1 = tk.Frame(root, bg="lightblue")
frame1.grid(row=0, column=0)
frame1.grid_propagate(False)  # Tắt khả năng thay đổi kích thước của frame1

# Tạo frame thứ hai
frame2 = tk.Frame(root, bg="lightgreen")
frame2.grid(row=1, column=0)
frame2.grid_propagate(False)  # Tắt khả năng thay đổi kích thước của frame2

# Thêm nhãn vào các frame để hiển thị U1 và U2
label1 = tk.Label(frame1, text="Click here for U1", bg="lightblue", width=20, height=5)
label1.pack(expand=True)

label2 = tk.Label(frame2, text="Click here for U2", bg="lightgreen", width=20, height=5)
label2.pack(expand=True)

# Gắn sự kiện click vào label
label1.bind("<Button-1>", show_u1)
label2.bind("<Button-1>", show_u2)

# Chạy vòng lặp chính
root.mainloop()
