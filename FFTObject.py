import tkinter

class FFT:
    name = None
    formula = None
    def __init__(self, i):
       self.name = "New quantity {}".format(i)
       self.formula = "0"
       self.symbol = "f{}".format(i)
       self.util = ""
       self.decimalPlaces = 3
       self.textValue = None  
       self.form = 0
       self.to = 20
    

    def createDisplay(self, window):
        valueDisplay = tkinter.Toplevel(window)
        valueDisplay.attributes("-topmost", True)
        
        # Tạo frame để chứa các nhãn
        frame = tkinter.Frame(valueDisplay)
        frame.pack(pady=40, padx=40)  # Điều chỉnh khoảng cách nếu cần
        # Tạo nhãn với chữ lớn hơn
        label1 = tkinter.Label(frame, text="{}=".format(self.symbol), font=("Arial", 20))
        label1.pack(side=tkinter.LEFT)
        self.textValue = tkinter.Label(frame, font=("Arial", 20))
        self.textValue.pack(side=tkinter.LEFT)
    def resetValue(self, value):
        try:
            if self.textValue is not None:  # Kiểm tra nếu đã tạo Label
                self.textValue.config(text=value)
            else:
                print("Display has not been created yet.")
        except:
            pass
        
