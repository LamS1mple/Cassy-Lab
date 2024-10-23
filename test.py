import tkinter as tk
import threading
import time

# Tạo một event để dừng luồng khi cần
stop_event = threading.Event()

def background_task():
    for i in range(5):
        if stop_event.is_set():  # Kiểm tra xem event có được kích hoạt không
            break  # Dừng luồng nếu event đã được kích hoạt
        time.sleep(2)  # Giả lập tác vụ nặng, chờ 2 giây
        # Cập nhật giao diện người dùng (UI) thông qua hàm update_label
        app.after(0, update_label, f"Processing {i + 1}/5")
    else:
        app.after(0, update_label, "Task completed!")
    
    # Sau khi dừng hoặc hoàn thành công việc
    app.after(0, update_label, "Thread stopped or completed.")

def update_label(text):
    label.config(text=text)

def start_thread():
    global stop_event
    stop_event.clear()  # Đảm bảo event không bị kích hoạt
    # Tạo và bắt đầu luồng
    thread = threading.Thread(target=background_task)
    thread.start()

def stop_thread():
    stop_event.set()  # Kích hoạt event để dừng luồng

# Tạo giao diện Tkinter
app = tk.Tk()
app.geometry("300x150")

# Label để hiển thị trạng thái
label = tk.Label(app, text="Press start to begin")
label.pack(pady=20)

# Nút để bắt đầu tác vụ trong background
start_button = tk.Button(app, text="Start", command=start_thread)
start_button.pack()

# Nút để dừng tác vụ
stop_button = tk.Button(app, text="Stop", command=stop_thread)
stop_button.pack()

app.mainloop()
