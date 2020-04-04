import pygame


class Grid:
	colours = {0: (0, 0, 0), 1: (178, 250, 180), 2: (222, 98, 91), 3: (74, 178, 199), 4: (227, 221, 107), 5: (235, 167, 84), 6: (104, 174, 217), 7: (208, 111, 227)}
	dark_grey = ((30, 30, 30))
	pygame.font.init()
	font = pygame.font.Font("visitor1.ttf", 20) 
	

	def __init__(self, x, y, block_size, window):
		self.x = x
		self.y = y
		self.block_size = block_size
		self.window = window
		self.total_lines = 0
		self.level = 1
		self.score = 0
		self.grid = self.create_grid()
		self.locked_positions = []
		self.queue = []
		self.draw_board(self.window)
		# self.display_info(self.window)

	def create_grid(self):
		grid = []
		for i in range(21):
			grid.append([0 for j in range(11)])
		return grid

	def draw_board(self, window):
		pygame.draw.rect(window, self.dark_grey, (self.x, self.y, 10*self.block_size, 20*self.block_size))
		# for i in range(11):
		# 	pygame.draw.line(window, self.dark_grey, (self.x + i*self.block_size, self.y), (self.x + i*self.block_size, self.y + 20*self.block_size))

		# for j in range(21):
		# 	pygame.draw.line(window, self.dark_grey, (self.x, self.y + j*self.block_size), (self.x + 10*self.block_size, self.y + j*self.block_size))

	def draw_grid(self, window):
		for i in range(20):
			for j in range(10):
				# print(self.grid[i][j])
				if self.grid[i][j] != 0:
					pygame.draw.rect(window, self.colours[self.grid[i][j]], (self.x + self.block_size*j, self.y + self.block_size*i, self.block_size, self.block_size))


	def display_info(self, window):
		lines = self.font.render(f"LINES: {self.total_lines}", True, (255, 255, 255), (0, 0, 0))
		level = self.font.render(f"LEVEL: {self.level}", True, (255, 255, 255), (0, 0, 0))

		next_shape = self.font.render(f"NEXT", True, (255, 255, 255), (0, 0, 0))
		score = self.font.render(f"SCORE: {self.score}", True, (255, 255, 255), (0, 0, 0))
		window.blit(lines, (self.x + 11*self.block_size, self.y + 1*self.block_size))
		window.blit(level, (self.x + 11*self.block_size, self.y + 1*self.block_size + 50))
		window.blit(next_shape, (self.x + 19*self.block_size, self.y + 1*self.block_size))
		window.blit(score, (self.x + 11*self.block_size, self.y + 1*self.block_size + 100))
		for i in range(len(self.queue[1][0])):
			for j in range(len(self.queue[1][0][i])):
				# print(self.queue[0][0][i][j])
				pygame.draw.rect(window, self.colours[int(self.queue[1][0][i][j])], (self.x + j*self.block_size + 380, self.y + self.block_size*i + 50, self.block_size, self.block_size))


		for i in range(len(self.queue[2][0])):
			for j in range(len(self.queue[2][0][i])):
				# print(self.queue[0][0][i][j])
				pygame.draw.rect(window, self.colours[int(self.queue[2][0][i][j])], (self.x + j*self.block_size + 380, self.y + self.block_size*i + 125, self.block_size, self.block_size))


		for i in range(len(self.queue[3][0])):
			for j in range(len(self.queue[3][0][i])):
				# print(self.queue[0][0][i][j])
				pygame.draw.rect(window, self.colours[int(self.queue[3][0][i][j])], (self.x + j*self.block_size + 380, self.y + self.block_size*i + 200, self.block_size, self.block_size))

		for i in range(len(self.queue[4][0])):
			for j in range(len(self.queue[4][0][i])):
				# print(self.queue[0][0][i][j])
				pygame.draw.rect(window, self.colours[int(self.queue[4][0][i][j])], (self.x + j*self.block_size + 380, self.y + self.block_size*i + 275, self.block_size, self.block_size))


		for i in range(len(self.queue[5][0])):
			for j in range(len(self.queue[5][0][i])):
				# print(self.queue[0][0][i][j])
				pygame.draw.rect(window, self.colours[int(self.queue[5][0][i][j])], (self.x + j*self.block_size + 380, self.y + self.block_size*i + 350, self.block_size, self.block_size))


		for i in range(len(self.queue[6][0])):
			for j in range(len(self.queue[6][0][i])):
				# print(self.queue[0][0][i][j])
				pygame.draw.rect(window, self.colours[int(self.queue[6][0][i][j])], (self.x + j*self.block_size + 380, self.y + self.block_size*i + 425, self.block_size, self.block_size))
	
