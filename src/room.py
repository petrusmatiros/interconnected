from inspect import CO_ASYNC_GENERATOR
from re import X
from secrets import choice
from traceback import print_stack
import pygame 
from config import *
from tile import Tile
from csv_handler import *
from enum import Enum
from player import Player

class Room_type(Enum):
    POWERSUPPLY = 'power supply'
    MOTHERBOARD = 'motherboard'
    CPU = 'CPU'
    DRAM = 'DRAM'
    L1 = 'L1'
    L2 = 'L2'
    L3 = 'L3'
    GPU = 'GPU'
    VRAM = 'VRAM'
    SSD = 'SSD'
    INTERNET = 'internet'

class Collider_type(Enum):
    POWERSUPPLY = 'collider_powersupply'
    MOTHERBOARD = 'collider_motherboard'
    CPU = 'collider_CPU'
    DRAM = 'collider_DRAM'
    L1 = 'collider_L1'
    L2 = 'collider_L2'
    L3 = 'collider_L3'
    GPU = 'collider_GPU'
    VRAM = 'collider_VRAM'
    SSD = 'collider_SSD'
    INTERNET = 'collider_internet'
    
class Room:
	"""Room stores data about the current room and handles the camera movement
	"""
	def __init__(self):
		"""Initializes a new Room object
		"""
		# get the display surface 
		self.display_surface = pygame.display.get_surface()
		# sprite group setup
		self.visible_sprites = Camera()
		self.obstacle_sprites = pygame.sprite.Group()
		self.prev_room = Room_type.MOTHERBOARD.value
		# sprite setup
		self.create_map(Collider_type.MOTHERBOARD.value, 'both', 'motherboard', False, None)

	def create_map(self, current_room, choice, player_location, override_player_location, position):
		"""Initializes the current map layout with the player position and colliders
		"""
		layouts = {
			current_room : import_csv_layout('../assets/mapdata/' + current_room + '.csv'),
   			'player': import_csv_layout('../assets/mapdata/initial_position.csv'),
		}
		self.prev_room = current_room.replace('collider_', '')
		for type, layout in layouts.items():
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != AIR:
						x = col_index * TILESIZE
						y = row_index * TILESIZE
      
					if 'room' in choice or 'both' in choice:
						if type == current_room:
							Tile((x,y), col, [self.obstacle_sprites], 'invisible')
					
					if 'player' in choice or 'both' in choice:
						if type == 'player':
							if col == IS_PLAYER:
								if not override_player_location:
									self.player = Player(
										(x,y),
										player_location,
										[self.visible_sprites],
										self.obstacle_sprites,
									)
								elif override_player_location:
									self.player = Player(
										position,
										player_location,
										[self.visible_sprites],
										self.obstacle_sprites,
									)
						        
	def room_traversal(self):
		"""Handles the room traversal
		"""
		self.obstacle_sprites.empty()
		self.visible_sprites.empty()
		self.visible_sprites.set_room(self.player.get_location())
		current_room = 'collider_' + self.player.get_location()
		 
		layouts = {
			current_room : import_csv_layout('../assets/mapdata/' + current_room + '.csv'),
		}
		
		x_pos = 0
		y_pos = 0
		middle = 2
		door_opening = 0
		for row_index, row in enumerate(layouts[current_room]):
				for col_index, col in enumerate(row):
					x = col_index * TILESIZE
					y = row_index * TILESIZE
					if col == DOORS[self.prev_room]:
						door_opening += 1
						if door_opening == middle:
							x_pos = x	
							y_pos = y	

		keys = pygame.key.get_pressed()
  
		if keys[pygame.K_w] or keys[pygame.K_UP]:
			y_pos -= 75
		elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
			y_pos += 75
		elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			x_pos -= 75
		elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
			x_pos += 75

		player_position = (x_pos,y_pos)
   
		self.create_map(current_room, 'both', self.player.get_location(), True, player_position)
			
		self.player.colliding = False
		

	def handle(self):
		"""Handles the drawing of the player in the room
		"""
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		if (self.player.colliding == True):
			self.room_traversal()

class Camera(pygame.sprite.Group):
	"""Camera stores relevant data about the camera object

	Args:
		pygame (pygame.sprite): the group of sprites
	"""
	def __init__(self):
		"""Initializes a new Camera object
  		"""
		# general setup 
		super().__init__()
  
		# setup
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		# set the path to the current room
		room_path = '../assets/rooms/' + Room_type.MOTHERBOARD.value + '.png'
  
		# create floor
		self.floor_surf = pygame.image.load(room_path).convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
  
	def set_room(self, room):
		# set the path to the current room
		room_path = '../assets/rooms/' + room + '.png'
  
		# create floor
		self.floor_surf = pygame.image.load(room_path).convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	def custom_draw(self,player):
		"""Draws the player with the moving camera
  		"""
		# set offsets 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# draw floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf,(floor_offset_pos))

		# display with given offset
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image, offset_pos)
        
