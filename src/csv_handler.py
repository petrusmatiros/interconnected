from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
	"""Imports the csv files with the given map layout

	Args:
		path (string): the path to the csv file

	Returns:
		list: a map of lists, of the csv file
	"""
	map = []
	with open(path) as room:
		layout = reader(room, delimiter = ',')
		for row in layout:
			map.append(list(row))
		return map

def import_folder(path):
	"""Imports the folders with player sprites

	Args:
		path (string): the path to the folders

	Returns:
		list: a list of all the paths to the sprites
	"""
	surfaces = []
	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surfaces.append(image_surf)

	return surfaces
