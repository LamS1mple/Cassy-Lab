import tkinter as tk
from tkinter import ttk
import numpy as np
import serial.tools.list_ports
import scan_com
import logging
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import asyncio
import FFTObject
import threading
import time as TIME
import queue
from scipy.optimize import curve_fit
from math import cos, sin ,tan
logging.basicConfig(level=logging.DEBUG)


# ardunio.ardunio(3,1)
window = tk.Tk()
width= window.winfo_screenwidth() 
height= window.winfo_screenheight()
#setting tkinter window size
window.state('zoomed')
n = 0
# data radio
recording_mode = tk.IntVar(window)
recording_mode.set(1)
# window
windowF5 = None
showU1Box = None
showU2Box = None
measuringParametesWindow = None
timeStart = 0
window.title("Cassy")

stop_eventData = threading.Event()
stop_eventInsert = threading.Event()

startIndex = None
endIndex = None
highlighted_line = None
xData = []
yData = []
yData2 = []
# global variable
xAxis = None
yAxis = None
yAxis2 = None

increase = 1
UA1 = None
UB1 = None
time = 0
n = 0
listDisplayValue = []
listFFT = []
indexNameFFT = -2
formulaEntry = tk.StringVar()
symolFFT = tk.StringVar()
unitFFT = tk.StringVar()
decimalPlacesFFT = tk.IntVar()
formFFT = tk.IntVar()
toFFT = tk.IntVar()
measInter = tk.IntVar()
measTime = tk.IntVar()

def displayColumn():
    global tableView
    nameTable = ['t(s)', "n"]

    for i in range(len(listDisplayValue)):
        nameTable.append("{}".format(listDisplayValue[i].symbol))

    tableView['columns'] = nameTable
    tableView.heading(nameTable[0] , text = nameTable[0])
    tableView.heading(nameTable[1] , text = nameTable[1])

    tableView.column("t(s)", width=50)
    tableView.column("n", width=50)

    for i in range(2,len( nameTable)):
        tableView.column(nameTable[i], width=50)
        tableView.heading(nameTable[i], text= "{}({})".format(nameTable[i] ,  listDisplayValue[i - 2].util))
        



def changeDisplayValue():
    global listDisplayValue
    listDisplayValue = []
    if UA1 is not None:
        oU1 =  FFTObject.FFT(0)
        oU1.name = "UA1"
        oU1.formula = "UA1"
        oU1.symbol = "UA1"
        oU1.util = "V"
        oU1.decimalPlaces = 3
        listDisplayValue.append(oU1)
    if UB1 is not None:
        oU2 =  FFTObject.FFT(0)
        oU2.name = "UB1"
        oU2.formula = "UB1"
        oU2.symbol = "UB1"
        oU2.util = "V"
        oU2.decimalPlaces = 3
        listDisplayValue.append(oU2)
    listDisplayValue += listFFT
    displayColumn()
    
    



def readData():
    global dataText, UA1, UB1
    while not stop_eventData.is_set():
        l = len(listDisplayValue)
        try:
            data = arduino.readline().decode().strip()
            if data:
                # print(data)
                dataText = data.split("|")
                if UA1 is not None:
                    UA1 = float(dataText[0])
                if UB1 is not None:
                    UB1 = float(dataText[1])
                for i in range(len(listDisplayValue)):
                    
                    value = eval(listDisplayValue[i].formula)
                    listDisplayValue[i].resetValue(value)
        except:
            arduino.close()
            return
            
        
                

threadingData = threading.Thread(target=readData)

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
    
    # print(1)
    if new_width > 50:  # Đảm bảo kích thước không quá nhỏ
        frame.config(width=new_width)
        drag_data = {"x": event.x, "y": event.y}

def updateMatplotlib():
    global plt

    lineM.set_data(np.array(xData), np.array(yData) )
    if ( yAxis2.get() != 'off'):
        lineN.set_data(np.array(xData), np.array(yData2))
    canvas.draw()
    pass
def onpick(event):
    # Lấy thông tin điểm được click
    if event.artist != lineM:
        return
    ind = event.ind
    if isinstance(ind, (list, np.ndarray)):
        print(ind)
        ind = ind[0]
    print(f"Clicked data: x={xData[ind]}, y={yData[ind]}")
def matplotlib():
    global tableView
    # Tạo một khung để chứa canvas và thanh công cụ
    frameTreeView = tk.Frame(window,width=300,padx=20)
    frameTreeView.pack_propagate(False)  # Đảm bảo kích thước của Frame không thay đổi theo nội dung
    frameTreeView.pack(side=tk.LEFT, fill=tk.Y)
    tableView = ttk.Treeview(frameTreeView, show='headings')
    tableView.pack(fill=tk.BOTH,expand=True)
    frameTreeView.bind("<Button-1>", start_resize)
    frameTreeView.bind("<B1-Motion>", perform_resize)

    scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=tableView.yview)
    tableView.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)

    scrollbar_x = ttk.Scrollbar(frameTreeView, orient=tk.HORIZONTAL, command=tableView.xview)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    tableView.configure(xscrollcommand=scrollbar_x.set)
    
    # Tạo một figure cho matplotlib
    global fig , ax, lineM, lineN

    fig, ax = plt.subplots()
    lineM , = ax.plot([], [], marker = ".", picker = True)
    lineN , = ax.plot([], [], marker = ".", picker = True)
    ax.legend()
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    fig.canvas.mpl_connect('button_press_event', onClick)
    fig.canvas.mpl_connect('motion_notify_event', onMove)
    fig.canvas.mpl_connect('button_release_event', onRelease)
    # Vẽ các đường lưới (grid lines) và thiết lập giới hạn trục
    ax.grid(True)
    ax.set_ylim(0, 40)
    ax.set_xlim(0 , 10)
    global canvas
    # Tạo canvas để hiển thị biểu đồ trong cửa sổ Tkinter
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    fig.canvas.mpl_connect("pick_event", onpick)
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
            threadingData.start()
            measuringParametes()

            

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
    global UA1
    try:
        UA1 = float(dataText[0])
        label1.config(text="UA1")
        show_u1_box()
        changeDisplayValue()
        listDisplayValue[0].createDisplay(window)
    except:
        pass
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
    global UB1
    try:
        UB1 = float(dataText[1])
        label2.config(text="UB1")
        show_u2_box()
        changeDisplayValue()
        if UA1 is not None:
            listDisplayValue[1].createDisplay(window)
        else:
            listDisplayValue[0].createDisplay(window)
    except: 
        pass

def defCassy(frameMain):
    global label1
    global label2
    frameCassy = ttk.Frame(frameMain, borderwidth=5, relief="sunken", padding="10")
    frameCassy.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
    label1 = tk.Label(frameCassy, text="Click here for UA1", bg="lightblue", width=20, height=5)
    label1.grid(row=0, column=0)

    label2 = tk.Label(frameCassy, text="Click here for UB1", bg="lightgreen", width=20, height=5)
    label2.grid(row=1, column=0)
    if UA1 is not None:
        label1.config(text="UA1")
    if UB1 is not None:
        label2.config(text="UB1")

    # Gắn sự kiện click vào label
    label1.bind("<Button-1>", click_u1)
    label2.bind("<Button-1>", click_u2)


    # print(1)


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

            tk.Radiobutton(prop_frame, text="Formula (time,date,n,t,UA1,UB1) =", value=2).grid(row=1, column=0, sticky='w')
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

            tk.Label(prop_frame, text="From: ").grid(row=7, column=0, sticky='w')
            from_entry = tk.Entry(prop_frame, width=5, textvariable=formFFT)
            from_entry.grid(row=7, column=1, sticky='w', padx=5)

            tk.Label(prop_frame, text="To:").grid(row=7, column=2, sticky='w')
            to_entry = tk.Entry(prop_frame, width=5, textvariable=toFFT)
            to_entry.grid(row=7, column=3, sticky='w', padx=5)

            tk.Label(prop_frame, text="Decimal Places:").grid(row=8, column=0, sticky='w')
            decimal_entry = tk.Entry(prop_frame, width=5 , textvariable = decimalPlacesFFT)
            decimal_entry.grid(row=8, column=1, sticky='w', padx=5)
            # set value
            symolFFT.set(listFFT[indexNameFFT].symbol)
            unitFFT.set(listFFT[indexNameFFT].util)
            decimalPlacesFFT.set(listFFT[indexNameFFT].decimalPlaces)
            toFFT.set(listFFT[indexNameFFT].to)
            formFFT.set(listFFT[indexNameFFT].form)

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
        changeDisplayValue()
    def deleteQuantity():
        global indexNameFFT
        if len(listFFT) > 0:
            listFFT.pop(indexNameFFT)
            indexNameFFT = len(listFFT) - 1
            changeValueCombobox()
        displayFFT()
        changeDisplayValue()
            
            
            
        
            
     

        

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

        if UA1  is not None:
            listNameQuatity.append("UA1")
        if UB1 is not None:
            listNameQuatity.append("UB1")
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
    global xAxis, yAxis, yAxis2
    # X-Axis and Y-Axis
    xAxis = tk.StringVar()
    yAxis = tk.StringVar()
    yAxis2 = tk.StringVar()
    xAxis.set("t")
    yAxis.set("n")
    yAxis2.set("off")
    tk.Label(frameDisplay, text="X-Axis:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
    x = ttk.Combobox(frameDisplay, values = changeValueComboboxDisplay(),textvariable=xAxis , state='readonly')
    x.grid(row=1, column=1, padx=10, pady=5)
    x.current(0)

    tk.Label(frameDisplay, text="Y-Axes:").grid(row=1, column=2, padx=10, pady=5, sticky='w')
    y = ttk.Combobox(frameDisplay, values=changeValueComboboxDisplay(), textvariable=yAxis, state='readonly')
    y.grid(row=1, column=3, padx=10, pady=5)
    y.current(1)

    tk.Label(frameDisplay, text="Y-Axes2:").grid(row=1, column=5, padx=10, pady=5, sticky='w')
    z = ttk.Combobox(frameDisplay, values=changeValueComboboxDisplay(), textvariable=yAxis2, state='readonly')
    z.grid(row=1, column=6, padx=10, pady=5)
    z.set("off")
    
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

        auto_radio = ttk.Radiobutton(main_frame, text="Automatic Recording", variable=recording_mode, value=1)
        manual_radio = ttk.Radiobutton(main_frame, text="Manual Recording", variable=recording_mode, value=2)
        append_check = ttk.Checkbutton(main_frame, text="Append New Meas. Series")
        meas_interval_label = ttk.Label(main_frame, text="Meas. Interv.:(ms)")
        meas_interval = ttk.Entry(main_frame, width=5, textvariable=measInter)
        meas_interval.insert(0, "10")
        x_number_label = ttk.Label(main_frame, text="x Number:")
        x_number = ttk.Entry(main_frame, width=5 )
        x_number.insert(0, "5000")
        trigger_label = ttk.Label(main_frame, text="Trigger:")
        trigger = ttk.Combobox(main_frame, width=5)
        meas_time_label = ttk.Label(main_frame, text="= Meas. Time:")
        meas_time = ttk.Entry(main_frame, textvariable= measTime, width=5)
        measTime.set(10)
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


def openValueDisplay(data):
    valueDisplay = tk.Toplevel(window)
    valueDisplay.attributes("-topmost", True)
    
    # Tạo frame để chứa các nhãn
    frame = tk.Frame(valueDisplay)
    frame.pack(pady=40, padx=40)  # Điều chỉnh khoảng cách nếu cần
    # Tạo nhãn với chữ lớn hơn
    label1 = tk.Label(frame, text="{}=".format(data.symbol), font=("Arial", 20))
    label1.pack(side=tk.LEFT)

    data.setTopWindow(frame)
    data.textValue.pack(side=tk.LEFT)



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

        windowF5.update_idletasks()
        screen_width = windowF5.winfo_screenwidth()
        screen_height = windowF5.winfo_screenheight()

        # Lấy kích thước của cửa sổ
        window_width = windowF5.winfo_width()
        window_height = windowF5.winfo_height()

        # Tính toán vị trí để đặt cửa sổ ở giữa màn hình
        position_right = int(screen_width/2 - window_width/2)
        position_down = int(screen_height/2 - window_height/2)

        # Đặt cửa sổ ở giữa màn hình mà không cần cố định kích thước
        windowF5.geometry(f'+{position_right}+{position_down}')

def enterFormula(*arg):
    listFFT[indexNameFFT].formula = formulaEntry.get()
    changeDisplayValue()

def enterSymolFFT (*arg):
    listFFT[indexNameFFT].symbol = symolFFT.get()
    changeDisplayValue()
def enterUnitFFT (*arg):
    listFFT[indexNameFFT].util = unitFFT.get()
    changeDisplayValue()
def enterDecimalPlaceFFT (*arg):
    listFFT[indexNameFFT].decimalPlaces = decimalPlacesFFT.get()
    changeDisplayValue()
def enterFormFFT(*arg):
    listFFT[indexNameFFT].form = formFFT.get()
    changeDisplayValue()

def enterToFFT(*arg):
    listFFT[indexNameFFT].to = toFFT.get()
    changeDisplayValue()


def changeRecording():
    global timeStart 
    timeStart = 0

def startReadValue (event = None):
    global lineM, lineN, ax
    lineM.set_label(yAxis.get())
    lineN.set_label(yAxis2.get())
    ax.legend()
    changeValueAxis()
    global timeStart, n, time
    n = 0
    if timeStart == 0:
        timeStart = int(TIME.time())
    time = 0
    # print(recording_mode.get())
    if recording_mode.get() == 2:
        timeCurrent = int(TIME.time())
        between = timeCurrent - timeStart
        time = between
        data = [between, n]
        if xAxis.get() == 't':
            xData.append(between)
        if yAxis.get() == 't':
            yData.append(between)
        if xAxis.get() == 'n':
            xData.append(n)
        if yAxis.get() == 'n':
            yData.append(n)
        for i in range(len(listDisplayValue)):
            value = eval(listDisplayValue[i].formula)
            data.append(value)
            if xAxis.get() == listDisplayValue[i].symbol:
                xData.append(value)
            if yAxis.get() == listDisplayValue[i].symbol:
                yData.append(value)
        tableView.insert("", 'end', values=data)
        updateMatplotlib()
        changelength()
    else:
        global stop_eventInsert
        stop_eventInsert.clear()
        threadingInser.start()

        pass
def threadingPart2Insert():
    print(measInter.get(), measTime.get())
    print(yAxis2.get())
    timeEnd = 0
    global n ,time
    rou = measInter.get() / 1000
    while timeEnd <= measTime.get() :
        if  stop_eventInsert.is_set(): 
            
            break
        # print(2)
        data = [round(timeEnd,2), n]
        if xAxis.get() == 't':
            xData.append(timeEnd)
        if yAxis.get() == 't':
            yData.append(timeEnd)
        if xAxis.get() == 'n':
            xData.append(n)
        if yAxis.get() == 'n':
            yData.append(n)
        if yAxis2.get() == 't':
            yData2.append(timeEnd)
        if yAxis2.get() == 'n':
            yData2.append(n)
        for i in range(len(listDisplayValue)):
            value = round(float (eval(listDisplayValue[i].formula)), 2)
            data.append(value)
            if xAxis.get() == listDisplayValue[i].symbol:
                xData.append(value)
            if yAxis.get() == listDisplayValue[i].symbol:
                yData.append(value)
            if  yAxis2.get() != 'off' and yAxis2.get() == listDisplayValue[i].symbol :
                yData2.append(value)
        try:
            tableView.insert("", 'end', values=data)
            updateMatplotlib()
            TIME.sleep( rou)
            timeEnd += rou  
            time = timeEnd
            n += 1
            changelength()
        except:
            pass
fitFunction = [0 , 0, 0, 0, 0, 0 , 0]





def fitLine(fuc,xFit, yFit):
    
    popt, pcov = curve_fit(fuc, xFit, yFit)
    
    ax.plot(xFit, fuc(xFit, *popt), color='black', label='Hàm fit')
    fig.canvas.draw()
    

def fitStraightLineOrigin(x, a):
    return a * x

def fitStraightLine(x, a , b):
    return a*x + b
def parabola(x, a, b, c):
    return a*x**2 + b*x + c
def funcBola1(x, a, b):
    return a / x + b
def funcBola2(x, a, b):
    return a / x**2 + b
def exponential_function(x, a, b):
    return a * np.exp(b * x)
def exponential_function2(x, a, b):
    return a * np.exp(-x) + b
def line1():
    global fitFunction
    fitFunction = [1 , 0, 0, 0, 0, 0 , 0]

    pass
def line2():
    global fitFunction
    fitFunction = [0 , 2, 0, 0, 0, 0 , 0]

    pass
def parabola():
    global fitFunction
    fitFunction = [0 , 0, 3, 0, 0, 0 , 0]
    pass
def bolaX1():
    global fitFunction
    fitFunction = [0 , 0, 0, 4, 0, 0 , 0]
    pass
def bolaX2():
    global fitFunction
    fitFunction = [0 , 0, 0, 0, 5, 0 , 0]
    pass
def bolaEX():
    global fitFunction
    fitFunction = [0 , 0, 0, 0, 0, 6 , 0]
    pass
def bolaEX2():
    global fitFunction
    fitFunction = [0 , 0, 0, 0, 0, 0 , 7]
    pass
def changeValueAxis():
    global ax
    if xAxis.get() == 't':
        ax.set_xlim(0, measTime.get())
    if yAxis.get() == 't':
        ax.set_ylim(0, measTime.get())
    for i in range(len(listDisplayValue)):
        if xAxis.get() == listDisplayValue[i].symbol:
            ax.set_xlim(listDisplayValue[i].form, listDisplayValue[i].to)
        if yAxis.get() == listDisplayValue[i].symbol:
            print(1123)
            ax.set_ylim(listDisplayValue[i].form, listDisplayValue[i].to)
            print(listDisplayValue[i].form, listDisplayValue[i].to)
    
def changelength():
    left, right = ax.get_xlim()
    bottom, top = ax.get_ylim()
    if (left > xData[0]):
        left = xData[0] - 5
    if (right <= xData[-1]):
        right = xData[-1] + 5
    if (bottom > yData[0]):
        bottom = yData[0] - 5
    if (top <= yData[-1]):
        top = yData[-1] + 5
    if ( yAxis2.get() != 'off' and bottom > yData2[0]):
        bottom = yData2[0] - 5
    if (yAxis2.get() != 'off' and  top <= yData2[-1]):
        top = yData2[-1] + 5
    ax.set_xlim(left, right)
    ax.set_ylim(bottom, top)

    

    pass

def on_right_click(event):
    context_menu = tk.Menu(window, tearoff=0)
    context_menu.add_command(label="Straight line throught Origin", command=line1)
    context_menu.add_command(label="Best – fit straight line", command=line2)
    context_menu.add_command(label="Parabola", command=parabola)
    context_menu.add_command(label="Hyperbola 1/x", command=bolaX1)
    context_menu.add_command(label="Hyperbola 1/x^2", command=bolaX2)
    context_menu.add_command(label="Exponential Function e^x", command=bolaEX)
    context_menu.add_command(label="Exponential Function e^-x", command=bolaEX2)
    context_menu.tk_popup(event.x_root, event.y_root)

    print("Bạn đã click chuột phải tại tọa độ:", event.x, event.y)

indexClick = None
def focus_on_item():
    dataTable =  tableView.get_children()
    indexView = dataTable[indexClick]
    tableView.selection_set(indexView)
    tableView.see(indexView)
def onClick(event):
    global lineMM, indexClick,startIndex, selectDoThi
    selectDoThi = False
    check = True
    if event.inaxes != ax:
        return
    startIndex = np.argmin(np.abs(xData - event.xdata))
    dist1 = np.abs(yData[startIndex] - event.ydata)  # Đồ thị 1
    dist2 = 0
    if (yAxis2.get() != 'off'):
        dist2 = np.abs(yData2[startIndex] - event.ydata)  # Đồ thị 2
    print(yAxis2.get())
    # Kiểm tra đồ thị nào gần hơn
    if yAxis2.get() == 'off' or dist1 < dist2:
        indexClick = startIndex  # Chọn đồ thị 1
        selectDoThi = False
        print("Chọn đồ thị 1")
    else:
        indexClick = startIndex  # Chọn đồ thị 2
        selectDoThi = True
        print("Chọn đồ thị 2")
    
    focus_on_item()
    for i in fitFunction:
        if i != 0:
            check = False
    if (check):
        startIndex = None
        return
    
    
    figg, axx = plt.subplots()
    lineMM , = ax.plot([], [], color='red', linewidth=2)
    
    print(startIndex)
def onMove(event):
    global endIndex, indexClick , lineMM, selectDoThi
    if event.inaxes != ax :
        return
    
    if startIndex is None:
        return
    endIndex = np.argmin(np.abs(xData - event.xdata))
    indexClick = endIndex
    focus_on_item()
    if endIndex > startIndex:
        if not selectDoThi:
            lineMM.set_data(xData[startIndex:endIndex+1], yData[startIndex:endIndex+1])
        else:
            lineMM.set_data(xData[startIndex:endIndex+1], yData2[startIndex:endIndex+1])
    
    fig.canvas.draw()
    
    print(endIndex)
def onRelease(event):
    global lineMM, fitFunction
    check = True
    for i in fitFunction:
        if i != 0:
            check = False
    if (check ):
        return
    
    
    global startIndex, endIndex
    xFit = np.array(xData[startIndex:endIndex+1])
    yFit = np.array(yData[startIndex:endIndex+1])
    if (selectDoThi):
        yFit = np.array(yData2[startIndex:endIndex+1])

    # xFit = np.array([1, 2, 3, 4, 5])
    # yFit = np.array([1, 2, 3, 4, 5])
    startIndex = None
    endIndex = None
    lineMM.remove()
    fig.canvas.draw()
    lineMM = None
    
    for i in fitFunction:
        if (i == 1 ):
            fitLine(fitStraightLineOrigin,xFit, yFit)
        if (i == 2 ):
            fitLine(fitStraightLine,xFit, yFit)
        if (i == 3):
            fitLine(parabola, xFit, yFit)
        if (i == 4):
            fitLine(funcBola1, xFit, yFit)
        if (i == 5):
            fitLine(funcBola2, xFit, yFit)
        if (i == 6):
            fitLine(exponential_function, xFit, yFit)
        if (i == 7):
            fitLine(exponential_function2, xFit, yFit)
    fitFunction =  [0 , 0, 0, 0, 0, 0 , 0]
    

    
threadingInser = threading.Thread(target=threadingPart2Insert)
window.bind('<F5>', openWindowF5)
window.bind('<F9>', startReadValue)
formulaEntry.trace('w', enterFormula)
symolFFT.trace('w', enterSymolFFT)
unitFFT.trace('w', enterUnitFFT)
decimalPlacesFFT.trace('w', enterDecimalPlaceFFT)
toFFT.trace('w', enterToFFT)
formFFT.trace('w', enterFormFFT)
window.bind("<Button-3>", on_right_click)

recording_mode.trace('w', changeRecording)

openWindowF5()


def on_closing():


    global stop_eventData, stop_eventInsert, arduino, window, canvas

    stop_eventData.set()
    stop_eventInsert.set()
    window.quit()
    print("out")
    

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()