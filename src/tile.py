import pygame 
from config import *

class Tile(pygame.sprite.Sprite):
	"""Tile is the base class for all tiles.

	Args:
		pygame (pygame.sprite): the sprites
	"""
	def __init__(self, position, id, groups, sprite_type, surface = pygame.Surface((TILESIZE,TILESIZE))):
		"""Initializes a new Tile object

		Args:
			position (position): the tile position
			groups (pygame.sprite): the sprites to be drawn
			sprite_type (string): the sprite type
			surface (pygame.Surface): the surface to draw with the specified tile size. Defaults to pygame.Surface((TILESIZE, TILESIZE)).
		"""
		super().__init__(groups)
		self.id = id
		self.position = position
		self.sprite_type = sprite_type
		y_offset = HITBOX_OFFSET[sprite_type]
		self.image = surface
		# set the position of the tile and it's hitbox
		if sprite_type == 'object':
			self.rect = self.image.get_rect(topleft = (position[0], position[1] - TILESIZE))
		else:
			self.rect = self.image.get_rect(topleft = position)
		self.hitbox = self.rect.inflate(0, y_offset)
  
	def set_pos(self, position):
		"""Sets the tile position
		"""
		self.position = position
	
	def set_sprite_type(self, sprite_type):
		"""Sets the sprite type
		"""
		self.sprite_type = sprite_type