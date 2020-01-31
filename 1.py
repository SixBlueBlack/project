import pygame
import sys
import os
from random import choice, randint

title = "map.txt"

fon = None
k = 0
r = 0
count = 0
pygame.init()
screen = pygame.display.set_mode((800, 600))
screen.fill((0, 0, 0))
pygame.display.flip()
clock = pygame.time.Clock()
player = None
up, down, left, right = False, False, False, False
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
chests_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
aim_group = pygame.sprite.Group()
indestructible_walls_group = pygame.sprite.Group()
tile_width = tile_height = 50


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {'empty': pygame.transform.scale(load_image('empty.png'), (50, 50)),
               'wall': pygame.transform.scale(load_image('wall.png'), (50, 50)),
               'indestructible_wall': pygame.transform.scale(load_image('indestructible_wall.png'), (50, 50))}
player_image = pygame.transform.scale(load_image('down1.png', -1), (45, 55))
enemy_image = pygame.transform.scale(load_image('enemy.png', -1), (50, 50))
closed_chest_image = pygame.transform.scale(load_image('chest_closed.png', -1), (45, 40))
opened_chest_image = pygame.transform.scale(load_image('chest_open.png', -1), (45, 40))
aim_image = pygame.transform.scale(load_image('aim.png'), (45, 45))
aim2_image = pygame.transform.scale(load_image('aim2.png', -1), (30, 30))
start_button_image = pygame.transform.scale(load_image('start.png'), (600, 300))


def end_screen():
    pass
    global fon
    fon = pygame.transform.scale(load_image('end_screen.jpg'), (800, 600))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pass
        pygame.display.flip()
        clock.tick(120)


def start_screen():
    global fon
    start_group = pygame.sprite.Group()
    screen.fill((0, 0, 0))
    start_button = pygame.sprite.Sprite(start_group)
    start_button.image = start_button_image
    start_button.rect = start_button.image.get_rect()
    start_button.rect.x = 100
    start_button.rect.y = 100

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                y, x = pygame.mouse.get_pos()
                if event.button == 1 and (100 < x < 400) and (100 < y < 700):
                    return
        start_group.draw(screen)
        pygame.display.flip()
        clock.tick(120)


def ui():
    font = pygame.font.SysFont('arial', 18)
    text = font.render('Hp: ' + str(board.player_hp), 1, (100, 255, 100))
    text_x = 0
    text_y = 50 // 2 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))

    text = font.render('Money: ' + str(board.cash), 1, (253, 233, 16))
    text_x = 70
    text_y = 50 // 2 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))


def update_screen():
    if not board.generation:
        global player, cursor
        player.image = player_image
        player.update()
        if not enemies_group:
            board.turn = 'player'
        if board.turn == 'enemy':
            for enemy in enemies_group:
                enemy.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        camera.update(player)
        all_sprites.add(aim)
        ui()

        for sprite in all_sprites:
            if sprite not in aim_group:
                camera.apply(sprite)

        pygame.display.flip()
    else:
        pygame.time.delay(75)
        board.generation = False


class Board:
    def __init__(self):
        self.board = []
        self.player = ()
        self.load()
        self.generate()
        self.generation = False
        self.vis = [[False for _ in range(32)] for _ in range(32)]
        self.used = []
        self.turn = 'player'
        self.player_hp = 100
        with open('data/money.txt') as f:
            self.cash = int(f.read())

    def load(self):
        lev = load_level(title)
        for el in lev:
            self.board.append(list(el))
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == '/':
                    self.board[i][j] = 2
                elif self.board[i][j] == '#':
                    self.board[i][j] = 3
                elif self.board[i][j] in ['.', '@']:
                    self.board[i][j] = 0

    def generate(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    z = [self.board[i - 1][j], self.board[i][j - 1], self.board[i - 1][j - 1], self.board[i - 1][j + 1],
                         self.board[i + 1][j - 1], self.board[i + 1][j + 1], self.board[i + 1][j], self.board[i][j + 1]]
                    if 3 in z and choice([1, 2]) == 1:
                        self.board[i][j] = 1
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 3:
                    self.board[i][j] = 1
        for _ in range(3):
            r1, r2 = randint(1, 31), randint(1, 31)
            while self.board[r1][r2] != 0:
                r1, r2 = randint(1, 31), randint(1, 31)
            self.board[r1][r2] = 6
        for _ in range(7):
            r1, r2 = randint(1, 31), randint(1, 31)
            while self.board[r1][r2] != 0:
                r1, r2 = randint(1, 31), randint(1, 31)
            self.board[r1][r2] = 7
        r1, r2 = randint(1, 31), randint(1, 31)
        while self.board[r1][r2] != 0:
            r1, r2 = randint(1, 31), randint(1, 31)
        self.board[r1][r2] = 5
        self.player = (r1, r2)

    def generate_level(self):
        self.generation = True
        self.used = []
        self.vision(self.player[0], self.player[1])
        new_player, x, y = None, None, None
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if not self.vis[y][x]:
                    continue
                if self.board[y][x] in [0, 5, 7]:
                    Tile('empty', x, y)
                elif self.board[y][x] == 6:
                    Tile('empty', x, y)
                    Chest(x, y, 'close')
                elif self.board[y][x] == 8:
                    Tile('empty', x, y)
                    Chest(x, y, 'open')
                elif self.board[y][x] == 1:
                    Wall('wall', x, y)
                elif self.board[y][x] == 2:
                    IndestructibleWall('indestructible_wall', x, y)
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if not self.vis[y][x]:
                    continue
                if self.board[y][x] == 7:
                    Enemy(x, y)
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == 5:
                    new_player = Player(x, y)
        all_sprites.remove(aim)
        all_sprites.add(aim)
        return new_player

    def vision(self, x, y):
        self.vis[x][y] = True
        self.used.append((x, y))
        if self.board[x][y + 1] in [0, 6, 7, 8] and (x, y + 1) not in self.used:
            self.vision(x, y + 1)
        if self.board[x][y + 1] not in [0, 6, 7, 8] and (x, y + 1) not in self.used:
            self.vis[x][y + 1] = True
            self.used.append((x, y + 1))
        if self.board[x][y - 1] in [0, 6, 7, 8] and (x, y - 1) not in self.used:
            self.vision(x, y - 1)
        if self.board[x][y - 1] not in [0, 6, 7, 8] and (x, y - 1) not in self.used:
            self.vis[x][y - 1] = True
            self.used.append((x, y - 1))
        if self.board[x + 1][y] in [0, 6, 7, 8] and (x + 1, y) not in self.used:
            self.vision(x + 1, y)
        if self.board[x + 1][y] not in [0, 6, 7, 8] and (x + 1, y) not in self.used:
            self.vis[x + 1][y] = True
            self.used.append((x + 1, y))
        if self.board[x - 1][y] in [0, 6, 7, 8] and (x - 1, y) not in self.used:
            self.vision(x - 1, y)
        if self.board[x - 1][y] not in [0, 6, 7, 8] and (x - 1, y) not in self.used:
            self.vis[x - 1][y] = True
            self.used.append((x - 1, y))

    def move(self, way):
        flag = True
        for chest in chests_group:
            if chest.x == self.player[1] and chest.y == self.player[0]:
                flag = False
                self.board[self.player[0]][self.player[1]] = 8
                break
        if flag:
            self.board[self.player[0]][self.player[1]] = 0
        if way == 'up' and self.board[self.player[0] - 1][self.player[1]] in [0, 6, 8]:
            self.player = (self.player[0] - 1, self.player[1])
        elif way == 'down' and self.board[self.player[0] + 1][self.player[1]] in [0, 6, 8]:
            self.player = (self.player[0] + 1, self.player[1])
        elif way == 'left' and self.board[self.player[0]][self.player[1] - 1] in [0, 6, 8]:
            self.player = (self.player[0], self.player[1] - 1)
        elif way == 'right' and self.board[self.player[0]][self.player[1] + 1] in [0, 6, 8]:
            self.player = (self.player[0], self.player[1] + 1)
        else:
            self.board[self.player[0]][self.player[1]] = 5
            return False
        self.board[self.player[0]][self.player[1]] = 5
        return True


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - 550 // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - 550 // 2)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(walls_group, all_sprites)
        self.image = tile_images[tile_type]
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class IndestructibleWall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(indestructible_walls_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Cursor(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.rect = pos

    def update(self, *args):
        global player, cursor
        a0 = pygame.sprite.spritecollideany(cursor, aim_group)
        a = pygame.sprite.spritecollideany(cursor, enemies_group)
        a1 = pygame.sprite.spritecollideany(cursor, walls_group)
        if a0:
            if cursor.image == aim2_image:
                cursor.image = pygame.transform.scale(load_image("cursor.png", -1), (20, 21))
            else:
                cursor.image = aim2_image
        elif a:
            a2 = [board.board[a.y - 1][a.x], board.board[a.y][a.x - 1], board.board[a.y + 1][a.x],
                  board.board[a.y][a.x + 1]]
            if cursor.image == aim2_image:
                a2.extend([board.board[a.y - 2][a.x], board.board[a.y][a.x - 2], board.board[a.y + 2][a.x],
                           board.board[a.y][a.x + 2], board.board[a.y + 1][a.x + 1], board.board[a.y + 1][a.x - 1],
                           board.board[a.y - 1][a.x + 1], board.board[a.y - 1][a.x - 1]])
            if 5 not in a2:
                return
            a.get_hit()
            if a.hp <= 0:
                board.cash += randint(0, 2)
                with open('data/money.txt', 'w') as f:
                    f.write(str(board.cash))
                board.board[a.y][a.x] = 0
                all_sprites.remove(a)
                enemies_group.remove(a)
            cursor.image = pygame.transform.scale(load_image("cursor.png", -1), (20, 21))
            board.turn = 'enemy'
        elif a1:
            board.board[a1.y][a1.x] = 0
            all_sprites.empty()
            walls_group.empty()
            indestructible_walls_group.empty()
            tiles_group.empty()
            enemies_group.empty()
            player = board.generate_level()
            cursor = Cursor(pygame.mouse.get_pos)
            cursor.image = pygame.transform.scale(load_image("cursor.png", -1), (20, 21))
            cursor.rect = cursor.image.get_rect()
            board.turn = 'enemy'


class Chest(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, status):
        super().__init__(all_sprites, chests_group)
        self.x = pos_x
        self.y = pos_y
        self.status = status
        if status == 'open':
            self.image = opened_chest_image
        else:
            self.image = closed_chest_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 2, tile_height * pos_y + 8)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, enemies_group)
        self.x = pos_x
        self.y = pos_y
        self.damage = (8, 12)
        self.hp = 50
        self.image = enemy_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 2, tile_height * pos_y + 2)

    def move(self):
        try:
            a = [board.board[self.y][self.x + 1], board.board[self.y][self.x + 2], board.board[self.y][self.x + 3]]
            if 5 in a and (1 not in a or a.index(5) < a.index(1)):
                board.board[self.y][self.x] = 0
                self.x += 1
                self.rect.x += 50
                board.board[self.y][self.x] = 7
                return
        except IndexError:
            pass
        try:
            a = [board.board[self.y][self.x - 1], board.board[self.y][self.x - 2], board.board[self.y][self.x - 3]]
            if 5 in a and (1 not in a or a.index(5) < a.index(1)):
                board.board[self.y][self.x] = 0
                self.x -= 1
                self.rect.x -= 50
                board.board[self.y][self.x] = 7
                return
        except IndexError:
            pass
        try:
            a = [board.board[self.y + 1][self.x], board.board[self.y + 2][self.x], board.board[self.y + 3][self.x]]
            if 5 in a and (1 not in a or a.index(5) < a.index(1)):
                board.board[self.y][self.x] = 0
                self.y += 1
                self.rect.y += 50
                board.board[self.y][self.x] = 7
                return
        except IndexError:
            pass
        try:
            a = [board.board[self.y - 1][self.x], board.board[self.y - 2][self.x], board.board[self.y - 3][self.x]]
            if 5 in a and (1 not in a or a.index(5) < a.index(1)):
                board.board[self.y][self.x] = 0
                self.y -= 1
                self.rect.y -= 50
                board.board[self.y][self.x] = 7
                return
        except IndexError:
            pass

        if board.board[self.y - 1][self.x - 1] == 5:
            if board.board[self.y - 1][self.x] != 1:
                board.board[self.y][self.x] = 0
                self.y -= 1
                self.rect.y -= 50
                board.board[self.y][self.x] = 7
                return
            if board.board[self.y][self.x - 1] != 1:
                board.board[self.y][self.x] = 0
                self.x -= 1
                self.rect.x -= 50
                board.board[self.y][self.x] = 7
                return

        if board.board[self.y - 1][self.x + 1] == 5:
            if board.board[self.y - 1][self.x] != 1:
                board.board[self.y][self.x] = 0
                self.y -= 1
                self.rect.y -= 50
                board.board[self.y][self.x] = 7
                return
            if board.board[self.y][self.x + 1] != 1:
                board.board[self.y][self.x] = 0
                self.x += 1
                self.rect.x += 50
                board.board[self.y][self.x] = 7
                return

        if board.board[self.y + 1][self.x - 1] == 5:
            if board.board[self.y + 1][self.x] != 1:
                board.board[self.y][self.x] = 0
                self.y += 1
                self.rect.y += 50
                board.board[self.y][self.x] = 7
                return
            if board.board[self.y][self.x - 1] != 1:
                board.board[self.y][self.x] = 0
                self.x -= 1
                self.rect.x -= 50
                board.board[self.y][self.x] = 7
                return
        if board.board[self.y + 1][self.x + 1] == 5:
            if board.board[self.y + 1][self.x] != 1:
                board.board[self.y][self.x] = 0
                self.y += 1
                self.rect.y += 50
                board.board[self.y][self.x] = 7
                return
            if board.board[self.y][self.x + 1] != 1:
                board.board[self.y][self.x] = 0
                self.x += 1
                self.rect.x += 50
                board.board[self.y][self.x] = 7
                return

        n1 = [1, 2, 3, 4]
        for _ in range(4):
            n = choice(n1)
            if n == 1:
                if board.board[self.y - 1][self.x] == 0:
                    board.board[self.y][self.x] = 0
                    self.y -= 1
                    self.rect.y -= 50
                    board.board[self.y][self.x] = 7
                    break
                else:
                    n1.remove(1)
            if n == 2:
                if board.board[self.y + 1][self.x] == 0:
                    board.board[self.y][self.x] = 0
                    self.y += 1
                    self.rect.y += 50
                    board.board[self.y][self.x] = 7
                    break
                else:
                    n1.remove(2)
            if n == 3:
                if board.board[self.y][self.x - 1] == 0:
                    board.board[self.y][self.x] = 0
                    self.x -= 1
                    self.rect.x -= 50
                    board.board[self.y][self.x] = 7
                    break
                else:
                    n1.remove(3)
            if n == 4:
                if board.board[self.y][self.x + 1] == 0:
                    board.board[self.y][self.x] = 0
                    self.x += 1
                    self.rect.x += 50
                    board.board[self.y][self.x] = 7
                    break
                else:
                    n1.remove(4)

    def attack(self):
        player.hp -= randint(self.damage[0], self.damage[1])
        board.player_hp = player.hp
        return

    def get_hit(self):
        self.hp -= randint(player.damage[0], player.damage[1])

    def update(self, *args):
        if (self.x + 1 == board.player[1] and self.y == board.player[0]) or (
                self.x - 1 == board.player[1] and self.y == board.player[0]) or (
                self.x == board.player[1] and self.y - 1 == board.player[0]) or (
                self.x == board.player[1] and self.y + 1 == board.player[0]):
            self.attack()
        else:
            self.move()
        board.turn = 'player'


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, x=False, y=False):
        super().__init__(all_sprites)
        self.image = player_image
        self.damage = (10, 13)
        self.hp = board.player_hp
        if not (x and y):
            self.rect = self.image.get_rect().move(tile_width * pos_x + 2, tile_height * pos_y - 2)
        else:
            self.rect = self.image.get_rect().move(x, y)

    def update(self, *args):
        a = pygame.sprite.spritecollideany(player, chests_group)
        if a and a.status != 'open':
            a.status = 'open'
            board.board[a.y][a.x] = 8
            a.image = opened_chest_image

        if self.hp <= 0:
            end_screen()
        global player_image, k, r, pressed, count
        if count != 0 or (pressed and board.move(pressed)):
            k += 1
            if k > 60:
                k = 1
            if k <= 20:
                r = 1
            elif k <= 40:
                r = 2
            else:
                r = 3
            if pressed == 'down':
                player_image = pygame.transform.scale(load_image('down' + str(r) + '.png', -1), (45, 55))
            elif pressed == 'up':
                player_image = pygame.transform.scale(load_image('up' + str(r) + '.png', -1), (45, 55))
            elif pressed == 'left':
                player_image = pygame.transform.scale(load_image('left' + str(r) + '.png', -1), (45, 55))
            elif pressed == 'right':
                player_image = pygame.transform.scale(load_image('right' + str(r) + '.png', -1), (45, 55))
            if pressed == 'up':
                self.rect.y -= 1
                cursor.rect.y -= 1
            elif pressed == 'down':
                self.rect.y += 1
                cursor.rect.y += 1
            elif pressed == 'right':
                self.rect.x += 1
                cursor.rect.x += 1
            elif pressed == 'left':
                self.rect.x -= 1
                cursor.rect.x -= 1
            count += 1
        else:
            count = 50
        if count == 50:
            if pressed == 'down':
                player_image = pygame.transform.scale(load_image('down1.png', -1), (45, 55))
            elif pressed == 'up':
                player_image = pygame.transform.scale(load_image('up1.png', -1), (45, 55))
            elif pressed == 'left':
                player_image = pygame.transform.scale(load_image('left1.png', -1), (45, 55))
            elif pressed == 'right':
                player_image = pygame.transform.scale(load_image('right1.png', -1), (45, 55))
            if pressed:
                board.turn = 'enemy'
            pressed = ''
            count = 0


start_screen()
board = Board()
aim = pygame.sprite.Sprite(all_sprites, aim_group)
aim.image = aim_image
aim.rect = aim.image.get_rect()
aim.rect.x = 0
aim.rect.y = 100
player = board.generate_level()
camera = Camera()
cursor = Cursor(pygame.mouse.get_pos)
cursor.image = pygame.transform.scale(load_image("cursor.png", -1), (20, 21))
cursor.rect = cursor.image.get_rect()
pygame.mouse.set_visible(False)
running = True
pressed = ''
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_focused():
                cursor.rect.x = event.pos[0]
                cursor.rect.y = event.pos[1]
        if not pressed:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pressed = 'right'
                if event.key == pygame.K_LEFT:
                    pressed = 'left'
                if event.key == pygame.K_UP:
                    pressed = 'up'
                if event.key == pygame.K_DOWN:
                    pressed = 'down'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cursor.update()
    clock.tick(120)
    update_screen()
