import pygame 
from config import *
from csv_handler import import_folder
from entity import Entity

class Player(Entity):
	"""Player stores relevant data about the player such as: player sprite, speed, hitbox

	Args:
		Entity (Entity): entity object of class Entity
	"""
	def __init__(self, init_position, groups, obstacle_sprites):
		"""Initializes the player object

		Args:
			position (integer): the player position
			groups (pygame.sprite): the visible sprites on the map
			obstacle_sprites (pygame.sprite): the obsctacles on the map
		"""
		super().__init__(groups)
		self.currentPosition = init_position
		# display player and set it's hitbox
		self.image = pygame.image.load('../assets/sprites/player/down/down_0.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = self.currentPosition)
		self.hitbox = self.rect.inflate(0, HITBOX_OFFSET['player'])
		
		# graphics setup
		self.import_player_assets()
		self.status = 'down'
		
		# movement 
		self.obstacle_sprites = obstacle_sprites
  
        # speed stats
		self.stats = {'speed': WALKING}
	
 
	def set_pos(self, position):
		"""Sets the player position
		"""
		self.rect.centerx = position[0]
		self.rect.centery = position[0]
		
 
	def import_player_assets(self):
		"""Imports the player sprites from the assets folder
		"""
		sprite_path = '../assets/sprites/player/'
		self.animations = {'up': [],'down': [],'left': [],'right': []}

		for animation in self.animations.keys():
			full_path = sprite_path + animation
			self.animations[animation] = import_folder(full_path)


	def input(self):
		"""Handles the player input
		"""
		keys = pygame.key.get_pressed()

		# sprinting
		if keys[pygame.K_LSHIFT]:
			self.stats = {'speed': RUNNING}
		if not keys[pygame.K_LSHIFT]:
			self.stats = {'speed': WALKING}

		# normal movement
		if keys[pygame.K_w] or keys[pygame.K_UP]:
			self.direction.y = -1
			self.status = 'up'
		elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
			self.direction.y = 1
			self.status = 'down'
		else:
			self.direction.y = 0

		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.status = 'right'
		elif keys[pygame.K_a] or keys[pygame.K_LEFT] :
			self.direction.x = -1
			self.status = 'left'
		else:
			self.direction.x = 0
    
    
	def animate(self):
		"""Animates the player sprite
		"""
		animation = self.animations[self.status]

		# iterate through the animation frames 
		self.currentFrame += self.animation_speed
		if self.currentFrame >= len(animation):
			self.currentFrame = 0

		# set animation frame
		self.image = animation[int(self.currentFrame)]
		self.rect = self.image.get_rect(center = self.hitbox.center)


	def update(self):
		"""Updates all relevant player data
		"""
		self.input()
		self.animate()
		self.movement_handler(self.stats['speed'])