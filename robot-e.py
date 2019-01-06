from tkinter import *
from PIL import ImageTk, Image

class App():
	def __init__(self):
		self.root = Tk()
		self.canvas = Canvas(self.root, width = 800, height = 600)
		
		img = ImageTk.PhotoImage(Image.open("pinguin-man.png"))		
		self.xPos = 100
		self.yPos = 100
		self.player = self.canvas.create_image(self.xPos, self.yPos, image=img)
		









		self.canvas.pack(expand=1, fill=BOTH)
		self.update_clock()
		self.root.mainloop()


	def update_clock(self):
		self.canvas.move(self.player, 1, 0)
		self.root.after(0, self.update_clock)

app=App()
