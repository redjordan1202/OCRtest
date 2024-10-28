import cv2 as cv
import pytesseract
import re
import os
import imutils
from tkinter import filedialog

img_path = filedialog.askopenfilename(initialdir=os.getcwd())

org_img = cv.imread(img_path)
img = org_img.copy()
img = imutils.resize(img, width=500)
ratio = org_img.shape[0] / float(org_img.shape[1])
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

price_pattern = r'([0-9]+\.[0-9]+)'
raw_data = pytesseract.image_to_string(img, lang='eng', config='--psm 4')
total_lines = []

for line in raw_data.splitlines():
    line = re.sub(r'[^a-zA-Z0-9 .-]',r'', line)
    line = line.lower()
    print(line)
    if re.search(price_pattern, line):
        if 'total' in line:
            total_lines.append(line)

if total_lines:
    total = re.findall(price_pattern, total_lines[-1])
    if total:
        print(f"Estimated total is {total[0]}")
else:
    raw_data = pytesseract.image_to_string(img, lang='eng', config='--psm 11')
    print("=" * 10)
    prices = re.findall(price_pattern, raw_data)
    if prices:
        total = max(prices)
        print(f"Estimated total is {total}")
    else:
        print("No estimated prices found")
