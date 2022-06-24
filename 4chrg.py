import tkinter as tk
import threading
import traceback


# TODO: downloading ID, complete ID status labels


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

		self.add_elements()


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

		self.toggle_is_on = tk.StringVar(value='Listening..')
		self.toggle_colour = tk.StringVar(value='green')
		self.toggle_is_on.trace('w', self.update_check_text)

		self.checkbox = tk.Checkbutton(self.top_frame, image=self.off_image, selectimage=self.on_image, indicatoron=False,
			onvalue='Listening..', offvalue='Waiting..', variable=self.toggle_is_on)

		self.check_label = tk.Label(self.top_frame, text=self.toggle_is_on.get())

		self.status_label = tk.Label(self.bot_frame, text='Downloaded 23489234982398.png.')


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




def get_geometry():
	"""Return geometry to spawn the program in the middle of the screen.
	Only in 1920px width.
	"""
	return '250x90+94+145'

def start_gui():
	"""Launch GUI."""

	root = tk.Tk(className='4chan-reply-grabber')
	root.title('4chan-reply-grabber')
	root.geometry(get_geometry())

	app = Gui(master=root)

	app.mainloop()


if __name__ == '__main__':
	start_gui()
