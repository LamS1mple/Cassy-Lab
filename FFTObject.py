

class FFT:
    name = None
    formula = None
    def __init__(self, i):
       self.name = "New quantity {}".format(i)
       self.formula = ""
       self.symbol = "f{}".format(i)
       self.util = ""
       self.decimalPlaces = 3
