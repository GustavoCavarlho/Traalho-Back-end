import pygame
import random

# ---------------------------
# CONFIG
# ---------------------------
pygame.init()
LARGURA, ALTURA = 900, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("RPG de Cartas")

fonte = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

# ---------------------------
# CARTAS
# ---------------------------
cartas = [
    {"nome": "Espada Sombria", "dano": 25, "cura": 0, "defesa": 0},
    {"nome": "Bola de Fogo", "dano": 30, "cura": 0, "defesa": 0},
    {"nome": "Cura Divina", "dano": 0, "cura": 20, "defesa": 0},
    {"nome": "Escudo", "dano": 0, "cura": 0, "defesa": 20},
    {"nome": "Flecha Rápida", "dano": 15, "cura": 0, "defesa": 0},
]

# ---------------------------
# ESTADO
# ---------------------------
jogador = {"vida": 100, "defesa": 0}
inimigo = {"vida": 100, "defesa": 0}

mao = random.sample(cartas, 3)
mensagem = ""

# ---------------------------
# FUNÇÕES
# ---------------------------
def aplicar_carta(atacante, defensor, carta):
    global mensagem

    mensagem = f"{carta['nome']} usado!"

    if carta["dano"] > 0:
        dano = max(0, carta["dano"] - defensor["defesa"])
        defensor["vida"] -= dano
        mensagem += f" | -{dano} dano"

    if carta["cura"] > 0:
        atacante["vida"] = min(100, atacante["vida"] + carta["cura"])
        mensagem += f" | +{carta['cura']} cura"

    if carta["defesa"] > 0:
        atacante["defesa"] = carta["defesa"]
        mensagem += f" | defesa {carta['defesa']}"

def reset_defesa():
    jogador["defesa"] = 0
    inimigo["defesa"] = 0

def inimigo_joga():
    carta = random.choice(cartas)
    aplicar_carta(inimigo, jogador, carta)

def comprar_mao():
    return random.sample(cartas, 3)

# ---------------------------
# DESENHO
# ---------------------------
def desenhar():
    tela.fill((25, 25, 35))

    # STATUS
    txt_j = fonte.render(f"Jogador: {jogador['vida']} HP | DEF {jogador['defesa']}", True, (255,255,255))
    txt_i = fonte.render(f"Inimigo: {inimigo['vida']} HP | DEF {inimigo['defesa']}", True, (255,255,255))

    tela.blit(txt_j, (20, 20))
    tela.blit(txt_i, (20, 50))

    # CARTAS
    for i, carta in enumerate(mao):
        x = 50 + i * 280
        y = 350

        rect = pygame.Rect(x, y, 250, 180)
        pygame.draw.rect(tela, (70, 70, 120), rect)
        pygame.draw.rect(tela, (255, 255, 255), rect, 2)

        nome = fonte.render(carta["nome"], True, (255,255,255))
        tela.blit(nome, (x + 10, y + 10))

        stats = fonte.render(
            f"ATK:{carta['dano']} CURA:{carta['cura']} DEF:{carta['defesa']}",
            True,
            (200,200,200)
        )
        tela.blit(stats, (x + 10, y + 50))

        carta["rect"] = rect

    # MENSAGEM
    msg = fonte.render(mensagem, True, (255, 255, 0))
    tela.blit(msg, (20, 100))

    pygame.display.update()

# ---------------------------
# LOOP
# ---------------------------
rodando = True

while rodando:
    clock.tick(60)

    desenhar()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            for carta in mao:
                if carta["rect"].collidepoint(pos):
                    aplicar_carta(jogador, inimigo, carta)

                    reset_defesa()

                    if inimigo["vida"] > 0:
                        inimigo_joga()
                        reset_defesa()

                    mao = comprar_mao()

    if jogador["vida"] <= 0:
        mensagem = "💀 Você perdeu!"
    if inimigo["vida"] <= 0:
        mensagem = "🏆 Você venceu!"

pygame.quit()