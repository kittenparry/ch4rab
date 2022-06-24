from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


URL = 'https://boards.4channel.org/mu/thread/111250954#p111251146'
ID = URL.split('#')[-1]                   # p111251146
THREAD = URL.split('/')[-1].split('#')[0] # 111250954
BOARD = URL.split('/')[-3]                # mu

RES = 'results'
if not os.path.isdir(RES):
	os.mkdir(RES)

# results/mu/111250954/
DEST_DIR = os.path.join(RES, BOARD, THREAD)
if not os.path.isdir(DEST_DIR):
	os.makedirs(DEST_DIR)

END_RES = os.path.join(DEST_DIR, f'{ID}.png')

chrome_options = Options()
chrome_options.add_argument('--headless')

def start():
	browser = webdriver.Chrome(options=chrome_options)
	browser.get(URL)

	element = browser.find_element_by_id(ID)
	element.screenshot(END_RES)


if __name__ == '__main__':
	start()
