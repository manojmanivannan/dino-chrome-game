import sys, pygame, os
from snakes import Snake, Food, SCREEN_SIZE
import random
import neat, math, re

pygame.init()

SCREEN = pygame.display.set_mode(SCREEN_SIZE)
FONT = pygame.font.Font('freesansbold.ttf', 10)
WIDTH, HEIGHT = SCREEN_SIZE[0], SCREEN_SIZE[1]

def random_x_y_coord(WIDTH,HEIGHT):
    return 25 * round(random.randrange(0, WIDTH - 25) / 25),25 * round(random.randrange(0, HEIGHT - 25) / 25)

def remove_snake(index):
    snakes.pop(index)
    foods.pop(index)
    ge.pop(index)
    nets.pop(index)

def distance(pos_a,pos_b):
    dx = pos_a[0]-pos_b[0]
    dy = pos_a[1]-pos_b[1]
    return math.sqrt(dx**2+dy**2)

def get_max_checkpoint():
    local_dir = os.path.dirname(__file__)
    try:
        last_check_point = max([int(f.split('point-')[1]) for f in os.listdir(local_dir) if re.match(r'neat-checkpoint+.*', f)])
    except ValueError:
        return None
    print(f'Found neat-checkout-{last_check_point}')
    return 'neat-checkpoint-'+str(last_check_point)


def eval_genomes(genomes, config):

    global game_speed, x_pos_bg, y_pos_bg, points, snakes, foods, ge, nets
    clock = pygame.time.Clock()
    points = 0

    # snakes = [Snake(POS=random_x_y_coord(WIDTH,HEIGHT)), Snake(POS=random_x_y_coord(WIDTH,HEIGHT))]
    # foods = [Food(),Food()]
    snakes = []
    foods = []
    ge = [] # fitness scores of each geomes
    nets = []

    for genome_id, genome in genomes:
        snakes.append(Snake(POS=random_x_y_coord(WIDTH,HEIGHT),id=genome_id))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        nets.append(net)
        genome.fitness = 0
        foods.append(Food(POS=random_x_y_coord(WIDTH,HEIGHT)))


    x_pos_bg = 0
    y_pos_bg = 0
    game_speed = 30


    def score():

        # global snakes
        text_2 = FONT.render(f'# Snakes:  {str(len(snakes))}', True, (200, 0, 0))
        text_3 = FONT.render(f'Generation:  {pop.generation+1}', True, (200, 0, 0))
        SCREEN.blit(text_2, (5, HEIGHT-15))
        SCREEN.blit(text_3, (5, HEIGHT-30))

    RUN = True
    while RUN:

        # Set background color
        SCREEN.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # break when all snakes die
        if len(snakes) == 0: RUN = False

        for food in foods:
            food.draw(SCREEN)

        for snake in snakes:
            snake.update()
            snake.draw(SCREEN)

        # check if any of snakes is dead, if so , remove it from our list of snakes
        for i, snake in enumerate(snakes):
            if snake.is_dead: 
                ge[i].fitness -= 1.0
                remove_snake(i)

        for (i, snake),food in zip(enumerate(snakes),foods):
            if snake.head == food.pos:
                snake.food_obtained=True
                snake.food_history.append(1)
                ge[i].fitness+=float(snake.__len__())
                food.respawn()
            else:
                snake.food_obtained=False
                snake.food_history.append(0)

        for (i,snake),food in zip(enumerate(snakes),foods):
            output = nets[i].activate((
                                        snake.head.x-food.pos.x,
                                        snake.head.y-food.pos.y,
                                        distance(snake.head,food.pos)
                                        ))

            if output[0] > 0.5 and snake.direction != 'UP':
                snake.snake_up = True
                snake.snake_down = False
                snake.snake_left = False
                snake.snake_right = False

            if output[1] > 0.5 and snake.direction != 'DOWN':
                snake.snake_up = False
                snake.snake_down = True
                snake.snake_left = False
                snake.snake_right = False

            if output[2] > 0.5 and snake.direction != 'LEFT':
                snake.snake_up = False
                snake.snake_down = False
                snake.snake_left = True
                snake.snake_right = False

            if output[3] > 0.5 and snake.direction != 'RIGHT':
                snake.snake_up = False
                snake.snake_down = False
                snake.snake_left = False
                snake.snake_right = True

        score()
        clock.tick(game_speed)
        pygame.display.update()
        

def run(config_path):
    global pop, genomes
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path)

    if get_max_checkpoint() != None:
        pop = neat.Checkpointer.restore_checkpoint(get_max_checkpoint())
        print('Checkout point found, resuming')
    else:
        print('No checkout, Creating new population')
        pop = neat.Population(config)
    

    # Add stoud reported to show progress in the terminal
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(20))

    pop.run(eval_genomes,200)
    

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,'config.txt')
    run(config_path)

