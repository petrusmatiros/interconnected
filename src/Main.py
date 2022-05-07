import pygame, sys
from config import *
from room import *

class Game:
	"""Game initialises the game and runs the main game loop
	"""
	def __init__(self):
		"""Initializes a new Game object
		"""
		# setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption('Interconnected')
		self.clock = pygame.time.Clock()

		# init room
		self.room = Room()
	
	def run(self):
		"""Runs the main game loop
		"""
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			
			self.screen.fill((0,0,0))
			self.room.handle()
			pygame.display.update()
			self.clock.tick(FPS)
       

if __name__ == '__main__':
	game = Game()
	game.run()