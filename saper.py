import random
import pygame
from time import *


pygame.init()

class Rectangle(pygame.Rect):
    def __init__(self, x,y,width,height, pos1, pos2, data):
        super().__init__(x,y,width, height)
        self.pos1 = pos1
        self.pos2 = pos2
        self.data = data
        self.is_clicked = False
        self.is_flag = False
    def print_info(self):
        print(f'{self.pos1}:{self.pos2}, data: {self.data}')

class Button():
    def __init__(self, x,y,w,h,text,color,color_text, fsize=20):
        self.rect = pygame.Rect(x,y,w,h)
        self.fill_color = color
        self.text = pygame.font.Font(None, fsize).render(text, True, color_text)
    def draw(self):
        pygame.draw.rect(window, self.fill_color, self.rect)
        window.blit(self.text, [self.rect.x, self.rect.y])

MINS_COUNT = 10
LENGTH = 10
HEIGHT = 10
STATE = 0 #0 - game, 1 - menu, 2 - settings
LEVEL = 1 

flag_images = []
mins_images = []
pole = []
texts = []
rects = []

game = True
lose = False
win = False 

w,h = 700,700
window = pygame.display.set_mode([w,h])

SDVIG = 100

W_RECT = (w) // LENGTH
H_RECT = (h-SDVIG) // HEIGHT

def create_numbers1():
    global pole
    for pos1 in range(len(pole)):
        for pos2 in range(len(pole[pos1])):
            if pole[pos1][pos2] == '*':
                continue
            k = 0
            try:
                if pole[pos1][pos2-1] == '*':
                    k += 1
            except:
                pass
            try:
                if pole[pos1][pos2+1] == '*':
                    k += 1
            except:
                pass
            try:
                if pole[pos1-1][pos2] == '*':
                    k += 1
            except:
                pass
            try:
                if pole[pos1+1][pos2] == '*':
                    k += 1
            except:
                pass
            try:
                if pole[pos1-1][pos2-1] == '*':
                    k += 1
            except:
                pass
            try:
                if pole[pos1+1][pos2-1] == '*':
                    k += 1
            except:
                pass
            try:
                if pole[pos1-1][pos2+1] == '*':
                    k += 1
            except:
                pass
            try:
                if pole[pos1+1][pos2+1] == '*':
                    k += 1  
            except:
                pass
            pole[pos1][pos2] = k

def create_numbers():
    ruleTop, ruleBottom, ruleLeft, ruleRight = True, True, True, True
    for pos1 in range(len(pole)):
        for pos2 in range(len(pole[pos1])):
            if pole[pos1][pos2] == '*':
                continue
            if pos1 == 0:
                ruleTop = False
            if pos2 == 0:
                ruleLeft = False
            if pos1 == HEIGHT-1:
                ruleBottom = False
            if pos2 == LENGTH-1:
                ruleRight = False
            res = around(ruleTop, ruleBottom, ruleLeft, ruleRight, pos1, pos2, pole)
            pole[pos1][pos2] = res
            ruleTop, ruleBottom, ruleLeft, ruleRight = True, True, True, True
            
def around(Top, Bottom, Left, Right, pos1, pos2, pole):
    k = 0
    if Top and Bottom and Left and Right:
        if pole[pos1][pos2-1] == '*':
            k += 1
        if pole[pos1][pos2+1] == '*':
            k += 1
        if pole[pos1-1][pos2] == '*':
            k += 1
        if pole[pos1+1][pos2] == '*':
            k += 1
        if pole[pos1-1][pos2-1] == '*':
            k += 1
        if pole[pos1+1][pos2-1] == '*':
            k += 1
        if pole[pos1-1][pos2+1] == '*':
            k += 1
        if pole[pos1+1][pos2+1] == '*':
            k += 1     
    elif Top and Bottom:
        if Right:
            if pole[pos1+1][pos2] == '*':
                k += 1
            if pole[pos1+1][pos2+1] == '*':
                k += 1
            if pole[pos1][pos2+1] == '*':
                k += 1
            if pole[pos1-1][pos2] == '*':
                k += 1
            if pole[pos1-1][pos2+1] == '*':
                k += 1
        elif Left:
            if pole[pos1+1][pos2] == '*':
                k += 1
            if pole[pos1+1][pos2-1] == '*':
                k += 1
            if pole[pos1][pos2-1] == '*':
                k += 1
            if pole[pos1-1][pos2] == '*':
                k += 1
            if pole[pos1-1][pos2-1] == '*':
                k += 1
    elif Top:
        if Right and Left:
            if pole[pos1-1][pos2] == '*':
                k += 1
            if pole[pos1-1][pos2+1] == '*':
                k += 1
            if pole[pos1][pos2+1] == '*':
                k += 1
            if pole[pos1-1][pos2-1] == '*':
                k += 1
            if pole[pos1][pos2-1] == '*':
                k += 1
        elif Left:
            if pole[pos1-1][pos2] == '*':
                k += 1
            if pole[pos1-1][pos2-1] == '*':
                k += 1
            if pole[pos1][pos2-1] == '*':
                k += 1
        elif Right:
            if pole[pos1-1][pos2] == '*':
                k += 1
            if pole[pos1-1][pos2+1] == '*':
                k += 1
            if pole[pos1][pos2+1] == '*':
                k += 1
    elif Bottom:
        if Right and Left:
            if pole[pos1+1][pos2] == '*':
                k += 1
            if pole[pos1+1][pos2+1] == '*':
                k += 1
            if pole[pos1][pos2+1] == '*':
                k += 1
            if pole[pos1+1][pos2-1] == '*':
                k += 1
            if pole[pos1][pos2-1] == '*':
                k += 1
        elif Left:
            if pole[pos1+1][pos2] == '*':
                k += 1
            if pole[pos1+1][pos2-1] == '*':
                k += 1
            if pole[pos1][pos2-1] == '*':
                k += 1
        elif Right:
            if pole[pos1+1][pos2] == '*':
                k += 1
            if pole[pos1+1][pos2+1] == '*':
                k += 1
            if pole[pos1][pos2+1] == '*':
                k += 1
    return k

def create_mins():
    global pole,rects,texts, LENGTH, HEIGHT, SDVIG, MINS_COUNT, W_RECT, H_RECT, LEVEL
    if LEVEL == 1:
        MINS_COUNT = 10
    if LEVEL == 2:
        MINS_COUNT = 35 
    if LEVEL == 3:
        MINS_COUNT = 65 

    LENGTH = 10 * LEVEL
    HEIGHT = 10 * LEVEL
    W_RECT = (w) // LENGTH
    H_RECT = (h-SDVIG) // HEIGHT
    pole.clear()
    pole = [[0 for i in range(LENGTH)] for i in range(HEIGHT)]
    for mins in range(MINS_COUNT):
        pos1 = random.randint(0,LENGTH-1)
        pos2 = random.randint(0,HEIGHT-1)
        try:
            while pole[pos2][pos1] == '*':
                pos1, pos2 = random.randint(0,HEIGHT-1),random.randint(0,LENGTH-1)
            pole[pos2][pos1] = '*'
            mins_images.append([pos1*W_RECT, SDVIG + pos2*H_RECT])
        except Exception as e:
            print('!!!Питон сошел с ума и выдает диапазон рандома больше заданного!!!')
            print(pos1, pos2)
            create_mins()
    create_numbers()
    rects = [[Rectangle(0+j*W_RECT,SDVIG+i*H_RECT, W_RECT, H_RECT, j,i, pole[i][j]) for i in range(LENGTH)] for j in range(HEIGHT)]
    texts = [[pygame.font.Font(None, W_RECT).render(str(pole[i][j]), True, [255,255,255]) for i in range(LENGTH)] for j in range(HEIGHT)]
    for mins in pole:
        print(mins, end='\n')

create_mins()

text_lose = pygame.font.Font(None, w//12).render('Проигрыш', True, [255,0,0])
text_win = pygame.font.Font(None, w//12).render('Победа', True, [0,255,0])
text_info = pygame.font.Font(None, w//12).render('нажми на r для рестарта', True, [0,0,255])

start = time()


def open(pos1,pos2):
    if pos1 > -1 and pos2 > -1 and pos1 < LENGTH and pos2 < HEIGHT:
        if rects[pos1][pos2].data == 0:
            if rects[pos1][pos2].is_clicked == False and rects[pos1][pos2].is_flag == False: 
                rects[pos1][pos2].is_clicked = True
                try:
                    open(pos1, pos2-1)
                except:
                    pass
                try:
                    open(pos1, pos2+1)
                except:
                    pass
                try:
                    open(pos1+1, pos2)
                except:
                    pass
                try:
                    open(pos1-1, pos2)
                except:
                    pass
                try:
                    open(pos1-1, pos2+1)
                except:
                    pass
                try:
                    open(pos1-1, pos2-1)
                except:
                    pass
                try:
                    open(pos1+1, pos2+1)
                except:
                    pass
                try:
                    open(pos1+1, pos2-1)
                except:
                    pass
        elif rects[pos1][pos2].data != 0 and rects[pos1][pos2].data != '*':
            rects[pos1][pos2].is_clicked = True

def restart():
    global lose 
    lose = False
    win = False
    flag_images.clear()
    mins_images.clear()
    create_mins()

button1 = Button(250,0,200,50,'НАСТРОЙКИ', [24,150,56], [255,255,255], 40)
menu1 = Button(0,0,500,500,"ВЫБЕРИ СЛОЖНОСТЬ", [0,255,0], [255,255,255], 50)
level_info = Button(10,50,100,100, 'Текущий lvl:' + str(LEVEL), [0,255,0], [255,255,255], 40)
button2 = Button(150,100,200,50,'1 уровень', [24,150,56], [255,255,255], 40)
button3 = Button(150,200,200,50,'2 уровень', [24,150,56], [255,255,255], 40)
button4 = Button(150,300,200,50,'3 уровень', [24,150,56], [255,255,255], 40)
button5 = Button(150,400,200,50,'ИГРАТЬ', [24,150,56], [255,255,255], 40)

while game:
    k = 0 # кол-во мин, которые пометил в игре
    window.fill([255,255,255])  
    button1.draw()
    
    level_info = Button(10,50,100,100, 'Текущий lvl:' + str(LEVEL), [0,255,0], [255,255,255], 40)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
        if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    pos_mouse = pygame.mouse.get_pos()
                    if STATE == 0:
                        for i in rects:
                            for r in i:
                                if r.collidepoint(pos_mouse):
                                    if not r.is_clicked:
                                        open(r.pos1, r.pos2)
                                    if r.data == '*':
                                        if win == False:
                                            lose = True
                    if button1.rect.collidepoint(pos_mouse):
                        STATE = 1
                    if STATE == 1:
                        pos_mouse = pygame.mouse.get_pos()
                        if button2.rect.collidepoint(pos_mouse):
                            LEVEL = 1
                        if button3.rect.collidepoint(pos_mouse):
                            LEVEL = 2
                        if button4.rect.collidepoint(pos_mouse):
                            LEVEL = 3
                        if button5.rect.collidepoint(pos_mouse):
                            STATE = 0
                            restart()
                            start = time()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_f:
                pos_mouse = pygame.mouse.get_pos()
                for i in rects:
                    for r in i:
                        if r.collidepoint(pos_mouse):
                            if r.is_flag == True:
                                flag_images.remove(r)
                                r.is_flag = False
                            else:
                                flag_images.append(r)
                                r.is_flag = True
                            print(r.pos1, r.pos2, pole[r.pos2][r.pos1])
                print(flag_images)
            if e.key == pygame.K_r:
                if lose == True or win == True:
                    restart()
                    start = time()
    if STATE == 0:
        if not lose and not win:
            end = time()
        text_time = pygame.font.Font(None, w//12).render('Время: ' +str(int(end-start)), True, [0,0,255])
        for i in range(len(rects)):
            for j in range(len(rects[i])):
                if rects[i][j].is_flag == True and pole[j][i] == '*':
                    k += 1
        if k == MINS_COUNT:
            
            win = True
            window.blit(text_win,[0, 0])
            window.blit(text_info, [0, h//12])
            for i in range(HEIGHT):
                for j in range(LENGTH):
                    rects[i][j].is_clicked = True
        if len(flag_images) != 0:
            for r in flag_images:
                window.blit(pygame.transform.scale(pygame.image.load('flag.jpg'), (20, 20)), [r.pos1*W_RECT, SDVIG + r.pos2*H_RECT])
        
        for i in range(LENGTH):
            for j in range(HEIGHT):
                pygame.draw.rect(window, [215,215,215], rects[i][j], width=2)
                if rects[i][j].is_clicked:
                    pygame.draw.rect(window, [0,0,0], rects[i][j], width=0)
                    window.blit(texts[i][j], [rects[i][j].pos1*W_RECT+W_RECT//10,SDVIG+rects[i][j].pos2*H_RECT + H_RECT//10]) 
        if lose:
            for mins in mins_images:
                window.blit(pygame.transform.scale(pygame.image.load('mina.jpg'), [W_RECT-10,H_RECT-10]),[mins[0]+5, mins[1]+5]) 
            window.blit(text_lose,[0, 0])
            window.blit(text_info, [0, h//12])

        window.blit(text_time, [470, 10])
    if STATE == 1:
        menu1.draw()
        button2.draw()
        button3.draw()
        button4.draw()
        level_info.draw()
        button5.draw()

    pygame.display.update()