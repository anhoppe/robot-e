from tkinter import *
from PIL import ImageTk, Image
import random

class App():
	def __init__(self):
		self.playerShotSpeed = 3
		self.enemySpeed = 2
		self.maxY = 600
		self.maxX = 800

		self.clockSpeed = 15
		
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
		self.alive = 3
		self.size = 80

		# Setup player round
		self.roundImage = ImageTk.PhotoImage(Image.open("feuerball.png"))
		self.round = None
		self.roundX = 0
		self.roundY = 0

		
		# Setup enemy
		doveImg =  ImageTk.PhotoImage(Image.open("buntemoewe.png"))
		self.enemyAlive = 3
		self.doveX = 40
		self.doveY = 120
		self.dove = self.canvas.create_image(self.doveX, self.doveY, image=doveImg)
		self.moveDown = True
		self.enemySize = 100
		self.enemyShotSpeed = 6
		
		# Setup enemy round
		self.enemyRoundImage = ImageTk.PhotoImage(Image.open("moewenball.png"))
		self.enemyRround = None
		self.enemyRoundX = 0
		self.enemyRoundY = 0
		self.enemyShotPropabilityPercent = 5

		# Key binding
		self.canvas.bind("<KeyPress>", self.keydown)
		self.canvas.bind("<KeyRelease>", self.keyup)
		
		self.canvas.pack(expand=1, fill=BOTH)
		self.canvas.focus_set()
		self.update_clock()
		self.root.mainloop()


	def update_clock(self):
		# Move player
		if self.alive > 0:
			if self.arrowUp:
				self.yPos -= 1
			if self.arrowDown:
				self.yPos += 2
			if self.arrowLeft:
				self.xPos -= 3
			if self.arrowRight:
				self.xPos += 4

			self.canvas.move(self.player, self.xPos - self.xPrev, self.yPos - self.yPrev)
			self.xPrev = self.xPos
			self.yPrev = self.yPos

		# Move player shot
		if self.round != None:
			self.canvas.move(self.round, -self.playerShotSpeed, 0)
			self.roundX -= self.playerShotSpeed
			if abs(self.roundX - self.doveX) < self.enemySize and abs(self.roundY - self.doveY) < self.enemySize:
				self.enemyAlive -= 1
				self.canvas.delete(self.round)
				self.round = None

		if self.enemyAlive > 0:
			# Move enemy
			enemyDelta = self.enemySpeed = 2
			if self.moveDown:
				if self.doveY > self.maxY:
					self.moveDown = False
			else:
				enemyDelta = -self.enemySpeed
				if self.doveY < 0:
					self.moveDown = True

			self.canvas.move(self.dove, 0, enemyDelta)
			self.doveY += enemyDelta

			# Move enemy round
			if self.enemyRround != None:
				self.canvas.move(self.enemyRround, self.enemyShotSpeed, 0)
				self.enemyRoundX += self.playerShotSpeed
				
				if abs(self.enemyRoundX - self.xPos) < self.size and abs(self.enemyRoundY - self.yPos) < self.size:
					self.alive -= 1
					self.canvas.delete(self.enemyRround)
					self.enemyRround = None

				if self.enemyRoundX > self.maxX:
					self.canvas.delete(self.enemyRround)
					self.enemyRround = None
			# Shoot enemy
			else:
				shoot = random.randint(0, 100)

				if shoot < self.enemyShotPropabilityPercent:				
					self.enemyRround = self.canvas.create_image(self.doveX, self.doveY, image=self.enemyRoundImage)
					self.enemyRoundX = self.doveX
					self.enemyRoundY = self.doveY

		self.root.after(self.clockSpeed, self.update_clock)


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
			if self.round != None:
				self.canvas.delete(self.round)
				self.round = None
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
