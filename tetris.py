import pygame
import random
import time

win_width = 1280
win_height = 720
board_start_x = 250
board_start_y = 10
block_size = 30
board_width = 10 * block_size
board_height = 20 * block_size
temp_positions = []
locked_positions = {}
grid = {}
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colours = [(178, 250, 180), (222, 98, 91), (74, 178, 199), (227, 221, 107), (235, 167, 84), (104, 174, 217), (208, 111, 227)]

def create_grid():
	global grid
	for i in range(10):
		for j in range(20):
			grid[(i, j)] = (0, 0, 0)
	return grid 

def draw_grid(window):
	global locked_positions
	global grid
	for block in locked_positions:
		grid[block] = locked_positions[block]
	for block in grid:
		pygame.draw.rect(window, grid[block], [board_start_x + block[0] * block_size, board_start_y + block[1] * block_size, block_size, block_size], 0)

def draw_window(window):
	draw_grid(window)
	for i in range(11):
		pygame.draw.line(window, (82,82,82), (board_start_x + i*block_size,board_start_y), (board_start_x + i*block_size, board_start_y + 20*block_size), 2)
		for j in range(21):
			pygame.draw.line(window, (82,82,82), (board_start_x,board_start_y + j*block_size), (board_start_x + 10*block_size, board_start_y + j*block_size), 2)
	
def convert_block(x, y, shape, rotation):
	global grid, temp_positions
	positions = []
	if len(temp_positions) > 0:
		for position in temp_positions:
			grid[position] = (0, 0, 0)
	case = shape[rotation % len(shape)]
	for i in range(len(case)):
		for j in range(len(case)):
			if case[i][j] == "0":
				positions.append((i + x - 2, j + y - 1))
	temp_positions = positions
	for position in positions:
		grid[position] = shape_colours[shapes.index(shape)]

	return positions

def create_shape(x, y, rotation):
	shape = get_shape()
	return x, y, rotation, shape


def get_shape():
	return random.choice(shapes)

def check_lost():
	global locked_positions
	for position in locked_positions:
		if position[1] <= 0:
			return True
	return False

def clear_row():
	global grid
	"""
	plan:
	DONE check if any rows have all values which are not 0, 0, 0
	delete that row
	insert a row before everything
	"""
	colours = []
	for position in grid:
		colours.append(grid[position])
	for i in range(20):
		print(colours[i*10:(i*10)+10])
				
		# for j in range(20):
		# if (0, 0, 0) not in colours[i*10:(i*10) + 10]:

			# del colours[i*10:(i*10) + 10]
			# for j in range(10):
				# colours.append((0, 0, 0))
			
		# print(colours)
	# print(colours)
def collide_detect(x, y, shape, rotation):
	global grid, locked_positions
	valid_positions = []
	for position in grid:
		if position not in locked_positions:
			valid_positions.append(position)

	positions = convert_block(x, y, shape, rotation)
	for position in positions:
		if position not in valid_positions:
			if position[1] > 0:
				return True
		
	return False
		
	
def main(window): 
	run = True
	clock = pygame.time.Clock()
	x, y, rotation, shape = create_shape(5, 0, 0)
	rotation = 0
	grid = create_grid()
	fall_time = 0
	while run:
		fall_time += clock.get_time()
		if fall_time % 250 == 0:
			y += 1
			if collide_detect(x, y, shape, rotation):
				y -= 1
				for position in positions:
					locked_positions[position] = shape_colours[shapes.index(shape)]
				x, y, rotation, shape = create_shape(5, 0, 0)
				fall_time = 0
				clear_row()
		positions = convert_block(x, y, shape, rotation)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x -= 1
					if collide_detect(x, y, shape, rotation):
						x += 1
				if event.key == pygame.K_RIGHT:
					x += 1
					if collide_detect(x, y, shape, rotation):
						x -= 1
				if event.key == pygame.K_DOWN:
					y += 1
					if collide_detect(x, y, shape, rotation):
						y -= 1
						for position in positions:
							locked_positions[position] = shape_colours[shapes.index(shape)]
						x, y, rotation, shape = create_shape(5, 0, 0)
						fall_time = 0
						clear_row()
				if event.key == pygame.K_f:
					rotation -= 1
				if event.key == pygame.K_d:
					rotation += 1
		positions = convert_block(x, y, shape, rotation)
		draw_window(window)
		if check_lost():
			run = False
		pygame.display.update()
		
		clock.tick()


def main_menu():
	pygame.init()
	window = pygame.display.set_mode((win_width, win_height))
	pygame.display.set_caption('Tetris')
	main(window)

main_menu()

"""
Plan:
. create a grid full of black rectangles
. have list of fixed positions (shapes which already fully fallen)
. generate shape from a list of shapes with corresponding colours
. once shape is added, append to the variable grid (holds a tuple of (x, y) with a corresponding colour)
. in main function, detect key presses
. edit grid based on key press
. update screen

"""

