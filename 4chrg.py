from selenium import webdriver
import cv2
import os


# 4chan and 4channel have different background colours
# likely will need to crop the image to the borders of these background colours

# 4channel: #d6bad0, #ba9dbf (border)
# 4chan:    #f0c0b0, #d99f91 (border)
# as long as it's the default theme, so maybe use a different method?


URL = 'https://boards.4channel.org/mu/thread/111250954#p111251146'

RES = 'results'
if not os.path.isdir(RES):
	os.mkdir(RES)

TEMP_IMG = os.path.join(RES, 'screen_temp.png')
END_RES = os.path.join(RES, 'screen.png')

def start():
	browser = webdriver.Chrome()
	browser.get(URL)
	browser.save_screenshot(TEMP_IMG)

	img = cv2.imread(TEMP_IMG)
	y = 0
	x = 0
	h = 100
	w = 200
	crop_img = img[y: y + h, x: x + w]

	cv2.imwrite(END_RES, crop_img)







if __name__ == '__main__':
	start()
