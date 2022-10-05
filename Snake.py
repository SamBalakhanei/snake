from importlib import resources
import pygame
from pygame.locals import *
import time
import random


SIZE = 40 #dimensions of block.jpg is 40x40

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("C:\\Users\\Sam Balakhanei\\Desktop\\SnakeProj\\resources\\apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3 #spawns the first apple at 120,120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y)) #draws the apples
        pygame.display.flip() #updatescreen basically --> use .update() when only wanting to update a portion of the screen (optimized)

    def move(self):
        self.x = random.randint(0,24) * SIZE
        self.y = random.randint(0,19) * SIZE




class Snake:
    def __init__(self, parent_screen, length): #FIELDS!! parent_screen IS A FIELD! #constructor method
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("C:\\Users\\Sam Balakhanei\\Desktop\SnakeProj\\resources\\block.jpg").convert() #inserts the block object
        self.block_x = [SIZE] * length
        self.block_y = [SIZE] * length
        self.direction = 'down' #default direction so no insta death
        self.speed = 0.25 #sleep timer which gets decreased to increase difficulty


    def draw(self):
        self.parent_screen.fill((100,165,67)) #call it here to get rid of old block position on screen
        for i in range(self.length): #multiple x,y's for multiple blocks
            self.parent_screen.blit(self.block, (self.block_x[i], self.block_y[i])) #draws the blocks
        pygame.display.flip() #updatescreen basically --> use .update() when only wanting to update a portion of the screen (optimized)

    def move_left(self): #self is kinda like a reflexive verb in spanish --> doing it to itself
        self.direction = 'left'
    def move_right(self):
        self.direction = 'right'
    def move_up(self):
        self.direction = 'up'
    def move_down(self):
        self.direction = 'down'
    
    def walk(self): 
        #since it's called in run() under a while loop, can use if statements

        for i in range(self.length-1,0,-1):
            self.block_x[i] = self.block_x[i-1]
            self.block_y[i] = self.block_y[i-1]
        if (self.direction == 'left'):
            self.block_x[0] -= SIZE #use size to keep the blocks properly spaced apart
        if (self.direction == 'right'):
            self.block_x[0] += SIZE
        if (self.direction == 'up'):
            self.block_y[0] -= SIZE
        if (self.direction == 'down'):
            self.block_y[0] += SIZE
        
        self.draw()

    def increase_length(self):
        self.length +=1
        self.block_x.append(5)
        self.block_y.append(5)
    



class Game:
    def __init__(self): #constructor method of the class
        pygame.init()
        pygame.mixer.init()
        self.surface = pygame.display.set_mode((1000,800)) #creates the 1000 x 500 display screen
        pygame.display.set_caption('Snake')
        self.surface.fill((100,165,67)) #color of the background
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()


    def is_collision(self, x1, y1, x2, y2):
        if ((x1 == x2) and (y1 == y2)):
            return True
                
        return False



    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        #snake colliding with apple
        if(self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.apple.x, self.apple.y)):
            self.apple.move()
            self.snake.increase_length()
            if(self.snake.length % 5 == 0):
                self.snake.speed -= 0.05

            
        #snake colliding with snake
        for i in range(3, self.snake.length):
            if(self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[i], self.snake.block_y[i])):
                raise "Game Over!"
        #snake going out of bounds (1000x800)
        if((self.snake.block_x[0] < 0) or (self.snake.block_x[0] > 1000) or (self.snake.block_y[0] < 0) or (self.snake.block_y[0] > 800)):
            raise "Game Over!"



    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255,255,255))
        self.surface.blit(score, (800,10))



    def show_game_over(self):
        self.surface.fill((100,165,67))
        font = pygame.font.SysFont('arial', 40)
        over = font.render(f"GAME OVER! Final Score: {self.snake.length}", True, (255,255,255))
        self.surface.blit(over, (200,300))
        over2 = font.render(f"Press enter to play again. To exit, press escape", True, (255,255,255))
        self.surface.blit(over2, (100,350))
        pygame.display.flip()
        

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self): #"kinda the main function"
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if(event.type == KEYDOWN): #if the event is a key being pressed
                    if(event.key == K_ESCAPE):
                        running = False
                    if (event.key == K_RETURN):
                        pause = False
                    if not pause:
                        if(event.key == K_UP): #if that pressed key is up, etc.
                            self.snake.move_up()
                        if(event.key == K_DOWN):
                            self.snake.move_down()
                        if(event.key == K_LEFT):
                            self.snake.move_left()
                        if(event.key == K_RIGHT):
                            self.snake.move_right()
                elif event.type == QUIT:#if click X
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(self.snake.speed)



if __name__ == "__main__":
    
    game = Game()
    game.run()