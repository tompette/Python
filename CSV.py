import cv2
import csv
import os
import numpy as np

with open('csv_data.csv', 'w') as f:
    pass

path = "\data"
photos = os.listdir(path)
row = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for foto in photos:
    row[0] = foto[5:7] # 1 kolumna - miesiac
    print(foto[5:7])
    row[1] = foto[8:10] # 2 kolumna - dzien
    print(foto[8:10])
    row[2] = foto[11:15] # 3 kolumna - godzina w formacie godzmin (np. 1200)
    print(foto[11:15])
    img = cv2.imread("data\\"+foto) #current foto

    # --------2. PRZYCINANIE ZDJECIA--------------------------------------------
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

    # -------------rozne maski na zdjeciach - do przejrzenia--------------------
    mask_open1 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask_dilate1 = cv2.morphologyEx(mask_open1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
    mask_close1 = cv2.morphologyEx(mask_dilate1, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    # res11 = cv2.bitwise_and(crop,crop, mask = mask_close1)
    # cv2.imwrite("C:/Users/misia/Documents/tl2/1_2021-08-15-0000_crop1.jpg", res11)
    res22 = cv2.bitwise_and(crop, crop, mask=mask)

    # -------4. POLICZ PIKSELE ---------------------------------------------------------------
    tot_pixel = res22.size
    green_pixel = np.count_nonzero(res22)  # -----------------------------------------4 kolumna - ilosc zielonych pikseli
    row[3] = green_pixel
    percentage1 = round(green_pixel * 100 / tot_pixel, 2)  # -------------------------5 kolumna - piksele w procentach
    row[4] = percentage1

    # -------5. BIN GLOB ---------------------------------------------------------------------
    # -----------odczyt w skali szarosci--------------------
    img_gray = cv2.cvtColor(res22, cv2.COLOR_BGR2GRAY)
    
    # -------PROGROWANIE GLOBALNE------------
    ret, img_bin = cv2.threshold(img_gray, 40, 255, cv2.THRESH_BINARY)  # bylo: 128
    bin_pixel = np.count_nonzero(img_bin)  # -----------------------------------------6 kolumna - bin piksele
    row[5] = bin_pixel
    percentage_bin = round(bin_pixel * 100 / tot_pixel, 2)  # ------------------------7 kolumna - % bin
    row[6] = percentage_bin

    # -------6. BINARYZACJA OTSU--------------------------------------------------------------
    retval2, img_otsu = cv2.threshold(img_gray, 175, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    otsu_pixel = np.count_nonzero(img_otsu)  # ---------------------------------------8 kolumna - otsu piksele
    row[7] = otsu_pixe
    percentage_otsu = round(otsu_pixel * 100 / tot_pixel, 2)  # ----------------------9 kolumna - otsu %
    row[8] = percentage_otsu

    # -------7. OTWARCIE=DYLATACJA + EROZJA---------------------------------------------------
    kernel = np.ones((5, 5), np.uint8)
    img_open = cv2.morphologyEx(img_otsu, cv2.MORPH_OPEN, kernel)
    open_pixel = np.count_nonzero(img_open)  # ---------------------------------------10 kolumna - open piksele
    row[9] = open_pixel
    percentage_open = round(open_pixel * 100 / tot_pixel, 2)  # ----------------------11 kolumna - open %
    row[10] = percentage_open

    # -------8. ZAMKNIĘCIE -------------------------------------------------------------------
    img_close = cv2.morphologyEx(img_otsu, cv2.MORPH_CLOSE, kernel)
    close_pixel = np.count_nonzero(img_close)  # -------------------------------------12 kolumna - close piksele
    row[11] = close_pixel
    percentage_close = round(close_pixel * 100 / tot_pixel, 2)  # --------------------13 kolumna - close %
    row[12] = percentage_close
    
    with open('csv_data.csv', 'a', newline='') as f:
        data = row # wpisuje sie wartosc row do wiersza w CSV
        csvwriter = csv.writer(f)
        csvwriter.writerow(data)
