import pygame
import random
from config import *
class Dialogue():
    
    def __init__(self, surface):
        self.room_dialogue = {
            'motherboard': ['1','2','3'],
            'CPU': ['1','2','3'],
            'DRAM': ['1','2','3'],
            'L1': ['1','2','3'],
            'L2': ['1','2','3'],
            'L3': ['1','2','3'],
            'GPU': ['1','2','3'],
            'VRAM': ['1','2','3'],
            'SSD': ['1','2','3'],
            'internet': ['1','2','3'],
            'power supply': ['1','2','3'],
            'Pill': ['1','2','3'],
            'Blue_Pill': ['1','2','3'],
            'Red_Pill': ['1','2','3'],
            }
        self.surface = surface
        self.font = pygame.font.Font('../assets/font/Abaddon Bold.ttf', 16)
        
    def print_room(self, location):
        
        self.print_txt('The electron is in the ' + location, TXT_X, TXT_Y - 25)
        
        keys = pygame.key.get_pressed()
        
        if (keys[pygame.K_e]):
            self.print_info(location)
        
    def print_txt(self, text, x, y):
        self.text = self.font.render(text, True, (255,255,255))
        self.textRect = self.text.get_rect()
        self.textRect.center = (x, y)
        self.surface.blit(self.text, self.textRect)
        pygame.display.update()
        
    def print_info(self, location):
        rand = random.randint(0, len(self.room_dialogue.get(location))-1)
        self.print_txt(self.room_dialogue.get(location)[rand], TXT_X, TXT_Y)
        pygame.display.update()