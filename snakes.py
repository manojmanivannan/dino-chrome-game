import pygame, os, random
from statistics import mean
from dataclasses import dataclass, field
from pygame.surface import Surface
from pygame.rect import Rect

SCREEN_SIZE = WIDTH, HEIGHT = 600, 600

SnakeHEAD = pygame.image.load(os.path.join("assets/Snake", "SnakeBlock.png"))
FoodBLOCK = pygame.image.load(os.path.join("assets/obstacle", "FoodBlock.png"))

@dataclass
class Snake:

    image:          Surface     = field(init=False, default=SnakeHEAD)
    pos:            tuple       = field(init=True, default=(300,475))
    id:             int         = field(init=True, default=0)
    snake_up:       bool        = field(init=False, default=False)
    snake_down:     bool        = field(init=False, default=False)
    snake_left:     bool        = field(init=False, default=False)
    snake_right:    bool        = field(init=False, default=False)
    food_obtained:  bool        = field(init=False, default=False)
    snake_body:     list[Rect]  = field(init=False,default_factory=list)
    food_history:   list[int]   = field(init=False,default_factory=list)
    direction:      str         = field(init=False, default='')
    is_dead:        bool        = field(init=False, default=False)
    new_head:       Rect        = field(init=False, default=None)

    def __post_init__(self) -> None:
        self.X_POS = self.pos[0]
        self.Y_POS = self.pos[1]
        self.snake_body.append(pygame.Rect(self.X_POS, self.Y_POS,self.image.get_width(), self.image.get_height()))
        self.head = self.snake_body[0]
        
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
        if self.food_history.__len__() > 4*round((WIDTH/25)):
            if mean(self.food_history[-3*round((WIDTH/25)):]) == 0:
                self.is_dead = True 

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
                    # print('New head',self.new_head,'| current head',self.head)
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
                self.food_history.append(0)
            else:
                self.food_history.append(1)
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
                self.food_history.append(0)
            else:
                self.food_history.append(1)
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
                self.food_history.append(0)
            else:
                self.food_history.append(1)
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
                self.food_history.append(0)
            else:
                self.food_history.append(1)
        else:
            self.is_dead = True






class Food:

    def __init__(self,img=FoodBLOCK,POS=(300,475)):
        self.image = img
        self.X_POS = POS[0]
        self.Y_POS = POS[1]
        self.pos = pygame.Rect(self.X_POS, self.Y_POS,img.get_width(), img.get_height())

        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.step_index = 0

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.pos.x, self.pos.y))

    def respawn(self):
        self.X_POS = 25 * round(random.randrange(0, WIDTH - 25) / 25)
        self.Y_POS = 25 * round(random.randrange(0, HEIGHT - 25) / 25)
        self.pos = pygame.Rect(self.X_POS, self.Y_POS,self.image.get_width(), self.image.get_height())

