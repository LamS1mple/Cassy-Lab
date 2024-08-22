import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
import scan_com
import logging
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import asyncio
import FFTObject

logging.basicConfig(level=logging.DEBUG)


# ardunio.ardunio(3,1)
window = tk.Tk()
width= window.winfo_screenwidth() 
height= window.winfo_screenheight()
#setting tkinter window size
window.state('zoomed')
# data radio
recording_mode = tk.IntVar(window)

# window
windowF5 = None
showU1Box = None
showU2Box = None
measuringParametesWindow = None

window.title("Geeeks For Geeks")

# global variable
increase = 1
U1 = None
U2 = None
time = 0
n = 0
listFFT = []
indexNameFFT = -2
formulaEntry = tk.StringVar()
symolFFT = tk.StringVar()
unitFFT = tk.StringVar()
decimalPlacesFFT = tk.IntVar()

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


def show_u1_box():
   

    def correct_action():
        print("Correct button clicked")

    def delete_action():
        print("Delete button clicked")

    def help_action():
        print("Help button clicked")

    def close_action():
        showU1Box.destroy()
    global showU1Box
    if showU1Box is None or not showU1Box.winfo_exists():
        showU1Box = tk.Toplevel(window)
        showU1Box.attributes("-topmost", True)
    
        main_frame = ttk.Frame(showU1Box, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))


        # Input A1 label and display
        ttk.Label(main_frame, text="Input A1:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(main_frame, text="No Sensor Box").grid(row=0, column=1, sticky=tk.W)

        # Quantity dropdown
        ttk.Label(main_frame, text="Quantity:").grid(row=1, column=0, sticky=tk.W)
        quantity = ttk.Combobox(main_frame, values=["Voltage UA1"])
        quantity.set("Voltage UA1")
        quantity.grid(row=1, column=1, sticky=(tk.W, tk.E))

        # Meas. Range dropdown
        ttk.Label(main_frame, text="Meas. Range:").grid(row=2, column=0, sticky=tk.W)
        meas_range = ttk.Combobox(main_frame, values=["-10 V .. 10 V"])
        meas_range.set("-10 V .. 10 V")
        meas_range.grid(row=2, column=1, sticky=(tk.W, tk.E))

        # Record Measured Values section
        record_frame = ttk.Labelframe(main_frame, text="Record Measured Values", padding="10")
        record_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))

        value_type = tk.StringVar(value="Instantaneous")

        tk.Radiobutton(record_frame, text="Instantaneous Values", variable=value_type, value="Instantaneous").grid(row=0, column=0, sticky=tk.W)
        tk.Radiobutton(record_frame, text="Averaged Values", variable=value_type, value="Averaged").grid(row=1, column=0, sticky=tk.W)

        avg_time_label = ttk.Label(record_frame, text="100 ms")
        avg_time_label.grid(row=1, column=1, sticky=tk.W)

        tk.Radiobutton(record_frame, text="RMS Values (cos φ)", variable=value_type, value="RMS").grid(row=2, column=0, sticky=tk.W)

        # Zero Point section
        zero_point_frame = ttk.Labelframe(main_frame, text="Zero Point", padding="10")
        zero_point_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))

        zero_point = tk.StringVar(value="Middle")

        tk.Radiobutton(zero_point_frame, text="Left", variable=zero_point, value="Left").grid(row=0, column=0, sticky=tk.W)
        tk.Radiobutton(zero_point_frame, text="Middle", variable=zero_point, value="Middle").grid(row=0, column=1, sticky=tk.W)
        tk.Radiobutton(zero_point_frame, text="Right", variable=zero_point, value="Right").grid(row=0, column=2, sticky=tk.W)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.E, tk.W))

        ttk.Button(button_frame, text="Correct", command=correct_action).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(button_frame, text="Help", command=help_action).grid(row=0, column=1, sticky=tk.W)
        ttk.Button(button_frame, text="Delete", command=delete_action).grid(row=0, column=2, sticky=tk.W)
        ttk.Button(button_frame, text="Close", command=close_action).grid(row=0, column=3, sticky=tk.W)



def click_u1(event):
    global U1
    U1 = 0
    label1.config(text="U1")
    show_u1_box()

def show_u2_box():
   

    def correct_action():
        print("Correct button clicked")

    def delete_action():
        print("Delete button clicked")

    def help_action():
        print("Help button clicked")

    def close_action():
        showU2Box.destroy()
    global showU2Box
    if showU2Box is None or not showU2Box.winfo_exists():
        showU2Box = tk.Toplevel(window)
        showU2Box.attributes("-topmost", True)
    
        main_frame = ttk.Frame(showU2Box, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))


        # Input A1 label and display
        ttk.Label(main_frame, text="Input A2:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(main_frame, text="No Sensor Box").grid(row=0, column=1, sticky=tk.W)

        # Quantity dropdown
        ttk.Label(main_frame, text="Quantity:").grid(row=1, column=0, sticky=tk.W)
        quantity = ttk.Combobox(main_frame, values=["Voltage UA2"])
        quantity.set("Voltage UA2")
        quantity.grid(row=1, column=1, sticky=(tk.W, tk.E))

        # Meas. Range dropdown
        ttk.Label(main_frame, text="Meas. Range:").grid(row=2, column=0, sticky=tk.W)
        meas_range = ttk.Combobox(main_frame, values=["-10 V .. 10 V"])
        meas_range.set("-10 V .. 10 V")
        meas_range.grid(row=2, column=1, sticky=(tk.W, tk.E))

        # Record Measured Values section
        record_frame = ttk.Labelframe(main_frame, text="Record Measured Values", padding="10")
        record_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))

        value_type = tk.StringVar(value="Instantaneous")

        tk.Radiobutton(record_frame, text="Instantaneous Values", variable=value_type, value="Instantaneous").grid(row=0, column=0, sticky=tk.W)
        tk.Radiobutton(record_frame, text="Averaged Values", variable=value_type, value="Averaged").grid(row=1, column=0, sticky=tk.W)

        avg_time_label = ttk.Label(record_frame, text="100 ms")
        avg_time_label.grid(row=1, column=1, sticky=tk.W)

        tk.Radiobutton(record_frame, text="RMS Values (cos φ)", variable=value_type, value="RMS").grid(row=2, column=0, sticky=tk.W)

        # Zero Point section
        zero_point_frame = ttk.Labelframe(main_frame, text="Zero Point", padding="10")
        zero_point_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))

        zero_point = tk.StringVar(value="Middle")

        tk.Radiobutton(zero_point_frame, text="Left", variable=zero_point, value="Left").grid(row=0, column=0, sticky=tk.W)
        tk.Radiobutton(zero_point_frame, text="Middle", variable=zero_point, value="Middle").grid(row=0, column=1, sticky=tk.W)
        tk.Radiobutton(zero_point_frame, text="Right", variable=zero_point, value="Right").grid(row=0, column=2, sticky=tk.W)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.E, tk.W))

        ttk.Button(button_frame, text="Correct", command=correct_action).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(button_frame, text="Help", command=help_action).grid(row=0, column=1, sticky=tk.W)
        ttk.Button(button_frame, text="Delete", command=delete_action).grid(row=0, column=2, sticky=tk.W)
        ttk.Button(button_frame, text="Close", command=close_action).grid(row=0, column=3, sticky=tk.W)


def click_u2(event):
    global U2
    U2 = 0
    label2.config(text="U2")
    show_u2_box()

def defCassy(frameMain):
    global label1
    global label2
    frameCassy = ttk.Frame(frameMain, borderwidth=5, relief="sunken", padding="10")
    frameCassy.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
    label1 = tk.Label(frameCassy, text="Click here for U1", bg="lightblue", width=20, height=5)
    label1.grid(row=0, column=0)

    label2 = tk.Label(frameCassy, text="Click here for U2", bg="lightgreen", width=20, height=5)
    label2.grid(row=1, column=0)
    if U1 is not None:
        label1.config(text="U1")
    if U2 is not None:
        label2.config(text="U2")

    # Gắn sự kiện click vào label
    label1.bind("<Button-1>", click_u1)
    label2.bind("<Button-1>", click_u2)


    print(1)


def defFFT(frameMain):
    def seletedQuantityFFT(*arg):
        global indexNameFFT
     
        if  indexNameFFT == -2 or indexNameFFT >= 0 :

            if quantity_combo.current() >= 0:
                indexNameFFT = quantity_combo.current()
        displayFFT()

    def getIndexNameFFT(*arg):
        global indexNameFFT
     
        if  indexNameFFT == -2 or indexNameFFT >= 0 :

            if quantity_combo.current() >= 0:
                indexNameFFT = quantity_combo.current()
            listFFT[indexNameFFT].name = nameFFTSelected.get()
            changeValueCombobox()
            print(indexNameFFT)
            

        
    def changeValueCombobox():
        global indexNameFFT
        listNameQuatity = []
        for i in range(len(listFFT)):
            listNameQuatity.append(listFFT[i].name)
        if len(listNameQuatity) > 0 :
            quantity_combo['values'] = listNameQuatity
            quantity_combo['state'] = 'normal'
            
        else:
            quantity_combo['state'] = 'readonly'
            quantity_combo['values'] = []
            indexNameFFT = -2
            nameFFTSelected.set('')
        
    def displayFFT():
        for widget in frameFFT.winfo_children():
            if isinstance(widget, tk.LabelFrame) and widget.cget("text") == "Properties":
                widget.destroy()
        prop_frame = tk.LabelFrame(frameFFT, text="Properties", padx=10, pady=10)
       
        if len(listFFT) > 0:
            quantity_combo.current(indexNameFFT)
            # Properties frame
            prop_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

            # Parameter or Formula
            tk.Radiobutton(prop_frame, text="Parameter (Manual Entry in Table or Here) =", value=1).grid(row=0, column=0, sticky='w')
            param_entry = tk.Entry(prop_frame)
            param_entry.grid(row=0, column=1, padx=5)

            tk.Radiobutton(prop_frame, text="Formula (time,date,n,t,UA1,f1) =", value=2).grid(row=1, column=0, sticky='w')
            formula_entry = tk.Entry(prop_frame, textvariable=formulaEntry)
            formula_entry.grid(row=1, column=1, padx=5)

            formulaEntry.set(listFFT[indexNameFFT].formula)

            # Checkboxes for different options
            tk.Checkbutton(prop_frame, text="Derivation over Time from").grid(row=2, column=0, sticky='w')
            tk.Checkbutton(prop_frame, text="Integral over Time from").grid(row=3, column=0, sticky='w')
            tk.Checkbutton(prop_frame, text="Mean Value over").grid(row=4, column=0, sticky='w')
            mean_value_entry = tk.Entry(prop_frame, width=5)
            mean_value_entry.grid(row=4, column=1, sticky='w', padx=5)
            tk.Label(prop_frame, text="s from").grid(row=4, column=2, sticky='w')
            tk.Checkbutton(prop_frame, text="Fast Fourier Transformation from").grid(row=5, column=0, sticky='w')

            # Additional fields (Symbol, Unit, From, To, Decimal Places)
            tk.Label(prop_frame, text="Symbol:").grid(row=6, column=0, sticky='w')
            symbol_entry = tk.Entry(prop_frame, width=5, textvariable=symolFFT)
            symbol_entry.grid(row=6, column=1, sticky='w', padx=5)

            tk.Label(prop_frame, text="Unit:").grid(row=6, column=2, sticky='w')
            unit_entry = tk.Entry(prop_frame, width=5, textvariable=unitFFT)
            unit_entry.grid(row=6, column=3, sticky='w', padx=5)

            tk.Label(prop_frame, text="From:").grid(row=7, column=0, sticky='w')
            from_entry = tk.Entry(prop_frame, width=5)
            from_entry.grid(row=7, column=1, sticky='w', padx=5)

            tk.Label(prop_frame, text="To:").grid(row=7, column=2, sticky='w')
            to_entry = tk.Entry(prop_frame, width=5)
            to_entry.grid(row=7, column=3, sticky='w', padx=5)

            tk.Label(prop_frame, text="Decimal Places:").grid(row=8, column=0, sticky='w')
            decimal_entry = tk.Entry(prop_frame, width=5 , textvariable = decimalPlacesFFT)
            decimal_entry.grid(row=8, column=1, sticky='w', padx=5)
            # set value
            symolFFT.set(listFFT[indexNameFFT].symbol)
            unitFFT.set(listFFT[indexNameFFT].util)
            decimalPlacesFFT.set(listFFT[indexNameFFT].decimalPlaces)

        else:
            prop_frame.destroy()
    def newFFT():
        global indexNameFFT
        global increase
        fft =  FFTObject.FFT(increase)
        listFFT.append(fft)
        changeValueCombobox()
        increase += 1
        print(indexNameFFT)
        indexNameFFT = len(listFFT) - 1
        quantity_combo.current(indexNameFFT)
        displayFFT()
    def deleteQuantity():
        global indexNameFFT
        if len(listFFT) > 0:
            listFFT.pop(indexNameFFT)
            indexNameFFT = len(listFFT) - 1
            changeValueCombobox()
        displayFFT()
            
            
            
        
            
     

        

    frameFFT = ttk.Frame(frameMain, borderwidth=5, relief="sunken", padding="10")
    frameFFT.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

    # Select Quantity
    tk.Label(frameFFT, text="Select Quantity:").grid(row=0, column=0, padx=10, pady=5)
    nameFFTSelected = tk.StringVar()
    quantity_combo = ttk.Combobox(frameFFT, textvariable= nameFFTSelected)
    quantity_combo.grid(row=0, column=1, padx=10, pady=5)
    quantity_combo.bind('<<ComboboxSelected>>', seletedQuantityFFT)
    nameFFTSelected.trace('w', getIndexNameFFT)

    # Buttons for New Quantity and Delete Quantity
    tk.Button(frameFFT, text="New Quantity", command=lambda: newFFT()).grid(row=0, column=2, padx=10, pady=5)
    tk.Button(frameFFT, text="Delete Quantity", command=deleteQuantity).grid(row=0, column=3, padx=10, pady=5)
    changeValueCombobox()
    displayFFT()
    
    
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

def defDisplay(frameMain):
    def changeValueComboboxDisplay():
        global indexNameFFT
        listNameQuatity = []
        listNameQuatity.append("t")
        listNameQuatity.append("n")

        if U1  is not None:
            listNameQuatity.append("U1")
        if U2 is not None:
            listNameQuatity.append("U2")
        for i in range(len(listFFT)):
            listNameQuatity.append(listFFT[i].symbol)
        return listNameQuatity
    frameDisplay = ttk.Frame(frameMain, borderwidth=5, relief="sunken", padding="10")
    frameDisplay.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

    # Select Display
    tk.Label(frameDisplay, text="Select Display:").grid(row=0, column=0, padx=10, pady=5)
    display_combo = ttk.Combobox(frameDisplay, values = ["New"])
    display_combo.grid(row=0, column=1, padx=10, pady=5)
    display_combo.current(0)

    # Buttons for New Display and Clear Display
    tk.Button(frameDisplay, text="New Display").grid(row=0, column=2, padx=10, pady=5)
    tk.Button(frameDisplay, text="Clear Display").grid(row=0, column=3, padx=10, pady=5)

    # X-Axis and Y-Axis
    tk.Label(frameDisplay, text="X-Axis:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
    x_axis_combo = ttk.Combobox(frameDisplay, values = changeValueComboboxDisplay())
    x_axis_combo.grid(row=1, column=1, padx=10, pady=5)
    x_axis_combo.current(0)

    tk.Label(frameDisplay, text="Y-Axes:").grid(row=1, column=2, padx=10, pady=5, sticky='w')
    y_axis_combo = ttk.Combobox(frameDisplay, values=changeValueComboboxDisplay())
    y_axis_combo.grid(row=1, column=3, padx=10, pady=5)
    y_axis_combo.current(1)

    # X-Axis Transformation Options
    x_frame = tk.LabelFrame(frameDisplay, text="X-Axis Transformation")
    x_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
    
    x_var = tk.IntVar()
    
    tk.Radiobutton(x_frame, text="x", variable=x_var, value=1).grid(row=0, column=0, sticky='w')
    tk.Radiobutton(x_frame, text="x²", variable=x_var, value=2).grid(row=1, column=0, sticky='w')
    tk.Radiobutton(x_frame, text="1/x", variable=x_var, value=3).grid(row=2, column=0, sticky='w')
    tk.Radiobutton(x_frame, text="1/x²", variable=x_var, value=4).grid(row=3, column=0, sticky='w')
    tk.Radiobutton(x_frame, text="log x", variable=x_var, value=5).grid(row=4, column=0, sticky='w')
    x_var.set(1)
    # Y-Axis Transformation Options
    y_frame = tk.LabelFrame(frameDisplay, text="Y-Axis Transformation")
    y_frame.grid(row=2, column=2, columnspan=2, padx=10, pady=10, sticky='ew')
    
    y_var = tk.IntVar()
    tk.Radiobutton(y_frame, text="y", variable=y_var, value=1).grid(row=0, column=0, sticky='w')
    tk.Radiobutton(y_frame, text="y²", variable=y_var, value=2).grid(row=1, column=0, sticky='w')
    tk.Radiobutton(y_frame, text="1/y", variable=y_var, value=3).grid(row=2, column=0, sticky='w')
    tk.Radiobutton(y_frame, text="1/y²", variable=y_var, value=4).grid(row=3, column=0, sticky='w')
    tk.Radiobutton(y_frame, text="log y", variable=y_var, value=5).grid(row=4, column=0, sticky='w')
    y_var.set(1)
    # Additional Options (Polar, Bars)
    tk.Checkbutton(frameDisplay, text="Polar").grid(row=3, column=0, padx=10, pady=5, sticky='w')
    tk.Checkbutton(frameDisplay, text="Bars").grid(row=3, column=2, padx=10, pady=5, sticky='w')


def deleteWidget(windowFrame):
    for widget in windowFrame.winfo_children():
        if isinstance(widget, tk.LabelFrame) and widget.cget("text") == "Properties":
            widget.destroy()


# giao dien auto hay bam tay
def measuringParametes():
    global measuringParametesWindow
    
    if measuringParametesWindow is None or not measuringParametesWindow.winfo_exists():
        measuringParametesWindow = tk.Toplevel(window)
        measuringParametesWindow.attributes("-topmost", True)
        main_frame = ttk.Frame(measuringParametesWindow, padding="10")
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
        close_button = ttk.Button(main_frame, text="Close", command=measuringParametesWindow.destroy)
        help_button = ttk.Button(main_frame, text="Help")
        close_button.grid(column=0, row=3, sticky=tk.W)
        help_button.grid(column=1, row=3, sticky=tk.W)

        # Thiết lập khoảng cách giữa các thành phần
        for child in main_frame.winfo_children(): 
            child.grid_configure(padx=5, pady=5)






def openWindowF5(event=None):
    global windowF5
    global main_frame
    if windowF5 is None or not windowF5.winfo_exists():
        windowF5 = tk.Toplevel(window)
        
        windowF5.attributes("-topmost", True)
    
        main_frame = ttk.Frame(windowF5, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Tạo phần 1 - 5 button nằm ngang
        frame1 = ttk.Frame(main_frame, borderwidth=5, relief="sunken")
        frame1.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        button_texts1 = ["CASSY", "Parameter/Formula/FFT`", "Comment", "General", "Display"]
        
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
        # Button Display
        buttonCassy = ttk.Button(frame1, text=button_texts1[4], comman = lambda: defDisplay(main_frame))
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

        
        buttonClose = ttk.Button(frame3, text="Close", command=lambda: windowF5.destroy)
        buttonClose.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=2)

        buttonDisplayMeasuring = ttk.Button(frame3, text="Display Measuring Parameters", command=measuringParametes)
        buttonDisplayMeasuring.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=2)

        # Cấu hình lưới
        windowF5.columnconfigure(0, weight=1)
        windowF5.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

def enterFormula(*arg):
    listFFT[indexNameFFT].formula = formulaEntry.get()

def enterSymolFFT (*arg):
    listFFT[indexNameFFT].symbol = symolFFT.get()
def enterUnitFFT (*arg):
    listFFT[indexNameFFT].util = unitFFT.get()
def enterDecimalPlaceFFT (*arg):
    listFFT[indexNameFFT].decimalPlaces = decimalPlacesFFT.get()

window.bind('<F5>', openWindowF5)
formulaEntry.trace('w', enterFormula)
symolFFT.trace('w', enterSymolFFT)
unitFFT.trace('w', enterUnitFFT)
decimalPlacesFFT.trace('w', enterDecimalPlaceFFT)

openWindowF5()

window.mainloop()