from pygame import *

display.set_caption("Maze Game")
mw = display.set_mode((700, 500))
background = (0, 50, 255)

class gamesprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        mw.blit(self.image,(self.rect.x, self.rect.y))
class player(gamesprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        gamesprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        if pacman.rect.x <= 700-80 and pacman.x_speed > 0 or pacman.rect.x >= 0 and pacman.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if pacman.rect.y <= 700-80 and pacman.y_speed > 0 or pacman.rect.y >= 0 and pacman.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.y_speed = 0
                if p.rect.bottom > self.rect.top:
                    self.rect.top = p.rect.bottom

    def fire(self):
        bullet = bullet('bullet.png',self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)
    
    
class enemy(gamesprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        gamesprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        if self.rect.x <= 500:
            self.side = "right"
        if self.rect.x >= 700 - 80:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class bullet(gamesprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        gamesprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 700 + 10:
            self.kill()
            
bullets = sprite.Group()
barriers = sprite.Group()
monsters = sprite.Group()
plath = gamesprite("platformh.png", 700 / 2 - 500 / 3, 500 / 2, 300, 50)
platv = gamesprite("platformv.png", 450, 100, 50, 400)
pacman = player('pacman.png', 5, 500 - 80, 80, 80, 0, 0)
barriers.add(plath)
barriers.add(platv)
final_sprite = gamesprite('win_trophy.png', 700 - 85, 500 - 100, 80, 80)
monster1 = enemy('hero.png', 700 - 80, 500 - 200, 80, 80, 10)
monster2 = enemy('cyborg.png', 700 - 80, 500 - 400, 80, 80, 10)
monsters.add(monster1)
monsters.add(monster2)

finish = False

run = True
while run:
    time.delay(500)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                pacman.x_speed = -50
            elif e.key == K_RIGHT:
                pacman.x_speed = 50
            elif e.key == K_UP:
                pacman.y_speed = -50
            elif e.key == K_DOWN:
                pacman.y_speed = 50
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                pacman.x_speed = 0
            elif e.key == K_RIGHT:
                pacman.x_speed = 0
            elif e.key == K_UP:
                pacman.y_speed = 0
            elif e.key == K_DOWN:
                pacman.y_speed = 0
    if not finish:
        mw.fill(background)
        barriers.draw(mw)
        bullets.draw(mw)
        final_sprite.reset()   

        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(mw)     
        sprite.groupcollide(bullets, barriers, True, False)

    pacman.reset()
    pacman.update()
    plath.reset()
    plath.update()
    platv.reset()
    platv.update()
    bullets.update()

    if sprite.spritecollide(pacman, monsters, False):
       finish = True
       img = image.load('game-over_1.png')
       d = img.get_width() // img.get_height()
       mw.fill((255, 255, 255))
       mw.blit(transform.scale(img, (500 * d, 500)), (90, 0))
    if sprite.collide_rect(pacman, final_sprite):
       finish = True
       img = image.load('thumbsup.png')
       mw.fill((255, 255, 255))
       mw.blit(transform.scale(img, (700, 500)), (0, 0))

    display.update()