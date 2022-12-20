import sys, pygame, os
from snakes import Snake, Food, SCREEN_SIZE


pygame.init()

SCREEN = pygame.display.set_mode(SCREEN_SIZE)

def main():

    snake = Snake()
    food = Food()

    RUN = True
    while RUN:

        clock = pygame.time.Clock()

        # Set background color
        SCREEN.fill((255, 255, 255))



        # Get directions from arrow keys
        # user_input = pygame.key.get_pressed()
        for event in pygame.event.get():
            
            # Enable game exit
            if event.type == pygame.QUIT:
                RUN = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:     
                    snake.snake_up = True
                    snake.snake_down = False
                    snake.snake_left = False
                    snake.snake_right = False
                elif event.key==pygame.K_DOWN:
                    snake.snake_up = False
                    snake.snake_down = True
                    snake.snake_left = False
                    snake.snake_right = False
                elif event.key==pygame.K_LEFT: 
                    snake.snake_up = False
                    snake.snake_down = False
                    snake.snake_left = True
                    snake.snake_right = False
                elif event.key==pygame.K_RIGHT: 
                    snake.snake_up = False
                    snake.snake_down = False
                    snake.snake_left = False
                    snake.snake_right = True
                else:
                    snake.snake_up = False
                    snake.snake_down = False
                    snake.snake_left = False
                    snake.snake_right = False
        snake.update()
        food.draw(SCREEN)
        
        

        if snake.head == food.pos:
            snake.food_obtained=True
            print('Yummy')
            food.respawn()
        else:
            snake.food_obtained=False

        snake.draw(SCREEN)

        clock.tick(4)
        pygame.display.update()
    
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
