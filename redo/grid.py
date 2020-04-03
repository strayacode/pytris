import pygame


class Grid:
	colours = {0: (0, 0, 0), 1: (178, 250, 180), 2: (222, 98, 91), 3: (74, 178, 199), 4: (227, 221, 107), 5: (235, 167, 84), 6: (104, 174, 217), 7: (208, 111, 227)}
	dark_grey = ((50, 50, 50))
	def __init__(self, x, y, block_size, window):
		self.x = x
		self.y = y
		self.block_size = block_size
		self.window = window
		self.locked_positions = []
		self.grid = self.create_grid()
		self.draw_board(self.window)

	def create_grid(self):
		grid = []
		for i in range(21):
			grid.append([0 for j in range(11)])
		return grid

	def draw_board(self, window):
		for i in range(11):
			pygame.draw.line(window, self.dark_grey, (self.x + i*self.block_size, self.y), (self.x + i*self.block_size, self.y + 20*self.block_size))

		for j in range(21):
			pygame.draw.line(window, self.dark_grey, (self.x, self.y + j*self.block_size), (self.x + 10*self.block_size, self.y + j*self.block_size))

	def draw_grid(self, window):
		for i in range(20):
			for j in range(10):
				# print(self.grid[i][j])
				pygame.draw.rect(window, self.colours[self.grid[i][j]], (self.x + self.block_size*j, self.y + self.block_size*i, self.block_size, self.block_size))

	
