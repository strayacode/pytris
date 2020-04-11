import pygame


class Button:
	pygame.font.init()
	font = pygame.font.Font("visitor1.ttf", 20)
	def __init__(self, x, y, width, height, bg, fg, text, window):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.bg = bg
		self.fg = fg
		self.text = text
		self.window = window
		self.hidden = False
		self.draw()
		


	def draw(self):
		pygame.draw.rect(self.window, self.bg, (self.x, self.y, self.width, self.height), 0)

		text = self.font.render(self.text, True, self.fg)
		self.window.blit(text, (self.x + self.width/2 - text.get_width()/2, self.y + self.height/2 - text.get_height()/2))

	def enter(self, pos):
		if pos[0] > self.x and pos[0] < self.x + self.width:
			if pos[1] > self.y and pos[1] < self.y + self.height:
				return True

		return False

	def hide(self):
		self.hidden = True














