import csv
import pygame
import sys
from game import Game
from colors import Colors

#1. me ocupe del loop inicial del juegp
#2.cree la cuadricula 
#3.cree los bloques, 7 tipos de figuras,cada una tiene su propio ID. lo pense como si fueran matrices y despues los puse en la cuadricula para ir probando
#4. despues me fije como mover los bloques, y ya que estaba resolvi el tema de que las figuras se salieran de la cuadricula
#5. investigue como mover las figuras, y la mejor forma era actualizando el estado actual de cada figura, cada una tiene 4.
#6. despues probe el juego y me encontre con el tema de las colisiones, en este punto mis bloques se movian y rotaban, pero se superponian entre si, asi que
#me ocupe de las colisiones
#7. ahora resolvi que al completar filas, estas desaparezcan y los bloques caigan hacia abajo encajando en la cuadricula
#8.configure el game over, llegas hasta arriba de la cuadricula con las figuras y perdiste
#cree el input para el usurio, el score y el bloque siguiente, estas 3 cosas son capaces de mostrarse mientras el usuario esta jugando. el score, dependiendo
#cuantas filas rompas a la vez, suma de una forma o de otra.
#casi ultimo, le agregue la imagen game over para que aparezca cuando perdes
#despues le meti los sonidos, hay 3, uno para cuando rompes filas, otro para rotar y otro es la musica de fondo del juego
#cree el archivo csv el cual almacena los nombres y los score de los competidores, ordenandolos de mayor a menor
#por ultimo cree una lista de diccionarios que guarda los nombres y los score tambien, y me los blitea en la imagen de game over para poder ver quien fue el ganador
# hasta aca el fin del tetris del pueblo, gracias ;)


pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("El Tetris del pueblo")

# Fuentes y superficies de texto
title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render(" NICE TRY :)", True, Colors.black)

# Rectángulos para ubicar los textos
score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)
name_rect = pygame.Rect(320, 540, 170, 60)

# Reloj del juego
clock = pygame.time.Clock()

# Creación del objeto de juego
game = Game()

# Evento de actualización del juego
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 300)  # Intervalo de actualización de 300 milisegundos (0.3 segundos)
# Lista de diccionarios para almacenar los nombres y puntajes de los jugadores
players = []

# Cargar la imagen de fondo y redimensionarla
background_image = pygame.image.load("pypeGames/TP_Tetris/game over.jpg")
nuevo_ancho = 500
nuevo_alto = 620
background_image = pygame.transform.scale(background_image, (nuevo_ancho, nuevo_alto))
background_rect = background_image.get_rect()

while True:
    # Variables para el nombre del jugador
    player_name = ""
    input_active = True
    input_font = pygame.font.Font(None, 32)

    # Dibujar el título "Competitor" desde el principio
    name_title_surface = title_font.render("Competitor", True, Colors.white)
    name_title_pos = (name_rect.x + name_rect.width // 2 - name_title_surface.get_width() // 2,
                      name_rect.y - name_title_surface.get_height() - 10)

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        screen.fill(Colors.dark_blue)
        pygame.draw.rect(screen, Colors.light_blue, name_rect, 0, 10)
        screen.blit(name_title_surface, name_title_pos)
        name_value_surface = input_font.render(player_name, True, Colors.white)
        screen.blit(name_value_surface, name_value_surface.get_rect(center=name_rect.center))

        pygame.display.update()
        clock.tick(60)

    # Reiniciar el juego y el puntaje
    game.reset()

    while True:
        # Gestión de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == GAME_UPDATE:  # Evento de actualización del juego
                if not game.game_over:  # Solo si el juego no ha terminado
                    game.move_down()
                    game.update_score(0, 1)
            if event.type == pygame.KEYDOWN:
                if game.game_over:
                    # Guardar nombre y puntaje en la lista de diccionarios
                    players.append({"name": player_name, "score": game.score})
                    game.game_over = False
                    game.reset()
                    # Reiniciar el juego y el puntaje
                    input_active = True
                    break
                if event.key == pygame.K_LEFT and not game.game_over:
                    game.move_left()
                if event.key == pygame.K_RIGHT and not game.game_over:
                    game.move_right()
                if event.key == pygame.K_DOWN and not game.game_over:
                    game.move_down()
                    game.update_score(0, 1)
                if event.key == pygame.K_UP and not game.game_over:
                    game.rotate()
                if event.key == pygame.K_z:  # Terminar el juego al presionar la tecla 'z'
                    # Cargar la imagen de fondo y ajustar su posición en el centro de la pantalla
                    screen.blit(background_image, (0, -20))
                    game_over_pos = (screen.get_width() // 2 - background_rect.width // 2,
                                    screen.get_height() // 2 - background_rect.height // 2)
                    screen.blit(game_over_surface, game_over_pos)

                    # Mostrar los nombres y puntajes en la imagen de "Game Over"
                    for i, player in enumerate(players):
                        player_surface = title_font.render(f"{player['name']}: {player['score']}", True, Colors.white)
                        player_pos = (game_over_pos[0] + 20, game_over_pos[1] + 50 + 40 * i)
                        screen.blit(player_surface, player_pos)

                    pygame.display.update()

                    # Esperar unos segundos antes de cerrar el juego
                    pygame.time.wait(8000)

                    pygame.quit()
                    sys.exit()

        if input_active:
            break

        # Dibujos en pantalla
        score_value_surface = title_font.render(str(game.score), True, Colors.white)

        screen.fill(Colors.dark_blue)
        screen.blit(score_surface, (365, 20))
        screen.blit(next_surface, (375, 180))

        if game.game_over:
            # Borra la superficie del competidor y su título
            pygame.draw.rect(screen, Colors.dark_blue, name_rect)
            pygame.draw.rect(screen, Colors.dark_blue, name_title_pos + name_title_surface.get_size())

            # Muestra la imagen"GAME OVER"
            screen.blit(game_over_surface, (320, 450))

        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(center=score_rect.center))
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        game.draw(screen)

        # Mostrar el nombre del competidor mientras se juega
        pygame.draw.rect(screen, Colors.light_blue, name_rect, 0, 10)
        screen.blit(name_title_surface, name_title_pos)
        screen.blit(name_value_surface, name_value_surface.get_rect(center=name_rect.center))

        pygame.display.update()
        clock.tick(60)

    # Ordenar la lista de jugadores por puntaje de forma descendente
    players = sorted(players, key=lambda x: x["score"], reverse=True)

    # Crear el archivo CSV y escribir los nombres y puntajes
    with open("scores.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Score"])  # Escribir encabezados
        for player in players:
            writer.writerow([player["name"], player["score"]])

     
