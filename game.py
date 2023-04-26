import pygame
import math
import random

#CONST
SCREENWIDTH=1280
SCREENHEIGHT=720

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
FPS=60
pygame.display.set_caption('TANK')
#variables
x_target=[]
y_target=[]
checkVar =1
showHelp=False
#functions
#Start screen
isStartingScreen=True
def start_Screen():
    screen.fill('white')
    font = pygame.font.Font('fonts/TitleFont.ttf', 150)
    sfont = pygame.font.Font('fonts/TitleFont.ttf', 50)
    title = font.render('TANKS',True,'black','white')
    titleRect = screen.get_rect(center=(SCREENWIDTH//2+SCREENWIDTH//3+30,SCREENHEIGHT//2+SCREENHEIGHT//3))
    subtext= sfont.render("PRESS 'E' TO CONTINUE", True,'black','white')
    subRect = screen.get_rect(center=(SCREENWIDTH//2+SCREENWIDTH//3,SCREENHEIGHT//2+SCREENHEIGHT//3+200))
    screen.blit(title, titleRect)
    screen.blit(subtext, subRect)

class Target:
    def __init__(self,x,y):
        self.x = int(x)
        self.y = int(y)
    #spawnTarget
    def spawnTarget(self):
        for i in range(10):
            x= random.randint(SCREENWIDTH//2,SCREENWIDTH*0.9)
            y = random.randint(50,SCREENHEIGHT*0.8)
            x_target.append(x)
            y_target.append(y)
            
    #drawTarget
    def drawTarget(self):
        targetIMG = pygame.image.load('images/target.png').convert_alpha()
        for i in range(0,10):
            screen.blit(targetIMG,(x_target[i],y_target[i]))

#classes
class Player:
    KEYS = pygame.key.get_pressed()
    def __init__(self,x,y,alpha,g,V0,t,dt,isShoted,score,bx,by):
        self.x = int(x)
        self.y = int(y)
        self.alpha =int(alpha)
        self.g = g
        self.V0 = V0
        self.t = t 
        self.dt = dt
        self.isShoted = isShoted
        self.score = score
        self.bx = bx 
        self.by = by
    def draw(self):
        #tank_body
        tank= pygame.image.load('images/Tank.png').convert_alpha()
        tank= pygame.transform.scale(tank, (65, 40))
        screen.blit(tank, (self.x,self.y))
    def move(self):
        if(self.isShoted==False):
            if(KEYS[pygame.K_a]):
                self.x-=3
            if(KEYS[pygame.K_d]):
                self.x+=3
    def tankTurret(self):
        global turretPointX,turretPointY
        if(self.isShoted==False):
            if(KEYS[pygame.K_w]):
                self.alpha+=1
            if(KEYS[pygame.K_s]):
                self.alpha-=1
            if(self.alpha<=0):
                self.alpha=0
            if(self.alpha>=90):
                self.alpha=90
        theta = math.radians(self.alpha)
        end_x = (self.x+35) + 40 * math.cos(theta)
        end_y = (self.y+5) - 40 * math.sin(theta)
        pygame.draw.line(screen, 'black', (self.x+35,self.y+5), (end_x,end_y),5)
        pygame.draw.circle(screen, 'black', (end_x,end_y), 2)
        pygame.draw.circle(screen, 'black', (self.x+35,self.y+5), 2)
        turretPointX,turretPointY=end_x,end_y
    def wallCollision(self):
        if(self.x<=0): self.x=0
        if(self.x>=231): self.x=231
    def shoot(self):
        #meth needed for this math XD
        theta = math.radians(self.alpha)
        V0x = self.V0 * math.cos(theta)
        V0y = self.V0 * math.sin(theta)
        self.bx= turretPointX+V0x *self.t
        self.by=turretPointY- V0y*self.t+0.5*self.g+self.t**2
        pygame.draw.circle(screen, 'black', (int(self.bx),int(self.by)), 5)
        if(self.bx<0 or self.bx>1280 or self.by>720):
            self.bx=(self.x+35)
            self.by=(self.y+5)
            V0x = self.V0 * math.cos(theta)
            V0y = self.V0 * math.sin(theta)
            self.isShoted=False
            self.t=0
    def checkColl(self):
        for i in range(10):
            if(self.bx>=x_target[i] and self.bx<=x_target[i]+50 and self.by>=y_target[i] and self.by<=y_target[i]+50 and self.bx<=x_target[i]+50 and self.by<=y_target[i]+50):
                self.score+=1
                x_target[i]=2000
                y_target[i]=2000
        
class gameGUI:
    def __init__(self,x,y):
        self.x = int(x)
        self.y = int(y)
    def draw(self):
        ground = pygame.image.load('images/ground.png').convert_alpha()
        ground = pygame.transform.scale(ground, (300,300))
        screen.blit(ground, (0,SCREENHEIGHT*0.62))
        font = pygame.font.Font('fonts/TitleFont.ttf', 30)
        
        
        Q = pygame.image.load('images/Q.png').convert_alpha()
        Q = pygame.transform.scale(Q, (50,50))
        screen.blit(Q, (SCREENWIDTH*0.75,SCREENHEIGHT*0.9+5))
        Qtxt = font.render("PRESS FOR HELP ", True, 'black','white')
        QtxtRect = screen.get_rect(center=(SCREENWIDTH+SCREENWIDTH-900,SCREENHEIGHT+SCREENHEIGHT-420))
        screen.blit(Qtxt, QtxtRect)
        angle = font.render("ANGLE "+str(player.alpha), True, 'black','white')
        angleRect = screen.get_rect(center=(SCREENWIDTH//2+20,SCREENHEIGHT+SCREENHEIGHT-550))
        screen.blit(angle, angleRect)
        power = font.render("POWER "+str(player.V0), True, 'black','white')
        powerRect = screen.get_rect(center=(SCREENWIDTH//2+20,SCREENHEIGHT+SCREENHEIGHT-500))
        screen.blit(power, powerRect)
        scoreText = font.render("SCORE "+str(player.score), True, 'black','white')
        scoreRect = screen.get_rect(center=(SCREENWIDTH//2+20,SCREENHEIGHT+SCREENHEIGHT-450))
        screen.blit(scoreText, scoreRect)
    def helpMenu(self):
        pUD = pygame.image.load('images/powerUPpowerDown.png').convert_alpha()
        pUD = pygame.transform.scale(pUD, (260,130))
        screen.blit(pUD, (0,SCREENHEIGHT*0.1))
        
        font = pygame.font.Font('fonts/TitleFont.ttf', 30)
        
        ptext = font.render("POWER +1 ", True, 'black','white')
        ptextRect = screen.get_rect(center=(SCREENWIDTH-530,SCREENHEIGHT-268))
        screen.blit(ptext, ptextRect)
        ptext2 = font.render("POWER -1 ", True, 'black','white')
        ptextRect2 = screen.get_rect(center=(SCREENWIDTH-530,SCREENHEIGHT-213))
        screen.blit(ptext2, ptextRect2)
        
        wasd = pygame.image.load('images/WASD.png').convert_alpha()
        wasd = pygame.transform.scale(wasd, (260,130))
        screen.blit(wasd, (30,SCREENHEIGHT*0.2+50))
        
        WASDT1 = font.render("W,S- ANGLE", True, 'black','white')
        ptextRect = screen.get_rect(center=(SCREENWIDTH-450,SCREENHEIGHT-140))
        screen.blit(WASDT1, ptextRect)
        
        WASDT2 = font.render("A,D- MOVE", True, 'black','white')
        ptextRect = screen.get_rect(center=(SCREENWIDTH-450,SCREENHEIGHT-90))
        screen.blit(WASDT2, ptextRect)
        
#class variables
player = Player(50, SCREENHEIGHT*0.6,0,9.81,10,0,0.01,False,0,0,0)
gui = gameGUI(0,SCREENHEIGHT-200)
target= Target(0, 0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #Controls
    KEYS = pygame.key.get_pressed()
    if(KEYS[pygame.K_ESCAPE]):
        running=False
    if(KEYS[pygame.K_q]):
        showHelp= not showHelp
    if(KEYS[pygame.K_e]):
        isStartingScreen=False
    if(KEYS[pygame.K_SPACE]):
        player.isShoted = True
    if(player.isShoted==False):
        if(KEYS[pygame.K_UP]):
            player.V0 +=1
        if(KEYS[pygame.K_DOWN]):
            player.V0 -=1
    if(player.V0<=10):
        player.V0=10
    if(player.V0>=50):
        player.V0=50
    #GAME section
    if(isStartingScreen==True):
        start_Screen()
    else:

        screen.fill('white')      
        gui.draw()
        target.spawnTarget()
        target.drawTarget()
        if(player.score/10==checkVar and player.score!=0):
            x_target.clear()
            y_target.clear()
            target.spawnTarget()
            target.drawTarget()
            checkVar+=1
        if(showHelp==True):
            gui.helpMenu()
        player.checkColl()
        player.draw()
        player.move()
        player.tankTurret()
        player.wallCollision()
        if(player.isShoted):
            player.shoot()
            player.t+=0.2
    #pygame essentials
    pygame.display.flip()
    dt = clock.tick(FPS) / 1000
pygame.quit()