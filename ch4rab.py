import tkinter as tk
import threading
import traceback
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


ON_LBL = 'Listening..'
OFF_LBL = 'Waiting..'


class Gui(tk.Frame):

	def __init__(self, master = None):
		tk.Frame.__init__(self, master)
		master.grid_columnconfigure(0, weight=1)
		self.top_frame = tk.Frame(master)
		self.bot_frame = tk.Frame(master)
		self.top_frame.grid(row=0, column=0)
		self.bot_frame.grid(row=1, column=0)

		# Theming™
		self.colour_scheme('dark')
		master.configure(bg=self.bg)
		for frame in [self.top_frame, self.bot_frame]:
			frame.configure(bg=self.bg)

		self.is_downloading = False
		self.last_url = ''
		self.current_url = 'X'

		self.add_elements()
		self.run_listener()


	def colour_scheme(self, mode):
		"""Define colour scheming for the whole program.
		
		Keyword arguments:
		mode -- selection of dark/light colouring for the program. only dark for now.
		"""
		if mode == 'dark':
			self.bg, self.fg, self.ac1, self.ac2 = ('#282828', '#CAD2C5', '#404040', '#B3B3B3')
		if mode == 'light':
			self.bg, self.fg, self.ac1, self.ac2 = ('#FBF8F1', 'black', '#F7ECDE', '#E9DAC1')

	def add_elements(self):
		"""Draw GUI elements."""
		self.on_image = tk.PhotoImage(width=48, height=24)
		self.off_image = tk.PhotoImage(width=48, height=24)
		self.on_image.put(('green',), to=(0, 0, 23, 23))
		self.off_image.put(('red',), to=(24, 0, 47, 23))

		self.toggle_is_on = tk.StringVar(value=OFF_LBL)
		self.toggle_colour = tk.StringVar(value='red')
		self.toggle_is_on.trace('w', self.update_check_text)

		self.checkbox = tk.Checkbutton(self.top_frame, image=self.off_image, selectimage=self.on_image, indicatoron=False,
			onvalue=ON_LBL, offvalue=OFF_LBL, variable=self.toggle_is_on)
		self.check_label = tk.Label(self.top_frame, text=self.toggle_is_on.get())
		self.status_label = tk.Label(self.bot_frame, text='Copy a 4chan reply URL.')

		for el in [self.checkbox, self.check_label, self.status_label]:
			el.pack(side='left', pady=10, padx=10)
			el.configure(bg=self.bg, fg=self.fg, borderwidth=0)

		self.check_label.configure(fg=self.toggle_colour.get())
		self.checkbox.configure(bg=self.ac1)

	def update_check_text(self, *args):
		if self.toggle_colour.get() == 'red':
			self.toggle_colour.set('green')
		else:
			self.toggle_colour.set('red')
		self.check_label.configure(text=self.toggle_is_on.get(), fg=self.toggle_colour.get())

	def run_listener(self):
		"""Header function for periodic calls, gets recalled every 1s."""
		self.check_clipboard()
		self.check_last_url()
		self.after(1000, self.run_listener)

	def check_last_url(self):
		# if toggle is on
		# and not downloading
		# FIXME: i mean, as long as the status callback doesn't return from cad, it will always be not downloading
		# and current url is not the same as the last
		# and url is a 4chan url
		if (self.toggle_is_on.get() == ON_LBL 
			and not self.is_downloading
			and not (self.current_url == self.last_url)
			and (self.current_url.startswith('https://boards.4chan.org/') or self.current_url.startswith('https://boards.4channel.org/'))):

			self.is_downloading = True
			self.last_url = self.current_url
			self.current_url = 'X'
			t = threading.Thread(target=self.start, args=(self.last_url,))
			t.start()

	def check_clipboard(self):
		"""Check if a 4chan URL is on clipboard & pass to cad.check_url().
		Gets called periodically in run_listener().
		"""
		try:
			clip_val = self.clipboard_get()
			if (clip_val.startswith('https://boards.4chan.org/') or clip_val.startswith('https://boards.4channel.org/')):
				self.current_url = clip_val
		except Exception:
			# FIXME: could possibly pass this to not fill up the terminal with errors when it copies an image to the clipboard
			traceback.print_exc()

	def start(self, url):
		self.update_status('Downloading..')
		response = check_url(url)
		print(f'response: {response}')
		self.update_status(response)
		self.is_downloading = False

	def update_status(self, text):
		self.status_label.configure(text=str(text))

# --- beg: cad.py ---

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

	response = download_panel(url, id, end_res)
	if response:
		return response

	return f'Complete /{board}/ {id}.png.'

def download_panel(url, id, end_res):
	chrome_options = Options()
	chrome_options.add_argument('--headless')

	browser = webdriver.Chrome(options=chrome_options)
	browser.get(url)

	try: # wait a bit of loading until element could be present on the page
		element = WebDriverWait(browser, 10).until(
			EC.presence_of_element_located((By.ID, id))
		)
		element.screenshot(end_res)
	except Exception:
		traceback.print_exc()
		return 'Could not get the image.'

# --- end: cad.py ---

def get_geometry():
	"""Return geometry to spawn the program in the middle of the screen.
	Only in 1920px width.
	"""
	return '215x90+94+145'

def start_gui():
	"""Launch GUI."""
	root = tk.Tk(className='ch4rab')
	root.title('ch4rab')
	root.geometry(get_geometry())
	app = Gui(master=root)
	app.mainloop()


if __name__ == '__main__':
	start_gui()
