import pygame
import random
from config import *
from inventory import *
import time
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
        
        self.print_txt('The electron is in the ' + location, TXT_X, TXT_Y - 10)
        
        keys = pygame.key.get_pressed()
        
        if (keys[pygame.K_e]):
            self.print_info(location)
            
    def check_access(self, location):
        self.print_txt('The path to the ' + location + ' seems to be locked', TXT_X, TXT_Y)
        pygame.display.update()
        
    def picked_up_key(self, color):
        if color == Color.RED:
            self.print_txt('Picked up red key piece', TXT_X, TXT_Y)
        if color == Color.PURPLE:
            self.print_txt('Picked up purple key', TXT_X, TXT_Y)
        pygame.display.update()
    
    def win_normal(self):
        self.print_txt('You win! That\'s it, just a simple normal adventure game ;)', TXT_X, TXT_Y + 40)
        pygame.display.update()
        
    def pill(self):
        self.print_txt('2 colors, 2 choices, 2 destinies - all up to you...old friend', TXT_X, TXT_Y + 40)
        pygame.display.update()
        
    def win_blue(self):
        self.print_txt('The electron experiences a weird electric sensation - the electron is reset', TXT_X, TXT_Y + 40)
        pygame.display.update()
        
    def win_red(self):
        self.print_txt('The electron experiences a weird electric sensation - the electron escapes the simulation"', TXT_X, TXT_Y + 40)
        pygame.display.update()
    
    
    def print_inventory(self, inventory):
        self.print_txt('Inventory:', 120, TXT_Y - 10)
        self.print_txt('Red keypieces: ' + str(inventory.get_amount(Color.RED)) + '/3', 120, TXT_Y + 20)
        self.print_txt('Purple key: ' + str(inventory.get_amount(Color.PURPLE)) + '/1', 120, TXT_Y + 40)
    
    # TODO:
    # Add function comments
    # Use self.quit from room at endings
    # Add room info
    # Make it so you print text slower when viewing room info
    # Add VRAM information text
    # Add endings text
    def print_txt(self, text, x, y):
        self.text = self.font.render(text, True, (255,255,255))
        self.textRect = self.text.get_rect()
        self.textRect.center = (x, y)
        self.surface.blit(self.text, self.textRect)
        # pygame.display.update()
        
    def print_info(self, location):
        rand = random.randint(0, len(self.room_dialogue.get(location))-1)
        self.print_txt(self.room_dialogue.get(location)[rand], TXT_X, TXT_Y + 40)
        # pygame.display.update()