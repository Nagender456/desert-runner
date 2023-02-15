import pygame
import random
import os
import time
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()



size = (1200,600)
WHITE = (255,255,255)
clock = pygame.time.Clock()
FPS = 60
to_update=[]
game_started = False
sprite_group = pygame.sprite.Group()
sprite_group2 = pygame.sprite.Group()
speed_base=None
highscore = 0
speed_difference = 0
paused = False





CWD = os.getcwd()
os.chdir("{}/data/".format(CWD))

file_HS = open("highscore.txt","r")
highscore = int(file_HS.read(),16)
font_score = pygame.font.Font('score_font.ttf',100)
font_HS = pygame.font.Font('score_font.ttf',50)

os.chdir("{}/data/audio".format(CWD))
musicbg1 = pygame.mixer.music.load("music (2).mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

jump_sound = pygame.mixer.Sound("jump.wav")
die_sound = pygame.mixer.Sound("die.wav")
slide_sound = pygame.mixer.Sound("slide.wav")
HS_sound = pygame.mixer.Sound("HS.wav")
slide_sound.set_volume(1.5)

# IMAGES


os.chdir("{}/data/images/player".format(CWD))
player_images = dict()
player_images["dead"] = []
player_images["idle"] = []
player_images["jump"] = []
player_images["run"] = []
player_images["slide"] = []

for i in range(10):
    a = pygame.image.load("Dead ({}).png".format(i+1))
    player_images["dead"].append(a)
for i in range(10):
    a = pygame.image.load("Idle ({}).png".format(i+1))
    player_images["idle"].append(a)
for i in range(10):
    a = pygame.image.load("Jump ({}).png".format(i+1))
    player_images["jump"].append(a)
for i in range(10):
    a = pygame.image.load("Run ({}).png".format(i+1))
    player_images["run"].append(a)
for i in range(10):
    a = pygame.image.load("Slide ({}).png".format(i+1))
    player_images["slide"].append(a)


os.chdir("{}/data/images/other".format(CWD))

img_start = pygame.image.load("start_message.png")
msg_dead = pygame.image.load("dead_message.png")
high_scoreImg = pygame.image.load("high_scored.png")
img_base = pygame.image.load("ground.png")
img_HS = pygame.image.load("HS.png")
img_BG =  pygame.image.load("BG.png")
pausedImg = pygame.image.load("paused.png")
pausedRect = pausedImg.get_rect()
pausedRect.centerx, pausedRect.top = 600,100
list_obstaclesImg =[]
img_tut = []
for i in range(3):
    a = pygame.image.load("tut{}.png".format(i+1))
    img_tut.append(a)
for i in range(20):
    a = pygame.image.load("Obstacle ({}).png".format(i+1))
    list_obstaclesImg.append(a)



# FUNCTIONS

def get_HS():
    global highscore
    str_hs = str(highscore)
    length = len(str_hs)
    for i in range(6-length):
        str_hs = "0"+str_hs
    return str_hs
def display_HS():
    global str_HS,font_score,screen
    img_score = font_HS.render(str_HS,True,(0,0,0))
    rect = img_score.get_rect()
    rect.centerx,rect.top = 1080,60
    screen.blit(img_score,rect)
    
        
def display_score():
    global currentscore,font_score,screen
    img_score = font_score.render(str(round(currentscore)),True,(0,0,0))
    rect = img_score.get_rect()
    y1 = 100
    if player.facing=='right': x1 = 900
    else: x1 = 300
    if player.state=='dead':
        x1=600
        y1=200
    rect.centerx,rect.top = x1,y1
    screen.blit(img_score,rect)
    
    
    
def initialize_game():
    global sprite_group,to_update,list_base,list_bg,player,start_screen,end_screen,currentscore,high_scoreMsg,current_speed,speed_difference
    speed_difference=0
    currentscore=0
    current_speed=8
    sprite_group.empty()
    sprite_group2.empty()
    del to_update
    player = Player(player_images,(600,500),"idle")
    start_screen = StartScreen(img_start,(620,200))
    end_screen = StartScreen(msg_dead,(620,225))
    high_scoreMsg = StartScreen(high_scoreImg,(610,450))
    list_base = []
    list_bg = []
    for i in range(0,1200+128,128):
        a = ScrollingBase(img_base,(i,620))
        list_base.append(a)
    for i in range(0,1200+1280,1280):
        a = ScrollingBG(img_BG,(i,600),1)
        list_bg.append(a)

    
    sprite_group.add(list_bg,start_screen,list_base,player)
    sprite_group2.add(end_screen)
    to_update = [list_bg,player,list_base]
    

def coin_toss():
    a = random.randint(1,2)
    if a==1:
        return "heads"
    else:
        return "tails"

def update_list(x):
    for i in x:
        try:
            i.update()
        except Exception:
            for j in i:
                j.update()

def set_speed():
    global speed_base,currentscore,speed_difference,current_speed,player
    if speed_difference<250 or current_speed==15:
        speed_base=current_speed
        speed_difference+=0.1
    else:
        if current_speed<15:
            current_speed+=1
            if current_speed==14:
                player.framerate=1
        speed_difference=0


def add_bases():
    global list_base
    if player.facing=='right':
        if list_base[0].rect.right < 0:
            a = list_base.pop(0)
            a.rect.left = list_base[-1].rect.right
            list_base.append(a)
    if player.facing=='left':
        if list_base[-1].rect.left > 1200:
            a = list_base.pop(-1)
            a.rect.right = list_base[0].rect.left
            list_base.insert(0,a)

def add_bg():
    global list_base
    if player.facing=='right':
        if list_bg[0].rect.right < 0:
            a = list_bg.pop(0)
            a.rect.left = list_bg[-1].rect.right
            list_bg.append(a)
    if player.facing=='left':
        if list_bg[-1].rect.left > 1200:
            a = list_bg.pop(-1)
            a.rect.right = list_bg[0].rect.left
            list_bg.insert(0,a)
        


def events():
    global game_started,speed_base,list_bg,obstacle,to_update,high_scoreMsg,currentscore,highscore,str_HS,paused
    for ev in pygame.event.get():
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if not game_started and player.state!="dead":
                if ev.key == pygame.K_LEFT:
                    player.facing = "left"
                    player.state = 'run'
                    game_started = True
                    sprite_group.remove(start_screen)
                    obstacle = Obstacle(list_obstaclesImg)
                    sprite_group.remove(player)
                    sprite_group.add(obstacle,player)
                    to_update.append(obstacle)
                    
                elif ev.key == pygame.K_RIGHT:
                    player.facing = "right"
                    player.state = 'run'
                    game_started = True
                    obstacle = Obstacle(list_obstaclesImg)
                    sprite_group.remove(player)
                    sprite_group.add(obstacle,player)
                    to_update.append(obstacle)
                    sprite_group.remove(start_screen)
            elif player.state=="dead":
                if ev.key==pygame.K_p:
                    initialize_game()
                        
                    
            else:
                if not paused:
                    if ev.key==pygame.K_p:
                        paused = True
                    elif ev.key==pygame.K_UP and player.state!="jump":
                        pygame.mixer.Sound.play(jump_sound)
                        pygame.mixer.Sound.stop(slide_sound)
                        player.jump = True
                        player.state = "jump"
                        
                    elif ev.key==pygame.K_DOWN and player.state!="slide":
                        pygame.mixer.Sound.play(slide_sound)
                        player.slide = True
                        player.state = "slide"
                else:
                    if ev.key==pygame.K_p:
                        paused = False
                    
                    
                
                    
                    
        if ev.type == pygame.QUIT:
            pygame.quit()
            quit()
    if game_started:
        if pygame.sprite.spritecollide(player,[obstacle],False,pygame.sprite.collide_mask) and player.state!="dead":
            pygame.mixer.Sound.play(die_sound)
            if round(currentscore)>highscore:
                pygame.mixer.Sound.play(HS_sound)
                sprite_group2.add(high_scoreMsg)
                highscore = round(currentscore)
                str_HS = get_HS()
                os.chdir("{}/data/".format(CWD))
                file_HS = open("highscore.txt","wt")
                file_HS.write(hex(highscore))
            game_started=False
            player.state="dead"
            player.index=0



# CLASSES
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,images):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.image = self.images[0]
        self.rect = self.image.get_rect()
        if player.facing=="right":
            self.rect.left,self.rect.bottom = 1200,500
        else:
            self.rect.right,self.rect.bottom = 0,500   
        self.mask = pygame.mask.from_surface(self.image)
        self.counter = 0
        self.moving = False
        self.startI = 0
        self.finalI = 8
    def update(self):
        global tutorial,currentscore
        if 1000>currentscore>300:
            self.startI = 6
            self.finalI = 12
        elif 1500>currentscore>1000:
            self.startI = 9
            self.finalI = 20
        elif currentscore>1500:
            self.startI = 0
            self.finalI = 20
            
        if self.rect.left==1200 or self.rect.right==0 and not self.moving:
            self.counter+=1
            if self.counter==10:
                self.moving =  True
                self.counter=0
        if self.moving:
            if player.facing=="left": self.rect.x+=speed_base
            else: self.rect.x-=speed_base
            if self.rect.right<0 or self.rect.left>1200:
                self.moving = False
                self.image = random.choice(self.images[self.startI:self.finalI])
                if tutorial<3:
                    self.image = self.images[6] if tutorial==1 else self.images[7]
                a = coin_toss()
                if a=="heads":
                    self.image = pygame.transform.flip(self.image,True,False)
                self.rect = self.image.get_rect()
                self.rect.bottom = 500
                if player.facing=="right":
                    self.rect.left = 1200
                else:
                    self.rect.right = 0
        self.mask = pygame.mask.from_surface(self.image)
            
            
                
        
class ScrollingBG(pygame.sprite.Sprite):
    def __init__(self,image,pos,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.bottom=pos
        self.speed = speed
    def update(self):
        if player.facing=='left': self.rect.x+=self.speed
        else: self.rect.x-=self.speed

class ScrollingBase(pygame.sprite.Sprite):
    def __init__(self,image,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.bottom=pos
    def update(self):
        global speed_base
        if player.facing=='left': self.rect.x+=speed_base
        else: self.rect.x-=speed_base
        



        
class Player(pygame.sprite.Sprite):
    def __init__(self,images,pos,state):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images["idle"][0]
        self.rect = self.image.get_rect()
        self.rect.centerx,self.rect.bottom = pos
        self.state = state
        self.index=0
        self.counter = 0
        self.facing="right"
        self.jump = False
        self.slide = False
        self.jump_index = 0
        self.jump_list = [25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,0,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-24]
        self.index2=0
        self.index3=0
        self.slide_counter=0
        self.framerate=2
        self.counterrun=0
    def update(self):
        global speed_base
        self.counter+=1
        if self.state=="dead":
            if self.counter==2:
                self.index3+=1
                if self.index3 == len(self.images[self.state]):
                    self.index3-=1
                self.image = self.images[self.state][self.index3]
                
                if self.facing=='right': self.x = self.rect.centerx
                else: self.x = self.rect.centerx
                self.y = 525
                self.rect = self.image.get_rect()
                self.rect.centerx,self.rect.bottom  = self.x,self.y
                
                self.counter=0
                if self.facing=='left':
                    self.image = pygame.transform.flip(self.image,True,False)

            
        elif self.jump or self.slide:
            if self.jump: self.jump_Player()
            if self.slide: self.slide_Player()
            if self.counter==2:
                self.index2+=1
                if self.index2 == len(self.images[self.state]):
                    self.index2-=1
                self.image = self.images[self.state][self.index2]
                self.x = self.rect.centerx
                self.y = self.rect.bottom
                self.rect = self.image.get_rect()
                self.rect.centerx,self.rect.bottom  = self.x,self.y
                
                self.counter=0
                if self.facing=='left':
                    self.image = pygame.transform.flip(self.image,True,False)
                self.mask = pygame.mask.from_surface(self.image)
        
        elif self.state=='run' or self.state=='idle':
            self.counterrun+=1
            if self.counterrun==self.framerate or self.counterrun>self.framerate:
                self.index+=1
                self.counterrun=0
            if self.index==len(self.images[self.state]):
                self.index=0
            self.image = self.images[self.state][self.index]
            self.x = self.rect.centerx
            self.y = self.rect.bottom
            self.rect = self.image.get_rect()
            self.rect.centerx,self.rect.bottom  = self.x,self.y
            self.counter=0
            if self.facing=='left':
                self.image = pygame.transform.flip(self.image,True,False)
            self.mask = pygame.mask.from_surface(self.image)
    def jump_Player(self):
        self.jump_index+=1
        if self.jump_index==len(self.jump_list):
            self.jump=False
            if not self.slide and self.state!="dead": self.state="run"
            self.jump_index=0
        else:
            self.rect.bottom-=self.jump_list[self.jump_index]

    def slide_Player(self):
        global speed_base
        self.slide_counter+=1
        if self.slide_counter<50:
            if speed_base<0:
                speed_base-=4
            else:
                speed_base+=4
        else:
            self.slide = False
            if not self.jump and self.state!="dead": self.state="run"
            self.slide_counter=0
        
        

class StartScreen(pygame.sprite.Sprite):
    def __init__(self,image,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.centerx,self.rect.bottom=pos
        self.ychange = 1
        self.counter = 0



# OBJECTS
initialize_game()
str_HS = get_HS()
     





screen = pygame.display.set_mode(size)
tutorial = 3
tut_counter=0
tutRect=img_tut[0].get_rect()
tutRect.centerx, tutRect.top = 600,200
if highscore<100:
    tutorial = 0

        


#MainLoop

while True:
    pygame.display.update()
    screen.fill(WHITE)
    set_speed()
    if not game_started and player.state=='idle':
        
        sprite_group.draw(screen)
        screen.blit(img_HS,(900,50))
        start_screen.update()
        player.update()
        display_HS()
    elif player.state!="dead":
        sprite_group.draw(screen)
        if not paused:
            currentscore+=0.1
            update_list(to_update)
            add_bases()
            add_bg()
        else:
            screen.blit(pausedImg,pausedRect)
        display_score()
        if tutorial<3:
            tut_counter+=1
            if tut_counter in [150,300,450]:
                tutorial+=1
                tutRect.top = 200
            if tut_counter<100:
                screen.blit(img_tut[tutorial],tutRect)
                tutRect.top-=1
            elif tut_counter<300:
                screen.blit(img_tut[tutorial],tutRect)
                tutRect.top-=1
            elif tut_counter<450:
                screen.blit(img_tut[tutorial],tutRect)
                tutRect.top-=1
        
            
    else:
        if highscore<100:
            tutorial = 0
            tut_counter=0
            tutRect.top=100
        sprite_group.draw(screen)
        player.update()
        display_score()
        sprite_group2.draw(screen)
        sprite_group2.update()
    events()
    clock.tick(FPS)
