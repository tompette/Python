import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

month, day, hour, green_p, pr_green, bin_p, pr_bin, otsu_p, pr_otsu, open_p, pr_open, close_p, pr_close = np.loadtxt("csv_data.csv", unpack = True, delimiter=',')
number = []
for i in range(0, 4028):
    number.append(i)
plt.plot(number,pr_close)
plt.grid()
plt.xlabel('Liczba zdjęć')
plt.ylabel('Białe piksele')
plt.title('Wykres zależności białych pikseli do wszystkich pikseli na obrazie - close [%]')
plt.show()