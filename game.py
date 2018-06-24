import sys, random, pygame, math, os, time
from pygame.locals import *
from os.path import expanduser
pygame.init()


###INSTALATION INSTRUCTIONS###
# 1) Rename folder "Bazooka Bob"
# 2) Bethany please I just want one weekend with the kids
# 3) Put folder in Application Support 
# 4) Last time I goddamn checked BETHANY you were the one who cheated on me you were the one who left bobby at the park for three hours alone because you wanted to watch Fifty Shades Darker with your dumb fucking friends bethany let me see my goddamn kids 


fps = 60
health = 5
fpsClock = pygame.time.Clock()
creditsOn = False
is_shot = False

score = 0
wave_score = 0
enemy_num = 1
n = []
leg_frame = 0


#Loading sprites
width, height = (800, 600)
screenWidth = 800
screenHeight = 600
# APP_FOLDER = os.path.dirname.(os.path.realpath.(sys.argv[0]))

# def full_path(file):
#     full_path = os.path.join.(APP_FOLDER, file)
def full_path(file):
    #home = expanduser("~")
    #full_path = os.path.join(home, "Desktop/bazooka-bob/GFX/" + file)
    full_path = "/Library/Application Support/Bazooka Bob/GFX/" + file
    return full_path

screen = pygame.display.set_mode((width, height))
floor = pygame.image.load(full_path("floor.png"))
bob = pygame.transform.scale(pygame.image.load(full_path("bob.png")),(62,128))
bullet = pygame.image.load(full_path("rocket.png"))
enemy = pygame.image.load(full_path("/enemy1/enemy1.png"))
health_bar = pygame.image.load(full_path("health_5.png"))
screen1 = pygame.image.load(full_path("open_screen.png"))
pygame.display.set_caption(full_path('Beter eaT salami'))
white = (255, 255, 255)
black = (0, 0, 0,)
current_x = 0
current_y = 0
bulletR = bullet
final_pos = (0,0)
# def things(thing_x,thing_y, thing_w, thing_h):
#     pygame.draw.rect(game)

# def text_objects(text,font):
#     txtSurf = font.render(text,False,black)
#     return textSurf, textSurf.get_rect()

def msg(text_output, text_x, text_y):
    pixelfont = pygame.font.Font(full_path("umberdale.ttf"), 20)
    txt = pixelfont.render(text_output, False, white, black)
    textrect = txt.get_rect()
    textrect.centerx = text_x
    textrect.centery = text_y
    screen.blit(txt, (text_x, text_y))

class bobClass:
    global is_shot
    def __init__(self):
        self.move = 0
        self.x = 0
        self.y = 372
        self.w = 55
        self.jump = 0
        self.jump_factor = 30
        self.shoot = 0
        self.last = 0
        self.frame = 1
        self.padding = 0
    def bob_move(self):
        global is_shot, bob
        if self.x >= 800 - self.w:
            self.x = 0
        if self.x < 0:
            self.x = 750
        if self.move == "right":
            self.x += 3
            self.padding += 1
            if self.padding == 5:
                self.frame += 1
                if self.frame >4:
                    self.frame = 1
                bob = pygame.transform.scale(pygame.image.load(full_path("bob_legs" + str(self.frame) +".png")),(62,128))
                self.padding = 0
        elif self.move == "left":
            self.x -= 3
            self.padding += 1
            if self.padding == 5:
                self.frame += 1
                if self.frame >4:
                    self.frame = 1
                bob = pygame.transform.flip(pygame.transform.scale(pygame.image.load(full_path("bob_legs" + str(self.frame) +".png")),(62,128)),True,False)
                self.padding = 0
        if self.jump == "up":
            self.y -= 0.3 * self.jump_factor
            self.jump_factor -= 1
            if self.y <= 300:
                self.jump = "down"
                self.jump_factor = 10
            if self.jump_factor < 10:
                self.jump_factor = 10
        elif self.jump == "down":
            self.y += 0.3 * self.jump_factor
            self.jump_factor += 1
            if self.y >= 372:
                self.jump = 0
                self.y = 372
                self.jump_factor = 30
            if self.jump_factor > 30:
                self.jump_factor = 30
            


bob_1 = bobClass()

class enemyClass:
    global enemy_num, wave_score
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 75 #change with current width
        self.alive = True
        self.move_x = random.random()
        self.move_y = random.random()
        self.dist = 0
        self.padding = 0
        self.frame = random.randint(1,5)
        self.slope = 0
        self.type =str(random.randint(1,2))
        self.typeset = False
    def enemy_angle(self):
        if self.alive == True:
            self.move_x = random.random()
            self.move_y = random.random()
            
            if (bob_1.y - 100) > self.y:
                if bob_1.x < self.x:
                    self.move_x = -self.move_x
                    
            else:
                if bob_1.x < self.x:
                    self.move_x = -self.move_x
                    self.move_y = -self.move_y
                    
                else:
                    self.move_y = -self.move_y
                    
            self.slope = 270 - math.atan2(self.move_y,self.move_x)*180/math.pi

            print("slope:   " + str(self.slope))
            # if self.slope >= 270 and self.slope <= 360:
            #     self.slope -= 90
            #     print("new coke:   " + str(self.slope))
            # elif self.slope >= 180 and self.slope <= 270:
            #     self.slope += 90
            #     print("new coke:   " + str(self.slope))

    def enemy_pos(self):      
        if self.alive == True:
            side = random.randint(0,2)
            if self.typeset == False:
                self.type = random.randint(1,2)
                self.type = True
            if side == 0:
                self.x = random.randint(0 -self.w,800)
                self.y = 0
            elif side == 1:
                self.x = 0 -self.w
                self.y = random.randint(0,200)
            elif side == 2:
                self.x = 800
                self.y = random.randint(0,200)
            self.enemy_angle()

    def moveEnemy(self):
        global enemy
        if self.alive == True:
            if self.dist < 100:
                #test code
                self.padding += 1
                if self.padding == 10:
                    self.frame += 1
                    self.padding = 0
                    # print(self.frame)
                if self.frame >4:
                    self.frame = 1
                # self.slope = 360-math.atan2(self.y-self.move_y,self.x-self.move_x)*180/math.pi
                # print("slope:   " + str(self.slope))
                enemy = pygame.transform.rotate(pygame.transform.scale(pygame.transform.flip(pygame.image.load(full_path("/enemy"+self.type+"/enemy" + str(self.frame) +".png")),True,False),(100,100)),self.slope)
                #end of test code
                self.x += self.move_x * 2
                self.y += self.move_y * 2
                self.dist += 1
            else:
                self.dist = 0
                self.enemy_angle()
        
    def load_health(self):
        global health_bar
        global health
        ##start = 0
        if ((bob_1.x < self.x + self.w and bob_1.x > self.x - self.w) and (bob_1.y < self.y + self.w and bob_1.y > self.y - self.w)):
            health -= 1
            self.enemy_pos()
        if health == 5:
            health_bar = pygame.image.load(full_path("health_5.png"))
        elif health == 4:
            health_bar = pygame.image.load(full_path("health_4.png"))
        elif health == 3:
            health_bar = pygame.image.load(full_path("health_3.png"))
        elif health == 2:
            health_bar = pygame.image.load(full_path("health_2.png"))
        elif health == 1:
            health_bar = pygame.image.load(full_path("health_1.png"))            
        else:
            health_bar = pygame.image.load(full_path("health_0.png"))
            msg("GAME OVER", 400, 300)

    def enemy_death(self):
        global score, is_shot, wave_score, enemy_num
        if ((bulletInst.current_x < self.x + self.w and bulletInst.current_x > self.x) and (bulletInst.current_y < self.y + self.w and bulletInst.current_y > self.y) and is_shot == True):
            score += 1
            wave_score += 1
            is_shot = False
            self.alive = False
            self.hideOffScreen()
            enemy_num -= 1
            
    def hideOffScreen(self):
        self.x = -500
        self.y = -50 * random.randint(1,100)

    def please_revive_i_have_raygun(self):
        self.alive = True
        print("revive called")
        self.enemy_pos()
            

class bulletClass:
    global is_shot
    def __init__(self):
        self.current_x = bob_1.x + (bob_1.w/2)
        self.current_y = bob_1.y + (bob_1.w/2)
        is_shot = False
        self.w = 15
    def bullet_load(self):
        global distance_x, distance_y, final_pos_x, final_pos_y, final_pos
        final_pos = str(pygame.mouse.get_pos())
        self.current_x = bob_1.x + (bob_1.w / 2)
        self.current_y = bob_1.y + (bob_1.w/2)
        final_pos = final_pos.strip("(") 
        final_pos = final_pos.strip(")") 
        i = final_pos.find(",")
        final_pos_x = int(final_pos[:i])
        final_pos_y = int(final_pos[i+1:])
        distance_x = self.current_x - final_pos_x
        distance_y = self.current_y - final_pos_y
        if(distance_y == 0):
            distance_y = 0.1
        if(distance_x == 0):
            distance_x = 0.1
    def bullet_shoot(self): 
        global distance_x, distance_y, final_pos_x, final_pos_y, final_pos, is_shot, bulletR, bullet, bobtempx,bobtempy
        if is_shot == True:
            slope = (distance_y / distance_x)
            if slope == 0:
                slope = .001
            mult=5 #make slower for rocket
            if (self.current_x < 800 + self.w and self.current_x > -self.w and self.current_y > -self.w and self.current_y <500 - self.w): #change for bullet size
                dx= math.cos((math.atan(slope)))
                dy= math.sin((math.atan(slope)))
                #test code (FIX ROCKET ANGLE, IT IS SLIGHTLY OFF)
                dSlope = 360-math.atan2(final_pos_y-bobtempy,final_pos_x-bobtempx)*180/math.pi
                bulletR = pygame.transform.rotate(bullet,dSlope)
                #end of test code
                if((distance_x > 0) and (distance_y>0)) or ((distance_x > 0) and (distance_y<0)):
                    self.current_y -= dy *mult 
                    self.current_x -= dx *mult 
                else:
                    self.current_x += dx *mult
                    self.current_y += dy *mult
                
            else:
                is_shot = False
        else:
            self.current_x = bob_1.x + (bob_1.w/2)
            self.current_y = bob_1.y + (bob_1.w/2)
bullet_1 = None
bulletInst = bullet_1
bulletInst = bulletClass()
bullet_num = 1
def auto_bullet():
    global bullet_num, bulletInst
    bullet_num += 1
    globals()["bullet_" + str(bullet_num)] = bulletInst
    bulletInst = bulletClass()
    
enemy_1 = None
enemyInst = enemy_1
enemyInst = enemyClass()
def auto_enemy():
        global enemy_num, enemyInst
        globals()["enemy_" + str(enemy_num)] = enemyInst
        n.append("enemy_" + str(enemy_num))
        # print("enemy_" + str(enemy_num))
        enemyInst = enemyClass()
        enemyInst.enemy_pos()
        enemy_num += 1
        globals()["enemy_" + str(enemy_num)] = enemyClass()
def enemy_blit(pre):
    screen.blit(enemy,(pre.x,pre.y))

def restart():
    global health_bar, health, wave_num, wave_size, score
    bob_1.y = 372
    bob_1.x = 0
    bob_1.move = 0
    health = 5
    enemy_1.enemy_pos()
    for x in range (0,score):
        globals()[n[x]].please_revive_i_have_raygun()
    score = 0
    wave_num = 1
    wave_size = 4
    ## health_bar = pygame.image.load(full_path("health_5.png"))


# enemies_spawned = 0
ma = 4
def enemy_all():
    global n, ma, wave_score
    for x in range(0,ma):
        globals()[n[x]].load_health()
        enemy_blit(globals()[n[x]])
        globals()[n[x]].enemy_death()
        globals()[n[x]].moveEnemy()
        

wave_num=1
wave_size = 4
wave_size_dead = 4
def do_waves():
    global ma, wave_num, wave_size, wave_score, wave_size_dead
    if score < wave_size_dead:
        enemy_all()
    elif score >= wave_size_dead:
        wave_num += 1
        wave_score = 0
        wave_size = round(wave_size * 1.25)
        wave_size_dead = wave_size + score + 1
        ma = wave_size_dead
        enemy_all()

def prints_score():
    global score
    if score < 10:
        print_score = "Score: 00" + str(score)
        return print_score
    elif score > 9 and score < 100:
        print_score = "Score: 0" + str(score)
        return print_score
    else: 
        print_score = "Score: " + str(score)
        return print_score

def prints_wave():
    global wave_num
    if wave_num < 10:
        print_wave = "Wave: 00" + str(wave_num)
        return print_wave
    elif score > 9 and score < 100:
        print_wave = "Wave: 0" + str(wave_num)
        return print_wave 
    else: 
        print_wave = "Wave: " + str(wave_num)
        return print_wave








scr = 0
for x in range(0,1000):
    auto_enemy()
while scr == 0:
    screen.blit(screen1,(0,0))
    pygame.display.update()
    fpsClock.tick(fps)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_c:
                if creditsOn == False:
                    screen1 = pygame.image.load(full_path("credits.png"))
                    creditsOn = True
            if event.key == K_d:
                if creditsOn == True:
                    screen1 = pygame.image.load(full_path("open_screen.png"))
                    creditsOn = False
        if event.type == MOUSEBUTTONDOWN:
            scr = 1
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

while scr == 1:
    screen.fill((0, 0, 0))
    screen.blit(floor,(0,0))
    screen.blit(bulletR,(bulletInst.current_x,bulletInst.current_y))
    screen.blit(bob,(bob_1.x,bob_1.y))
    # screen.blit(bullet,(current_x,current_y))
    bob_1.bob_move()
    # load_player_health()
    bulletInst.bullet_shoot()
    do_waves()
    msg(prints_score(), 555, 5)
    msg(prints_wave(), 575, 35)
    screen.blit(health_bar,(5,5))
    # enemy_all()
    pygame.display.update()
    fpsClock.tick(fps)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                bob_1.move = "right"
            if event.key == K_a:
                bob_1.move = "left"
            if event.key == K_SPACE:
                if bob_1.jump != "down":
                    bob_1.jump = "up"
                # bob_1.bob_up()
            if event.key == K_r:
                restart()
        if event.type == KEYUP:
            if event.key == K_d:
                bob_1.move = None
                bob = pygame.transform.scale(pygame.image.load(full_path("bob.png")),(62,128))
            if event.key == K_a:
                bob_1.move = None
                bob = pygame.transform.flip(pygame.transform.scale(pygame.image.load(full_path("bob.png")),(62,128)),True,False)
            # if event.key == K_SPACE:
            #     bob_1.bob_down()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if is_shot == False:
                bobtempx= bob_1.x
                bobtempy= bob_1.y
                bulletInst.bullet_load()
                is_shot = True
                auto_bullet()



pygame.display.update()
fpsClock.tick(fps)
