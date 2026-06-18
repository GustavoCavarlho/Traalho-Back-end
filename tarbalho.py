import pygame
import random

pygame.init()

WIDTH, HEIGHT = 900, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Clash Royale (Pygame)")

font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

# -----------------------
# CARDS
# -----------------------
CARDS = {
    "soldado": {"hp": 5, "atk": 1, "color": (0, 200, 0)},
    "arqueiro": {"hp": 3, "atk": 2, "color": (0, 150, 255)},
    "gigante": {"hp": 10, "atk": 3, "color": (200, 100, 0)},
}

# -----------------------
# UNIT
# -----------------------
class Unit:
    def __init__(self, name, x, y, owner):
        self.name = name
        self.hp = CARDS[name]["hp"]
        self.atk = CARDS[name]["atk"]
        self.color = CARDS[name]["color"]
        self.x = x
        self.y = y
        self.owner = owner
        self.speed = 1 if owner == "player" else -1
        self.cooldown = 0

    def update(self):
        self.x += self.speed
        if self.cooldown > 0:
            self.cooldown -= 1

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, (self.x, self.y, 20, 20))
        hp_text = font.render(str(self.hp), True, (255, 255, 255))
        surf.blit(hp_text, (self.x, self.y - 10))

# -----------------------
# GAME STATE
# -----------------------
player_units = []
enemy_units = []

player_hp = 20
enemy_hp = 20

deck = ["soldado", "arqueiro"]
message = ""

# -----------------------
# SPAWN
# -----------------------
def spawn(card, owner):
    if owner == "player":
        player_units.append(Unit(card, 50, 300, "player"))
    else:
        enemy_units.append(Unit(card, 820, 100, "enemy"))

# -----------------------
# CHEST
# -----------------------
def open_chest():
    global message
    reward = random.choice(list(CARDS.keys()))
    deck.append(reward)
    message = f"Você ganhou {reward.upper()}!"

# -----------------------
# COMBAT (CORRIGIDO)
# -----------------------
def combat():
    global player_hp, enemy_hp

    for p in player_units:
        for e in enemy_units:
            if abs(p.x - e.x) < 20:

                if p.cooldown == 0:
                    e.hp -= p.atk
                    p.cooldown = 30

                if e.cooldown == 0:
                    p.hp -= e.atk
                    e.cooldown = 30

    # remove mortos com segurança
    player_units[:] = [u for u in player_units if u.hp > 0]
    enemy_units[:] = [u for u in enemy_units if u.hp > 0]

# -----------------------
# Desenho
# -----------------------
def draw():
    screen.fill((30, 30, 30))

    pygame.draw.line(screen, (255, 255, 255), (0, 200), (900, 200), 2)

    pygame.draw.rect(screen, (0, 255, 0), (20, 250, 40, 100))
    pygame.draw.rect(screen, (255, 0, 0), (840, 50, 40, 100))

    p_hp = font.render(f"PLAYER HP: {player_hp}", True, (255, 255, 255))
    e_hp = font.render(f"ENEMY HP: {enemy_hp}", True, (255, 255, 255))
    screen.blit(p_hp, (20, 20))
    screen.blit(e_hp, (650, 20))

    msg = font.render(message, True, (255, 255, 0))
    screen.blit(msg, (300, 20))

    for u in player_units + enemy_units:
        u.draw(screen)

    pygame.display.update()

# -----------------------
# LOOP
# -----------------------
running = True
frame = 0

while running:
    clock.tick(60)
    frame += 1

    if frame % 120 == 0:
        spawn(random.choice(list(CARDS.keys())), "enemy")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_1:
                spawn("soldado", "player")
            if event.key == pygame.K_2:
                spawn("arqueiro", "player")
            if event.key == pygame.K_3:
                spawn("gigante", "player")

            if event.key == pygame.K_c:
                open_chest()

    # update
    for u in player_units:
        u.update()
    for u in enemy_units:
        u.update()

    combat()

    # TORRES (CORRIGIDO - SEM CRASH)
    for u in player_units[:]:
        if u.x > 860:
            enemy_hp -= u.atk
            player_units.remove(u)

    for u in enemy_units[:]:
        if u.x < 20:
            player_hp -= u.atk
            enemy_units.remove(u)

    draw()

    if player_hp <= 0 or enemy_hp <= 0:
        running = False

pygame.quit()
print("Fim de jogo!")