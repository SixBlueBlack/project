import pygame, sys, os, sqlite3
from random import choice, randint


def load_image(name, colorkey=None):  # Загрузка картинок
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():  # Выход из программы
    pygame.quit()
    sys.exit()


def load_level(filename):  # Загрузка уровня из файла
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def end_screen(i=False):  # Экран при окончании игры
    global base, player_hp
    pygame.mouse.set_visible(True)
    restart_group = pygame.sprite.Group()
    base.screen.fill((0, 0, 0))
    restart_button = pygame.sprite.Sprite(restart_group)
    restart_button.image = restart_button_image
    restart_button.rect = restart_button.image.get_rect()
    restart_button.rect.x = 250
    restart_button.rect.y = 475
    if i:
        base.fon = pygame.transform.scale(load_image('the_end.jpg'), (800, 600))
    else:
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


def start_screen():  # Главное меню
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
                if event.button == 1 and (135 < y < 366) and (132 < x < 668):
                    return
                elif event.button == 1 and (399 < y < 501) and (314 < x < 515):
                    shop()
        start_group.draw(base.screen)
        pygame.display.flip()
        base.clock.tick(120)


def shop():  # Меню магазина
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    base.screen.fill((0, 0, 0))
                    return
        goods_group.draw(base.screen)
        pygame.display.flip()
        base.clock.tick(120)


def ui():  # Пользовательский интерфейс
    font = pygame.font.SysFont('arial', 18)
    text = font.render('Hp: ' + str(base.board.player_hp) + '/100', 1, (100, 255, 100))
    text_x = 0
    text_y = 50 // 2 - text.get_height() // 2
    base.screen.blit(text, (text_x, text_y))

    text = font.render('Money: ' + str(base.board.cash), 1, (253, 233, 16))
    text_x = 100
    text_y = 50 // 2 - text.get_height() // 2
    base.screen.blit(text, (text_x, text_y))

    text = font.render('Level: ' + str(base.level), 1, (255, 77, 0))
    text_x = 700
    text_y = 50 // 2 - text.get_height() // 2
    base.screen.blit(text, (text_x, text_y))

    text = font.render('X: ' + str(number_of_potions), 1, (255, 0, 0))
    text_x = 750
    text_y = 300 // 2 - text.get_height() // 2
    base.screen.blit(text, (text_x, text_y))

    text = font.render('Long-range weapon: ' + str(base.equipment.long_range[4]), 1, (255, 165, 0))
    text_x = 200
    text_y = 50 // 2 - text.get_height() // 2
    base.screen.blit(text, (text_x, text_y))

    text = font.render('Damage: ' + str(base.equipment.long_range[1]), 1, (255, 165, 0))
    text_x = 200
    text_y = 100 // 2 - text.get_height() // 2
    base.screen.blit(text, (text_x, text_y))

    text = font.render('Short-range weapon: ' + str(base.equipment.short_range[4]), 1, (0, 0, 255))
    text_x = 400
    text_y = 50 // 2 - text.get_height() // 2
    base.screen.blit(text, (text_x, text_y))

    text = font.render('Damage: ' + str(base.equipment.short_range[1]), 1, (0, 0, 255))
    text_x = 400
    text_y = 100 // 2 - text.get_height() // 2
    base.screen.blit(text, (text_x, text_y))

    if base.equipment.armor != 0:
        text = font.render('Armor: ' + str(base.equipment.armor[2]), 1, (174, 160, 75))
        text_x = 0
        text_y = 100 // 2 - text.get_height() // 2
        base.screen.blit(text, (text_x, text_y))

    if base.player.chest_ui:
        y, x = base.board.player
        if (x, y) not in base.drop:
            x -= 1
        if (x, y) not in base.drop:
            x += 2
        if (x, y) not in base.drop:
            x -= 1
            y -= 1
        if (x, y) not in base.drop:
            y += 2
        base.all_sprites.add(base.menu)
        if base.drop[(x, y)]:
            font = pygame.font.SysFont('arial', 18)
            text = font.render('Title: ' + str(base.drop[(x, y)][4]), 1, (255, 0, 0))
            text_x = 300
            text_y = 1050 // 2 - text.get_height() // 2
            base.screen.blit(text, (text_x, text_y))

            text = font.render('Equip?', 1, (255, 0, 0))
            text_x = 530
            text_y = 1160 // 2 - text.get_height() // 2
            base.screen.blit(text, (text_x, text_y))

            if base.drop[(x, y)][2] != 0:
                text = font.render('Armor: ' + str(base.drop[(x, y)][2]), 1, (255, 0, 0))
                text_x = 300
                text_y = 1100 // 2 - text.get_height() // 2
                base.screen.blit(text, (text_x, text_y))
            else:
                text = font.render('Damage: ' + str(base.drop[(x, y)][1]), 1, (255, 0, 0))
                text_x = 300
                text_y = 1100 // 2 - text.get_height() // 2
                base.screen.blit(text, (text_x, text_y))


def update_screen():  # Обновление экрана
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
        base.all_sprites.add(base.heal)
        ui()

        for sprite in base.all_sprites:
            if sprite not in base.aim_group and sprite not in base.menu_group and sprite not in base.heal_group:
                base.camera.apply(sprite)

        pygame.display.flip()
    else:
        pygame.time.delay(75)
        base.board.generation = False


class EventsModel:  # Класс для работы с базой данных
    def __init__(self):
        self.conn = sqlite3.connect('data/items.db')
        self.cursor = self.conn.cursor()

    def on_sale(self):  # Выбор продающихся товаров
        result = []
        for elem in ['long-range', 'short-range', 'armor']:
            result.append(self.cursor.execute("""SELECT * FROM items
             WHERE queue = ? and type=?""", (1, elem)).fetchone())
        return result

    def purchase(self, type, i):  # Покупка
        res = self.cursor.execute("SELECT * FROM items WHERE type = ? and queue<>?", (type, 0)).fetchall()
        for elem in res:
            self.cursor.execute("UPDATE items SET queue=? WHERE id=?", (elem[-1] - 1, elem[0]))
        self.cursor.execute("UPDATE items SET unlocked=? WHERE id=?", ('True', i))
        self.conn.commit()

    def possible_drop(self):  # Возможный дроп с сундука
        return self.cursor.execute("SELECT * FROM items WHERE unlocked=?", ('True',)).fetchall()

    def get_item(self, i):  # Получение предмета по id
        return self.cursor.execute("SELECT * FROM items WHERE id=?", (i,)).fetchone()


class Board:  # Класс для работы с пошаговой частью игры
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

    def load(self):  # Перевод уровня из текстового файла в матрицу
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

    def generate(self):  # Генерация уровня
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
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 3:
                    self.board[i][j] = 1
        for _ in range(3):
            r1, r2 = randint(1, 31), randint(1, 31)
            while self.board[r1][r2] != 0:
                r1, r2 = randint(1, 31), randint(1, 31)
            self.board[r1][r2] = 6
        for _ in range(14):
            r1, r2 = randint(1, 31), randint(1, 31)
            while self.board[r1][r2] != 0:
                r1, r2 = randint(1, 31), randint(1, 31)
            self.board[r1][r2] = 7
        r1, r2 = randint(1, 31), randint(1, 31)
        while self.board[r1][r2] != 0:
            r1, r2 = randint(1, 31), randint(1, 31)
        self.board[r1][r2] = 5
        self.player = (r1, r2)

    def generate_level(self):  # Графическое построение уровня
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
                    base.drop[(x, y)] = list(choice(base.possible_drop))
                    base.drop[(x, y)][3] = pygame.transform.scale(load_image(base.drop[(x, y)][3]), (80, 80))
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
                    Portal(x, y)
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == 5:
                    new_player = Player(x, y)
        base.all_sprites.remove(base.aim)
        base.all_sprites.remove(base.heal)
        base.all_sprites.add(base.aim)
        base.all_sprites.add(base.heal)
        return new_player

    def vision(self, x, y):  # Определение видимых клеток
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

    def move(self, way):  # Изменение координат персонажа в матрице
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


class Camera:  # Класс камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - 550 // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - 550 // 2)


class Tile(pygame.sprite.Sprite):  # Пустые клетки
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(base.tiles_group, base.all_sprites)
        self.image = tile_images[tile_type + str(base.level)]
        self.rect = self.image.get_rect().move(base.tile_width * pos_x, base.tile_height * pos_y)


class Wall(pygame.sprite.Sprite):  # Стены
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(base.walls_group, base.all_sprites)
        self.image = tile_images[tile_type + str(base.level)]
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(base.tile_width * pos_x, base.tile_height * pos_y)


class IndestructibleWall(pygame.sprite.Sprite):  # Неразрушимые стены
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(base.indestructible_walls_group, base.all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(base.tile_width * pos_x, base.tile_height * pos_y)


class Portal(pygame.sprite.Sprite):  # Порталы
    def __init__(self, pos_x, pos_y):
        super().__init__(base.portal_group, base.all_sprites)
        self.image = portal_image1
        self.rect = self.image.get_rect().move(base.tile_width * pos_x + 8, base.tile_height * pos_y + 3)

    def update(self, *args):  # Анимация портала
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


class Cursor(pygame.sprite.Sprite):  # Курсор
    def __init__(self, pos):
        super().__init__(base.all_sprites)
        self.rect = pos

    def update(self, *args):
        global number_of_potions
        a0 = pygame.sprite.spritecollideany(base.cursor,
                                            base.aim_group)  # Считывания нажатия на кнопку смены режима стрельбы
        a = pygame.sprite.spritecollideany(base.cursor, base.enemies_group)  # Считывания нажатия на врага
        a1 = pygame.sprite.spritecollideany(base.cursor, base.walls_group)  # Считывания нажатия на стену
        if pygame.sprite.spritecollideany(base.cursor, base.equip_group):  # Считывания нажатия на кнопку подтверждения
            y, x = base.board.player
            item = base.drop[(x, y)]
            if item:
                if item[5] == 'long-range':
                    base.drop[(x, y)] = ''
                    base.equipment.change_long_range_weapon(item)
                elif item[5] == 'short-range':
                    base.drop[(x, y)] = ''
                    base.equipment.change_short_range_weapon(item)
                elif item[5] == 'armor':
                    base.drop[(x, y)] = ''
                    base.equipment.change_armor(item)
        if pygame.sprite.spritecollideany(base.cursor, base.heal_group) and number_of_potions > 0:
            number_of_potions -= 1
            base.player.heal()
        elif a0:
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
            a.get_hit('long-range')
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


class Equipment:  # Экипировка
    def __init__(self, lr=7, sr=16, ar=0):
        self.long_range = e_model.get_item(lr)
        self.short_range = e_model.get_item(sr)
        if ar == 0:
            self.armor = 0
        else:
            self.armor = e_model.get_item(ar)

    def change_armor(self, armor):
        self.armor = armor

    def change_long_range_weapon(self, long_range):
        self.long_range = long_range

    def change_short_range_weapon(self, short_range):
        self.short_range = short_range


class Chest(pygame.sprite.Sprite):  # Сундуки
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


class Enemy(pygame.sprite.Sprite):  # Враги
    def __init__(self, pos_x, pos_y):
        super().__init__(base.all_sprites, base.enemies_group)
        self.x = pos_x
        self.y = pos_y
        self.damage = (7 + 1 * base.level, 11 + 1 * base.level)
        self.hp = 20 * base.level
        self.image = enemy_image
        self.rect = self.image.get_rect().move(base.tile_width * pos_x + 2, base.tile_height * pos_y + 2)

    def move(self):  # Передвижение
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

    def attack(self):  # Атака
        rand = randint(self.damage[0], self.damage[1])
        if base.equipment.armor != 0:
            if base.equipment.armor[2] > rand:
                rand = 0
            else:
                rand -= base.equipment.armor[2]
        base.player.hp -= rand
        if base.player.hp < 0:
            base.player.hp = 0
        base.board.player_hp = base.player.hp
        return

    def get_hit(self, type='short-range'):  # Получение урона
        if type == 'long-range':
            self.hp -= base.equipment.long_range[1]
        else:
            self.hp -= base.equipment.short_range[1]

    def update(self, *args):  # "ИИ"
        if (self.x + 1 == base.board.player[1] and self.y == base.board.player[0]) or (
                self.x - 1 == base.board.player[1] and self.y == base.board.player[0]) or (
                self.x == base.board.player[1] and self.y - 1 == base.board.player[0]) or (
                self.x == base.board.player[1] and self.y + 1 == base.board.player[0]):
            self.attack()
        else:
            self.move()
        base.board.turn = 'player'


class Player(pygame.sprite.Sprite):  # Игрок
    def __init__(self, pos_x, pos_y, x=False, y=False):
        super().__init__(base.all_sprites)
        self.chest_ui = False
        self.image = player_image
        self.hp = base.board.player_hp
        if not (x and y):
            self.rect = self.image.get_rect().move(base.tile_width * pos_x + 2, base.tile_height * pos_y - 2)
        else:
            self.rect = self.image.get_rect().move(x, y)

    def heal(self):  # Лечение
        self.hp += 50
        base.board.player_hp += 50
        if base.board.player_hp > 100:
            base.board.player_hp = 100
            self.hp = 100

    def update(self, *args):
        global base, player_hp, number_of_potions
        a = pygame.sprite.spritecollideany(base.player, base.chests_group)
        if a and a.status != 'open':
            a.status = 'open'
            base.board.board[a.y][a.x] = 8
            a.image = opened_chest_image
        if a:
            base.all_sprites.add(base.menu)
            if base.drop[(a.x, a.y)]:
                base.item_image.image = base.drop[(a.x, a.y)][3]
                base.item_image.rect = base.item_image.image.get_rect()
                base.item_image.rect.x = 210
                base.item_image.rect.y = 510
                self.chest_ui = True
                base.all_sprites.add(base.item_image)
                base.all_sprites.add(base.equip_button)
            else:
                base.all_sprites.remove(base.equip_button)
                base.all_sprites.remove(base.item_image)
            base.all_sprites.remove(base.cursor)
            base.all_sprites.add(base.cursor)
        elif base.menu in base.all_sprites:
            self.chest_ui = False
            base.all_sprites.remove(base.menu)
            base.all_sprites.remove(base.equip_button)
            base.all_sprites.remove(base.item_image)

        if pygame.sprite.spritecollideany(base.player, base.portal_group):
            if base.level == 5:
                end_screen(True)
            player_hp = base.board.player_hp
            number_of_potions += 1
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


class Base:  # Класс, содержащий все основные переменные(Нужен для перезапуска уровней и для уровневой системы)
    def __init__(self, level):
        self.title = "map.txt"

        self.fon = None
        self.drop = {}
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
        self.menu_group = pygame.sprite.Group()
        self.heal_group = pygame.sprite.Group()
        self.equip_group = pygame.sprite.Group()
        self.indestructible_walls_group = pygame.sprite.Group()
        self.tile_width = self.tile_height = 50
        self.level = level
        self.possible_drop = e_model.possible_drop()
        self.equipment = Equipment()
        self.item_image = pygame.sprite.Sprite(self.menu_group)
        self.item_title = ''
        self.item_damage = 0
        self.item_armor = 0

    def b(self):
        self.board = Board()
        self.aim = pygame.sprite.Sprite(base.all_sprites, base.aim_group)
        self.aim.image = aim_image
        self.aim.rect = self.aim.image.get_rect()
        self.aim.rect.x = 0
        self.aim.rect.y = 100

        self.heal = pygame.sprite.Sprite(base.all_sprites, base.heal_group)
        self.heal.image = healing_potion
        self.heal.rect = self.heal.image.get_rect()
        self.heal.rect.x = 700
        self.heal.rect.y = 100

        base.player = self.board.generate_level()
        self.camera = Camera()
        self.cursor = Cursor(pygame.mouse.get_pos)
        self.cursor.image = pygame.transform.scale(load_image("cursor.png", -1), (20, 21))
        self.cursor.rect = self.cursor.image.get_rect()
        pygame.mouse.set_visible(False)
        self.running = True
        self.pressed = ''
        self.board.player_hp = player_hp

        self.menu = pygame.sprite.Sprite(self.menu_group)
        self.menu.image = chest_ui
        self.menu.rect = self.menu.image.get_rect()
        self.menu.rect.y = 500
        self.menu.rect.x = 200

        self.equip_button = pygame.sprite.Sprite(self.menu_group, self.equip_group)
        self.equip_button.image = equip_button_image
        self.equip_button.rect = self.equip_button.image.get_rect()
        self.equip_button.rect.y = 510
        self.equip_button.rect.x = 530


number_of_potions = 1
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
chest_ui = pygame.transform.scale(load_image('chest_ui.png', -1), (400, 100))
healing_potion = pygame.transform.scale(load_image('healing_potion.png', -1), (50, 50))
equip_button_image = pygame.transform.scale(load_image('equip_button.png'), (60, 60))

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
