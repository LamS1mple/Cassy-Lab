import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Hàm bậc 2 cần fit
def func(x, a, b, c):
    return a * x**2 + b * x + c

# Dữ liệu ví dụ
x_data = np.array([1, 2, 3, 4, 5, 6, 7])
y_data = np.array([1, 2, 3, 4, 5, 6, 7])

# Fit hàm với dữ liệu
popt, pcov = curve_fit(func, x_data, y_data)

# Kết quả fit


# Vẽ biểu đồ
plt.scatter(x_data, y_data, label="Dữ liệu thực")
plt.plot(x_data, func(x_data, *popt), label="Hàm fit", color='red')
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.show()
