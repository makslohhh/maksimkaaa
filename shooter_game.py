from pygame import *
from random import randint
from time import time as timer
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
font.init()
font1 = font.Font(None,80)
font2 = font.Font(None,36)
score = 0
lost = 0
lives = 3
num_fire = 0
rel_time = False
ufo = "ufo.png"
text_score = font2.render("WIN ",500, (20,60,250))
text_lost = font2.render("LOST ",500, (250,60,60))
text_lives = font2.render("LIVES"+str(lives),500, (250,60,60))


window = display.set_mode((700,500))
display.set_caption("Лабиринт")
background=transform.scale(image.load("galaxy.jpg"),(700,500))
bullets = sprite.Group()

class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y,sx,sy,player_speed):
       super().__init__()
       self.image = transform.scale(image.load(player_image), (sx,sy))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y-= self.speed
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def update(self):
       keys = key.get_pressed()
       if keys[K_DOWN] and self.rect.x > 50:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < 600:
           self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx-10,self.rect.top,20,20,20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 400:
            self.rect.x = randint(80,500)
            self.rect.y = 0
            lost = lost + 1

class Meteor(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 400:
            self.rect.x = randint(80,500)
            self.rect.y = 0
            lost = lost + 1

      
player = Player('rocket.png', 150, 350,60,60,5)
monsters = sprite.Group()
for i in range(1,7):
    monster = Enemy(ufo,randint(80,620),-40,60,60,1)
    monsters.add(monster)

meteors = sprite.Group()
for i in range(1,2):
    meteor = Meteor("asteroid.png",randint(40,60),-40,60,60,randint(1,2))
    meteors.add(meteor)

bullets = sprite.Group()

clock = time.Clock()
FPS = 6

game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    player.fire()
                if num_fire >=5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        window.blit(background,(0,0))

        player.update()
        bullets.update()
        player.reset()
        monsters.update()
        meteors.update()
        bullets.draw(window)
        monsters.draw(window)
        meteors.draw(window)
        ZOV = sprite.groupcollide(bullets,monsters,True,True)

        if rel_time == True:
            now_time = timer() 
            if now_time - last_time <3:
                reload = font2.render('Wait,reload...',1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False
        for c in ZOV:
            score = score+1
            monster = Enemy(ufo,randint(80,620),-40,60,60,1)
            monsters.add(monster)
        if sprite.spritecollide(player,monsters,False) or sprite.spritecollide(player,meteors,False):
            sprite.spritecollide(player,monsters,True)
            sprite.spritecollide(player,meteors,True)
            lives -=1
        if score >= 1:
            window.blit(text_score, (320, 240))
            finish = True
        if lives == 0 or lost>30:
            window.blit(text_lost, (320, 240))
            finish = True

        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        if lives == 3:
            life_color = (0,150,0)
        if lives == 2:
            life_color = (150,150,0)
        if lives == 1:
            life_color = (150,0,0)
        text_life = font1.render(str(lives), 1, life_color)
        window.blit(text_life, (650, 10))


        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        lives = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for m in meteors:
            m.kill()
        time.delay(500)
        for i in range(1,6):
            monster = Enemy(ufo,randint(80,620),-40,60,60,randint(1,3))
            monsters.add(monster)
        for i in range(1,2):
            meteor = Meteor("asteroid.png",randint(80,620),-40,60,60,randint(1,2))
            meteors.add(meteor)
    time.delay(5)