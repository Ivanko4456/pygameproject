from utils import *

pygame.init()

FPS = 60
W, H = 1000, 1000

clock = pygame.time.Clock()
screen = pygame.display.set_mode(size=(W, H))

tile_images = {
	'wall': load_sprite('stone_wall.png'),
	'empty': load_sprite('grass.png')
}
player_image = load_sprite('stone_wall.png')

tile_width = tile_height = 160
all_sprites_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
all_tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
	def __init__(self, tile_type, pos_x, pos_y):
		super().__init__(all_tiles_group, all_sprites_group)
		self.image = tile_images[tile_type]
		self.rect = self.image.get_rect().move(
			tile_width * pos_x, tile_height * pos_y)
		if tile_type == 'wall':
			walls_group.add(self)


class Player(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y):
		super().__init__(player_group, all_sprites_group)
		self.speed = 7
		self.image = player_image
		self.rect = self.image.get_rect().move(
			tile_width * pos_x, tile_height * pos_y)
	
	def update(self, dx, dy):
		self.rect.x += dx * self.speed
		self.rect.y += dy * self.speed
		if pygame.sprite.spritecollideany(self, walls_group):
			self.rect.y -= dy * self.speed
			self.rect.x -= dx * self.speed


class Camera:
	# зададим начальный сдвиг камеры
	def __init__(self):
		self.dx = 0
		self.dy = 0

	# сдвинуть объект obj на смещение камеры
	def apply(self, obj=None):

		obj.rect.x += self.dx
		obj.rect.y += self.dy

	# позиционировать камеру на объекте target
	def update(self, target):
		self.dx = -(target.rect.x + target.rect.w // 2 - W // 2)
		self.dy = -(target.rect.y + target.rect.h // 2 - H // 2)


def start_screen():
	pass


def generate_level(level):
	new_player, x, y = None, None, None
	for y in range(len(level)):
		for x in range(len(level[y])):
			if level[y][x] == '.':
				Tile('empty', x, y)
			elif level[y][x] == '#':
				Tile('empty', x, y)
				Tile('wall', x, y)
			elif level[y][x] == 'p':
				Tile('empty', x, y)
				new_player = Player(x, y)
			elif level[y][x] == 'f':
				Tile('empty', x, y)

	# вернем игрока, а также размер поля в клетках
	return new_player, x, y


def terminate():
	pygame.quit()
	sys.exit()


if __name__ == '__main__':
	player, level_x, level_y = generate_level(load_level('level0.txt'))
	start_screen()
	camera = Camera()
	
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminate()

		if pygame.key.get_pressed()[pygame.K_UP]:
			player.update(0, -1)
		if pygame.key.get_pressed()[pygame.K_DOWN]:
			player.update(0, 1)
		if pygame.key.get_pressed()[pygame.K_RIGHT]:
			player.update(1, 0)
		if pygame.key.get_pressed()[pygame.K_LEFT]:
			player.update(-1, 0)
			
		screen.fill((0, 0, 0))
		# изменяем ракурс камеры
		camera.update(player)
		# обновляем положение всех спрайтов
		for sprite in all_sprites_group:
			camera.apply(sprite)
		all_tiles_group.draw(screen)
		all_tiles_group.update()
		player_group.draw(screen)
		
		pygame.display.flip()
		clock.tick(FPS)
