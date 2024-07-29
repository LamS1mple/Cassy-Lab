import serial
import datetime
import time
import csv  
import numpy as np
from scipy.optimize import curve_fit
import threading



def function(x, a, b, c):
    return a * np.exp(-b * x) + c

# def hop():
#     plt.subplot(1, 2, 1)
#     dataframe = read_csv(nameFile)
#     # dataframe = read_csv("2.14.csv")

#     data = dataframe.values

#     x, y = data[:, 0], data[:, -1]
#     popt, _ = curve_fit(function, x, y)

#     a, b, c = popt

#     tau = (1/b) * 0.03
#     print()
#     print('tau =',  tau*1.35)
#     plt.scatter(x, y)
#     x_line = np.arange(min(x), max(x), 1)
#     y_line = function(x_line, a, b, c)

#     plt.plot(x_line, y_line, '--', color='red')




def ardunio(com, thoiGian):
    

    arduino = serial.Serial(port='COM{}'.format(com), baudrate=9600, timeout=.1)

    print("Ket noi thanh cong")
    giay = thoiGian
    print("Loading data...")
    inp = '120'
    timeBatDau = time.time()

    u = []
    v = []

    rows = []

    f = 0
    while True:
        timeKetThuc = time.time()
        kc = timeKetThuc - timeBatDau
        if (kc <= giay):

            arduino.write(str(inp + "\n").encode())
            
            try:
                s = arduino.readline().decode()
                tach = s.split("|")
                vi = float(tach[1].strip("\r\n"))
                ui = float(tach[0])
                if(vi > 0 and ui > 0):
                    v.append( vi)
                    u.append( ui)
                    f += 1
                    row = {
                        'STT': f,
                        'Time(s)': kc,
                        'Uc(V)': ui,
                        'Ur(V)': vi
                    }
                    rows.append(row)

            except:
                pass
        else:
            break

ardunio(4, 10)

# nameFile = 'data{}_{}_{}_{}_{}_{}.csv'.format(x.day,x.month , x.year , x.hour, x.minute,x.second)

# tenHang = ['STT', 'Time(s)' , 'Uc(V)', 'Ur(V)']

# # luu file csv
# with open(nameFile , 'w', newline='') as csvFile:
#     writer = csv.DictWriter(csvFile, fieldnames = tenHang)  
#     writer.writeheader()
#     writer.writerows(rows)



# Ox = input('Nhap ten truc Ox ')

# Oy = input('Nhap ten truc Oy ')
# hop()

# plt.subplot(1, 2, 2)

# plt.plot(u, label='Đường Uc(V)')
# plt.plot(v ,  label='Đường Ur(V)')


# plt.xlabel(Ox)
# plt.ylabel(Oy)

# plt.legend()
# plt.tight_layout()

# plt.show()



# input()
ardunio(4,1)