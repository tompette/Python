import cv2
import csv
import os
import numpy as np
#---------CHANGE THE NAME OF FILE FOR EVERY PLANTS----------------
with open('new_csv_data_all.csv', 'w') as f:
    pass

path = "C:\\Users\\misia\\Desktop\\mgr\\data"
photos = os.listdir(path)
row = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for foto in photos:
    row[0] = foto[5:7]
    row[1] = foto[8:10]
    row[2] = foto[11:15]
    img = cv2.imread("C:\\Users\\misia\\Desktop\\mgr\\data\\"+foto) #obecne zdjecie

    # --------2. PRZYCINANIE ZDJECIA--------------------------------------------
    #-----------PIERWSZA ROŚLINA---------------
    #y = 250
    #x = 0
    #h = 450
    #w = 450
    # ----------DRUGA ROŚLINA------------------
    #y = 250 #200
    #x = 450   #0
    #h = 450 #600
    #w = 450 #1920
    # -------TRZECIA ROŚLINA----------------
    #y = 250
    #x = 900
    #h = 450 #600
    #w = 430 #1920
    # -------CZWARTA ROŚLINA----------------
    #y = 250
    #x = 1330
    #h = 450  # 600
    #w = 590  # 1920

    #----------DLA WSZYSTKICH ROŚLIN USTAWIENIE PRZYCIĘCIA---------------------
    y = 200
    x = 0
    h = 600
    w = 1920

    # ------przycięte zdjęcia----------------
    crop = img[y:y + h, x:x + w]

    # -------3. OBROBKA ZDJECIA: SKALA HSV:-------------------------------------
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    green_lower = np.array([21, 0, 0])
    green_upper = np.array([69, 255, 157])
    mask = cv2.inRange(hsv, green_lower, green_upper)
    result_after_hsv_mask = cv2.bitwise_and(crop, crop, mask=mask)

    # -----------4. odczyt w skali szarosci--------------------
    img_gray = cv2.cvtColor(result_after_hsv_mask, cv2.COLOR_BGR2GRAY)
    gray_pixel = np.count_nonzero(img_gray)  # -------------------------2 kolumna
    row[3] = gray_pixel
    #------------5. POLICZ PIKSELE--------------------------
    tot_pixel = img_gray.size
    percentage1 = round(gray_pixel * 100 / tot_pixel, 2)  # -------------------------3 kolumna
    row[4] = percentage1
    # -------PROGROWANIE GLOBALNE------------
    ret, img_bin = cv2.threshold(img_gray, 40, 255, cv2.THRESH_BINARY)  # bylo: 128
    bin_pixel = np.count_nonzero(img_bin)  # -----------------------------------------4 kolumna
    row[5] = bin_pixel
    percentage_bin = round(bin_pixel * 100 / tot_pixel, 2)  # ------------------------5 kolumna
    row[6] = percentage_bin
    # -------6. BINARYZACJA OTSU--------------------------------------------------------------
    retval2, img_otsu = cv2.threshold(img_gray, 175, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    otsu_pixel = np.count_nonzero(img_otsu)  # ---------------------------------------6 kolumna
    row[7] = otsu_pixel
    percentage_otsu = round(otsu_pixel * 100 / tot_pixel, 2)  # ----------------------7 kolumna
    row[8] = percentage_otsu

    # -------7. OTWARCIE=DYLATACJA + EROZJA---------------------------------------------------
    kernel = np.ones((5, 5), np.uint8)
    img_open = cv2.morphologyEx(img_otsu, cv2.MORPH_OPEN, kernel)
    open_pixel = np.count_nonzero(img_open)  # ---------------------------------------8 kolumna
    row[9] = open_pixel
    percentage_open = round(open_pixel * 100 / tot_pixel, 2)  # ----------------------9 kolumna
    row[10] = percentage_open
    # -------8. ZAMKNIĘCIE -------------------------------------------------------------------
    img_close = cv2.morphologyEx(img_otsu, cv2.MORPH_CLOSE, kernel)
    close_pixel = np.count_nonzero(img_close)  # -------------------------------------10 kolumna
    row[11] = close_pixel
    percentage_close = round(close_pixel * 100 / tot_pixel, 2)  # --------------------11 kolumna
    row[12] = percentage_close

    # ---------CHANGE THE NAME OF FILE FOR EVERY PLANTS----------------
    with open('new_csv_data_all.csv', 'a', newline='') as f:
        data = row # wpisuje sie wartosc row do wiersza w CSV
        csvwriter = csv.writer(f)
        csvwriter.writerow(data)
