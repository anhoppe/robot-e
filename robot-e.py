from tkinter import *
from PIL import ImageTk, Image

class App():
	def __init__(self):
		self.shotSpeed = 3
		self.doveSpeed = 2
		self.maxY = 600
		
		self.root = Tk()
		self.canvas = Canvas(self.root, width = 800, height = 600)		

		# Setup player
		img = ImageTk.PhotoImage(Image.open("pinguin-man.png"))		
		self.xPos = 605
		self.yPos = 100
		self.xPrev = self.xPos
		self.yPrev = self.yPos
		self.arrowUp = False
		self.arrowDown = False
		self.arrowLeft = False
		self.arrowRight = False
		self.player = self.canvas.create_image(self.xPos, self.yPos, image=img)	

		
		# Setup enemy
		doveImg =  ImageTk.PhotoImage(Image.open("buntemoewe.png"))
		self.doveX = 40
		self.doveY = 120
		self.dove = self.canvas.create_image(self.doveX, self.doveY, image=doveImg)
		self.moveDown = True

		# Setup round
		self.roundImage = ImageTk.PhotoImage(Image.open("feuerball.png"))
		self.round = None
		self.roundX = 0
		self.roundY = 0

		# Key binding
		self.canvas.bind("<KeyPress>", self.keydown)
		self.canvas.bind("<KeyRelease>", self.keyup)
		
		self.canvas.pack(expand=1, fill=BOTH)
		self.canvas.focus_set()
		self.update_clock()
		self.root.mainloop()


	def update_clock(self):
		if self.arrowUp:
			self.yPos -= 1
		if self.arrowDown:
			self.yPos += 1
		if self.arrowLeft:
			self.xPos -= 1
		if self.arrowRight:
			self.xPos += 1

		self.canvas.move(self.player, self.xPos - self.xPrev, self.yPos - self.yPrev)
		self.xPrev = self.xPos
		self.yPrev = self.yPos
		self.root.after(15, self.update_clock)

		if self.round != None:
			self.canvas.move(self.round, -self.shotSpeed, 0)
			self.roundX -= self.shotSpeed

		doveDelta = self.doveSpeed = 2
		if self.moveDown:
			if self.doveY > self.maxY:
				self.moveDown = False
		else:
			doveDelta = -self.doveSpeed
			if self.doveY < 0:
				self.moveDown = True

		self.canvas.move(self.dove, 0, doveDelta)
		self.doveY += doveDelta



	def keyup(self, e):
		if e.keycode == 38:
			self.arrowUp = False
		if e.keycode == 40:
			self.arrowDown = False
		if e.keycode == 39:
			self.arrowRight = False
		if e.keycode == 37:
			self.arrowLeft = False
		if e.keycode == 32:
			self.round = self.canvas.create_image(self.xPos, self.yPos, image=self.roundImage)
			self.roundX = self.xPos
			self.roundY = self.yPos


	def keydown(self, e):
		if e.keycode == 38:
			self.arrowUp = True
		if e.keycode == 40:
			self.arrowDown = True
		if e.keycode == 39:
			self.arrowRight = True
		if e.keycode == 37:
			self.arrowLeft = True


app=App()
