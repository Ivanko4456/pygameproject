import os
import sys
import pygame


def load_sprite(name, colorkey=None):
	fname = os.path.join('data', 'sprites', name)
	# если файл не существует, то выходим
	if not os.path.isfile(fname):
		print(f"Файл с изображением '{fname}' не найден")
		sys.exit()
	img = pygame.image.load(fname)
	if colorkey is not None:
		img = img.convert()
		if colorkey == -1:
			colorkey = img.get_at((0, 0))
		img.set_colorkey(colorkey)
	else:
		img = img.convert_alpha()
	return img


def load_level(filename):
	filename = "data/levels/" + filename
	# читаем уровень, убирая символы перевода строки
	with open(filename, 'r') as mapFile:
		level_map = [line.strip() for line in mapFile]
	
	# и подсчитываем максимальную длину
	max_width = max(map(len, level_map))
	
	# дополняем каждую строку пустыми клетками ('.')
	level = list(map(lambda x: x.ljust(max_width, '.'), level_map))
	return level



