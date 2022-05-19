import pygame
from math import sin
from room import *
from current import Current

class Entity(pygame.sprite.Sprite):
	"""
	Entity is the base class for all entities.
	"""
	def __init__(self, groups, location):
		"""Initializes the entity.
		"""
		super().__init__(groups)
		# index of current frame
		self.currentFrame = 0
		# the speed of which the sprite is animated
		self.animation_speed = 0.15
		# the direction the sprite
		self.direction = pygame.math.Vector2()
		# the location of the sprite
		self.location = location
		# if the sprite is colliding with an obstacle
		self.colliding = False
		
  
	def get_location(self):
		"""Returns the entity's current location
		"""
		return self.location

	def movement_handler(self, speed):
		"""Handles the player movement

		Args:
			speed (integer): the speed of the player
		"""
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision_handler('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision_handler('vertical')
		self.rect.center = self.hitbox.center
		



	def door_handler(self):
		"""Handles the player entering doors (traversal)
		"""
		for sprite in self.obstacle_sprites:
			if sprite.id == DOORS['motherboard'] and sprite.hitbox.colliderect(self.hitbox):
				self.colliding = True
				self.location = 'motherboard'
			elif sprite.id == DOORS['CPU'] and sprite.hitbox.colliderect(self.hitbox):
				self.colliding = True
				self.location = 'CPU'
			elif sprite.id == DOORS['DRAM'] and sprite.hitbox.colliderect(self.hitbox):
				self.colliding = True
				self.location = 'DRAM'
			elif sprite.id == DOORS['L1'] and sprite.hitbox.colliderect(self.hitbox):
				self.colliding = True
				self.location = 'L1'
			elif sprite.id == DOORS['L2'] and sprite.hitbox.colliderect(self.hitbox):
				self.colliding = True
				self.location = 'L2'
			elif sprite.id == DOORS['L3'] and sprite.hitbox.colliderect(self.hitbox):
				self.colliding = True
				self.location = 'L3'
			elif sprite.id == DOORS['GPU'] and sprite.hitbox.colliderect(self.hitbox):
				self.colliding = True
				self.location = 'GPU'
			elif sprite.id == DOORS['VRAM'] and sprite.hitbox.colliderect(self.hitbox):
				self.colliding = True
				self.location = 'VRAM'
			elif sprite.id == DOORS['SSD'] and sprite.hitbox.colliderect(self.hitbox):
				self.colliding = True
				self.location = 'SSD'
			elif sprite.id == DOORS['internet'] and sprite.hitbox.colliderect(self.hitbox):
				self.colliding = True
				self.location = 'internet'
			elif sprite.id == DOORS['Pill'] and sprite.hitbox.colliderect(self.hitbox):
				self.colliding = True
				self.location = 'Pill'
			elif sprite.id == DOORS['Blue_Pill'] and sprite.hitbox.colliderect(self.hitbox):
				self.colliding = True
				self.location = 'Blue_Pill'
			elif sprite.id == DOORS['Red_Pill'] and sprite.hitbox.colliderect(self.hitbox):
				self.colliding = True
				self.location = 'Red_Pill'
    
	# # TODO: FIX THIS			
	# def key_handler(self, current):
	# 	"""Handles the player picking up keys
	# 	"""
	# 	for sprite in self.obstacle_sprites:
	# 		if sprite.id == KEYS['RED'] and sprite.hitbox.colliderect(self.hitbox):
	# 			self.current.red_key = True
	# 			self.current_sprite = sprite

	# 		elif sprite.id == KEYS['PURPLE'] and sprite.hitbox.colliderect(self.hitbox):
	# 			self.current.purple_key = True
	# 			self.current_sprite = sprite


	def collision_handler(self, direction):
		"""Handles the player collision with objects

		Args:
			direction (vector2): the direction of the player
		"""
		
		self.door_handler()
		# self.key_handler(self.current)
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				# if the player is colliding with an obstacle
				if sprite.hitbox.colliderect(self.hitbox):
					# moving right
					if self.direction.x > 0: 
						self.hitbox.right = sprite.hitbox.left
					# moving left
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					# moving down
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					# moving up
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom

    
    