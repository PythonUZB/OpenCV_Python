# pip install pandas opencv-python
'''
kanallarimizga obuna bo'ling
https://t.me/python_uzb_test
'''


import cv2
import pandas as pd

# --------------------------------------------------------------------------

img_path = 'pic1.jpg'
csv_path = 'colors.csv'

# CSV faylini o'qish
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)

# o'qish tasviri
img = cv2.imread(img_path)
img = cv2.resize(img, (800,600))

# global o'zgaruvchilarni e'lon qilish
clicked = False
r = g = b = xpos = ypos = 0

# rang, barcha ranglardan minimal masofani hisoblash va eng mos rangni olish
def rangni_nomini_olish(R,G,B):
	minimum = 1000
	for i in range(len(df)):
		d = abs(R - int(df.loc[i,'R'])) + abs(G - int(df.loc[i,'G'])) + abs(B - int(df.loc[i,'B']))
		if d <= minimum:
			minimum = d
			cname = df.loc[i, 'color_name']

	return cname

#funktsiya Sichqonchani ikki marta bosish x, y koordinatalarini olish uchun 
def chizish_funktsiyasi(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDBLCLK:
		global b, g, r, xpos, ypos, clicked
		clicked = True
		xpos = x
		ypos = y
		b,g,r = img[y,x]
		b = int(b)
		g = int(g)
		r = int(r)

# yaratish oynasi
cv2.namedWindow('image')
cv2.setMouseCallback('image', chizish_funktsiyasi)

while True:
	cv2.imshow('image', img)
	if clicked:
		# cv2.rectangle (rasm, boshlanish nuqtasi, so'nggi nuqta, rang, qalinlik) -1 butun to'rtburchakni to'ldiradi
		cv2.rectangle(img, (20,20), (600,60), (b,g,r), -1)

		# Ko'rsatish uchun matn satrini yaratish (Rang nomi va RGB qiymatlari)
		text = rangni_nomini_olish(r,g,b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
		#cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
		cv2.putText(img, text, (50,50), 2,0.8, (255,255,255),2,cv2.LINE_AA)

		# Juda ochiq ranglar uchun biz matnni qora rangda namoyish etamiz
		if r+g+b >=600:
			cv2.putText(img, text, (50,50), 2,0.8, (0,0,0),2,cv2.LINE_AA)

	if cv2.waitKey(20) & 0xFF == 27:
		break

cv2.destroyAllWindows()
