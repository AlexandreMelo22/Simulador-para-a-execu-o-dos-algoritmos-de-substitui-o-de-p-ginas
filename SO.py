import random  # Importa o módulo random para gerar números aleatórios.

# Define as dimensões das matrizes.
MTX_RAM = 10
MTX_SWAP = 100

# Gera a matriz SWAP.
matriz_swap = []
for i in range(MTX_SWAP):
    N = i
    I = i + 1
    D = random.randint(1, 50)
    R = 0
    M = 0
    T = random.randint(100, 9999)
    matriz_swap.append([N, I, D, R, M, T])

# Gera a matriz RAM.
matriz_ram = []
for i in range(MTX_RAM):
    N = random.randint(0, len(matriz_swap) - 1)
    I = matriz_swap[N][1]
    D = matriz_swap[N][2]
    R = 1
    M = matriz_swap[N][4]
    T = matriz_swap[N][5]
    pagina = [N, I, D, R, M, T]
    matriz_ram.append(pagina)

# Exibe as matrizes no início.
print("Matriz RAM no início:")
for pagina in matriz_ram:
    print(pagina)

print("\nMatriz SWAP no início:")
for pagina in matriz_swap:
    print(pagina)

# Define a função FIFO.
def fifo(matriz_ram, matriz_swap, instrucao):
    # Encontra a página na RAM que foi carregada há mais tempo.
    pagina_antiga = min(matriz_ram, key=lambda pagina: pagina[5])  # O tempo de envelhecimento é o índice 5.

    # Salva a página antiga em SWAP se o bit M=1.
    if pagina_antiga[4] == 1:
        matriz_swap[pagina_antiga[0]] = pagina_antiga.copy()
        pagina_antiga[4] = 0

    # Encontra a nova página na SWAP.
    for i, pagina in enumerate(matriz_swap):
        if pagina[1] == instrucao:
            # Carrega a nova página na RAM.
            matriz_ram[matriz_ram.index(pagina_antiga)] = pagina.copy()
            break

# Define a função NRU.
def nru(matriz_ram, matriz_swap, instrucao):
    # Cria classes para classificar páginas na RAM de acordo com os bits R e M.
    classes = {
        0: [],
        1: [],
        2: [],
        3: [],
    }

    for pagina in matriz_ram:
        class_key = (pagina[3] << 1) | pagina[4]
        classes[class_key].append(pagina)

    # Escolhe aleatoriamente uma página da classe mais baixa não vazia.
    for class_key in range(4):
        if classes[class_key]:
            pagina_substituida = random.choice(classes[class_key])
            break

    # Substitui a página escolhida pela nova página da SWAP.
    for i, pagina in enumerate(matriz_swap):
        if pagina[1] == instrucao:
            matriz_ram[matriz_ram.index(pagina_substituida)] = pagina.copy()
            break

# Define a função FIFO-SC.
def fifo_sc(matriz_ram, matriz_swap, instrucao):
    # Encontra a primeira página na RAM que não foi recentemente referenciada (bit R = 0).
    pagina_nao_referenciada = None
    for pagina in matriz_ram:
        if pagina[3] == 0:
            pagina_nao_referenciada = pagina
            break

    # Se não houver página não referenciada, escolhe a mais antiga.
    if not pagina_nao_referenciada:
        pagina_nao_referenciada = min(matriz_ram, key=lambda pagina: pagina[5])  # O tempo de envelhecimento é o índice 5.

    # Salva a página não referenciada em SWAP se o bit M=1.
    if pagina_nao_referenciada[4] == 1:
        matriz_swap[pagina_nao_referenciada[0]] = pagina_nao_referenciada.copy()
        pagina_nao_referenciada[4] = 0

    # Encontra a nova página na SWAP.
    for i, pagina in enumerate(matriz_swap):
        if pagina[1] == instrucao:
            # Carrega a nova página na RAM.
            matriz_ram[matriz_ram.index(pagina_nao_referenciada)] = pagina.copy()
            break

# Define a função RELÓGIO.
def relogio(matriz_ram, matriz_swap, instrucao):
    # Inicializa o ponteiro do relógio.
    ponteiro = 0

    # Procura uma página com bit R = 0.
    while True:
        pagina = matriz_ram[ponteiro]
        if pagina[3] == 0:
            # Salva a página em SWAP se o bit M=1.
            if pagina[4] == 1:
                matriz_swap[pagina[0]] = pagina.copy()
                pagina[4] = 0

            # Encontra a nova página na SWAP.
            for i, nova_pagina in enumerate(matriz_swap):
                if nova_pagina[1] == instrucao:
                    # Carrega a nova página na RAM.
                    matriz_ram[ponteiro] = nova_pagina.copy()
                    return
        else:
            # Reseta o bit R para 0.
            pagina[3] = 0

        # Avança o ponteiro do relógio.
        ponteiro = (ponteiro + 1) % len(matriz_ram)

# Define a função WS-CLOCK.
def ws_clock(matriz_ram, matriz_swap, instrucao):
    # Inicializa o ponteiro do relógio.
    ponteiro = 0

    # Sorteia um número para verificar o envelhecimento da página (EP).
    envelhecimento_pagina = random.randint(100, 9999)

    # Define uma variável para verificar se o loop já passou por todas as páginas.
    todas_as_paginas_passadas = False

    while True:
        pagina = matriz_ram[ponteiro]

        # Verifica o envelhecimento da página.
        if envelhecimento_pagina <= pagina[5]:
            # A página ainda está no conjunto de trabalho.
            # Reseta o bit R para 0.
            pagina[3] = 0
        else:
            # A página não faz mais parte do conjunto de trabalho.
            # Salva a página em SWAP se o bit M=1.
            if pagina[4] == 1:
                matriz_swap[pagina[0]] = pagina.copy()
                pagina[4] = 0

            # Encontra a nova página na SWAP.
            for i, nova_pagina in enumerate(matriz_swap):
                if nova_pagina[1] == instrucao:
                    # Carrega a nova página na RAM.
                    matriz_ram[ponteiro] = nova_pagina.copy()
                    return

        # Avança o ponteiro do relógio.
        ponteiro = (ponteiro + 1) % len(matriz_ram)

        # Verifica se todas as páginas já foram verificadas.
        if ponteiro == 0:
            todas_as_paginas_passadas = True

        # Se todas as páginas já foram verificadas, sai do loop.
        if todas_as_paginas_passadas:
            break

# Testa os algoritmos.
algoritmos = {
    "FIFO": fifo,
    "NRU": nru,
    "FIFO-SC": fifo_sc,
    "RELÓGIO": relogio,
    "WS-CLOCK": ws_clock,
}

for nome_algoritmo, algoritmo in algoritmos.items():
    print(f"\nExecutando {nome_algoritmo}")
    algoritmo(matriz_ram.copy(), matriz_swap.copy(), 42)

    print("\nMatriz RAM:")
    for pagina in matriz_ram:
        print(pagina)

    print("\nMatriz SWAP:")
    for pagina in matriz_swap:
        print(pagina)

    # Gera novas páginas para a próxima execução.
    matriz_ram = []
    for i in range(MTX_RAM):
        N = random.randint(0, len(matriz_swap) - 1)
        I = matriz_swap[N][1]
        D = matriz_swap[N][2]
        R = 1
        M = matriz_swap[N][4]
        T = matriz_swap[N][5]
        pagina = [N, I, D, R, M, T]
        matriz_ram.append(pagina)
