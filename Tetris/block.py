from colors import Colors
import pygame
from position import Position

class Block:
	def __init__(self, id):
		self.id = id
		self.cells = {}
		self.cell_size = 30
		self.row_offset = 0
		self.column_offset = 0
		self.rotation_state = 0
		self.colors = Colors.get_cell_colors()

#este método se utiliza para mover el bloque en una dirección específica. Los parámetros rows y columns
#  indican cuántas filas y columnas se deben mover el bloque respectivamente. Actualiza los desplazamientos
#  de fila y columna del bloque en consecuencia, lo que afectará la posición absoluta de las celdas del bloque al dibujarlo en la pantalla.
	def move(self, rows, columns):
		self.row_offset += rows
		self.column_offset += columns

#se utiliza para obtener las posiciones absolutas de las celdas del bloque en su estado de rotación actual,
#  teniendo en cuenta los desplazamientos de fila y columna.
	def get_cell_positions(self):
		tiles = self.cells[self.rotation_state]
		moved_tiles = []
		for position in tiles:
			position = Position(position.row + self.row_offset, position.column + self.column_offset)
			moved_tiles.append(position)
		return moved_tiles

# este método se utiliza para cambiar el estado de rotación del bloque. Incrementa el estado de rotación en 1 y,
#  si alcanza el valor máximo permitido, lo reinicia a cero para volver a la primera orientación.
	def rotate(self):
		self.rotation_state += 1
		if self.rotation_state == len(self.cells):
			self.rotation_state = 0

# este método se utiliza para deshacer la rotación anterior del bloque. Resta 1 al estado de rotación y,
#  si llega a 0, lo ajusta al valor máximo permitido (la última orientación). Esto permite al bloque volver
#  a su estado de rotación anterior antes de la última rotación realizada.
	def undo_rotation(self):
		self.rotation_state -= 1
		if self.rotation_state == 0:
			self.rotation_state = len(self.cells) - 1


#este método se utiliza para dibujar el bloque en una pantalla. Obtiene las posiciones absolutas de las celdas del bloque, crea un rectángulo
#para cada celda y lo dibuja en la pantalla utilizando un color específico. Los parámetros offset_x y offset_y se utilizan para ajustar la 
#posición del bloque en la pantalla.
	def draw(self, screen, offset_x, offset_y):
		tiles = self.get_cell_positions()
		for tile in tiles:
			tile_rect = pygame.Rect(offset_x + tile.column * self.cell_size, 
				offset_y + tile.row * self.cell_size, self.cell_size -1, self.cell_size -1)
			pygame.draw.rect(screen, self.colors[self.id], tile_rect)