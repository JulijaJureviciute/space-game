import pygame
from pygame.locals import *
from pygame import mixer
import random

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

clock = pygame.time.Clock()
fps = 60
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Impact")

pygame.font.init()
font1 = pygame.font.SysFont("Arial", 30)
font2 = pygame.font.SysFont("Arial", 40)

explosions = pygame.mixer.Sound("explosion.mp3")
explosions.set_volume(0.25)

shot = pygame.mixer.Sound("gunshot.mp3")
shot.set_volume(0.25)

hit = pygame.mixer.Sound("hit.mp3")
hit.set_volume(0.25)

countdown = 3
last_count = pygame.time.get_ticks()

red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

run = True
pygame.init()

bg = pygame.image.load("images.jpg")
bg_transformed = pygame.transform.scale_by(bg, 1.5)


def draw_bg():
    screen.blit(bg_transformed, (0, 0))


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("spaceship.png")
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        speed = 8

        cooldown = 100
        spaceship_dead = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed
        if key[pygame.K_DOWN] and self.rect.bottom < screen_height:
            self.rect.y += speed
        if key[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= speed

        time_now = pygame.time.get_ticks()

        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            shot.play()
            bullet = Bullets(self.rect.right, self.rect.centery)
            bullet_group.add(bullet)
            self.last_shot = time_now

        self.mask = pygame.mask.from_surface(self.image)

        pygame.draw.rect(screen, red, (15, 15, self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(
                screen,
                green,
                (
                    15,
                    15,
                    int(self.rect.width * (self.health_remaining / self.health_start)),
                    15,
                ),
            )
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            spaceship_dead = -1
        return spaceship_dead


class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png")
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.x += 5
        if self.rect.right > 1000:
            self.kill()
        if pygame.sprite.spritecollide(
            self, alien_group, True, pygame.sprite.collide_mask
        ):
            hit.play()
            self.kill()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)
        if pygame.sprite.spritecollide(
            self, monster_group, False, pygame.sprite.collide_mask
        ):
            hit.play()
            self.kill()
            monster.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)


class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("alien.png")
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x -= 1
        self.rect.y += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 60 and (
            self.rect.y < screen_height and self.rect.y > 0
        ):
            self.move_direction *= -1
            self.move_counter *= self.move_direction
        if self.rect.left < 10:
            spaceship.health_remaining -= 1
            self.kill()
        self.mask = pygame.mask.from_surface(self.image)


def create_aliens():
    alien = Aliens((screen_width + 100), random.randint(200, screen_height - 100))
    alien_group.add(alien)


class Alien_bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png")
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.x -= 3
        if self.rect.left < 10:
            self.kill()
        if pygame.sprite.spritecollide(
            self, spaceship_group, False, pygame.sprite.collide_mask
        ):
            explosions.play()
            self.kill()
            spaceship.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 8):
            img = pygame.image.load(f"explosions/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


class Trees(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bg.png")
        self.image = pygame.transform.scale(self.image, (100, random.randint(100, 200)))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_direction = 1
        self.collision_counter = 0

    def update(self):
        self.rect.x -= 1
        if self.rect.left < -100:
            self.kill()
        self.mask = pygame.mask.from_surface(self.image)
        if pygame.sprite.spritecollide(
            self, spaceship_group, False, pygame.sprite.collide_mask
        ):
            explosions.play()
            self.collision_counter += 1
            if self.collision_counter == 1:
                spaceship.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)


def create_trees():
    trees = Trees((screen_width + 100), (screen_height - 80))
    tree_group.add(trees)


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, health):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("monster.png")
        self.image = pygame.transform.scale(self.image, (400, 500))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_count = 0
        self.health_remaining = health
        self.health_start = health
        self.move_y = 0
        self.move_direction = 1

    def update(self):
        monster_dead = 0
        if self.move_count < 200:
            self.rect.x -= 1
            self.move_count += 1
        if self.move_count >= 200:
            self.rect.y += self.move_direction
            self.move_y += 1
            if abs(self.move_y) > 80:
                self.move_direction *= -1
                self.move_y *= self.move_direction
        self.mask = pygame.mask.from_surface(self.image)
        pygame.draw.rect(screen, red, (800, 15, int(self.rect.width / 3), 15))
        if self.health_remaining > 0:
            pygame.draw.rect(
                screen,
                green,
                (
                    800,
                    15,
                    (
                        int(self.rect.width / 3
                        * self.health_remaining / self.health_start)
                    ),
                    15,
                ),
            )
        if self.health_remaining <= 0:
            explosions.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            monster_dead = 1
        return monster_dead


class Monster_bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.x -= 3
        if self.rect.left < 10:
            self.kill()
        if pygame.sprite.spritecollide(
            self, spaceship_group, False, pygame.sprite.collide_mask
        ):
            explosions.play()
            self.kill()
            spaceship.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)


spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
spaceship = Spaceship((screen_width - 900), int(screen_height / 2), 5)
spaceship_group.add(spaceship)
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
tree_group = pygame.sprite.Group()
monster_group = pygame.sprite.Group()
monster = Monster((screen_width + 100), (screen_height - 400), 50)
monster_group.add(monster)
monster_bullet_group = pygame.sprite.Group()


alien_cooldown = 6000
last_alien_time = pygame.time.get_ticks()
last_alien_shot = pygame.time.get_ticks()
last_monster_shot = pygame.time.get_ticks()
last_monster_time = pygame.time.get_ticks()
last_tree = pygame.time.get_ticks()
alien_bullet_cooldown = 1000
generate_trees = 5000
total_alien_count = 0
monster_dead = 0
spaceship_dead = 0
alien_count_on_screen = 2

while run:
    clock.tick(fps)
    draw_bg()
    

    if countdown == 0:
        time_now = pygame.time.get_ticks()
        if time_now - last_tree > generate_trees:
            create_trees()
            last_tree = time_now

        if (
            time_now - last_alien_shot > alien_bullet_cooldown
            and len(alien_bullet_group) < 10
            and len(alien_group) > 0
        ):
            attacking_aliens = random.choice(alien_group.sprites())
            alien_bullet = Alien_bullets(
                attacking_aliens.rect.left, attacking_aliens.rect.centery
            )
            alien_bullet_group.add(alien_bullet)
            last_alien_shot = time_now

    if monster_dead == 0 and spaceship_dead == 0:
        alien_group.update()
        spaceship_dead = spaceship.update()
        bullet_group.update()
        alien_bullet_group.update()
        tree_group.update()

        if total_alien_count == int(alien_count_on_screen):
            monster_dead = monster.update()
            monster_group.update()
            monster_bullet_group.draw(screen)
            monster_bullet_group.update()
            if (
                time_now - last_monster_shot > alien_bullet_cooldown
                and len(monster_bullet_group) < 20
                and len(monster_group) > 0
            ):
                attacking_monster = random.choice(monster_group.sprites())
                monster_bullet = Monster_bullets(
                    attacking_monster.rect.centerx, attacking_monster.rect.centery
                )
                monster_bullet_group.add(monster_bullet)
                last_monster_shot = time_now

            
        if total_alien_count < int(alien_count_on_screen):
            time_now = pygame.time.get_ticks()
            if time_now - last_alien_time > alien_cooldown:
                create_aliens()
                last_alien_time = time_now
                total_alien_count += 1

    monster_bullet_group.update()
    monster_group.draw(screen)
    alien_group.draw(screen)
    explosion_group.update()
    explosion_group.draw(screen)
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_bullet_group.draw(screen)
    tree_group.draw(screen)

    if monster_dead == 1:
        draw_text(
            "YOU WON!",
            font1,
            white,
            int(screen_width / 2 - 110),
            int(screen_height / 2 - 50),
        )
    if spaceship_dead == -1:
        draw_text(
            "GAME OVER!",
            font1,
            white,
            int(screen_width / 2 - 110),
            int(screen_height / 2 - 50),
        )

    if countdown > 0:
        draw_text(
            "GET READY!",
            font2,
            white,
            int(screen_width / 2 - 110),
            int(screen_height / 2 - 50),
        )
        draw_text(
            str(countdown),
            font2,
            white,
            int(screen_width / 2 - 10),
            int(screen_height / 2),
        )
        current_timer = pygame.time.get_ticks()
        if current_timer - last_count > 1000:
            countdown -= 1
            last_count = current_timer

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()