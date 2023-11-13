import random

# Definindo as dimensões das matrizes
MTX_RAM = 10
MTX_SWAP = 100

# Gerando a matriz SWAP
matriz_swap = []
for i in range(MTX_SWAP):
    # Número da página
    N = i
    # Instrução
    I = i + 1
    # Dado
    D = random.randint(1, 50)
    # Bit de acesso
    R = 0
    # Bit de modificação
    M = 0
    # Tempo de envelhecimento
    T = random.randint(100, 9999)
    matriz_swap.append([N, I, D, R, M, T])

# Gerando a matriz RAM
matriz_ram = []
for i in range(MTX_RAM):
    # Número da página
    N = random.randint(0, len(matriz_swap) - 1)
    # Instrução
    I = matriz_swap[N][1]
    # Dado
    D = matriz_swap[N][2]
    # Bit de acesso
    R = 1
    # Bit de modificação
    M = matriz_swap[N][4]
    # Tempo de envelhecimento
    T = matriz_swap[N][5]

    # Criando uma nova lista para armazenar os valores da página
    pagina = [N, I, D, R, M, T]

    # Adicionando a página à matriz RAM
    matriz_ram.append(pagina)

# Exibindo as matrizes no início
print("Matriz RAM no início:")
for pagina in matriz_ram:
    print(pagina)

print("\nMatriz SWAP no início:")
for pagina in matriz_swap:
    print(pagina)

# Definindo a função FIFO
def fifo(matriz_ram, matriz_swap, instrucao):
    # Encontrar a página na RAM que foi carregada há mais tempo
    pagina_antiga = min(matriz_ram, key=lambda pagina: pagina[5])  # O tempo de envelhecimento é o índice 5

    # Salvar a página antiga em SWAP se o bit M=1
    if pagina_antiga[4] == 1:
        matriz_swap[pagina_antiga[0]] = pagina_antiga.copy()
        pagina_antiga[4] = 0

    # Encontrar a nova página na SWAP
    for i, pagina in enumerate(matriz_swap):
        if pagina[1] == instrucao:
            # Carregar a nova página na RAM
            matriz_ram[matriz_ram.index(pagina_antiga)] = pagina.copy()
            break

# Definindo as funções para os outros algoritmos
def nru(matriz_ram, matriz_swap, instrucao):
    classes = {
        0: [],
        1: [],
        2: [],
        3: [],
    }

    # Classificar páginas na RAM em classes de acordo com os bits R e M
    for pagina in matriz_ram:
        class_key = (pagina[3] << 1) | pagina[4]
        classes[class_key].append(pagina)

    # Escolher aleatoriamente uma página da classe mais baixa não vazia
    for class_key in range(4):
        if classes[class_key]:
            pagina_substituida = random.choice(classes[class_key])
            break

    # Substituir a página escolhida pela nova página da SWAP
    for i, pagina in enumerate(matriz_swap):
        if pagina[1] == instrucao:
            matriz_ram[matriz_ram.index(pagina_substituida)] = pagina.copy()
            break

def fifo_sc(matriz_ram, matriz_swap, instrucao):
    # Encontrar a primeira página na RAM que não foi recentemente referenciada (bit R = 0)
    pagina_nao_referenciada = None
    for pagina in matriz_ram:
        if pagina[3] == 0:
            pagina_nao_referenciada = pagina
            break

    # Se não houver página não referenciada, escolher a mais antiga
    if not pagina_nao_referenciada:
        pagina_nao_referenciada = min(matriz_ram, key=lambda pagina: pagina[5])  # O tempo de envelhecimento é o índice 5

    # Salvar a página não referenciada em SWAP se o bit M=1
    if pagina_nao_referenciada[4] == 1:
        matriz_swap[pagina_nao_referenciada[0]] = pagina_nao_referenciada.copy()
        pagina_nao_referenciada[4] = 0

    # Encontrar a nova página na SWAP
    for i, pagina in enumerate(matriz_swap):
        if pagina[1] == instrucao:
            # Carregar a nova página na RAM
            matriz_ram[matriz_ram.index(pagina_nao_referenciada)] = pagina.copy()
            break

def relogio(matriz_ram, matriz_swap, instrucao):
    # Inicializar o ponteiro do relógio
    ponteiro = 0

    # Procurar uma página com bit R = 0
    while True:
        pagina = matriz_ram[ponteiro]
        if pagina[3] == 0:
            # Salvar a página em SWAP se o bit M=1
            if pagina[4] == 1:
                matriz_swap[pagina[0]] = pagina.copy()
                pagina[4] = 0

            # Encontrar a nova página na SWAP
            for i, nova_pagina in enumerate(matriz_swap):
                if nova_pagina[1] == instrucao:
                    # Carregar a nova página na RAM
                    matriz_ram[ponteiro] = nova_pagina.copy()
                    return
        else:
            # Resetar o bit R para 0
            pagina[3] = 0

        # Avançar o ponteiro do relógio
        ponteiro = (ponteiro + 1) % len(matriz_ram)

def ws_clock(matriz_ram, matriz_swap, instrucao):
    # Inicializar o ponteiro do relógio
    ponteiro = 0

    # Sortear um número para verificar o envelhecimento da página (EP)
    envelhecimento_pagina = random.randint(100, 9999)

    # Definir uma variável para verificar se o loop já passou por todas as páginas
    todas_as_paginas_passadas = False

    while True:
        pagina = matriz_ram[ponteiro]

        # Verificar o envelhecimento da página
        if envelhecimento_pagina <= pagina[5]:
            # A página ainda está no conjunto de trabalho
            # Resetar o bit R para 0
            pagina[3] = 0
        else:
            # A página não faz mais parte do conjunto de trabalho
            # Salvar a página em SWAP se o bit M=1
            if pagina[4] == 1:
                matriz_swap[pagina[0]] = pagina.copy()
                pagina[4] = 0

            # Encontrar a nova página na SWAP
            for i, nova_pagina in enumerate(matriz_swap):
                if nova_pagina[1] == instrucao:
                    # Carregar a nova página na RAM
                    matriz_ram[ponteiro] = nova_pagina.copy()
                    return

        # Avançar o ponteiro do relógio
        ponteiro = (ponteiro + 1) % len(matriz_ram)

        # Verificar se todas as páginas já foram verificadas
        if ponteiro == 0:
            todas_as_paginas_passadas = True

        # Se todas as páginas já foram verificadas, sair do loop
        if todas_as_paginas_passadas:
            break

# Testando os algoritmos
algoritmos = {
    "FIFO": fifo,
    "NRU": nru,
    "FIFO-SC": fifo_sc,
    "RELÓGIO": relogio,
    "WS-CLOCK": ws_clock,
}

for nome_algoritmo, algoritmo in algoritmos.items():
    print(f"\nExecutando {nome_algoritmo}")
    algoritmo(matriz_ram, matriz_swap, 42)

# Exibindo as matrizes no final
print("\nMatriz RAM no final:")
for pagina in matriz_ram:
    print(pagina)

print("\nMatriz SWAP no final:")
for pagina in matriz_swap:
    print(pagina)