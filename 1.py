import pygame, sys, os, sqlite3
from random import choice, randint


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


def end_screen():
    global base, player_hp
    pygame.mouse.set_visible(True)
    restart_group = pygame.sprite.Group()
    base.screen.fill((0, 0, 0))
    restart_button = pygame.sprite.Sprite(restart_group)
    restart_button.image = restart_button_image
    restart_button.rect = restart_button.image.get_rect()
    restart_button.rect.x = 250
    restart_button.rect.y = 475
    base.fon = pygame.transform.scale(load_image('end_screen.jpg'), (800, 600))
    base.screen.blit(base.fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if event.button == 1 and (250 < x < 550) and (475 < y < 625):
                    player_hp = 100
                    base = Base(1)
                    base.b()
                    return
        restart_group.draw(base.screen)
        pygame.display.flip()
        base.clock.tick(120)


def start_screen():
    start_group = pygame.sprite.Group()
    base.screen.fill((0, 0, 0))
    start_button = pygame.sprite.Sprite(start_group)
    start_button.image = start_button_image
    start_button.rect = start_button.image.get_rect()
    start_button.rect.x = 100
    start_button.rect.y = 100
    shop_button = pygame.sprite.Sprite(start_group)
    shop_button.image = shop_button_image
    shop_button.rect = shop_button.image.get_rect()
    shop_button.rect.x = 315
    shop_button.rect.y = 400

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(x, y)
                if event.button == 1 and (135 < y < 366) and (132 < x < 668):
                    return
                elif event.button == 1 and (399 < y < 501) and (314 < x < 515):
                    shop()
        start_group.draw(base.screen)
        pygame.display.flip()
        base.clock.tick(120)


def shop():
    sold_out1 = False
    sold_out2 = False
    sold_out3 = False
    base.screen.fill((0, 0, 0))
    base.screen.blit(shop_background, (0, 0))
    long_range_weapon, short_range_weapon, armor = e_model.on_sale()
    goods_group = pygame.sprite.Group()

    long_range_weapon_sprite = pygame.sprite.Sprite(goods_group)
    long_range_weapon_sprite.image = pygame.transform.scale(load_image(long_range_weapon[3]), (100, 100))
    long_range_weapon_sprite.rect = long_range_weapon_sprite.image.get_rect()
    long_range_weapon_sprite.rect.y = 250
    long_range_weapon_sprite.rect.x = 150

    short_range_weapon_sprite = pygame.sprite.Sprite(goods_group)
    short_range_weapon_sprite.image = pygame.transform.scale(load_image(short_range_weapon[3]), (100, 100))
    short_range_weapon_sprite.rect = short_range_weapon_sprite.image.get_rect()
    short_range_weapon_sprite.rect.y = 250
    short_range_weapon_sprite.rect.x = 350

    armor_sprite = pygame.sprite.Sprite(goods_group)
    armor_sprite.image = pygame.transform.scale(load_image(armor[3]), (100, 100))
    armor_sprite.rect = armor_sprite.image.get_rect()
    armor_sprite.rect.y = 250
    armor_sprite.rect.x = 550

    font = pygame.font.SysFont('arial', 24)
    text = font.render('Cost: ' + str(long_range_weapon[7]), 1, (0, 0, 0))
    text_x = 162
    text_y = 750 // 2 - text.get_height() // 2
    base.screen.blit(text, (text_x, text_y))

    text = font.render('Cost: ' + str(short_range_weapon[7]), 1, (0, 0, 0))
    text_x = 365
    text_y = 750 // 2 - text.get_height() // 2
    base.screen.blit(text, (text_x, text_y))

    text = font.render('Cost: ' + str(armor[7]), 1, (0, 0, 0))
    text_x = 562
    text_y = 750 // 2 - text.get_height() // 2
    base.screen.blit(text, (text_x, text_y))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(x, y)

                if event.button == 1 and (249 < y < 351) and (149 < x < 351) and not sold_out1:
                    with open('data/money.txt') as f:
                        cash = int(f.read())
                    if cash >= long_range_weapon[-2]:
                        sold_out1 = not sold_out1
                        sold_out = pygame.sprite.Sprite(goods_group)
                        sold_out.image = sold_out_sprite
                        sold_out.rect = sold_out.image.get_rect()
                        sold_out.rect.y = 250
                        sold_out.rect.x = 150
                        e_model.purchase('long-range', long_range_weapon[0])
                        with open('data/money.txt', 'w') as f:
                            f.write(str(cash - long_range_weapon[7]))

                elif event.button == 1 and (249 < y < 351) and (349 < x < 451) and not sold_out2:
                    with open('data/money.txt') as f:
                        cash = int(f.read())
                    if cash >= short_range_weapon[-2]:
                        sold_out2 = not sold_out2
                        sold_out = pygame.sprite.Sprite(goods_group)
                        sold_out.image = sold_out_sprite
                        sold_out.rect = sold_out.image.get_rect()
                        sold_out.rect.y = 250
                        sold_out.rect.x = 150
                        e_model.purchase('short-range', short_range_weapon[0])
                        with open('data/money.txt', 'w') as f:
                            f.write(str(cash - short_range_weapon[7]))

                elif event.button == 1 and (249 < y < 351) and (549 < x < 651) and not sold_out3:
                    with open('data/money.txt') as f:
                        cash = int(f.read())
                    if cash >= armor[-2]:
                        sold_out3 = not sold_out3
                        sold_out = pygame.sprite.Sprite(goods_group)
                        sold_out.image = sold_out_sprite
                        sold_out.rect = sold_out.image.get_rect()
                        sold_out.rect.y = 250
                        sold_out.rect.x = 150
                        e_model.purchase('armor', armor[0])
                        with open('data/money.txt', 'w') as f:
                            f.write(str(cash - armor[7]))
        goods_group.draw(base.screen)
        pygame.display.flip()
        base.clock.tick(120)


def ui():
    font = pygame.font.SysFont('arial', 18)
    text = font.render('Hp: ' + str(base.board.player_hp), 1, (100, 255, 100))
    text_x = 0
    text_y = 50 // 2 - text.get_height() // 2
    base.screen.blit(text, (text_x, text_y))

    text = font.render('Money: ' + str(base.board.cash), 1, (253, 233, 16))
    text_x = 70
    text_y = 50 // 2 - text.get_height() // 2
    base.screen.blit(text, (text_x, text_y))

    text = font.render('Level: ' + str(base.level), 1, (255, 77, 0))
    text_x = 700
    text_y = 50 // 2 - text.get_height() // 2
    base.screen.blit(text, (text_x, text_y))


def update_screen():
    if not base.board.generation:
        base.player.image = player_image
        base.player.update()
        base.portal_group.update()
        if not base.enemies_group:
            base.board.turn = 'player'
        if base.board.turn == 'enemy':
            for enemy in base.enemies_group:
                enemy.update()
        base.screen.fill((0, 0, 0))
        base.all_sprites.draw(base.screen)
        base.camera.update(base.player)
        base.all_sprites.add(base.aim)
        ui()

        for sprite in base.all_sprites:
            if sprite not in base.aim_group:
                base.camera.apply(sprite)

        pygame.display.flip()
    else:
        pygame.time.delay(75)
        base.board.generation = False


class EventsModel:
    def __init__(self):
        self.conn = sqlite3.connect('data/items.db')
        self.cursor = self.conn.cursor()

    def on_sale(self):
        result = []
        for elem in ['long-range', 'short-range', 'armor']:
            result.append(self.cursor.execute("""SELECT * FROM items
             WHERE queue = ? and type=?""", (1, elem)).fetchone())
        return result

    def purchase(self, type, i):
        res = self.cursor.execute("SELECT * FROM items WHERE type = ? and queue<>?", (type, 0)).fetchall()
        for elem in res:
            self.cursor.execute("UPDATE items SET queue=? WHERE id=?", (elem[-1] - 1, elem[0]))
        self.cursor.execute("UPDATE items SET unlocked=? WHERE id=?", ('True', i))
        # self.conn.commit()


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
        lev = load_level(base.title)
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
        r1, r2 = randint(1, 31), randint(1, 31)
        while self.board[r1][r2] != 0:
            r1, r2 = randint(1, 31), randint(1, 31)
        self.board[r1][r2] = 10
        print(r1, r2)
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
                if self.board[y][x] in [0, 5, 7, 10]:
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
                elif self.board[y][x] == 10:
                    print(x, y)
                    Portal(x, y)
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == 5:
                    new_player = Player(x, y)
        base.all_sprites.remove(base.aim)
        base.all_sprites.add(base.aim)
        return new_player

    def vision(self, x, y):
        self.vis[x][y] = True
        self.used.append((x, y))
        if self.board[x][y + 1] in [0, 6, 7, 8, 10] and (x, y + 1) not in self.used:
            self.vision(x, y + 1)
        if self.board[x][y + 1] not in [0, 6, 7, 8, 10] and (x, y + 1) not in self.used:
            self.vis[x][y + 1] = True
            self.used.append((x, y + 1))
        if self.board[x][y - 1] in [0, 6, 7, 8, 10] and (x, y - 1) not in self.used:
            self.vision(x, y - 1)
        if self.board[x][y - 1] not in [0, 6, 7, 8, 10] and (x, y - 1) not in self.used:
            self.vis[x][y - 1] = True
            self.used.append((x, y - 1))
        if self.board[x + 1][y] in [0, 6, 7, 8, 10] and (x + 1, y) not in self.used:
            self.vision(x + 1, y)
        if self.board[x + 1][y] not in [0, 6, 7, 8, 10] and (x + 1, y) not in self.used:
            self.vis[x + 1][y] = True
            self.used.append((x + 1, y))
        if self.board[x - 1][y] in [0, 6, 7, 8, 10] and (x - 1, y) not in self.used:
            self.vision(x - 1, y)
        if self.board[x - 1][y] not in [0, 6, 7, 8, 10] and (x - 1, y) not in self.used:
            self.vis[x - 1][y] = True
            self.used.append((x - 1, y))

    def move(self, way):
        flag = True
        for chest in base.chests_group:
            if chest.x == self.player[1] and chest.y == self.player[0]:
                flag = False
                self.board[self.player[0]][self.player[1]] = 8
                break
        if flag:
            self.board[self.player[0]][self.player[1]] = 0
        if way == 'up' and self.board[self.player[0] - 1][self.player[1]] in [0, 6, 8, 10]:
            self.player = (self.player[0] - 1, self.player[1])
        elif way == 'down' and self.board[self.player[0] + 1][self.player[1]] in [0, 6, 8, 10]:
            self.player = (self.player[0] + 1, self.player[1])
        elif way == 'left' and self.board[self.player[0]][self.player[1] - 1] in [0, 6, 8, 10]:
            self.player = (self.player[0], self.player[1] - 1)
        elif way == 'right' and self.board[self.player[0]][self.player[1] + 1] in [0, 6, 8, 10]:
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
        super().__init__(base.tiles_group, base.all_sprites)
        self.image = tile_images[tile_type + str(base.level)]
        self.rect = self.image.get_rect().move(base.tile_width * pos_x, base.tile_height * pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(base.walls_group, base.all_sprites)
        self.image = tile_images[tile_type + str(base.level)]
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(base.tile_width * pos_x, base.tile_height * pos_y)


class IndestructibleWall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(base.indestructible_walls_group, base.all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(base.tile_width * pos_x, base.tile_height * pos_y)


class Portal(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(base.portal_group, base.all_sprites)
        self.image = portal_image1
        self.rect = self.image.get_rect().move(base.tile_width * pos_x + 8, base.tile_height * pos_y + 3)

    def update(self, *args):
        base.portal_animation += 1
        if base.portal_animation > 80:
            base.portal_animation = 1
        if base.portal_animation <= 20:
            self.image = portal_image1
        elif base.portal_animation <= 40:
            self.image = portal_image2
        elif base.portal_animation <= 60:
            self.image = portal_image3
        else:
            self.image = portal_image4


class Cursor(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(base.all_sprites)
        self.rect = pos

    def update(self, *args):
        a0 = pygame.sprite.spritecollideany(base.cursor, base.aim_group)
        a = pygame.sprite.spritecollideany(base.cursor, base.enemies_group)
        a1 = pygame.sprite.spritecollideany(base.cursor, base.walls_group)
        if a0:
            if base.cursor.image == aim2_image:
                base.cursor.image = pygame.transform.scale(load_image("cursor.png", -1), (20, 21))
            else:
                base.cursor.image = aim2_image
        elif a:
            a2 = [base.board.board[a.y - 1][a.x], base.board.board[a.y][a.x - 1], base.board.board[a.y + 1][a.x],
                  base.board.board[a.y][a.x + 1]]
            try:
                if base.cursor.image == aim2_image:
                    a2.extend(
                        [base.board.board[a.y - 2][a.x], base.board.board[a.y][a.x - 2], base.board.board[a.y + 2][a.x],
                         base.board.board[a.y][a.x + 2], base.board.board[a.y + 1][a.x + 1],
                         base.board.board[a.y + 1][a.x - 1], base.board.board[a.y - 1][a.x + 1],
                         base.board.board[a.y - 1][a.x - 1]])
            except IndexError:
                pass
            if 5 not in a2:
                return
            a.get_hit()
            if a.hp <= 0:
                base.board.cash += randint(0, 2 * base.level)
                with open('data/money.txt', 'w') as f:
                    f.write(str(base.board.cash))
                base.board.board[a.y][a.x] = 0
                base.all_sprites.remove(a)
                base.enemies_group.remove(a)
            base.cursor.image = pygame.transform.scale(load_image("cursor.png", -1), (20, 21))
            base.board.turn = 'enemy'
        elif a1:
            base.board.board[a1.y][a1.x] = 0
            base.all_sprites.empty()
            base.walls_group.empty()
            base.indestructible_walls_group.empty()
            base.tiles_group.empty()
            base.enemies_group.empty()
            base.player = base.board.generate_level()
            base.cursor = Cursor(pygame.mouse.get_pos)
            base.cursor.image = pygame.transform.scale(load_image("cursor.png", -1), (20, 21))
            base.cursor.rect = base.cursor.image.get_rect()
            base.board.turn = 'enemy'


class Chest(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, status):
        super().__init__(base.all_sprites, base.chests_group)
        self.x = pos_x
        self.y = pos_y
        self.status = status
        if status == 'open':
            self.image = opened_chest_image
        else:
            self.image = closed_chest_image
        self.rect = self.image.get_rect().move(base.tile_width * pos_x + 2, base.tile_height * pos_y + 8)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, boss=False):
        super().__init__(base.all_sprites, base.enemies_group)
        self.x = pos_x
        self.y = pos_y
        if boss:
            self.damage = (20, 25)
            self.hp = 300
            self.image = boss_image
        else:
            self.damage = (7 + 1 * base.level, 11 + 1 * base.level)
            self.hp = 10 + 20 * base.level
            self.image = enemy_image
        self.rect = self.image.get_rect().move(base.tile_width * pos_x + 2, base.tile_height * pos_y + 2)

    def move(self):
        try:
            a = [base.board.board[self.y][self.x + 1], base.board.board[self.y][self.x + 2],
                 base.board.board[self.y][self.x + 3]]
            if 5 in a and (1 not in a or a.index(5) < a.index(1)):
                base.board.board[self.y][self.x] = 0
                self.x += 1
                self.rect.x += 50
                base.board.board[self.y][self.x] = 7
                return
        except IndexError:
            pass
        try:
            a = [base.board.board[self.y][self.x - 1], base.board.board[self.y][self.x - 2],
                 base.board.board[self.y][self.x - 3]]
            if 5 in a and (1 not in a or a.index(5) < a.index(1)):
                base.board.board[self.y][self.x] = 0
                self.x -= 1
                self.rect.x -= 50
                base.board.board[self.y][self.x] = 7
                return
        except IndexError:
            pass
        try:
            a = [base.board.board[self.y + 1][self.x], base.board.board[self.y + 2][self.x],
                 base.board.board[self.y + 3][self.x]]
            if 5 in a and (1 not in a or a.index(5) < a.index(1)):
                base.board.board[self.y][self.x] = 0
                self.y += 1
                self.rect.y += 50
                base.board.board[self.y][self.x] = 7
                return
        except IndexError:
            pass
        try:
            a = [base.board.board[self.y - 1][self.x], base.board.board[self.y - 2][self.x],
                 base.board.board[self.y - 3][self.x]]
            if 5 in a and (1 not in a or a.index(5) < a.index(1)):
                base.board.board[self.y][self.x] = 0
                self.y -= 1
                self.rect.y -= 50
                base.board.board[self.y][self.x] = 7
                return
        except IndexError:
            pass

        if base.board.board[self.y - 1][self.x - 1] == 5:
            if base.board.board[self.y - 1][self.x] != 1:
                base.board.board[self.y][self.x] = 0
                self.y -= 1
                self.rect.y -= 50
                base.board.board[self.y][self.x] = 7
                return
            if base.board.board[self.y][self.x - 1] != 1:
                base.board.board[self.y][self.x] = 0
                self.x -= 1
                self.rect.x -= 50
                base.board.board[self.y][self.x] = 7
                return

        if base.board.board[self.y - 1][self.x + 1] == 5:
            if base.board.board[self.y - 1][self.x] != 1:
                base.board.board[self.y][self.x] = 0
                self.y -= 1
                self.rect.y -= 50
                base.board.board[self.y][self.x] = 7
                return
            if base.board.board[self.y][self.x + 1] != 1:
                base.board.board[self.y][self.x] = 0
                self.x += 1
                self.rect.x += 50
                base.board.board[self.y][self.x] = 7
                return

        if base.board.board[self.y + 1][self.x - 1] == 5:
            if base.board.board[self.y + 1][self.x] != 1:
                base.board.board[self.y][self.x] = 0
                self.y += 1
                self.rect.y += 50
                base.board.board[self.y][self.x] = 7
                return
            if base.board.board[self.y][self.x - 1] != 1:
                base.board.board[self.y][self.x] = 0
                self.x -= 1
                self.rect.x -= 50
                base.board.board[self.y][self.x] = 7
                return
        if base.board.board[self.y + 1][self.x + 1] == 5:
            if base.board.board[self.y + 1][self.x] != 1:
                base.board.board[self.y][self.x] = 0
                self.y += 1
                self.rect.y += 50
                base.board.board[self.y][self.x] = 7
                return
            if base.board.board[self.y][self.x + 1] != 1:
                base.board.board[self.y][self.x] = 0
                self.x += 1
                self.rect.x += 50
                base.board.board[self.y][self.x] = 7
                return

        n1 = [1, 2, 3, 4]
        for _ in range(4):
            n = choice(n1)
            if n == 1:
                if base.board.board[self.y - 1][self.x] == 0:
                    base.board.board[self.y][self.x] = 0
                    self.y -= 1
                    self.rect.y -= 50
                    base.board.board[self.y][self.x] = 7
                    break
                else:
                    n1.remove(1)
            if n == 2:
                if base.board.board[self.y + 1][self.x] == 0:
                    base.board.board[self.y][self.x] = 0
                    self.y += 1
                    self.rect.y += 50
                    base.board.board[self.y][self.x] = 7
                    break
                else:
                    n1.remove(2)
            if n == 3:
                if base.board.board[self.y][self.x - 1] == 0:
                    base.board.board[self.y][self.x] = 0
                    self.x -= 1
                    self.rect.x -= 50
                    base.board.board[self.y][self.x] = 7
                    break
                else:
                    n1.remove(3)
            if n == 4:
                if base.board.board[self.y][self.x + 1] == 0:
                    base.board.board[self.y][self.x] = 0
                    self.x += 1
                    self.rect.x += 50
                    base.board.board[self.y][self.x] = 7
                    break
                else:
                    n1.remove(4)

    def attack(self):
        base.player.hp -= randint(self.damage[0], self.damage[1])
        if base.player.hp < 0:
            base.player.hp = 0
        base.board.player_hp = base.player.hp
        return

    def get_hit(self):
        self.hp -= randint(base.player.damage[0], base.player.damage[1])

    def update(self, *args):
        if (self.x + 1 == base.board.player[1] and self.y == base.board.player[0]) or (
                self.x - 1 == base.board.player[1] and self.y == base.board.player[0]) or (
                self.x == base.board.player[1] and self.y - 1 == base.board.player[0]) or (
                self.x == base.board.player[1] and self.y + 1 == base.board.player[0]):
            self.attack()
        else:
            self.move()
        base.board.turn = 'player'


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, x=False, y=False):
        super().__init__(base.all_sprites)
        self.image = player_image
        self.damage = (10, 13)
        self.hp = base.board.player_hp
        if not (x and y):
            self.rect = self.image.get_rect().move(base.tile_width * pos_x + 2, base.tile_height * pos_y - 2)
        else:
            self.rect = self.image.get_rect().move(x, y)

    def update(self, *args):
        global base, player_hp
        a = pygame.sprite.spritecollideany(base.player, base.chests_group)
        if a and a.status != 'open':
            a.status = 'open'
            base.board.board[a.y][a.x] = 8
            a.image = opened_chest_image

        if pygame.sprite.spritecollideany(base.player, base.portal_group):
            player_hp = base.board.player_hp
            base = Base(base.level + 1)
            base.b()

        if self.hp <= 0:
            end_screen()
        global player_image
        if base.count != 0 or (base.pressed and base.board.move(base.pressed)):
            base.k += 1
            if base.k > 60:
                base.k = 1
            if base.k <= 20:
                base.r = 1
            elif base.k <= 40:
                base.r = 2
            else:
                base.r = 3
            if base.pressed == 'down':
                player_image = pygame.transform.scale(load_image('down' + str(base.r) + '.png', -1), (45, 55))
            elif base.pressed == 'up':
                player_image = pygame.transform.scale(load_image('up' + str(base.r) + '.png', -1), (45, 55))
            elif base.pressed == 'left':
                player_image = pygame.transform.scale(load_image('left' + str(base.r) + '.png', -1), (45, 55))
            elif base.pressed == 'right':
                player_image = pygame.transform.scale(load_image('right' + str(base.r) + '.png', -1), (45, 55))
            if base.pressed == 'up':
                self.rect.y -= 1
                base.cursor.rect.y -= 1
            elif base.pressed == 'down':
                self.rect.y += 1
                base.cursor.rect.y += 1
            elif base.pressed == 'right':
                self.rect.x += 1
                base.cursor.rect.x += 1
            elif base.pressed == 'left':
                self.rect.x -= 1
                base.cursor.rect.x -= 1
            base.count += 1
        else:
            base.count = 50
        if base.count == 50:
            if base.pressed == 'down':
                player_image = pygame.transform.scale(load_image('down1.png', -1), (45, 55))
            elif base.pressed == 'up':
                player_image = pygame.transform.scale(load_image('up1.png', -1), (45, 55))
            elif base.pressed == 'left':
                player_image = pygame.transform.scale(load_image('left1.png', -1), (45, 55))
            elif base.pressed == 'right':
                player_image = pygame.transform.scale(load_image('right1.png', -1), (45, 55))
            if base.pressed:
                base.board.turn = 'enemy'
            base.pressed = ''
            base.count = 0


class Base:
    def __init__(self, level):
        self.title = "map.txt"

        self.fon = None
        self.k = 0
        self.r = 0
        self.count = 0
        self.portal_animation = 0
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.screen.fill((0, 0, 0))
        pygame.display.flip()
        self.clock = pygame.time.Clock()
        self.player = None
        self.up, self.down, self.left, self.right = False, False, False, False
        self.all_sprites = pygame.sprite.Group()
        self.tiles_group = pygame.sprite.Group()
        self.walls_group = pygame.sprite.Group()
        self.chests_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.portal_group = pygame.sprite.Group()
        self.aim_group = pygame.sprite.Group()
        self.indestructible_walls_group = pygame.sprite.Group()
        self.tile_width = self.tile_height = 50
        self.level = level

    def b(self):
        self.board = Board()
        self.aim = pygame.sprite.Sprite(base.all_sprites, base.aim_group)
        self.aim.image = aim_image
        self.aim.rect = self.aim.image.get_rect()
        self.aim.rect.x = 0
        self.aim.rect.y = 100
        base.player = self.board.generate_level()
        self.camera = Camera()
        self.cursor = Cursor(pygame.mouse.get_pos)
        self.cursor.image = pygame.transform.scale(load_image("cursor.png", -1), (20, 21))
        self.cursor.rect = self.cursor.image.get_rect()
        pygame.mouse.set_visible(False)
        self.running = True
        self.pressed = ''
        self.board.player_hp = player_hp


e_model = EventsModel()
player_hp = 100
base = Base(1)

tile_images = {'empty1': pygame.transform.scale(load_image('empty1.png'), (50, 50)),
               'wall1': pygame.transform.scale(load_image('wall1.png'), (50, 50)),
               'empty2': pygame.transform.scale(load_image('empty2.png'), (50, 50)),
               'wall2': pygame.transform.scale(load_image('wall2.png'), (50, 50)),
               'empty3': pygame.transform.scale(load_image('empty3.png'), (50, 50)),
               'wall3': pygame.transform.scale(load_image('wall3.png'), (50, 50)),
               'empty4': pygame.transform.scale(load_image('empty4.png'), (50, 50)),
               'wall4': pygame.transform.scale(load_image('wall4.png'), (50, 50)),
               'empty5': pygame.transform.scale(load_image('empty5.png'), (50, 50)),
               'wall5': pygame.transform.scale(load_image('wall5.png'), (50, 50)),
               'indestructible_wall': pygame.transform.scale(load_image('indestructible_wall.png'), (50, 50))}
player_image = pygame.transform.scale(load_image('down1.png', -1), (45, 55))
enemy_image = pygame.transform.scale(load_image('enemy.png', -1), (50, 50))
boss_image = pygame.transform.scale(load_image('boss.png', -1), (50, 50))
closed_chest_image = pygame.transform.scale(load_image('chest_closed.png', -1), (45, 40))
opened_chest_image = pygame.transform.scale(load_image('chest_open.png', -1), (45, 40))
aim_image = pygame.transform.scale(load_image('aim.png'), (45, 45))
aim2_image = pygame.transform.scale(load_image('aim2.png', -1), (30, 30))
start_button_image = pygame.transform.scale(load_image('start.png'), (600, 300))
restart_button_image = pygame.transform.scale(load_image('restart_button.png', -1), (300, 150))
shop_button_image = pygame.transform.scale(load_image('shop.png'), (200, 100))
shop_background = pygame.transform.scale(load_image('shop_background.jpg'), (800, 600))
portal_image1 = pygame.transform.scale(load_image('portal1.png', -1), (35, 45))
portal_image2 = pygame.transform.scale(load_image('portal2.png', -1), (35, 45))
portal_image3 = pygame.transform.scale(load_image('portal3.png', -1), (35, 45))
portal_image4 = pygame.transform.scale(load_image('portal4.png', -1), (35, 45))
sold_out_sprite = pygame.transform.scale(load_image('sold_out.png', -1), (100, 100))

start_screen()
base.b()

while base.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_focused():
                base.cursor.rect.x = event.pos[0]
                base.cursor.rect.y = event.pos[1]
        if not base.pressed:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    base.pressed = 'right'
                if event.key == pygame.K_LEFT:
                    base.pressed = 'left'
                if event.key == pygame.K_UP:
                    base.pressed = 'up'
                if event.key == pygame.K_DOWN:
                    base.pressed = 'down'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    base.cursor.update()
    base.clock.tick(120)
    update_screen()
