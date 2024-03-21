#Создай собственный Шутер!
from pygame import *
from random import randint
font.init()
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
window = display.set_mode((700, 500))
display.set_caption('Догонялки')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
run = True
clock = time.Clock()
FPS = 60
lost = 0


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(0, 450)
            self.rect.y = 0
            lost += 1 
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 595:
            self.rect.x += self.speed 
    def fire (self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -10, 15, 20)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()  
class Asteroid(GameSprite):
    def update(self):
            self.rect.y += self.speed
            if self.rect.y > 500:
                self.rect.x = randint(0, 450)
                self.rect.y = 0
              


bullets = sprite.Group()
asteroid = Asteroid('asteroid.png', randint(0, 450), randint(-100, 0), 5, 80, 50) 
rocket = Player('rocket.png', 10, 400, 20, 80, 100)
monsters = sprite.Group()
for i in range(6):
    monster = Enemy('ufo.png', randint(0, 450), randint(-100, 0), 5, 80, 50) 
    monsters.add(monster)
font1 = font.SysFont('Arial', 36)
kill = 0
finish = 0

while run != False:
    if finish != 1:
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))

        text_win = font1.render('Kill' + str(kill), 1, (255, 255, 255))
        win = font1.render('YOU WIN', 1, (0, 255, 0))
        lose = font1.render('YOU LOSE', 1, (255, 0, 0))
        window.blit(background, (0, 0))
        window.blit(text_lose, (0, 10))
        window.blit(text_win, (0, 40))
        rocket.update()
        rocket.reset()
        asteroid.update()
        asteroid.reset()
        monsters.update()
        bullets.update()
        bullets.draw(window)
        monsters.draw(window)
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == KEYDOWN and e.key == K_SPACE:
                rocket.fire()
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for a in sprites_list:
            kill += 1
            monster = Enemy('ufo.png', randint(0, 450), randint(-100, 0), 5, 80, 50) 
            monsters.add(monster)
        if kill >= 10:
            window.blit(win, (350, 250))
            finish = 1
        if lost >= 10 or len(sprite.spritecollide(rocket, monsters, False)) > 0:
            window.blit(lose, (350, 250))
            finish = 1
        if rocket.rect.colliderect(asteroid.rect):
            window.blit(lose, (350, 250))
            finish = 1

    else:
        time.wait(2000)
        finish = 0
        run = 0
                
    clock.tick(FPS)
    display.update()
    
