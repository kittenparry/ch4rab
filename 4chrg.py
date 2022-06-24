import tkinter as tk
import threading
import traceback


class Gui(tk.Frame):

	def __init__(self, master = None):
		tk.Frame.__init__(self, master)
		self.main_frame = tk.Frame(master)
		self.main_frame.pack()

		self.add_elements()


	def add_elements(self):
		"""Draw GUI elements."""
		self.on_image = tk.PhotoImage(width=48, height=24)
		self.off_image = tk.PhotoImage(width=48, height=24)
		self.on_image.put(("green",), to=(0, 0, 23, 23))
		self.off_image.put(("red",), to=(24, 0, 47, 23))

		self.var1 = tk.IntVar(value=1)
		self.var2 = tk.IntVar(value=0)
		self.cb1 = tk.Checkbutton(self.main_frame, image=self.off_image, selectimage=self.on_image, indicatoron=False,
			onvalue=1, offvalue=0, variable=self.var1)
		self.cb2 = tk.Checkbutton(self.main_frame, image=self.off_image, selectimage=self.on_image, indicatoron=False,
			onvalue=1, offvalue=0, variable=self.var2)

		self.cb1.pack(padx=20, pady=10)
		self.cb2.pack(padx=20, pady=10)








def get_geometry():
	"""Return geometry to spawn the program in the middle of the screen.
	Only in 1920px width.
	"""
	program_width = 650
	screen_width = 1920
	x_position = (screen_width - program_width) / 2
	return '%dx555+%d+30' % (program_width, x_position)

def start_gui():
	"""Launch GUI."""

	root = tk.Tk(className='4chan-reply-grabber')
	root.title('4chan-reply-grabber')
	root.geometry(get_geometry())

	app = Gui(master=root)

	app.mainloop()


if __name__ == '__main__':
	start_gui()
