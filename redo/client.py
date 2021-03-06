import pygame
from grid import Grid
from interface import Button
from network import Network
import threading
import random
import sys
import os
import json

width = 1000
height = 600

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
		if len(self.grid.queue) == 0:
			self.generate_queue()
		else:
			self.grid.queue.pop(0)
			self.grid.queue.append(self.get_tetronimo())
		self.shape = self.grid.queue[0]
		# print(self.grid.queue)
		self.draw_shadow()

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

		self.grid.draw_grid()


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
		lines_cleared = 0
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
				for locked_position in self.grid.locked_positions:
					if locked_position[0] == i + 1:
						self.grid.locked_positions.remove(locked_position)

				for locked_position in self.grid.locked_positions:
					if locked_position[0] == i + 1:
						self.grid.locked_positions.remove(locked_position)

				for locked_position in self.grid.locked_positions:
					if locked_position[0] == i + 1:
						self.grid.locked_positions.remove(locked_position)
				for locked_position in self.grid.locked_positions:
					if locked_position[0] == i + 1:
						self.grid.locked_positions.remove(locked_position)
				# add 1 to all lock_position y values
				for j in range(len(self.grid.locked_positions)):
					if self.grid.locked_positions[j][0] < i + 1:
						position = list(self.grid.locked_positions[j])
						position[0] += 1
						position = tuple(position)
						self.grid.locked_positions[j] = position
				# print(self.grid.locked_positions)

				self.grid.total_lines += 1
				lines_cleared += 1
				
		if lines_cleared == 1:
			self.grid.score += 40 * (self.grid.level + 1)
			

		elif lines_cleared == 2:
			self.grid.score += 100 * (self.grid.level + 1)
			

		elif lines_cleared == 3:
			self.grid.score += 300 * (self.grid.level + 1)
			

		elif lines_cleared == 4:
			self.grid.score += 1200 * (self.grid.level + 1)
		
		
		# if lines_cleared > 0:
		# 	pygame.mixer.Sound.play(line_clear_sound)
		# else:
		# 	pygame.mixer.Sound.play(hit_sound)

	def draw_shadow(self):

		count = 0
		self.shape[self.rotation]
		while self.collision()[0] == False:
			self.y += 1
			count += 1
		self.y -= count
		for i in range(len(self.shape[self.rotation])):
			for j in range(len(self.shape[self.rotation])):
				if self.shape[self.rotation][i][j] != "0":
					colour = (self.grid.colours[int(self.shape[self.rotation][i][j])][0] - 74, self.grid.colours[int(self.shape[self.rotation][i][j])][1] - 74, self.grid.colours[int(self.shape[self.rotation][i][j])][2] - 74)
					pygame.draw.rect(self.window, colour, (self.grid.x + self.x*self.grid.block_size + self.grid.block_size*j, self.grid.y + (self.y + count - 1)*self.grid.block_size + i*self.grid.block_size, self.grid.block_size, self.grid.block_size))



	def hard_drop(self):
		collide = self.collision()
		while collide[0] == False:
			self.y += 1
			collide = self.collision()
		self.y -= 1
		self.update_grid()
		self.grid.locked_positions += collide[1]

	def generate_queue(self):
		for i in range(7):
			self.grid.queue.append(self.get_tetronimo())


def check_lost(positions):
		for position in positions:
			if position[0] <= 1:
				return True

		return False
	
def modern_mode():
	run = True
	clock = pygame.time.Clock()
	fall_time = 0
	fall_speed = 1
	move_left = False
	move_right = False
	move_down = False
	screen = Grid(10, 10, 20, window, "modern")
	piece = Tetronimo(screen, window)
	move_left_times = 0
	move_right_times = 0
	move_down_times = 0
	
	
	
	while run:
		window.fill((0, 0, 0))
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
				
				piece = Tetronimo(screen, window)
				screen.display_info()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					piece.x -= 1
					if piece.collision()[0]: 
						piece.x += 1
					move_left = True
					
				if event.key == pygame.K_RIGHT:
					piece.x += 1
					if piece.collision()[0]: 
						piece.x -= 1
					move_right = True
					
				if event.key == pygame.K_DOWN:
					piece.y += 1
					collide = piece.collision()
					if collide[0]:
						piece.y -= 1
						screen.locked_positions += collide[1]
						if check_lost(collide[1]):
							run = False
						piece.clear_row()
						
						piece = Tetronimo(screen, window)
						screen.display_info()
					move_down = True
						
						
						
						

				if event.key == pygame.K_z:
					piece.rotation_ccw()
					if piece.collision()[0]:
						piece.rotation_cw()
				if event.key == pygame.K_x:
					piece.rotation_cw()
					if piece.collision()[0]:
						piece.rotation_ccw()

				if event.key == pygame.K_SPACE:
					piece.hard_drop()
					piece.clear_row()
					piece = Tetronimo(screen, window)
					screen.display_info()
					
				
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					move_left = False
					move_left_times = 0
				if event.key == pygame.K_RIGHT:
					move_right = False
					move_right_times = 0
				if event.key == pygame.K_DOWN:
					move_down = False
					move_down_times = 0


		if move_left:

			move_left_times += 1
			if move_left_times > 50:
				piece.x -= 1
				# piece.draw_shadow()
				if piece.collision()[0]: 
					piece.x += 1
				pygame.time.wait(30)

		if move_right:
			move_right_times += 1
			if move_right_times > 50:
				piece.x += 1
				# piece.draw_shadow()
				if piece.collision()[0]: 
					piece.x -= 1
				pygame.time.wait(30)

		if move_down:
			move_down_times += 1
			if move_down_times > 50:
				piece.y += 1
				if piece.collision()[0]: 
					piece.y -= 1
				pygame.time.wait(30)
		
		screen.draw_board()
		piece.draw_shadow()
		piece.update_grid()
		
		screen.display_info()
		pygame.display.update()


def classic_mode():
	run = True
	clock = pygame.time.Clock()
	fall_time = 0
	fall_speed = 1
	
	screen = Grid(10, 10, 20, window, "classic")
	piece = Tetronimo(screen, window)
	
	while run:
		window.fill((0, 0, 0))
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
				
				piece = Tetronimo(screen, window)
				screen.display_info()

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
						piece.clear_row()
						
						piece = Tetronimo(screen, window)
						screen.display_info()
					
						
						
						
						

				if event.key == pygame.K_z:
					piece.rotation_ccw()
					if piece.collision()[0]:
						piece.rotation_cw()
				if event.key == pygame.K_x:
					piece.rotation_cw()
					if piece.collision()[0]:
						piece.rotation_ccw()
		
		screen.draw_board()
		piece.update_grid()
		screen.display_info()
		pygame.display.update()




def multiplayer_modern_mode():

	
	run = True
	clock = pygame.time.Clock()
	fall_time = 0
	fall_speed = 1
	move_left = False
	move_right = False
	move_down = False
	p1 = Grid(10, 10, 20, window, "modern")
	piece = Tetronimo(p1, window)
	move_left_times = 0
	move_right_times = 0
	move_down_times = 0
	p2 = Grid(600, 10, 20, window, "modern")
	
	FORMAT = "utf-8"
	n = Network()
	
	
	
	
	while run:
		window.fill((0, 0, 0))
		fall_time += clock.get_rawtime()
		clock.tick()
		if fall_time / 1000 > fall_speed:
			fall_time = 0
			piece.y += 1
			collide = piece.collision()
			if collide[0]:
				piece.y -= 1
				p1.locked_positions += collide[1]
				if check_lost(collide[1]):
					n.send("!DISCONNECT")
					run = False
				
				piece = Tetronimo(p1, window)
				p1.display_info()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				
				n.send("!DISCONNECT")
				run = False
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					piece.x -= 1
					if piece.collision()[0]: 
						piece.x += 1
					move_left = True
					
				if event.key == pygame.K_RIGHT:
					piece.x += 1
					if piece.collision()[0]: 
						piece.x -= 1
					move_right = True
					
				if event.key == pygame.K_DOWN:
					piece.y += 1
					collide = piece.collision()
					if collide[0]:
						piece.y -= 1
						p1.locked_positions += collide[1]
						if check_lost(collide[1]):
							n.send("!DISCONNECT")
							run = False
						piece.clear_row()
						
						piece = Tetronimo(p1, window)
						p1.display_info()
					move_down = True
						
						
						
						

				if event.key == pygame.K_z:
					piece.rotation_ccw()
					if piece.collision()[0]:
						piece.rotation_cw()
				if event.key == pygame.K_x:
					piece.rotation_cw()
					if piece.collision()[0]:
						piece.rotation_ccw()

				if event.key == pygame.K_SPACE:
					piece.hard_drop()
					piece.clear_row()
					piece = Tetronimo(p1, window)
					p1.display_info()
					
				
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					move_left = False
					move_left_times = 0
				if event.key == pygame.K_RIGHT:
					move_right = False
					move_right_times = 0
				if event.key == pygame.K_DOWN:
					move_down = False
					move_down_times = 0


		if move_left:

			move_left_times += 1
			if move_left_times > 50:
				piece.x -= 1
				# piece.draw_shadow()
				if piece.collision()[0]: 
					piece.x += 1
				pygame.time.wait(30)

		if move_right:
			move_right_times += 1
			if move_right_times > 50:
				piece.x += 1
				# piece.draw_shadow()
				if piece.collision()[0]: 
					piece.x -= 1
				pygame.time.wait(30)

		if move_down:
			move_down_times += 1
			if move_down_times > 50:
				piece.y += 1
				if piece.collision()[0]: 
					piece.y -= 1
				pygame.time.wait(30)
		

		p1.draw_board()
		p2.draw_board()
		piece.draw_shadow()
		piece.update_grid()
		p1.display_info()
		# send grid
		data = json.dumps(p1.grid)
		p2data = n.send(data)
		try:
			p2data = json.loads(p2data)
			p2.grid = p2data
			p2.draw_grid()
		except TypeError:
			pass
		
		
		

		
		
		
		pygame.display.update()

def main_menu():
	run = True
	single = Button(0, 0, 200, 50, (0, 0, 0), (255, 255, 255), "Singleplayer", window)
	multi = Button(0, 100, 200, 50, (0, 0, 0), (255, 255, 255), "Multiplayer", window)
	quit = Button(0, 200, 200, 50, (0, 0, 0), (255, 255, 255), "Quit", window)
	while run:
		for event in pygame.event.get():
			pos = pygame.mouse.get_pos()
			if event.type == pygame.QUIT:
				run = False
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if single.enter(pos):
						singleplayer()
					elif multi.enter(pos):
						multiplayer_modern_mode()
					elif quit.enter(pos):
						run = False
						sys.exit()
		window.fill((0, 0, 0))
		single.draw()
		multi.draw()
		quit.draw()
		pygame.display.update()

def singleplayer():
	run = True
	modern = Button(0, 0, 200, 50, (0, 0, 0), (255, 255, 255), "Modern Mode", window)
	classic = Button(0, 100, 200, 50, (0, 0, 0), (255, 255, 255), "Classic Mode", window)
	back = Button(0, 200, 200, 50, (0, 0, 0), (255, 255, 255), "Back", window)
	while run:
		for event in pygame.event.get():
			pos = pygame.mouse.get_pos()
			if event.type == pygame.QUIT:
				run = False
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if modern.enter(pos):
						modern_mode()
					elif classic.enter(pos):
						classic_mode()
					elif back.enter(pos):
						run = False
						
		window.fill((0, 0, 0))
		modern.draw()
		classic.draw()
		back.draw()
		pygame.display.update()


	
	
	
	
	
	
	
		


main_menu()


# FIX: bug where another rectangle is drawn when tetronimo hits an edge