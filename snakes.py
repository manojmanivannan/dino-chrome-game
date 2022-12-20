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
        self.direction = ''
        self.is_dead = False

        self.snake_body.append(pygame.Rect(self.X_POS, self.Y_POS,img.get_width(), img.get_height()))
        self.head = self.snake_body[0]
        self.new_head = None

    def __len__(self):
        return len(self.snake_body)
        
    def draw(self, SCREEN):
        for block in self.snake_body:
            SCREEN.blit(self.image, (block.x, block.y))
            # pygame.draw.rect(SCREEN, self.color, (block.x, block.y, self.head.width, self.head.height), 2)

    def update(self):
        if self.snake_up:
            self.direction='UP'
            self.move_up()
        if self.snake_down:
            self.direction='DOWN'
            self.move_down()
        if self.snake_right:
            self.direction='RIGHT'
            self.move_right()
        if self.snake_left:
            self.direction='LEFT'
            self.move_left()

    def get_new_head(self,DIRECTION):
        X_n = self.snake_body[0].x
        Y_n = self.snake_body[0].y

        match DIRECTION:
            case 'UP':
                Y_n += self.image.get_height()
            case 'DOWN':
                Y_n -= self.image.get_height()
            case 'RIGHT':
                X_n -= self.image.get_height()
            case 'LEFT':
                X_n += self.image.get_height()
                
        return pygame.Rect(X_n ,Y_n,self.image.get_width(), self.image.get_height())

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
            case 'BODY':
                return any([True if self.new_head == body else False for body in self.snake_body])
            case 'REVERSE':
                if self.new_head.x == self.head.x and self.new_head.y == self.head.y:
                    print('New head',self.new_head,'| current head',self.head)
                    return True

    def move_up(self):
        self.new_head = pygame.Rect(self.snake_body[0].x ,self.snake_body[0].y - self.image.get_height(),self.image.get_width(), self.image.get_height())
        # check if we are reversing on the snake itself
        if self.new_head.y == self.head.y: self.new_head = self.get_new_head(DIRECTION=self.direction)
        if self.is_collision(KIND='BODY'):
            self.is_dead = True
        if not self.is_collision(KIND='TOP'): 
            self.snake_body.insert(0,self.new_head)
            if not self.food_obtained:
                self.snake_body.pop()
        else:
            self.is_dead = True

    def move_down(self,):
        self.new_head = pygame.Rect(self.snake_body[0].x ,self.snake_body[0].y + self.image.get_height(),self.image.get_width(), self.image.get_height())
        # check if we are reversing on the snake itself
        if self.new_head.y == self.head.y: self.new_head = self.get_new_head(DIRECTION=self.direction)
        if self.is_collision(KIND='BODY'):
            self.is_dead = True
        if not self.is_collision(KIND='BOTTOM'): 
            self.snake_body.insert(0,self.new_head)
            if not self.food_obtained:
                self.snake_body.pop()
        else:
            self.is_dead = True

    def move_right(self):
        self.new_head = pygame.Rect(self.snake_body[0].x + self.image.get_width() ,self.snake_body[0].y,self.image.get_width(), self.image.get_height())
        if self.new_head.x == self.head.x: self.new_head = self.get_new_head(DIRECTION=self.direction)
        if self.is_collision(KIND='BODY'):
            self.is_dead = True
        if not self.is_collision(KIND='RIGHT'): 
            self.snake_body.insert(0,self.new_head)
            if not self.food_obtained:
                self.snake_body.pop()
        else:
            self.is_dead = True

    def move_left(self):
        self.new_head = pygame.Rect(self.snake_body[0].x - self.image.get_width() ,self.snake_body[0].y,self.image.get_width(), self.image.get_height())
        if self.new_head.x == self.head.x: self.new_head = self.get_new_head(DIRECTION=self.direction)
        if self.is_collision(KIND='BODY'):
            self.is_dead = True
        if not self.is_collision(KIND='LEFT'): 
            self.snake_body.insert(0,self.new_head)
            if not self.food_obtained:
                self.snake_body.pop()
        else:
            self.is_dead = True









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