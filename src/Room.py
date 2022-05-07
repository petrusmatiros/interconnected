from inspect import CO_ASYNC_GENERATOR
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
		# sprite setup
		self.create_map(Collider_type.MOTHERBOARD.value)

	def create_map(self, current_room):
		"""Initializes the current map layout with the player position and colliders
		"""
		layouts = {
			current_room : import_csv_layout('../assets/mapdata/' + current_room + '.csv'),
   			'player': import_csv_layout('../assets/mapdata/initial_position.csv'),
		}
		for type, layout in layouts.items():
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != AIR:
						x = col_index * TILESIZE
						y = row_index * TILESIZE
      
						if type == current_room:
							Tile((x,y), col, [self.obstacle_sprites], 'invisible')

						if type == 'player':
							if col == IS_PLAYER:
								self.player = Player(
									(x,y),
									[self.visible_sprites],
									self.obstacle_sprites,
         						)
						        
	def room_traversal(self):
		"""Handles the room traversal
		"""

		prev_location = self.player.location
		self.visible_sprites.set_room(self.player.get_location())
		current_room = 'collider_' + self.player.get_location()
  
		self.obstacle_sprites.empty()
		self.visible_sprites.empty()
  
		self.create_map(current_room)
		self.player.location = prev_location
		current_room = 'collider_' + self.player.get_location()
		
		location = self.player.get_location()
  
		# key_list = list(PATHS.keys())
		# val_list = list(PATHS.values())

		# index = val_list.index(DOORS[location])
		 
		# layouts = {
		# 	current_room : import_csv_layout('../assets/mapdata/' + current_room + '.csv'),
		# }

		# for row_index, row in enumerate(layouts[current_room]):
		# 		for col_index, col in enumerate(row):
		# 			x = col_index * TILESIZE
		# 			y = row_index * TILESIZE
		# 			if col == key_list[index]:
		# 				print("found:",col , x, y)
		# 				player_position = (x,y)

       
		# if self.player.get_location() == Collider_type.CPU.value:
		# 	self.player.set_pos(player_position)
			
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
        
