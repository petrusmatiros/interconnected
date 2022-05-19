import pygame 
from config import *
from tile import Tile
from csv_handler import *
from enum import Enum
from player import Player
from key import Color
from inventory import *
from current import Current
from dialogue import Dialogue

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
		self.create_map(Collider_type.MOTHERBOARD.value, 'both', 'motherboard', False, None, 'down', True)
		# init player inventory
		self.inventory = Inventory()
		# init current reference
		self.current = Current()
		# boolean to quit game
		self.quit = False
		# init dialogue
		
		self.dialogue = Dialogue(self.display_surface)
		

	def create_map(self, current_room, choice, player_location, override_player_location, position, status, draw_keys):
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
							# if col == KEYS["RED"] or col == KEYS["PURPLE"]:
								# # if draw_keys:
								# # TODO: draw key tile with hitbox, overlaying map, then remove it, and let air be left (air in csv, -1 in map)
								# 	Tile((x,y), col, [self.obstacle_sprites], 'key')
							# else:
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
											status,
										)
								elif override_player_location:
									self.player = Player(
										position,
										player_location,
										[self.visible_sprites],
										self.obstacle_sprites,
										status,
									)
	
 
	# def update_map(self):
	# 	"""Handles updates of the map when keys are picked up
	# 	"""
	# 	# self.obstacle_sprites.empty()
	# 	# self.visible_sprites.empty()
	# 	current_room = 'collider_' + self.player.get_location()
	# 	x = self.player.rect.centerx
	# 	y = self.player.rect.centery
	# 	player_position = (x,y)
	# 	draw_keys = False
	# 	# self.create_map(current_room, 'both', self.player.get_location(), True, player_position, self.player.status, draw_keys)
  
	# 	if (self.player.current.red_key):
	# 		self.player.current.red_key = False
	# 		self.inventory.add_key(Color.RED)
	# 	elif (self.player.current.purple_key):
	# 		self.player.current.purple_key = False
	# 		self.inventory.add_key(Color.PURPLE)
	# 	self.obstacle_sprites.remove(self.player.current_sprite)
	# 	print(self.inventory.get_amount(Color.RED))
	# 	# pygame.sprite.Sprite.remove(self.player.current_sprite)
  
	def check_visits(self):
		"""Checks if the player has visited a room
		"""
		if self.inventory.get_amount(Color.RED) < 3:
			
			if self.player.get_location() == 'L1' and self.current.L1_visited == False:
				self.current.L1_visited = True
				self.inventory.add_key(Color.RED)
			if self.player.get_location() == 'L2' and self.current.L2_visited == False:
				self.current.L2_visited = True
				self.inventory.add_key(Color.RED)
			if self.player.get_location() == 'L3' and self.current.L3_visited == False:
				self.current.L3_visited = True
				self.inventory.add_key(Color.RED)

		if self.inventory.get_amount(Color.PURPLE) < 1 and self.inventory.get_amount(Color.RED) == 3:
			if self.player.get_location() == 'SSD' and self.current.SSD_visited == False and self.current.has_information == False:
				self.current.SSD_visited = True
				self.current.has_information = True
				self.inventory.add_key(Color.PURPLE)

	def check_endings(self):
		"""Checks if the player has reached the end of the game and/or endings
		"""
		if self.player.get_location() == 'VRAM' and self.current.has_information == True and self.current.inserted_information == False:
			self.current.inserted_information = True
			self.player.colliding = False
		elif self.player.get_location() == 'internet' and self.inventory.get_amount(Color.PURPLE) == 1 and self.current.inserted_information == False:
			self.current.internet_visited = True
			self.player.colliding = False
		elif self.player.get_location() == 'internet' and self.current.inserted_information == True:
			self.current.internet_visited = True
			self.player.location = 'Pill'
			self.player.colliding = False

    
	def room_traversal(self):
		"""Handles the room traversal
		"""
		
		self.check_visits()
  
		if self.inventory.get_amount(Color.RED) < 3 and self.player.get_location() == 'SSD':
			self.player.location = 'motherboard'
			self.player.colliding = False
		elif self.inventory.get_amount(Color.PURPLE) < 1 and self.player.get_location() == 'internet':
			self.player.location = 'motherboard'
			self.player.colliding = False
		else:
			draw_keys = True
			self.obstacle_sprites.empty()
			self.visible_sprites.empty()
				
			self.check_endings()

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
				x_pos += 75
			elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
				x_pos -= 75

			ending_position = (WIDTH/2,300)
   
			if self.current.internet_visited and self.current.inserted_information == False:
				player_position = ending_position
			elif self.current.internet_visited and self.current.inserted_information == True:
				player_position = ending_position
			else:
				player_position = (x_pos,y_pos)
	
			self.create_map(current_room, 'both', self.player.get_location(), True, player_position, self.player.status, draw_keys)
				
			self.player.colliding = False
			
		

	def handle(self):
		"""Handles the drawing of the player and text in the room
		"""
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		if (self.player.colliding == True):
			self.room_traversal()
		self.dialogue.print_room(self.player.get_location())

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
		# self.half_width = self.display_surface.get_size()[0] // 2
		# self.half_height = self.display_surface.get_size()[1] // 2
		# self.offset = pygame.math.Vector2()

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
		# # set offsets 
		# self.offset.x = player.rect.centerx - self.half_width
		# self.offset.y = player.rect.centery - self.half_height

		# draw floor
		# floor_offset_pos = self.floor_rect.topleft - self.offset
		floor_offset_pos = self.floor_rect.topleft
		self.display_surface.blit(self.floor_surf,(floor_offset_pos))

		# display with given offset
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			# offset_pos = sprite.rect.topleft - self.offset
			offset_pos = sprite.rect.topleft
			self.display_surface.blit(sprite.image, offset_pos)
        
