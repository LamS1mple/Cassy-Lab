import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
import scan_com
import logging
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import asyncio

logging.basicConfig(level=logging.DEBUG)


# ardunio.ardunio(3,1)
window = tk.Tk()
width= window.winfo_screenwidth() 
height= window.winfo_screenheight()
#setting tkinter window size
window.state('zoomed')
# data radio
recording_mode = tk.IntVar(window)


window.title("Geeeks For Geeks")

def start_resize(event):
    global drag_data
    drag_data = {"x": event.x, "y": event.y}

def perform_resize(event):
    global drag_data
    frame = event.widget
    dx = event.x - drag_data["x"] 
    dy = event.y - drag_data["y"]
    if dx > 0:
        dx += 10
    else:
        dx -= 10
    new_width = frame.winfo_width() + dx 
    
    print(1)
    if new_width > 50:  # Đảm bảo kích thước không quá nhỏ
        frame.config(width=new_width)
        drag_data = {"x": event.x, "y": event.y}

def matplotlib():
    # Tạo một khung để chứa canvas và thanh công cụ
    frameTreeView = tk.Frame(window,width=100,padx=20)
    frameTreeView.pack_propagate(False)  # Đảm bảo kích thước của Frame không thay đổi theo nội dung
    frameTreeView.pack(side=tk.LEFT, fill=tk.Y)
    tableView = ttk.Treeview(frameTreeView, show='headings')
    tableView.pack(fill=tk.BOTH,expand=True)
    frameTreeView.bind("<Button-1>", start_resize)
    frameTreeView.bind("<B1-Motion>", perform_resize)

    scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=tableView.yview)
    tableView.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)

    
    # Tạo một figure cho matplotlib
    fig, ax = plt.subplots()
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    # Vẽ các đường lưới (grid lines) và thiết lập giới hạn trục
    ax.grid(True)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 100)

    # Tạo canvas để hiển thị biểu đồ trong cửa sổ Tkinter
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Tạo thanh công cụ tương tác
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    toolbar.pack(side=tk.TOP, fill=tk.X)

def changeValueOptionMenu(data , value):
    global arduino
    try:
        if (value.get() == "Cassy"):
            arduino = serial.Serial(port='{}'.format(scan_com.nameCom[data]), baudrate=9600)
            print("Ket not thanh cong")
            matplotlib()
            

    except NameError:
        value.set("Off")
        print(NameError)


    return
    
def defCassy(frameMain):
    print(1)
def defFFT(frameMain):
    print(2)
def defCommnet(frameMain):
    print(3)
def defGeneral(frameMain):
    frameGeneral = ttk.Frame(frameMain, borderwidth=5, relief="sunken", padding="10")
    frameGeneral.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)


    for i in range(len(scan_com.nameCom)):
        labelCom = ttk.Label(frameGeneral, text=scan_com.nameCom[i], font=("Helvetica", 12))  # Thay đổi cỡ chữ
        labelCom.grid(row=i, column=0, padx=5, pady=10)

        value_inside = tk.StringVar(frameMain) 
        value_inside.set("Off") 
        value_inside.trace_add("write", lambda *args, i=i, value_inside = value_inside: changeValueOptionMenu(i, value_inside))

        question_menu = ttk.OptionMenu(frameGeneral, value_inside, "Off", "Off", "Cassy")
        question_menu.config(width=20)
        


        # Tùy chỉnh phong cách
        style = ttk.Style()
        style.configure('TMenubutton', 
                        font=('Helvetica', 12), 
                        padding=5, 
                        relief='raised',
                        background='#99eee4', 
                        borderwidth=2)

        question_menu.grid(row=i, column=1, columnspan=3, padx=5, pady=10)



# giao dien auto hay bam tay
def measuringParametes():
    newWindow = tk.Toplevel(window)
    newWindow.attributes("-topmost", True)
    main_frame = ttk.Frame(newWindow, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Tạo các thành phần trên giao diện

    auto_radio = ttk.Radiobutton(main_frame, text="Automatic Recording", variable=recording_mode, value="auto")
    manual_radio = ttk.Radiobutton(main_frame, text="Manual Recording", variable=recording_mode, value="manual")
    append_check = ttk.Checkbutton(main_frame, text="Append New Meas. Series")
    meas_interval_label = ttk.Label(main_frame, text="Meas. Interv.:(ms)")
    meas_interval = ttk.Entry(main_frame, width=5)
    meas_interval.insert(0, "2")
    x_number_label = ttk.Label(main_frame, text="x Number:")
    x_number = ttk.Entry(main_frame, width=5)
    x_number.insert(0, "5000")
    trigger_label = ttk.Label(main_frame, text="Trigger:")
    trigger = ttk.Combobox(main_frame, width=5)
    meas_time_label = ttk.Label(main_frame, text="= Meas. Time:")
    meas_time = ttk.Entry(main_frame, width=5)
    meas_time.insert(0, "10")
    time_unit = ttk.Combobox(main_frame, width=3)
    time_unit['values'] = ('s', 'ms', 'us')
    time_unit.set('s')
    
    repeating_check = ttk.Checkbutton(main_frame, text="Repeating Measurement")
    acoustic_check = ttk.Checkbutton(main_frame, text="Acoustic Signal")

    # Đặt các thành phần lên giao diện
    auto_radio.grid(column=0, row=0, sticky=tk.W)
    manual_radio.grid(column=0, row=1, sticky=tk.W)
    append_check.grid(column=0, row=2, sticky=tk.W)
    meas_interval_label.grid(column=1, row=0, sticky=tk.E)
    meas_interval.grid(column=2, row=0, sticky=tk.W)
    x_number_label.grid(column=1, row=1, sticky=tk.E)
    x_number.grid(column=2, row=1, sticky=tk.W)
    trigger_label.grid(column=3, row=0, sticky=tk.E)
    trigger.grid(column=4, row=0, sticky=tk.W)
    meas_time_label.grid(column=1, row=2, sticky=tk.E)
    meas_time.grid(column=2, row=2, sticky=tk.W)
    time_unit.grid(column=3, row=2, sticky=tk.W)
    repeating_check.grid(column=4, row=1, sticky=tk.W)
    acoustic_check.grid(column=4, row=2, sticky=tk.W)

    # Thêm nút "Close" và "Help"
    close_button = ttk.Button(main_frame, text="Close", command=newWindow.destroy)
    help_button = ttk.Button(main_frame, text="Help")
    close_button.grid(column=0, row=3, sticky=tk.W)
    help_button.grid(column=1, row=3, sticky=tk.W)

    # Thiết lập khoảng cách giữa các thành phần
    for child in main_frame.winfo_children(): 
        child.grid_configure(padx=5, pady=5)






def openWindowF5(event=None):

    newWindow = tk.Toplevel(window)
    newWindow.attributes("-topmost", True)
 
    main_frame = ttk.Frame(newWindow, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Tạo phần 1 - 5 button nằm ngang
    frame1 = ttk.Frame(main_frame, borderwidth=5, relief="sunken")
    frame1.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

    button_texts1 = ["CASSY", "Parameter/Formula/FFT`", "Comment", "General"]
    
    # button cassy
    buttonCassy = ttk.Button(frame1, text=button_texts1[0], comman = lambda: defCassy(main_frame) )
    buttonCassy.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
    # button Parameter/Formula/FFT
    buttonCassy = ttk.Button(frame1, text=button_texts1[1], comman = lambda: defFFT(main_frame) )
    buttonCassy.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
    # button commmnet
    buttonCassy = ttk.Button(frame1, text=button_texts1[2], comman = lambda: defCommnet(main_frame) )
    buttonCassy.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
    # button General
    buttonCassy = ttk.Button(frame1, text=button_texts1[3], comman = lambda: defGeneral(main_frame))
    buttonCassy.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)



    # Tạo phần 2 - Chi tiết của các button
    frame2 = ttk.Frame(main_frame, borderwidth=5, relief="sunken", padding="10")
    frame2.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

    defGeneral(main_frame)

    details_label = ttk.Label(frame2, text="Chi tiết sẽ hiển thị ở đây")
    details_label.pack(side=tk.TOP, fill=tk.X)

    # Tạo phần 3 - 4 button khác
    frame3 = ttk.Frame(main_frame, borderwidth=5, relief="sunken", padding="10")
    frame3.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

    
    buttonClose = ttk.Button(frame3, text="Close", command=lambda: newWindow.destroy)
    buttonClose.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=2)

    buttonDisplayMeasuring = ttk.Button(frame3, text="Display Measuring Parameters", command=measuringParametes)
    buttonDisplayMeasuring.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=2)

    # Cấu hình lưới
    newWindow.columnconfigure(0, weight=1)
    newWindow.rowconfigure(0, weight=1)
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=1)
    main_frame.rowconfigure(2, weight=1)

window.bind('<F5>', openWindowF5)

openWindowF5()

window.mainloop()