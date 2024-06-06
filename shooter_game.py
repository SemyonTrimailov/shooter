#Создай собственный Шутер!


from typing import Any
from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

score = 0
lost = 0
goal = 10
max_lost = 3

mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = "galaxy.jpg" 
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"

monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, randint(80, 620), -40, 80,50, randint(1,3))
    monsters.add(monster)

bullets = sprite.Group()


font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
win = font1.render('Ты победил!', True, (255,255,255))
lose = font1.render('Ты проиграл (', True, (255,255,255))

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Стрелялка")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

game = True
finish = False
clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()
        
    if not finish:
        window.blit(background,(0,0))
        ship.update()
        ship.reset()
        
        text = font2.render('Счет: ' + str(score), 1,(255,255,255))
        window.blit(text,(10,20))
        text_lost = font2.render('Пропустил:  ' + str(lost), 1,(255,255,255))
        window.blit(text_lost,(10,50))
        
        monsters.update()
        monsters.draw(window)

        bullets.update()
        bullets.draw(window)

        collides =sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, 620), -40, 80,50, randint(1,3))
            monsters.add(monster)
        
        if score >= goal:
            finish = True
            window.blit(win, (200,200))

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range (5):
            monster = Enemy(img_enemy, randint(80, 620), -40, 80,50, randint(1,3))
            monsters.add(monster)

       
    display.update()
    clock.tick(FPS)