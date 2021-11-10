import csv
import os
from datetime import datetime

per_km_cost = 0
distances = []

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def log(string):
    now = datetime.now()
    f = open(now.strftime('%Y-%m-%d') + '.log', 'a')
    f.write(now.strftime('%H:%M:%S') + string + '\n')
    f.close()

def openCSV():
    f = open('distancias.csv')
    reader = csv.reader(f, delimiter=';')
    global distances
    distances = list(reader)
    f.close()
    

def alterarCustoPorKM():
    cls()
    print("Bem vindo ao sistema de gerenciamneto logístico\n\rPara inicialização do programa, precisamos que você informe o custo por kilômetro rodado, em R$.")
    km_cost = '0'
    while not isinstance(km_cost, float):
        km_cost = input('Custo por Kilômetro: R$')

        try:
            km_cost = float(km_cost)
        except:
            cls()
            print('Valor inválido, Digite um número válido.')

    global per_km_cost
    per_km_cost = km_cost
    log('[INFO] O valor do custo por km foi alterado para R${:.2f}'.format(per_km_cost))
    cls()

def verificarDistancia(origem, destino):
    if isinstance(origem, int) and isinstance(destino, int):
        return int(distances[destino+1][origem])
    else:
        origem_index = distances[0].index(origem.upper())
        destino_index = distances[0].index(destino.upper())
        return int(distances[destino_index+1][origem_index])

def verificarCidade(cidade):
    print(distances)
    if cidade.upper() in distances[0]:
        return distances[0].index(cidade.upper())
    else:
        return False

def consultarTrecho():
    flag = True
    cls()
    while flag:
        
        origem = input('Digite a cidade de origem: ')
        destino = input('Digite a cidade de destino: ')

        if verificarCidade(origem) and verificarCidade(destino) and origem != destino:
            flag = False
        else:
            cls()
            print('Essas cidades não existem ou são iguais.')
        
    cls()
    distancia_entre_cidades = verificarDistancia(origem, destino)
    print('A distância rodoviária entre cidades é de {}km.\nO custo total do trecho é de R${:.2f}'.format(distancia_entre_cidades, int(distancia_entre_cidades)*per_km_cost))
    log('[INFO] Foi consultada a distância entre as cidades de {} e {}. O trecho tem um total de {}km e custará R${:.2f}'.format(origem, destino, distancia_entre_cidades, int(distancia_entre_cidades)*per_km_cost))
    input("Digite qualquer coisa para continuar: ")
    cls()

def melhorRota():
    flag = True
    cls()
    while flag:
        cidades = input("Digite três cidades separadas por uma vígula: ")
        cidades = cidades.split(',')
        
        if len(cidades) == 3:
            if not (cidades[0] == cidades[1] or cidades[0] == cidades[2] or cidades[1] == cidades[2]):
                if cidades[0].upper() in distances[0] and cidades[1].upper() in distances[0] and cidades[2].upper() in distances[0]:
                    flag = False
                else:
                    cls()
                    ##print(cidades[0] in distances[0], cidades[1] in distances[0], cidades[2] in distances[0], cidades, distances[0])
                    print('Uma ou mais cidades que você digitou não constam na lista de cidades disponíveis.')
                    return
            else:
                cls()
                print('Você digitou cidades iguais, certifique-se que são cidades diferentes.')
                return
        else:
            cls()
            print('Você não digitou 3 cidades separadas por uma vírgula, tente novamente.')

    distance_AB = verificarDistancia(cidades[0], cidades[1])
    distance_BC = verificarDistancia(cidades[1], cidades[2])
    distance_AC = verificarDistancia(cidades[0], cidades[2])

    if (distance_AC + distance_BC) < (distance_AB + distance_BC):
        distancia_total = distance_AC+distance_BC
        string1 = '{}  === {} ===  {}  === {} ===  {}'.format(cidades[0], distance_AC, cidades[2], distance_BC, cidades[1])
        string2 = 'Distância total percorrida: {:d}km. O valor total gasto no trajeto é de R${:.2f}'.format(distancia_total, distancia_total*per_km_cost)
        
    else:
        distancia_total = distance_AB+distance_BC
        string1 = '{}  === {} ===  {}  === {} ===  {}'.format(cidades[0], distance_AB, cidades[1], distance_BC, cidades[2])
        string2 = 'Distância total percorrida: {:d}km. O valor total gasto no trajeto é de R${:.2f}'.format(distancia_total, distancia_total*per_km_cost)

    print('\n',string1,'\n',string2)
    log('[INFO]'+string1)
    log('[INFO]'+string2)
    input('\n\nDigite qualquer coisa para continuar: ')
    cls()

def rotaCompleta():
    flag = True
    cls()
    cidades = []
    while flag:
        entrada = input("Digite o nome de uma cidade ou 'fim' para finalizar a entrada de dados:\n")
        if entrada != 'fim':
            if verificarCidade(entrada):
                cidades.append(entrada)
                cls()
            else:
                cls()
                print('A cidade que você digitou não foi computada pois não foi localizada no sistema.')
        else:
            if(len(cidades) < 3):
                cls()
                print("Você deve digitar ao menos 3 cidades válidas.")
            else:
                flag = False
    
    cls()
    distancia_total = 0
    print("|De----------------|Para--------------|Km---------|")
    log('[INFO]' + "|De----------------|Para--------------|Km---------|")
    for i in range(len(cidades)-1):
        string = "|{:18}|{:18}|{:>11}|".format(cidades[i], cidades[i+1], verificarDistancia(cidades[i],cidades[i+1]))
        print(string)
        log("[INFO]" + string)
        distancia_total += verificarDistancia(cidades[i],cidades[i+1])

    print('|__________________|__________________|___________|')
    log('[INFO]|__________________|__________________|___________|')
    print('|{:18}|{:18}|{:>11}|'.format('Distancia Total','',distancia_total))
    log('[INFO]|{:18}|{:18}|{:>11}|'.format('Distancia Total','',distancia_total))
    print('|{:18}|{:18}|R${:>9.2f}|'.format('Custo Total','',distancia_total * per_km_cost))
    log('[INFO]|{:18}|{:18}|R${:>9.2f}|'.format('Custo Total','',distancia_total * per_km_cost))
    log('[INFO]|{:18}|{:18}|{:11.2f}|'.format("Cons. diesel total", '', distancia_total / 2.57))
    print('|{:18}|{:18}|{:11.2f}|'.format("Cons. diesel total", '', distancia_total / 2.57))
    log('[INFO]|{:18}|{:18}|{:>11.2f}|'.format("Dias totais",'',distancia_total/583))
    print('|{:18}|{:18}|{:>11.2f}|'.format("Dias totais",'',distancia_total/583))
    print('|__________________|__________________|___________|')
    log('[INFO]|__________________|__________________|___________|')
    input('Digite qualquer coisa para continuar: ')
    cls()

def mostrarCidades():
    cls()
    print('\n'.join(distances[0]))
    input('Digite qualquer coisa para continuar: ')
    cls()

def menu():
    user_choice = '0'
    cls()
    while user_choice != '6':
        print('Funções disponíveis:')
        print('1 - Alterar custo por Kilômetro rodado')
        print('2 - Consultar Trecho')
        print('3 - Melhor rota')
        print('4 - Rota completa')
        print('5 - Ver cidades disponíveis')
        print('6 - Sair do programa')

        user_choice = input('Digite o número da função desejada: ')

        if(user_choice == '1'):
            alterarCustoPorKM()
        elif(user_choice == '2'):
            consultarTrecho()
        elif(user_choice == '3'):
            melhorRota()
        elif(user_choice == '4'):
            rotaCompleta()
        elif(user_choice == '5'):
            mostrarCidades()
        elif(user_choice == '6'):
            return

##Execução principal do código (main)
openCSV()
alterarCustoPorKM()
menu()