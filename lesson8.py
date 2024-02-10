import pygame
from random import randint

# инициализируем модули pygame
pygame.init()

# цвет фона
COLOR_FRAME = (153, 203, 240)
# количество кадров в секунду
FPS = 2
# ширина поля в клетках
WIDTH_COUNT_RECT = 20
# высота поля в клетках
HEIGHT_COUNT_RECT = 20
# размер одной клетки (в пикселях)
SIZE_RECT = 25
# расстояние между клетками
RET = 1
# растояние от верхнего края окна (для счета)
HEADER = 70
# цвет четных клеток
COLOR_RECT_0 = (149, 247, 79)
# цвет нечетных клеток
COLOR_RECT_1 = (229, 250, 122)
# ширина окна
WIDTH = SIZE_RECT * 2 + SIZE_RECT * WIDTH_COUNT_RECT + RET * (WIDTH_COUNT_RECT - 1)
# высота окна
HEIGHT = HEADER + SIZE_RECT * 2 + SIZE_RECT * HEIGHT_COUNT_RECT + RET * (HEIGHT_COUNT_RECT - 1)
# цвет змейки
COLOR_SNAKE = (0, 229, 255)
# цвет окна прооигрыша
COLOR_END = (255, 0, 0)
# текст для проигрша
FONT_END = pygame.font.SysFont(None, 60)
TEXT_END = FONT_END.render('GAME OVER', 1, (255, 255, 255))
TEXT_RECT_END = TEXT_END.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70))
# цвет еды
COLOR_FOOD = (255, 50, 228)
text_count = FONT_END.render('Счет: 0', 1, (255, 255, 255))
TEXT_RECT_COUNT = text_count.get_rect(topleft=(SIZE_RECT, SIZE_RECT))
# перезапуск
TEXT_REFRESH = FONT_END.render('Перезапуск', 1, (255, 255, 255))
TEXT_RECT_REFRESH = TEXT_REFRESH.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))

# создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# заголовок окна
pygame.display.set_caption('Змейка')

# Фоновая музыка
#анечка асти❤❤❤
music = pygame.mixer.music.load('D:\музыка\смесь\ANNA ASTI - Сорри.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.4)

# звуки
#айфон
sound_apple = pygame.mixer.Sound(r"D:\музыка\смесь\ANNA ASTI - Сорри.mp3")
#brutto
sound_game_over = pygame.mixer.Sound(r"D:\музыка\смесь\Brutto - Сарума (минус).mp3")

# объект для отслеживания времени
clock = pygame.time.Clock()
done = False
# для режима игры
mode = 'game'
# счет
count = 0



class Snake:
    'Класс змейки'
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def is_in_map(self):
        'Проверка нахождения в пределах поля'
        return 0 <= self.x < WIDTH_COUNT_RECT and 0 <= self.y < HEIGHT_COUNT_RECT
    
    def __eq__(self, val):
        'Проверка на равенство'
        if isinstance(val, Snake):
            return self.x == val.x and self.y == val.y
        return False


def draw_rect(color, col, row):
    'функция рисования одной клетки'
    pygame.draw.rect(screen, color,
                    #  Отступ слева (ширина одной клетки) + общая ширина предыдущих клеток + 
                    #   + общее растояние между предыдущими клетками
                     [SIZE_RECT + SIZE_RECT * col + RET * col,
                    #   Место для счета + Отступ сверху (ширина одной клетки) + общая высота предыдущих клеток +
                    #   + общее растояние между предыдущими клетками
                      HEADER + SIZE_RECT + SIZE_RECT * row + RET * row,
                      SIZE_RECT, SIZE_RECT])


def draw_map():
    'функция отрисовки поля'
    for i in range(HEIGHT_COUNT_RECT):
        for j in range(WIDTH_COUNT_RECT):
            if (i + j) % 2 == 0:
                draw_rect(COLOR_RECT_0, j, i)
            else:
                draw_rect(COLOR_RECT_1, j, i)

def draw_snake():
    'рисование змейки'
    for snake in snake_rects:
        draw_rect(COLOR_SNAKE, snake.x, snake.y)

def move_snake(pos, speed):
    'передвижение змейки'
    snake_rects.append(Snake(pos[0] + speed[0], pos[1] + speed[1]))
    snake_rects.pop(0)

def generate_food():
    'генерация блока еды'
    x = randint(0, WIDTH_COUNT_RECT - 1)
    y = randint(0, HEIGHT_COUNT_RECT - 1)
    food_block = Snake(x, y)
    while food_block in snake_rects and len(snake_rects) < WIDTH_COUNT_RECT * HEIGHT_COUNT_RECT:
        x = randint(0, WIDTH_COUNT_RECT - 1)
        y = randint(0, HEIGHT_COUNT_RECT - 1)
        food_block = Snake(x, y)
    return food_block

def is_eat_self():
    'Проверка на съедение себя'
    return snake_rects[-1] in snake_rects[:-3]

def read_record():
    'читает рекорд из файла'
    try:
        with open('record.txt', 'r', encoding='utf-8') as f:
            record_str = f.read()
            if record_str:
                return int(record_str)
            else:
                return 0
    except ValueError:
        return 0

def write_record(record):
    'запись рекорда в файл'
    with open('record.txt', 'w', encoding='utf-8') as f:
        f.write(str(record))

snake_rects = [Snake(WIDTH_COUNT_RECT // 2, HEIGHT_COUNT_RECT // 2)]
speed = [1, 0]
food = generate_food()
record = read_record()
text_record = FONT_END.render('Рекорд: ' + str(record), 1, (255, 255, 255))
text_record_rect = text_record.get_rect(topright=(WIDTH - SIZE_RECT, SIZE_RECT))
# положение рекорда в режиме проигрыша
text_record_rect_end = text_record.get_rect(center=(WIDTH // 2, HEIGHT // 2))

while not done:
    # перебираем все события
    for event in pygame.event.get():
        # если событие закрытия окна
        if event.type == pygame.QUIT:
            done = True
        elif mode == 'game' and event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and speed[1] == 0:
                speed = [0, -1]
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and speed[0] == 0:
                speed = [1, 0]
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and speed[1] == 0:
                speed = [0, 1]
            elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and speed[0] == 0:
                speed = [-1, 0]
            break
        elif mode == 'end' and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if TEXT_RECT_REFRESH.collidepoint(event.pos):
                snake_rects = [Snake(WIDTH_COUNT_RECT // 2, HEIGHT_COUNT_RECT // 2)]
                speed = [1, 0]
                food = generate_food()
                count = 0
                text_count = FONT_END.render('Счет: ' + str(count), 1, (255, 255, 255))
                pygame.mixer.music.play(loops=-1)
                mode = 'game'

    if mode == 'game':
        last_snake = snake_rects[-1]
        move_snake([last_snake.x, last_snake.y], speed)
        last_snake = snake_rects[-1]
        if not last_snake.is_in_map() or is_eat_self():
            sound_game_over.play()
            mode = 'end'
            pygame.mixer.music.pause()
            if count > record:
                record = count
                write_record(record)
                text_record = FONT_END.render('Рекорд: ' + str(record), 1, (255, 255, 255))
            continue
        if food == last_snake:
            sound_apple.play()
            snake_rects.append(food)
            food = generate_food()
            count += 1
            text_count = FONT_END.render('Счет: ' + str(count), 1, (255, 255, 255))
        screen.fill(COLOR_FRAME)
        screen.blit(text_count, TEXT_RECT_COUNT)
        screen.blit(text_record, text_record_rect)
        draw_map()
        draw_rect(COLOR_FOOD, food.x, food.y)
        draw_snake()
    elif mode == 'end  ':
        screen.fill(COLOR_END)
        screen.blit(TEXT_END, TEXT_RECT_END)
        screen.blit(TEXT_REFRESH, TEXT_RECT_REFRESH)
        screen.blit(text_record, text_record_rect_end)
    
    # обновляем отображение окна
    pygame.display.flip()
    # задержка
    clock.tick(FPS)
    