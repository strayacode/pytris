import pygame
from grid import Grid
import random
import sys

width = 500
height = 500

pygame.init()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")

S = [[
		"011",
		"110",
		"000"
	],
	[
		"010",
		"011",
		"001"
	],
	[
		"000",
		"011",
		"110"
	],
	[
		"100",
		"110",
		"010"
	]]


Z = [[
		"220",
		"022",
		"000"
	],
	[
		"002",
		"022",
		"020"
	],
	[
		"000",
		"220",
		"022"
	],
	[
		"020",
		"220",
		"200"
	]]

I = [[
		"0000",
		"3333",
		"0000",
		"0000"
	],
	[
		"0030",
		"0030",
		"0030",
		"0030"
	],
	[
		"0000",
		"0000",
		"3333",
		"0000"
	],
	[
		"0300",
		"0300",
		"0300",
		"0300"
	]]


O = [[
		"0440",
		"0440",
		"0000"
	]]

J = [[
		"500",
		"555",
		"000"
	],
	[
		"055",
		"050",
		"050"
	],
	[
		"000",
		"555",
		"005"
	],
	[
		"050",
		"050",
		"550"
	]]


L = [[
		"006",
		"666",
		"000"
	],
	[
		"060",
		"060",
		"066"
	],
	[
		"000",
		"666",
		"600"
	],
	[
		"660",
		"060",
		"060"
	]]


T = [[
		"070",
		"777",
		"000"
	],
	[
		"070",
		"077",
		"070"
	],
	[
		"000",
		"777",
		"070"
	],
	[
		"070",
		"770",
		"070"
	]]
shapes = [S, Z, I, O, J, L, T]


class Tetronimo:
	def __init__(self, grid, window):
		self.grid = grid
		self.window = window
		self.x = 3
		self.y = 0
		self.rotation = 0
		self.previous_state = []
		self.shape = self.get_tetronimo()
		self.update_grid()

	def get_tetronimo(self):
		return random.choice(shapes)

	def update_grid(self):
		if len(self.previous_state) > 0:
			for pos in self.previous_state:
				self.grid.grid[pos[0]][pos[1]] = 0

		for i in range(0, len(self.shape[self.rotation])):
			for j in range(0, len(self.shape[self.rotation][i])):
				if self.shape[self.rotation][i][j] != "0":
					self.previous_state.append((self.y + i, self.x + j))
					self.grid.grid[self.y + i][self.x + j] = int(self.shape[self.rotation][i][j])

		self.grid.draw_grid(window)


	def collision(self):
		


		block_positions = []
		valid_positions = []
		for i in range(20):
			for j in range(10):
				if (i + 1, j) not in self.grid.locked_positions:
					valid_positions.append((i, j))

		
		for i in range(0, len(self.shape[self.rotation])):
			for j in range(0, len(self.shape[self.rotation][i])):
				if self.shape[self.rotation][i][j] != "0":
					block_positions.append((self.y + i, self.x + j))

		for position in block_positions:
			if position not in valid_positions:

				return (True, block_positions)
		
		return (False, block_positions)
			

	def rotation_cw(self):
		self.rotation = (self.rotation + 1) % len(self.shape)


	def rotation_ccw(self):
		self.rotation = (self.rotation - 1) % len(self.shape)

	def clear_row(self):
		
		for i in range(len(self.grid.grid)):
			count = 0
			for j in range(10):
				if self.grid.grid[i][j] != 0:
					count += 1

			if count == 10:
				self.grid.grid.pop(i)
				self.grid.grid.insert(0, [0 for j in range(11)])

				# delete row from lock_positions
				for locked_position in self.grid.locked_positions:
					if locked_position[0] == i + 1:
						self.grid.locked_positions.remove(locked_position)

				# add 1 to all lock_position y values
				for j in range(len(self.grid.locked_positions)):
					if self.grid.locked_positions[j][0] <= i + 1:
						position = list(self.grid.locked_positions[j])
						# print(new_position)
						position[0] += 1
						# print(new_position)
						position = tuple(position)
						self.grid.locked_positions[j] = position

def check_lost(positions):
		for position in positions:
			if position[0] <= 1:
				return True

		return False
	
def main():
	run = True
	clock = pygame.time.Clock()
	fall_time = 0
	fall_speed = 1


	screen = Grid(10, 10, 20, window)
	piece = Tetronimo(screen, window)



	while run:
		fall_time += clock.get_rawtime()
		clock.tick()
		if fall_time / 1000 > fall_speed:
			fall_time = 0
			piece.y += 1
			collide = piece.collision()
			if collide[0]:
				piece.y -= 1
				screen.locked_positions += collide[1]
				if check_lost(collide[1]):
					run = False
					sys.exit()
				piece.clear_row()
				piece = Tetronimo(screen, window)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					piece.x -= 1
					if piece.collision()[0]: 
						piece.x += 1
				if event.key == pygame.K_RIGHT:
					piece.x += 1
					if piece.collision()[0]:
						piece.x -= 1
				if event.key == pygame.K_DOWN:
					piece.y += 1
					collide = piece.collision()
					if collide[0]:
						piece.y -= 1
						screen.locked_positions += collide[1]
						if check_lost(collide[1]):
							run = False
							sys.exit()
						piece.clear_row()
						piece = Tetronimo(screen, window)

				if event.key == pygame.K_z:
					piece.rotation_ccw()
					if piece.collision()[0]:
						piece.rotation_cw()
				if event.key == pygame.K_x:
					piece.rotation_cw()
					if piece.collision()[0]:
						piece.rotation_ccw()

				if event.key == pygame.K_SPACE:
					while piece.collision()[0] == False:
						print(piece.y)
						piece.y += 1
					# piece.clear_row()
					piece = Tetronimo(screen, window)
		
		piece.update_grid()
		pygame.display.update()
main()