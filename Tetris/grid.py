import pygame
from colors import Colors

class Grid:
	def __init__(self):
		self.num_rows = 20
		self.num_cols = 10
		self.cell_size = 30
		self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
		self.colors = Colors.get_cell_colors()

#Este método imprime la matriz de la cuadrícula en la consola. Recorre cada fila y columna de la matriz y muestra el valor de cada celda.
	def print_grid(self):
		for row in range(self.num_rows):
			for column in range(self.num_cols):
				print(self.grid[row][column], end = " ")
			print()

# verifica si una posición dada (fila, columna) está dentro de los límites de la cuadrícula. Retorna True si la posición está dentro de la
#  cuadrícula y False en caso contrario.
	def is_inside(self, row, column):
		if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
			return True
		return False

#Este método verifica si una celda específica de la cuadrícula está vacía. Retorna True si la celda está vacía (valor igual a 0) y False en caso contrario.
	def is_empty(self, row, column):
		if self.grid[row][column] == 0:
			return True
		return False

#Este método verifica si una fila específica de la cuadrícula está completamente llena, es decir, todas las celdas tienen un valor distinto de cero.
#  Retorna True si la fila está llena y False en caso contrario.
	def is_row_full(self, row):
		for column in range(self.num_cols):
			if self.grid[row][column] == 0:
				return False
		return True
	
#Este método vacía una fila específica de la cuadrícula, estableciendo el valor de todas las celdas en cero.
	def clear_row(self, row):
		for column in range(self.num_cols):
			self.grid[row][column] = 0
# Este método mueve hacia abajo una fila específica de la cuadrícula y reemplaza las celdas en la nueva posición con los valores de las celdas originales de la fila.
#  Las celdas originales se establecen en cero.
	def move_row_down(self, row, num_rows):
		for column in range(self.num_cols):
			self.grid[row+num_rows][column] = self.grid[row][column]
			self.grid[row][column] = 0

#: Este método verifica todas las filas de la cuadrícula y elimina cualquier fila que esté completamente llena.
#  Además, desplaza hacia abajo las filas superiores para llenar el espacio vacío dejado por las filas eliminadas. Retorna el número de filas eliminadas.
	def clear_full_rows(self):
		completed = 0
		for row in range(self.num_rows-1, 0, -1):
			if self.is_row_full(row):
				self.clear_row(row)
				completed += 1
			elif completed > 0:
				self.move_row_down(row, completed)
		return completed

#Este método restablece la cuadrícula, estableciendo todas las celdas en cero.
	def reset(self):
		for row in range(self.num_rows):
			for column in range(self.num_cols):
				self.grid[row][column] = 0

#Este método dibuja la cuadrícula en la pantalla. Recorre cada celda de la cuadrícula y dibuja un rectángulo correspondiente
#  en la pantalla utilizando los colores definidos para cada valor de celda
	def draw(self, screen):
		for row in range(self.num_rows):
			for column in range(self.num_cols):
				cell_value = self.grid[row][column]
				cell_rect = pygame.Rect(column*self.cell_size + 11, row*self.cell_size + 11,
				self.cell_size -1, self.cell_size -1)
				pygame.draw.rect(screen, self.colors[cell_value], cell_rect)