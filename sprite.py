import pygame

from settings import *

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.rotation = 0
        self.color = SHAPE_COLORS[SHAPES.index(shape)]

class Label:
    def __init__(self, text, size, color=WHITE, bold=False, italic=False):
        font = pygame.font.SysFont("Consolas", size, bold, italic)
        self.label = font.render(text, True, color)

    def get_width(self):
        return self.label.get_width()

    def get_height(self):
        return self.label.get_height()

    def draw(self, surface, x, y, auto_align=False):
        if auto_align:
            surface.blit(self.label, (x - self.label.get_width()/2, y - self.label.get_height()/2))
        else:
            surface.blit(self.label, (x, y))

class Button:
    def __init__(self, text, size, text_color, color):
        font = pygame.font.SysFont("Consolas", size)
        self.label = font.render(text, True, text_color)
        self.color = color
    
    def draw(self, surface, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height

        pygame.draw.rect(surface, self.color, (self.x, self.y, width, height))

        x_pos = self.x + self.width/2 - self.label.get_width()/2
        y_pos = self.y + self.height/2 - self.label.get_height()/2
        surface.blit(self.label, (x_pos, y_pos))

    def click(self, mouse_x, mouse_y):
        return (self.x <= mouse_x <= self.x+self.width) and (self.y <= mouse_y <= self.y+self.height)
