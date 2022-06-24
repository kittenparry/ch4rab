from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import re

# https://boards.4channel.org/mu/thread/111250954#p111251146
# 1-4 characters including numbers for 4chan board names
pattern = 'https:\/\/boards\.(4chan|4channel).org\/[a-zA-Z0-9]{1,4}\/thread\/[0-9]+#p[0-9]+'

def check_url(url):
	if not url.startswith('https://boards.4chan.org/') and \
		not url.startswith('https://boards.4channel.org/'):
		# FIXME: never reaches here, as it gets filtered in the main program already
		print('Not 4chan URL, terminating.')
		return 'Not a 4chan URL.'

	print(f'Starting for {url}..')

	if not re.fullmatch(pattern, url):
		print('Not a reply URL, terminating.')
		return 'Not a 4chan reply URL.'

	RES = 'results'
	if not os.path.isdir(RES):
		os.mkdir(RES)

	# https://boards.4channel.org/mu/thread/111250954#p111251146
	id = url.split('#')[-1]                   # p111251146
	thread = url.split('/')[-1].split('#')[0] # 111250954
	board = url.split('/')[-3]                # mu

	# results/mu/111250954/
	dest_dir = os.path.join(RES, board, thread)
	if not os.path.isdir(dest_dir):
		os.makedirs(dest_dir)

	end_res = os.path.join(dest_dir, f'{id}.png')

	download_panel(url, id, end_res)
	return f'Complete /{board}/ {id}.png.'

def download_panel(url, id, end_res):
	chrome_options = Options()
	chrome_options.add_argument('--headless')

	browser = webdriver.Chrome(options=chrome_options)
	browser.get(url)

	element = browser.find_element_by_id(id)
	element.screenshot(end_res)


if __name__ == '__main__':
	url = 'https://boards.4channel.org/mu/thread/111250954#p111251146'
	check_url(url)
