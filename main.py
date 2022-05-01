from difflib import Match
from auxi import *
import copy
import math

def calcula_distancia(matriz_distancia, inicio, destino):
    return matriz_distancia[inicio][destino]

# utilidade
# quando menor melhor
def fitness(individuo):
    score = 0
    for caminho_van in individuo:
        for i in range(len(caminho_van) - 1):
            score += calcula_distancia(data["matriz_distancia"], caminho_van[i], caminho_van[i+1])
    print(f'Score:{score} Van: {individuo}')
    return score

def mutacao(populacao):
    qtd = math.ceil(tx_mutacao * len(populacao))
    populacao_escolhida = random.choices(populacao, k=qtd)
    populacao_mutacao = []
    
    for individuo in populacao_escolhida:
        tipo_mutacao = str(random.choices(["flip", "swap"])[0])
        match tipo_mutacao:
            case "flip": populacao_mutacao.append(mutacao_flip(individuo))
            case "swap": populacao_mutacao.append(mutacao_swap(individuo))
    return populacao_mutacao

# flip de valor de gene de um gene aleatório
def mutacao_flip(individuo):
    novo_individuo = individuo.copy()
    random.shuffle(novo_individuo)
    
    tamanho_caminho_van = []
    for van in novo_individuo:
        tamanho_caminho_van.append(len(van) - 2)

    for i in range(0, len(novo_individuo) - 1):
        no_local = novo_individuo[i].pop(random.randint(1, tamanho_caminho_van[i]))
        novo_individuo[i + 1].insert(random.randint(1, tamanho_caminho_van[i + 1]), no_local)
    
    return novo_individuo

def mutacao_swap(individuo):
    novo_individuo = copy.deepcopy(individuo)
    caminhos_van: list = []
    for van in novo_individuo:
        tamanho_caminho = len(van) - 1 
        if tamanho_caminho > 1:
            caminho = list(range(1, tamanho_caminho))
            caminhos_van.append(caminho)
        else:
            caminhos_van.append([1])

    for index in range(len(novo_individuo)):
        indice_van1 = index
        indice_van2 = index - 1
        
        indiceCaminho1 = random.choice(caminhos_van[indice_van1])
        indiceCaminho2 = random.choice(caminhos_van[indice_van2])
        novo_individuo[indice_van1][indiceCaminho1], novo_individuo[indice_van2][indiceCaminho2] = novo_individuo[indice_van2][indiceCaminho2], novo_individuo[indice_van1][indiceCaminho1] 
    
    return novo_individuo


# hiperparâmetros
tamanho_populacao = 3
tx_mutacao = 0.6
tx_crossover = 0.4
tx_tragedia = 0.2
geracoes_max = 1000
geracoes_tragedia = 100
geracao = 0

data = create_data_model()
populacao = [gerar_individuo(data) for a in range(0, tamanho_populacao)]
for p in populacao:
    print(p)
    print("\n")
print("-------------------------------------------------------------")
populacao = sorted(populacao, key=fitness)
for p in populacao:
    print(p)
    print("\n")

while geracao < geracoes_max:
    geracao += 1
    populacao_mutada = mutacao(populacao)