from grid import Grid
from blocks import *
import random
import pygame

class Game:
	def __init__(self):
		self.grid = Grid()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.game_over = False
		self.score = 0
		self.rotate_sound = pygame.mixer.Sound("C:\\Users\\juanm\\Programacion I\\pypeGames\\TP_Tetris\\rotate.ogg")

		self.clear_sound = pygame.mixer.Sound("pypeGames\TP_Tetris\clear.ogg")

		pygame.mixer.music.load("pypeGames\TP_Tetris\music.ogg")
		pygame.mixer.music.play(-1)

#update_score se utiliza para actualizar el puntaje en un juego. Toma dos parámetros: lines_cleared
#  (líneas eliminadas) y move_down_points (puntos por mover hacia abajo).
	def update_score(self, lines_cleared, move_down_points):
		if lines_cleared == 1:
			self.score += 100
		elif lines_cleared == 2:
			self.score += 300
		elif lines_cleared == 3:
			self.score += 500
		self.score += move_down_points

#esta función elige un bloque aleatorio de una lista de bloques disponibles, lo elimina de la lista y lo devuelve como resultado.
	def get_random_block(self):
		if len(self.blocks) == 0:
			self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		block = random.choice(self.blocks)
		self.blocks.remove(block)
		return block

	def move_left(self):
		self.current_block.move(0, -1)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, 1)

	def move_right(self):
		self.current_block.move(0, 1)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, -1)

	def move_down(self):
		self.current_block.move(1, 0)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(-1, 0)
			self.lock_block()

#esta función se encarga de bloquear el bloque actual en la cuadrícula del juego, actualizar el bloque actual y el siguiente bloque,
#  y realizar acciones adicionales como eliminar filas completas, reproducir sonidos y verificar si el juego ha terminado.
	def lock_block(self):
		tiles = self.current_block.get_cell_positions()
		for position in tiles:
			self.grid.grid[position.row][position.column] = self.current_block.id
		self.current_block = self.next_block
		self.next_block = self.get_random_block()
		rows_cleared = self.grid.clear_full_rows()
		if rows_cleared > 0:
			self.clear_sound.play()
			self.update_score(rows_cleared, 0)
		if self.block_fits() == False:
			self.game_over = True

#esta función se encarga de reiniciar el juego, restableciendo la cuadrícula, los bloques disponibles, los bloques actual y siguiente,
#  y el puntaje a sus valores iniciales.
	def reset(self):
		self.grid.reset()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.score = 0

#esta función verifica si todas las celdas ocupadas por el bloque actual están vacías en la cuadrícula del juego. Si alguna celda está
#  ocupada, se devuelve False, indicando que el bloque no encaja. Si todas las celdas están vacías, se devuelve True, indicando que el
#  bloque encaja correctamente.
	def block_fits(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_empty(tile.row, tile.column) == False:
				return False
		return True
	

	def rotate(self):
		self.current_block.rotate()
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.undo_rotation()
		else:
			self.rotate_sound.play()

	def block_inside(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_inside(tile.row, tile.column) == False:
				return False
		return True

# este código se encarga de dibujar una cuadrícula, el bloque actual y el siguiente bloque en una pantalla.
	def draw(self, screen):
		self.grid.draw(screen)
		self.current_block.draw(screen, 11, 11)

		if self.next_block.id == 3:
			self.next_block.draw(screen, 255, 290)
		elif self.next_block.id == 4:
			self.next_block.draw(screen, 255, 280)
		else:
			self.next_block.draw(screen, 270, 270)