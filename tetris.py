import pygame
import random

win_width = 1280
win_height = 720
board_start_x = 250
board_start_y = 10
block_size = 30
board_width = 10 * block_size
board_height = 20 * block_size

locked_positions = {}

S = [['.....',
      '......',
      '..00..',
      '.00...',
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
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

def create_grid():
	grid = {}
	for i in range(10):
		for j in range(20):
			grid[(i, j)] = (0, 0, 0)
	return grid 

def draw_grid(window):
	grid = create_grid()
	for block in grid:
		pygame.draw.rect(window, grid[block], [board_start_x + block[0] * block_size, board_start_y + block[1] * block_size, block_size, block_size], 0)

def draw_window(window):
	draw_grid(window)
	for i in range(11):
		pygame.draw.line(window, (82,82,82), (board_start_x + i*block_size,board_start_y), (board_start_x + i*block_size, board_start_y + 20*block_size), 2)
		for j in range(21):
			pygame.draw.line(window, (82,82,82), (board_start_x,board_start_y + j*block_size), (board_start_x + 10*block_size, board_start_y + j*block_size), 2)
	
def convert_block(x, y, shape, rotation):
	positions = []
	case = shape[rotation]
	for i in range(len(case)):
		for j in case[i]:
			if j == "0":

def create_shape(x, y):
	shape = get_shape()
	return x, y, shape


def get_shape():
	return random.choice(shapes)


def clear_row():
	pass


def main(window): 
	run = True
	clock = pygame.time.Clock()
	x, y, shape = create_shape(5, 0)
	rotation = 0
	
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		draw_window(window)
		pygame.display.update()
		convert_block(x, y, shape, rotation)
		clock.tick(30)


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

