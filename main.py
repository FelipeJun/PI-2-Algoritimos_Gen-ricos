from difflib import Match
from auxi import *
import math

def calcula_distancia(matriz_distancia, inicio, destino):
    return matriz_distancia[inicio][destino]

# utilidade
# quando menor melhor
def fitness(individuo):
    total_score = 0
    score = 0
    van_score = []
    j = 0
    for caminho_van in individuo:
        for i in range(len(caminho_van) - 1):
            score += calcula_distancia(data["matriz_distancia"], caminho_van[i], caminho_van[i+1])
        print(f'Score:{score} Individuo: {individuo}')
        total_score += score
        van_score.append(f'{score}{j}')
        score = 0
        j += 1
    van_score.sort()
    melhores_vans = []

    for vans in van_score:
        ultimo = vans[-1]
        melhores_vans.append(individuo[int(vans[-1])])
    individuo = melhores_vans
    return total_score

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
    novo_individuo = individuo.copy()
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

def limpar(individuo, troca, antigo,index):
    troca.pop(0)
    troca.pop(-1)
    tirar = []
    nao_entre = 0
    for el in individuo:
        if(nao_entre !=index):
            for i in el:
                for j in troca:
                    if(i == j):
                       el.remove(i)
        nao_entre += 1
    troca = list(set(troca.extend(antigo)))
    troca.insert(0,0)
    troca.append(0)

def crossover(populacao):
    for i in range(len(populacao)-1):
        swap = populacao[i][1]
        antigo = swap
        populacao[i]= [populacao[i][0], populacao[i+1][2], populacao[i][2], populacao[i][3]]
        limpar(populacao[i],  populacao[i+1][2], antigo,1)
        antigo = populacao[i+1][2]
        populacao[i+1] = [populacao[i+1][0] , populacao[i+1][1], swap, populacao[i+1][3]]
        limpar(populacao[i+1],  swap, antigo,2)

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
    populacao_crossover = crossover(populacao)
