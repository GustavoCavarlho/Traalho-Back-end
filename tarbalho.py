import random

# ---------------------------
# CARTAS
# ---------------------------
cartas = [
    {"nome": "Espada Sombria", "dano": 25, "cura": 0, "defesa": 0},
    {"nome": "Bola de Fogo", "dano": 30, "cura": 0, "defesa": 0},
    {"nome": "Cura Divina", "dano": 0, "cura": 20, "defesa": 0},
    {"nome": "Escudo Mágico", "dano": 0, "cura": 0, "defesa": 20},
    {"nome": "Flecha Rápida", "dano": 15, "cura": 0, "defesa": 0},
]

# ---------------------------
# JOGADOR E INIMIGO
# ---------------------------
jogador = {
    "vida": 100,
    "defesa": 0
}

inimigo = {
    "vida": 100,
    "defesa": 0
}


# FUNÇÕES

def comprar_carta():
    return random.choice(cartas)

def aplicar_carta(atacante, defensor, carta):
    print(f"\n🔥 Usou: {carta['nome']}")

    # dano
    if carta["dano"] > 0:
        dano_final = max(0, carta["dano"] - defensor["defesa"])
        defensor["vida"] -= dano_final
        print(f"⚔️ Dano causado: {dano_final}")

    # cura
    if carta["cura"] > 0:
        atacante["vida"] += carta["cura"]
        print(f"💚 Cura: {carta['cura']}")

    # defesa temporária
    if carta["defesa"] > 0:
        atacante["defesa"] = carta["defesa"]
        print(f"🛡️ Defesa aumentada: {carta['defesa']}")

def mostrar_status():
    print("\n======================")
    print(f"👤 Jogador: {jogador['vida']} HP | Defesa: {jogador['defesa']}")
    print(f"👾 Inimigo: {inimigo['vida']} HP | Defesa: {inimigo['defesa']}")
    print("======================\n")


# LOOP 
print("🎴 RPG DE CARTAS INICIADO!\n")

while jogador["vida"] > 0 and inimigo["vida"] > 0:

    mostrar_status()

    carta1 = comprar_carta()
    carta2 = comprar_carta()
    carta3 = comprar_carta()

    mao = [carta1, carta2, carta3]

    print("Suas cartas:")
    for i, c in enumerate(mao):
        print(f"{i+1} - {c['nome']} (ATQ:{c['dano']} CURA:{c['cura']} DEF:{c['defesa']})")

    escolha = int(input("\nEscolha uma carta (1-3): ")) - 1
    escolha = max(0, min(escolha, 2))

    aplicar_carta(jogador, inimigo, mao[escolha])

    # reset defesa após turno
    jogador["defesa"] = 0

    # turno inimigo (IA simples)
    carta_inimigo = comprar_carta()
    aplicar_carta(inimigo, jogador, carta_inimigo)

    inimigo["defesa"] = 0

# ---------------------------
# FIM DO JOGO
# ---------------------------
print("\n🏁 FIM DE JOGO!")

if jogador["vida"] > 0:
    print("🏆 Você venceu!")
else:
    print("💀 Você foi derrotado!")