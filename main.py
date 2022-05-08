from auxi import *
import math
import numpy as np
import copy
import random

def calcula_distancia(matriz_distancia, inicio, destino):
    return matriz_distancia[int(inicio)][int(destino)]

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
        # print(f'Score:{score} Individuo: {individuo}')
        total_score += score
        van_score.append(f'{score}{j}')
        score = 0
        j += 1
    van_score.sort()
    melhores_vans = []

    for vans in van_score:
        melhores_vans.append(individuo[int(vans[-1])])
    individuo = melhores_vans
    return total_score

def mutacao(populacao):
    qtd = math.ceil(tx_mutacao * len(populacao))
    populacao_escolhida = random.choices(populacao, k=qtd)
    populacao_mutacao = []
    
    for individuo in populacao_escolhida:
        mutacao = random.randint(0,1)
        if mutacao == 0:
            populacao_mutacao.append(mutacao_shuffle(individuo))
        else:
            populacao_mutacao.append(mutacao_swap(individuo))
    return populacao_mutacao


def mutacao_swap(individuo):
    individuo_copy = copy.deepcopy(individuo)
    rand_van1 = random.randint(0,3)
    rand_van2 = random.randint(0,3)
    while rand_van2 == rand_van1:
        rand_van2 = random.randint(0,3) 

    rand_index = random.randint(1,4)

    van1 = individuo_copy[rand_van1][rand_index]
    van2 = individuo_copy[rand_van2][rand_index]

    individuo_copy[rand_van1][rand_index] = van2
    individuo_copy[rand_van2][rand_index] = van1
    return individuo_copy



# pega as cidades e embaralha elas
def mutacao_shuffle(individuo):
    novo_individuo = []
    caminhos_van = []
    caminho = []
    for van in individuo:
        for i in van:
            if i != 0:
                caminho.append(i)
        caminhos_van.append(caminho)
        caminho = []

    for i,ca in enumerate(caminhos_van):
        random.shuffle(ca)
        ca.insert(0,0)
        ca.append(0)
        novo_individuo.append(ca)
    return novo_individuo


def limpar(individuo, troca, antigo,index):
    troca.pop(0)
    troca.pop(-1)
    nao_entre = 0
    antigo_copia = copy.deepcopy(antigo)
    antigo_copia.insert(0,0)
    len_troca = len(troca)
    print(troca)
    for el in range(len_troca):
        nao_entre = 0
        for i in range(len(individuo)):
            if(nao_entre !=index):
                for j in range(len(individuo[i])-1):
                    if(individuo[i][j] == troca[el]):
                        individuo[nao_entre].remove(individuo[i][j])
            nao_entre += 1
    troca = list(set(np.append(troca, antigo_copia)))
    troca.append(0)
    individuo[index] = troca
    return individuo 

def crossover(populacao):
    funcao_decaimento_crossover = math.exp(-geracao / 200)
    qtd = funcao_decaimento_crossover * tx_crossover * len(populacao)
    populacao_escolhida = copy.deepcopy(populacao)
    populacao_escolhida = random.choices(populacao_escolhida, k=math.ceil(qtd))
    for i in range(len(populacao_escolhida)-1):
        swap = populacao_escolhida[i][1]
        antigo = swap
        populacao_escolhida[i] = [populacao_escolhida[i][0], populacao_escolhida[i+1][2], populacao_escolhida[i][2], populacao_escolhida[i][3]]
        populacao_escolhida[i] = limpar(populacao_escolhida[i],  populacao_escolhida[i+1][2], antigo,1)
        antigo = populacao_escolhida[i+1][2]
        populacao_escolhida[i+1] = [populacao_escolhida[i+1][0] , populacao_escolhida[i+1][1], swap, populacao_escolhida[i+1][3]]
        populacao_escolhida[i+1] = limpar(populacao_escolhida[i+1],  swap, antigo,2)
    return populacao_escolhida

def selecao_tragedia(populacao, geracao):
    if (geracao % geracoes_tragedia == 0):
        tamanho_tragedia = math.ceil(tamanho_populacao*tx_tragedia)
        novos_individuos = [gerar_individuo(data) for _ in range(
            0, tamanho_populacao - tamanho_tragedia)]
        return sorted(populacao[0:tamanho_tragedia] + novos_individuos, key=fitness)
    else:
        nova_populacao = sorted(populacao, key=fitness)
        return nova_populacao[0:tamanho_populacao]

# hiperparâmetros
tamanho_populacao = 100
tx_mutacao = 0.6
tx_crossover = 0.4
tx_tragedia = 0.2
geracoes_max = 100
geracoes_tragedia = 100
geracao = 0

data = create_data_model()
populacao = [gerar_individuo(data) for a in range(0, tamanho_populacao)]
populacao = sorted(populacao, key=fitness)

while geracao < geracoes_max:
    geracao += 1
    populacao_mutada = mutacao(populacao)
    # populacao_crossover = crossover(populacao)
    # populacao = selecao_tragedia(populacao_mutada + populacao_crossover + populacao,geracao)
    populacao = selecao_tragedia(populacao_mutada + populacao,geracao)
    if geracao % 100 == 0 or (geracao % 10 == 0 and geracao < 100):
        print("---------------- Geração: " + str(geracao) + " ----------------")
        print(populacao[0])
        print("Distância percorrida com todas as vans: " + str(fitness(populacao[0])))

# output desejável
melhor_individuo = populacao[0]
for index, caminho_van in enumerate(melhor_individuo):
    print(f'Van {index + 1}')
    caminho_sem_deposito = [str(numero) for numero in caminho_van]
    caminho_sem_deposito = caminho_sem_deposito[1:len(caminho_sem_deposito)-1]
    print(' -> '.join(caminho_sem_deposito),end='\n\n')

print("Distância percorrida com todas as vans: " + str(fitness(populacao[0])))