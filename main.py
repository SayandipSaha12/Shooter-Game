import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter Game")

font = pygame.font.SysFont(None, 36)

def load_transform_image(filepath:str, angle:float = 0, scl:float = 1, smoothscale:bool = False) -> pygame.Surface:
    img = pygame.image.load(filepath)
    img = pygame.transform.rotate(img, angle)
    img = pygame.transform.smoothscale_by(img, scl) if smoothscale else pygame.transform.scale_by(img, scl)
    return img


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_transform_image("Art/ship.png", 90, 0.65)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 8
        self.health = 100

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = random.randint(20, 40)
        self.image = load_transform_image("Art/enemy.png", -90, 1)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.size)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(1, 5)
        self.speedx = random.randint(-2, 2)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > SCREEN_HEIGHT or self.rect.left < -25 or self.rect.right > SCREEN_WIDTH + 25:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.size)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(1, 5)
            self.speedx = random.randint(-2, 2)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_transform_image("Art/missile.png", 90, 0.6)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Enemy creation
def create_enemy():
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

def create_enemies(count:int):
    for _ in range(count):
        create_enemy()

create_enemies(8)

score = 0
game_over = False
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.shoot()
            elif event.key == pygame.K_r and game_over:
                game_over = False
                player.health = 100
                player.rect.centerx = SCREEN_WIDTH // 2
                player.rect.bottom = SCREEN_HEIGHT - 10
                score = 0
                for sprite in all_sprites:
                    if isinstance(sprite, Enemy) or isinstance(sprite, Bullet):
                        sprite.kill()
                create_enemies(8)

    if not game_over:
        all_sprites.update()

        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for _ in hits:
            score += 10
            create_enemy()

        hits = pygame.sprite.spritecollide(player, enemies, True)
        for _ in hits:
            player.health -= 20
            create_enemy()
            if player.health <= 0:
                game_over = True

    screen.fill(BLACK)
    all_sprites.draw(screen)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.draw.rect(screen, RED, (SCREEN_WIDTH - 110, 10, 100, 20))
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH - 110, 10, player.health, 20))

    if game_over:
        game_over_text = font.render("GAME OVER - Press R to restart", True, WHITE)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
