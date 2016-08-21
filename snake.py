"""
Snake game created using python and pygame module.
Written by Jiaxi Kang.
"""

import pygame
import time
import random

pygame.init()

game_end = False
score = 0

white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 200, 0)
bright_green = (0, 255, 0)
bright_red = (255, 0, 0)

game_width = 800
game_height = 600
size = 10

gameDisplay = pygame.display.set_mode((game_width, game_height))

x_head = game_width / 2 + size
y_head = game_height / 2 + size

pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

def drawSnake(snake):
    for body in snake:
        pygame.draw.circle(gameDisplay, white, (body[0], body[1]), size)

def drawFruit(fruit_X, fruit_Y):
    pygame.draw.circle(gameDisplay, bright_red, (fruit_X, fruit_Y), size)

def displayText(text, size, x_center, y_center, color):
    shownText = pygame.font.Font('freesansbold.ttf', size)
    TextSurf, TextRect = text_objects(text, shownText, color)
    TextRect.center = (x_center, y_center)
    gameDisplay.blit(TextSurf, TextRect)
    
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def draw_Buttons(text, text_size, rect_x, rect_y, width, height, text_color, rect_color):
    pygame.draw.rect(gameDisplay, rect_color, (rect_x, rect_y, width, height))
    displayText(text, text_size, rect_x + width/2, rect_y + height/2, text_color)
    
def end_Game():
    end = True
    global game_end
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(black)
        mouse = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        displayText("Your snake has collided", 40, game_width/2, 80, white)
        displayText("GAME OVER", 40, game_width/2, 160, white)
        displayText("You have achieved " + str(score) + " points", 40, game_width/2, 240, white)

        if 100 < mouse[0] < 100 + 150 and 350 < mouse[1] < 350 + 100:
            draw_Buttons("Restart", 20, 100, 350, 150, 100, white, bright_green)
            if mouse_press[0]:
                game_end = False
                gameloop()
                
        else:
            draw_Buttons("Restart", 20, 100, 350, 150, 100, white, green)

        if 550 < mouse[0] < 550 + 150 and 350 < mouse[1] < 350 + 100:
            draw_Buttons("Quit", 20, 550, 350, 150, 100, white, bright_red)
            if mouse_press[0]:
                pygame.quit()
                quit()
        else:
            draw_Buttons("Quit", 20, 550, 350, 150, 100, white, red)
        pygame.display.update()
        clock.tick(15)
        
def addBody(snake, snake_dir, length):
    if (snake_dir == "left"):
        snake.append([snake[length - 1][0] - (size * 2), snake[length - 1][1]])
    elif (snake_dir == "right"):
        snake.append([snake[length - 1][0] + (size * 2), snake[length - 1][1]])
    elif (snake_dir == "up"):
        snake.append([snake[length - 1][0], snake[length - 1][1] - (size * 2)])
    elif (snake_dir == "down"):
        snake.append([snake[length - 1][0], snake[length - 1][1] + (size * 2)])

def check_Snake_Collision(snake, length):
    for index in range(length - 1):
        if snake[index] == snake[length - 1]:
            return True
    return False

def check_Wall_Collision(snake, length):
    if  (snake[length - 1][0] < size or snake[length - 1][0] > game_width - size or 
        snake[length - 1][1] < size or snake[length - 1][1] > game_height - size):
        return True
    return False

def gameloop():
    global score
    global game_end
    
    score = 0
    snake = [[x_head, y_head]]
    x_head_change = 0
    y_head_change = 0
    length = 1
    snake_dir = ""
    fruit_X = random.randrange(10, game_width, 20)
    fruit_Y = random.randrange(10, game_height, 20)

    #prevents fruit generating from starting position
    if fruit_X == snake[0][0] and fruit_Y == snake[0][1]:
        fruit_X = random.randrange(10, game_width, 20)
        fruit_Y = random.randrange(10, game_height, 20)
        
    while game_end == False:
        gameDisplay.fill(black)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_head_change = -size*2
                    y_head_change = 0
                    snake_dir = "left"
                if event.key == pygame.K_RIGHT:
                    x_head_change = size*2
                    y_head_change = 0
                    snake_dir = "right"
                if event.key == pygame.K_UP:
                    y_head_change = -size*2
                    x_head_change = 0
                    snake_dir = "up"
                if event.key == pygame.K_DOWN:
                    y_head_change = size*2
                    x_head_change = 0
                    snake_dir = "down"
                    
        if check_Snake_Collision(snake, length) == True or check_Wall_Collision(snake, length) == True:
            game_end = True
        
        drawFruit(fruit_X, fruit_Y)
        drawSnake(snake)

        """
        the main game logic uses the list function to represent a structure similar to a stuck. As the snake eats a fruit, a snake body
        is pushed to the top of the stack. As the snake moves, the new coordinate representing the new head is pushed to the top and
        the bottom of the stack is popped. 
        """
        if snake[length - 1][0] == fruit_X and snake[length - 1][1] == fruit_Y: #event occurs when snake eats the fruit
            
            #prevents fruit from appearing from snake body
            for body in snake:
                while fruit_X == body[0] and fruit_Y == body[1]:
                    fruit_X = random.randrange(10, game_width, 20)
                    fruit_Y = random.randrange(10, game_height, 20)
                    
            addBody(snake, snake_dir, length)
            length += 1
        
        else: #event occurs when snake moves
            snake.append([snake[length - 1][0] + x_head_change, snake[length - 1][1] + y_head_change])
            snake.pop(0)

        score = (length - 1) * 10
        displayText("Score: " + str(score), 25, game_width - 70, game_height - 20, white)

        pygame.display.update()
        clock.tick(15)
        
gameloop()
end_Game()
