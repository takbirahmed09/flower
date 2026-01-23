import cv2
import numpy as np

# ছবি লোড করা (আপনার ছবির ফাইলের নাম অনুযায়ী পরিবর্তন করুন)
image = cv2.imread('flower_image.jpg')

# BGR থেকে HSV ফরম্যাটে রূপান্তর (রঙ শনাক্ত করার জন্য ভালো)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# বেগুনি রঙের রেঞ্জ নির্ধারণ (ফুলের পাপড়ির জন্য)
lower_purple = np.array([130, 50, 50])
upper_purple = np.array([170, 255, 255])

# মাস্ক তৈরি করা
mask = cv2.inRange(hsv, lower_purple, upper_purple)

# মূল ছবির ওপর মাস্ক প্রয়োগ করা
result = cv2.bitwise_and(image, image, mask=mask)

# ছবিগুলো দেখানো
cv2.imshow('Original Image', image)
cv2.imshow('Purple Parts Only', result)

cv2.waitKey(0)
cv2.destroyAllWindows()
