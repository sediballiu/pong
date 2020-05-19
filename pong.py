from tkinter import *
import random
import pygame, sys
from pygame.locals import *



win = Tk()

#krijojme menune fillestare duke perdorur tkinter
global highscore
global fituesi
with open("highestscore.txt","r") as hs:
    for line in hs:
        highscore = line
with open("fituesi.txt","r") as ft:
    for line in ft:
        fituesi = line

win.title("Pong Game")
win.geometry("200x210")

hs.close()
ft.close()

lojtar1 = Label(win,text="Emri i lojtarit te pare: ")
lojtar1.grid(row=0,column=0)

emri1 = Entry(win)
emri1.grid(row=1,column=0)


lojtar2 = Label(win,text="Emri i lojtarit te dyte: ")
lojtar2.grid(row=3,column=0)

emri2 = Entry(win)
emri2.grid(row=4,column=0)

labelfusha = Label(win,text="Zgjidh fushen: ")
labelfusha.grid(row=5,column=0)

optionVar = StringVar()
optionVar.set("Shkretetire")

option = OptionMenu(win, optionVar, "Shkretetire", "Hapsire", "Oqean", "Qiell", "Akull")
option.grid(row=6,column=0)


def fillo_lojen():
    nishi=emri1.get()
    dyshi=emri2.get()
    l = open("lojtari1.txt","w")
    l.write(nishi)
    r = open("lojtari2.txt","w")
    r.write(dyshi)
    f = open("fusha.txt","w")
    f.write(optionVar.get())
    f.close()
    quit()

butoni = Button(win,text="Luaj!",command=fillo_lojen)
butoni.grid(row=7,column=0,padx=10)

def quit():
    win.destroy()

plarta = Label(win,text="Piket me te larta: "+highscore+" nga "+fituesi)
plarta.grid(row=9,column=0)

win.mainloop()

#inizializojme lojen me ane te modulit pygame
pygame.init()
fps = pygame.time.Clock()
global LOJTARI1, LOJTARI2
with open("lojtari1.txt","r") as l:
    for line in l:
        LOJTARI1 = line
with open("lojtari2.txt","r") as r:
    for line in r:
        LOJTARI2 = line
with open("fusha.txt","r") as f:
    for line in f:
        zona = line

#ngjyra 
WHITE = (255,255,255)
BLACK = (0,0,0)

#globals
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 32
PAD_WIDTH = 8
PAD_HEIGHT = 64
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
ball_pos = [0,0]
ball_vel = [0,0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0

#statements per te zgjedhur fushen
if zona == "Shkretetire":
    fusha =  pygame.image.load("shkretetire.jpeg")
    topi = pygame.image.load("piramida.png")
elif zona == "Hapsire":
    fusha = pygame.image.load("space.jpg")
    topi = pygame.image.load("asteroid.png")
elif zona == "Oqean":
    fusha = pygame.image.load("water.jpg")
    topi = pygame.image.load("nendetese.png")
elif zona == "Qiell":
    fusha = pygame.image.load("clouds.jpg")
    topi = pygame.image.load("dielli.png")
elif zona == "Akull":
    fusha = pygame.image.load("snow.jpg")
    topi = pygame.image.load("bora.png")
hark = pygame.image.load("jepiiii.png")

#therrasim elementet grafike
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Pong Game')
bg = fusha

#funksion per levizjen e topit
def ball_init(right):
    global ball_pos, ball_vel
    ball_pos = [WIDTH//2,HEIGHT//2]
    horz = random.randrange(2,4)
    vert = random.randrange(1,3)
    
    if right == False:
        horz = - horz
        
    ball_vel = [horz,-vert]

def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,l_score,r_score  # these are floats
    global score1, score2
    paddle1_pos = [HALF_PAD_WIDTH - 6 + 1,HEIGHT//2]
    paddle2_pos = [WIDTH +1 -6 - HALF_PAD_WIDTH,HEIGHT//2]
    l_score = 0
    r_score = 0
    if random.randrange(0,2) == 0:
        ball_init(True)
    else:
        ball_init(False)


#funksion per vizatimin e fushes
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score
            
    canvas.fill(BLACK)
    canvas.blit(bg, (0, 0))
    if paddle1_pos[1] > HALF_PAD_HEIGHT - 32 and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT - 32:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT - 32 and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT - 32 and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel
    
    if paddle2_pos[1] > HALF_PAD_HEIGHT - 32 and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT - 32:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HALF_PAD_HEIGHT - 32 and paddle2_vel > 0:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT - 32 and paddle2_vel < 0:
        paddle2_pos[1] += paddle2_vel

    #updatojme pozicionin e topit
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    #vizatojme topit dhe pedalet
    canvas.blit(topi, ball_pos)
    canvas.blit(hark, paddle1_pos)
    canvas.blit(hark, paddle2_pos)


    #statements per perplasjet e topit ne muret lart dhe poshte
    if int(ball_pos[1]) <= BALL_RADIUS - 32:
        ball_vel[1] = - ball_vel[1]
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS - 32:
        ball_vel[1] = -ball_vel[1]
    
    #statements per perplasjet e topit ne muret anesore dhe pedale
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH - 32 and int(ball_pos[1]) in range(paddle1_pos[1] - HALF_PAD_HEIGHT,paddle1_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH - 32:
        r_score += 1
        ball_init(True)
        
    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH - 32 and int(ball_pos[1]) in range(paddle2_pos[1] - HALF_PAD_HEIGHT,paddle2_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH - 32:
        l_score += 1
        ball_init(False)

    #updatimi i pikeve
    shkronja1 = pygame.font.SysFont("Comic Sans MS", 25)
    label1 = shkronja1.render(LOJTARI1+" "+str(l_score), 1, (255,255,255))
    canvas.blit(label1, (50,20))

    shkronja2 = pygame.font.SysFont("Comic Sans MS", 25)
    label2 = shkronja2.render(LOJTARI2+" "+str(r_score), 1, (255,255,255))
    canvas.blit(label2, (470, 20))  
    
    
#funskion per marrjen e inputeve nga tastjera
def keydown(event):
    global paddle1_vel, paddle2_vel
    
    if event.key == K_UP:
        paddle2_vel = -8
    elif event.key == K_DOWN:
        paddle2_vel = 8
    elif event.key == K_w:
        paddle1_vel = -8
    elif event.key == K_s:
        paddle1_vel = 8

#funksion per marrjen e inputeve nga tastjera
def keyup(event):
    global paddle1_vel, paddle2_vel
    
    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0

init()


while True:

    draw(window)
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            if l_score > r_score:
                with open("highestscore.txt","r") as lhs:
                    for line in lhs:
                        if l_score > int(line):
                            #lhs.close()
                            ls = open("highestscore.txt","w")
                            ls.write(str(l_score))
                            ls.close()
                            lf = open("fituesi.txt","w")
                            lf.write(str(LOJTARI1))
                            lf.close
            else:
                with open("highestscore.txt","r") as rhs:
                    for line in rhs:
                        if r_score > int(line):
                            #rhs.close()
                            rs = open("highestscore.txt","w")
                            rs.write(str(r_score))
                            rs.close()
                            rf = open("fituesi.txt","w")
                            rf.write(str(LOJTARI2))
                            rf.close
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
    fps.tick(60)


