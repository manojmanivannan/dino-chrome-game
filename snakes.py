import pygame, os, random

SCREEN_SIZE = WIDTH, HEIGHT = 500, 500

SnakeHEAD = pygame.image.load(os.path.join("assets/Snake", "SnakeBlock.png"))
FoodBLOCK = pygame.image.load(os.path.join("assets/obstacle", "FoodBlock.png"))

class Snake:

    X_POS = 25 * round(random.randrange(0, WIDTH - 25) / 25)
    Y_POS = 25 * round(random.randrange(0, HEIGHT - 25) / 25)
    JUMP_VEL = 8.5

    def __init__(self,img=SnakeHEAD) -> None:
        self.image = img
        self.snake_up = False   # go up be default
        self.snake_down = False
        self.snake_left = False
        self.snake_right = False
        self.food_obtained = False
        self.snake_body = []

        self.snake_body.append(pygame.Rect(self.X_POS, self.Y_POS,img.get_width(), img.get_height()))
        self.head = self.snake_body[0]

    def draw(self, SCREEN):
        for block in self.snake_body:
            SCREEN.blit(self.image, (block.x, block.y))
            # pygame.draw.rect(SCREEN, self.color, (block.x, block.y, self.head.width, self.head.height), 2)

    def update(self):
        if self.snake_up:
            self.move_up()
        if self.snake_down:
            self.move_down()
        if self.snake_right:
            self.move_right()
        if self.snake_left:
            self.move_left()

    def is_collision(self, KIND):
        self.head = self.snake_body[0]

        match KIND:
            case 'TOP':
                return True if self.head.y < self.image.get_height() else False # top screen
            case 'BOTTOM':
                return True if self.head.y >= HEIGHT - self.image.get_height() else False # bottom screen
            case 'RIGHT':
                return True if self.head.x >= WIDTH - self.image.get_width() else False # right screen
            case 'LEFT':
                return True if self.head.x < self.image.get_width() else False # left screen

    def move_up(self):
        if not self.is_collision(KIND='TOP'): 
            self.snake_body.insert(0,pygame.Rect(self.snake_body[0].x ,self.snake_body[0].y - self.image.get_height(),self.image.get_width(), self.image.get_height()))
            if not self.food_obtained:
                self.snake_body.pop()
            # self.head.y -= self.image.get_height()

    def move_down(self,):
        if not self.is_collision(KIND='BOTTOM'): 
            self.snake_body.insert(0,pygame.Rect(self.snake_body[0].x ,self.snake_body[0].y + self.image.get_height(),self.image.get_width(), self.image.get_height()))
            if not self.food_obtained:
                self.snake_body.pop()
            # self.head.y += self.image.get_height()

    def move_right(self):
        if not self.is_collision(KIND='RIGHT'): 
            self.snake_body.insert(0,pygame.Rect(self.snake_body[0].x + self.image.get_width() ,self.snake_body[0].y ,self.image.get_width(), self.image.get_height()))
            if not self.food_obtained:
                self.snake_body.pop()
            # self.head.x += self.image.get_width()

    def move_left(self):
        if not self.is_collision(KIND='LEFT'): 
            self.snake_body.insert(0,pygame.Rect(self.snake_body[0].x - self.image.get_width() ,self.snake_body[0].y ,self.image.get_width(), self.image.get_height()))
            if not self.food_obtained:
                self.snake_body.pop()
            # self.head.x -= self.image.get_width()








class Food:
    X_POS = 25 * round(random.randrange(0, WIDTH - 25) / 25)
    Y_POS = 25 * round(random.randrange(0, HEIGHT - 25) / 25)

    def __init__(self,img=FoodBLOCK):
        self.image = img
        self.pos = pygame.Rect(self.X_POS, self.Y_POS,img.get_width(), img.get_height())

        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.step_index = 0

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.pos.x, self.pos.y))

    def respawn(self):
        self.X_POS = 25 * round(random.randrange(0, WIDTH - 25) / 25)
        self.Y_POS = 25 * round(random.randrange(0, HEIGHT - 25) / 25)
        self.pos = pygame.Rect(self.X_POS, self.Y_POS,self.image.get_width(), self.image.get_height())