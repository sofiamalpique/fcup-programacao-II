import csv
import numpy as np
import matplotlib.pyplot as plt
import json
import datetime
import dateutil.parser as date


# EXERCÍCIO 1

# Defina uma função que valida se os dados lidos são consistentes, isto é, cada estação metereológica
# possui exactamente três medições para as mesmas horas, e que todas as medições para a mesma estação
# possuem as mesmas coordenadas GPS e o mesmo nome de estação.

# Explore este conjunto de dados escrevendo programas Python que respondam às seguintes questões:

# (e) Quais as cidades mais quente e fria do país considerando a média das últimas três horas?
# (f) Retorne um dicionário que mapeie níveis de radiação em listas de pares nome/radiação de estações.
# Considere 5 níveis: "normal" (<1), "seguro" (>=1 e <3), "perigoso" (>=3 e < 4), "doentio" (>=4 e <5)
# e "mortal" (>=5).


with open('obs-surface.geojson', 'r') as file_estacoes:
    string1 = file_estacoes.read()

data1 = json.loads(string1)

array_de_features = data1['features']


def count(xs):
    c = {}
    for x in xs:
        c[x] = 1 + c.get(x, 0)
    return c


# Vou criar uma lista de tupulos, em que cada tupulo tem a seguinte estrutura:
#  (id_da_estacao,local_da_estacao,tupulo_de_coordenadas)
lista_de_medicoes = []

for i in range(len(array_de_features)):
    objeto = array_de_features[i]

    objeto_geometry = objeto['geometry']
    #tipo_do_objeto_geometry = objeto_geometry['type']
    tupulo_de_coordenadas = tuple(objeto_geometry['coordinates'])

    #tipo = objeto['type']

    objeto_properties = objeto['properties']
    #intensidade_vento = objeto_properties['intensidadeVentoKM']
    #temperatura = objeto_properties['temperatura']
    id_da_estacao = objeto_properties['idEstacao']
    #pressao = objeto_properties['pressao']
    #humidade = objeto_properties['humidade']
    local_da_estacao = objeto_properties['localEstacao']
    #precipitacao_acumulada = objeto_properties['precAcumulada']
    #id_direcao_vento = objeto_properties['idDireccVento']
    #radiacao = objeto_properties['radiacao']
    #data_e_hora = date.parse(objeto_properties['time'])
    #intensidade_vento = objeto_properties['intensidadeVento']
    #desc_direcao_vento = objeto_properties['descDirVento']

    lista = [id_da_estacao, local_da_estacao, tupulo_de_coordenadas]
    lista_de_medicoes.append(lista)



def contar_ids(lista):
    lista_de_ids = []
    for i in range(len(lista)):
        lista_de_ids.append(lista[i][0])
    dicionario_de_ocorrencias_ids = count(lista_de_ids)
    lista_de_ocorrencias_ids = list(dicionario_de_ocorrencias_ids.items())
    return lista_de_ocorrencias_ids


quantidade_de_ids = len(contar_ids(lista_de_medicoes))

dicionario_de_nomes = {item[1]: item[2] for item in lista_de_medicoes}


lista_de_ids_invalidos_por_ocorrencia = []
lista_de_ids_e_ocorrencia = contar_ids(lista_de_medicoes)
# aqui obtenho os ids que são medidos 1 ou 2 vezes
for item in lista_de_ids_e_ocorrencia:
    if item[1] != 3:                                         # logo inválidos
        lista_de_ids_invalidos_por_ocorrencia.append(item[0])


def validar(elemento_lista_a_validar):

    if elemento_lista_a_validar[0] in lista_de_ids_invalidos_por_ocorrencia:
        return 'Invalido'
    elif elemento_lista_a_validar[2] != dicionario_de_nomes[elemento_lista_a_validar[1]]:
        return 'Invalido'
    else:
        return 'Valido'


locais_validos = {item[1]: validar(item) for item in lista_de_medicoes}



# (a) Qual o nome da estação com a maior diferença de pressão entre a primeira e a última hora registadas?

lista_de_tupulos_pressoes = []
for i in range(len(array_de_features)):
    objeto = array_de_features[i]


    objeto_properties = objeto['properties']
    pressao = objeto_properties['pressao']
    local_da_estacao = objeto_properties['localEstacao']
    data_e_hora = date.parse(objeto_properties['time'])
    

    tupulo = (local_da_estacao, pressao, data_e_hora.hour)
    lista_de_tupulos_pressoes.append(tupulo)

for tupulo in lista_de_tupulos_pressoes:
    if locais_validos[tupulo[0]] == 'Invalido':
        lista_de_tupulos_pressoes.remove(tupulo)
    elif tupulo[2] == 16:
        lista_de_tupulos_pressoes.remove(tupulo)


# Neste momento tenho uma lista só de medicoes de pressao validas que ocorreram as 15 e as 17

# vamos criar uma lista de tupulos cujo cada tupulo está no formato
# (nome_da_estacao,pressao_as_15h,pressao_as_17h)

lista_dos_15 = []
lista_dos_17 = []
for tupulo_a_iterar in lista_de_tupulos_pressoes:
    if tupulo_a_iterar[2] == 15:

        tupulo = (tupulo_a_iterar[0], tupulo_a_iterar[1])
        lista_dos_15.append(tupulo)

for tupulo_a_iterar in lista_de_tupulos_pressoes:
    if tupulo_a_iterar[2] == 17:
        tupulo = (tupulo_a_iterar[0], tupulo_a_iterar[1])
        lista_dos_17.append(tupulo)

lista_dos_15_e_17 = []

for tupulo1 in lista_dos_15:
    for tupulo2 in lista_dos_17:
        if tupulo1[0] == tupulo2[0]:
            tupulo = (tupulo1[0], tupulo1[1], tupulo2[1])
            lista_dos_15_e_17.append(tupulo)

diferencas = {trio[0]: abs(trio[2]-trio[1]) for trio in lista_dos_15_e_17}


m = max(diferencas)  # daqui sai um nome (str)
dif_maxima = diferencas[m]   # daqui sai um int

chave_com_maior_diferenca = max(diferencas, key=diferencas.get)
# print(chave_com_maior_diferenca)    #descomentar para printar qual o nome da estação


# (b) Por cada hora registada, qual a maior diferença de temperatura no país? Retorne um dicionário que
# mapeie cada hora num par de nomes das duas estações em causa.

lista_de_locais_a_considerar = []

for i in range(len(array_de_features)):
    objeto = array_de_features[i]


    objeto_properties = objeto['properties']
    temperatura = objeto_properties['temperatura']
    local_da_estacao = objeto_properties['localEstacao']
    data_e_hora = date.parse(objeto_properties['time'])

    lista = [data_e_hora.hour, local_da_estacao, temperatura]
    lista_de_locais_a_considerar.append(lista)

# curar a lista de temperaturas iguais a -99.0

lista_de_locais_a_considerar_curada = []

for item in lista_de_locais_a_considerar:
    if locais_validos[item[1]] == 'Valido' and item[2] != (-99.0):
        lista_de_locais_a_considerar_curada.append(item)



dicionario_das_15h = { item[1] : item[2] for item in lista_de_locais_a_considerar_curada if item[0] == 15 }
dicionario_das_16h = { item[1] : item[2] for item in lista_de_locais_a_considerar_curada if item[0] == 16 }
dicionario_das_17h = { item[1] : item[2] for item in lista_de_locais_a_considerar_curada if item[0] == 17 }

temp_min_15h = dicionario_das_15h[min(dicionario_das_15h)]
temp_max_15h = dicionario_das_15h[max(dicionario_das_15h)]

temp_min_16h = dicionario_das_16h[min(dicionario_das_16h)]
temp_max_16h = dicionario_das_16h[max(dicionario_das_16h)]

temp_min_17h = dicionario_das_17h[min(dicionario_das_17h)]
temp_max_17h = dicionario_das_17h[max(dicionario_das_17h)]


#print('A maior diferença de temperatura às 15h é:', temp_max_15h-temp_min_15h)      #descomentar para printar a resposta

#print('A maior diferença de temperatura às 16h é:', temp_max_16h-temp_min_16h)      #descomentar para printar a resposta

#print('A maior diferença de temperatura às 17h é:', temp_max_17h-temp_min_17h)      #descomentar para printar a resposta

estacao_fria_15 = min(dicionario_das_15h)
estacao_quente_15 = max(dicionario_das_15h)

estacao_fria_16 = min(dicionario_das_16h)
estacao_quente_16 = max(dicionario_das_16h)

estacao_fria_17 = min(dicionario_das_17h)
estacao_quente_17 = max(dicionario_das_17h)


maiores_diferencas = {}


maiores_diferencas[15] = [estacao_fria_15, estacao_quente_15]

maiores_diferencas[16] = [estacao_fria_16, estacao_quente_16]

maiores_diferencas[17] = [estacao_fria_17, estacao_quente_17]



# (c) Liste os nomes e coordenadas GPS de todas as estações metereológicas com a string 'Porto' no seu
# nome. Identifique manualmente qual corresponde à estação metereológica da cidade do Porto.

lista_das_estacoes_alinea_c = []
for i in range(len(array_de_features)):
    objeto = array_de_features[i]

    objeto_geometry = objeto['geometry']
    array_de_coordenadas = objeto_geometry['coordinates']


    objeto_properties = objeto['properties']
    local_da_estacao = objeto_properties['localEstacao']


    lista = [local_da_estacao, array_de_coordenadas]
    lista_das_estacoes_alinea_c.append(lista)

estacoes_com_porto_no_nome = { lista[0] : lista[1] for lista in lista_das_estacoes_alinea_c if locais_validos[lista[0]] == 'Valido' and 'Porto' in lista[0]}

for chave,valor in estacoes_com_porto_no_nome.items():
    if 'Porto,' in chave:
        coordenadas_porto = valor

#print('As coordenadas referentes à cidade do porto são:', coordenadas_porto)    #descomentar para printar a resposta


# (d) Quantas estações metereológicas existem na região do Porto? Considere uma estação na região se a
# sua latitude e longitude estiverem no máximo a uma distância de 0.1º das cordenadas GPS da estação
# metereológica do Porto.

lista_das_estacoes_alinea_d = []
for i in range(len(array_de_features)):
    objeto = array_de_features[i]

    objeto_geometry = objeto['geometry']
    array_de_coordenadas = objeto_geometry['coordinates']


    objeto_properties = objeto['properties']
    local_da_estacao = objeto_properties['localEstacao']


    lista = [local_da_estacao, array_de_coordenadas]
    lista_das_estacoes_alinea_d.append(lista)

dicionario_regioes_porto = {
    lista[0] : lista[1] for lista in lista_das_estacoes_alinea_d
    if ((lista[1][0] >= (coordenadas_porto[0]-0.1)) and (lista[1][0] <= (coordenadas_porto[0]+0.1))) and ((lista[1][1] >= (coordenadas_porto[1]-0.1)) and (lista[1][1] <= coordenadas_porto[1]+0.1))
}

#print('Existem', len(dicionario_regioes_porto), 'estações na região do Porto')           #descomentar para printar a resposta


# (e) Quais as cidades mais quente e fria do país considerando a média das últimas três horas?

#Como na alínea (b) já criei uma lista com as horas da medição, com os nomes das estações, com 
#as temperaturas, vou reutilizá-lo!



lista_de_zonas_para_dicionario = list(dicionario_das_15h.keys())


dicionario_zonas_e_temp_media = {}

for zona in lista_de_zonas_para_dicionario:
    dicionario_zonas_e_temp_media[zona] = ((dicionario_das_15h[zona] + dicionario_das_16h[zona] + dicionario_das_17h[zona])/3)

cidade_mais_quente = max(dicionario_zonas_e_temp_media,key=lambda k : dicionario_zonas_e_temp_media[k])
cidade_mais_fria = min(dicionario_zonas_e_temp_media,key=lambda k : dicionario_zonas_e_temp_media[k])

#print('A cidade mais quente é',cidade_mais_quente,'e a cidade mais fria é',cidade_mais_fria)   #descomentar para printar a resposta



# (f) Retorne um dicionário que mapeie níveis de radiação em listas de pares nome/radiação de estações.
# Considere 5 níveis: "normal" (<1), "seguro" (>=1 e <3), "perigoso" (>=3 e < 4), "doentio" (>=4 e <5)
# e "mortal" (>=5).

def avaliar(n):
    if n >= 5000:
        return 'mortal'
    elif n >= 4000:
        return 'doentio'
    elif n >= 3000:
        return 'perigoso'
    elif n >= 1000:
        return 'seguro'
    else:
        return 'normal'


lista_radiacao = []
for i in range(len(array_de_features)):
    objeto = array_de_features[i]


    objeto_properties = objeto['properties']
    local_da_estacao = objeto_properties['localEstacao']
    radiacao = objeto_properties['radiacao']
    data_e_hora = date.parse(objeto_properties['time'])


    lista = [local_da_estacao, radiacao, data_e_hora.hour]
    lista_radiacao.append(lista)


lista_radiacao_curada = []

for item in lista_radiacao:
    if locais_validos[item[0]] == 'Valido' and item[1] != (-99.0) :

        lista_radiacao_curada.append(item)


dicionario_das_15h_radiacao = {item[0] : item[1] for item in lista_radiacao_curada if item[2] == 15}
dicionario_das_16h_radiacao = {item[0] : item[1] for item in lista_radiacao_curada if item[2] == 16}
dicionario_das_17h_radiacao = {item[0] : item[1] for item in lista_radiacao_curada if item[2] == 17}


lista_de_zonas_dicionario = list(dicionario_das_15h_radiacao.keys())
dicionario_radiacao_media = {}

for zona in lista_de_zonas_dicionario:
    dicionario_radiacao_media[zona] = ((dicionario_das_15h_radiacao[zona] + dicionario_das_16h_radiacao[zona] + dicionario_das_17h_radiacao[zona])/3)

classificacao_zonas_radiacao = {zona : avaliar(valor) for zona,valor in dicionario_radiacao_media.items() }

#print(classificacao_zonas_radiacao)           #descomentar para printar resposta


# TAREFA 1

# Leia o conteúdo do ficheiro JSON para uma estrutura de dados em Python.


with open('7.json', 'r') as file_sismos:
    dicionario = json.load(file_sismos)

array_data = dicionario['data']



# EXERCÍCIO 2

# Pode facilmente ler uma imagem com cores num array numpy tri-dimensional,
# ou seja, uma matriz de píxeis em que a terceira dimensão é um array [r,g,b]
# com os três componentes RGB (entre 0 e 255) da cor desse píxel.

dcc = plt.imread('dcc.jpg')


h, w, rgb = dcc.shape
colors = dcc.reshape((w*h), rgb)


def luminosity(rgb):
    return 0.21 * rgb[0] + 0.72 * rgb[1] + 0.07 * rgb[2]


colors_red = []
colors_green = []
colors_blue = []
for lista in colors:
    colors_red.append(lista[0])
    colors_green.append(lista[1])
    colors_blue.append(lista[2])

# se quisermos os três histogramas numa só janela não descomentar o comando
# plt.show(). se quisermos um histograma por cada cor, entao basta só descomentar


'''plt.hist(colors_red,bins=256,color='red')'''
# plt.show()
'''plt.hist(colors_green,bins=256,color='green')'''
# plt.show()
'''plt.hist(colors_blue,bins=256,color='blue')'''
# plt.show()


# EXERCICIO 3

# Similarmente, pode converter um array numpy numa imagem. Assumindo que aplica
# uma transformação f ao array original dcc (do exercício anterior) que retorna um
# array modificado, pode gravá-lo numa nova imagem 'dcc_modified.jpg' na pasta atual
# da seguinte forma.

# Defina as seguintes transformações:

# (a) Inverter as cores da imagem (i.e., invertendo cada componente RGB c calculando 255 - c).

def inverter(arr):

    array_para_inverter = []

    for i in range(len(arr)):
        array_para_inverter.append([])

        for j in range(len(arr[i])):
            array_para_inverter[i].append([])

            for k in range(len(arr[i, j])):

                invertido = 255 - arr[i, j, k]

                array_para_inverter[i][j].append(invertido)

    array_invertido = np.array(array_para_inverter)

    return array_invertido


# plt.imshow(inverter(dcc));     #descomentar para funcionar
plt.savefig('dcc_modified_a.jpg')


# (b) Converter a imagem em grayscale (i.e., convertendo o array de componentes
# RGB num só valor). Note que para visualizar um array no mapa de cores grayscale,
# deve passar o argumento adicional cmap='gray' à função imgshow.

def preto_branco(imagem):
    rgb_weights = [0.21, 0.72, 0.07]
    grayscale_image = np.dot(imagem[..., :3], rgb_weights)

    return grayscale_image


# plt.imshow(preto_branco(dcc), cmap=plt.get_cmap("gray"))       # descomentar para funcionar
plt.savefig('dcc_modified_b.jpg')


# (c)  Rodar a imagem 90º para a esquerda.

def rodar_90_esquerda(imagem):
    imagem_rodada = np.rot90(dcc, k=1, axes=(0, 1))

    return imagem_rodada


# plt.imshow(rodar_90_esquerda(dcc))        # descomentar para funcionar
plt.savefig('dcc_modified_c.jpg')


# (d) Cortar a imagem de forma a preservar apenas com os 200x200 píxeis centrais.

def cortar_quadrado_200(imagem):
    altura = h
    largura = w

    largura_esquerda = int((w-200)/2)
    largura_direita = int(w - largura_esquerda)

    altura_baixo = int((h-200)/2)
    altura_cima = int(h - altura_baixo)

    a = largura_esquerda
    b = largura_direita
    c = altura_baixo
    d = altura_cima

    cropped = imagem[c:d, a:b]

    return cropped


# plt.imshow(cortar_quadrado_200(dcc))       # descomentar para funcionar
plt.savefig('dcc_modified_d.jpg')




# EXERCÍCIO 4

# Faça download para uma pasta local dos ficheiros CSV mtnmn-1312-porto.csv e mtxmx-1312-porto.csv,
# atualizados regularmente, que contêm respetivamente as temperaturas mínimas e máximas previstas
# durante os últimos 2 meses para a cidade do Porto.

# Estes ficheiros CSV são essencialmente matrizes de valores numéricos, que podem ser lidos para
# arrays multi-dimensionais utilizando a biblioteca numpy da seguinte forma.

with open('mtnmn-1312-porto.csv', 'r') as file1:

    tabela1 = csv.reader(file1)
    temp_minimas = list(tabela1)


with open('mtxmx-1312-porto.csv', 'r') as file2:

    tabela2 = csv.reader(file2)
    temp_maximas = list(tabela2)


cabecalho_temp_min = temp_minimas[0]
cabecalho_temp_max = temp_maximas[0]

# Imprima no ecrã ambas as matrizes e inspecione o seu formato e o tipo de cada célula. Repare que os
# campos não numéricos têm o valor NaN por defeito. Para limpar os dados, apague a primeira linha
# (o cabeçalho do ficheiro CSV) e a primeira coluna (o dia de cada entrada) de cada array.

meses_e_dia_min = temp_minimas[1:]
meses_e_dia_max = temp_maximas[1:]

temp_minimas.remove(temp_minimas[0])
temp_maximas.remove(temp_maximas[0])

# neste momento as minhas listas estão curadas, só têm data e valores de temperatura

datas_tem_min = []
for i in range(len(temp_minimas)):
    str1 = str(date.parse(temp_minimas[i][0]).month)
    str2 = str(date.parse(temp_minimas[i][0]).day)
    str3 = str1 + '/' + str2
    datas_tem_min.append(str3)


datas_tem_max = []
for i in range(len(temp_maximas)):
    str1 = str(date.parse(temp_maximas[i][0]).month)
    str2 = str(date.parse(temp_maximas[i][0]).day)
    str3 = str1 + '/' + str2
    datas_tem_max.append(str3)


# agora vamos tirar as datas das listas:

for i in range(len(temp_minimas)):
    temp_minimas[i].remove(temp_minimas[i][0])

for i in range(len(temp_maximas)):
    temp_maximas[i].remove(temp_maximas[i][0])

temperaturas_minimas = np.array(temp_minimas)
temperaturas_maximas = np.array(temp_maximas)


# print(temperaturas_minimas)
# print(temperaturas_maximas)

# Explore este conjunto de dados escrevendo programas Python que respondam às seguintes questões:

# (a) Qual o dia com a temperatura mínima mais baixa? E qual o dia com a temperatura máxima mais alta?

array_medias_min = []
for i in range(len(temperaturas_minimas)):
    array_medias_min.append(float(temperaturas_minimas[i, 3]))

array_medias_max = []
for i in range(len(temperaturas_maximas)):
    array_medias_max.append(float(temperaturas_maximas[i, 3]))

arr_avg_min = np.array(array_medias_min)
arr_avg_max = np.array(array_medias_max)

dicionario_datas_e_medias_min = {}
for i in range(len(temperaturas_minimas)):
    dicionario_datas_e_medias_min[datas_tem_min[i]] = arr_avg_min[i]

dicionario_datas_e_medias_max = {}
for i in range(len(temperaturas_maximas)):
    dicionario_datas_e_medias_max[datas_tem_max[i]] = arr_avg_max[i]


min_key_avg = min(dicionario_datas_e_medias_min,
                  key=dicionario_datas_e_medias_min.get)
max_key_avg = max(dicionario_datas_e_medias_max,
                  key=dicionario_datas_e_medias_max.get)


# (b) Calcule a amplitude térmica ao longo dos últimos 2 meses. Quais as amplitudes
# térmicas miníma,média e máxima por dia? Filtre apenas os dias com amplitude térmica
# superior a 10ºC.

maximo_media = np.amax(arr_avg_max)
minimo_media = np.amin(arr_avg_min)
amplitude_termica_2_meses = maximo_media - minimo_media

array_amplitudes_min = []
for i in range(len(temperaturas_minimas)):
    array_amplitudes_min.append(float(temperaturas_minimas[i, 2]))

array_amplitudes_max = []
for i in range(len(temperaturas_maximas)):
    array_amplitudes_max.append(float(temperaturas_maximas[i, 2]))


arr_amp_min = np.array(array_amplitudes_min)
arr_amp_max = np.array(array_amplitudes_max)


dicionario_datas_e_amplitudes_min = {}
for i in range(len(temperaturas_minimas)):
    dicionario_datas_e_amplitudes_min[datas_tem_min[i]] = arr_amp_min[i]

dicionario_datas_e_amplitudes_max = {}
for i in range(len(temperaturas_maximas)):
    dicionario_datas_e_amplitudes_max[datas_tem_max[i]] = arr_amp_max[i]


min_key_amp = min(dicionario_datas_e_amplitudes_min,
                  key=dicionario_datas_e_amplitudes_min.get)
max_key_amp = max(dicionario_datas_e_amplitudes_max,
                  key=dicionario_datas_e_amplitudes_max.get)

lista_medias_de_amplitude = []
soma_amp = 0
for i in range(len(arr_amp_min)):
    soma_amp += (arr_amp_max[i] + arr_amp_min[i])

media_amp = soma_amp/(2*len(arr_amp_min))

# vamos agora filtrar os dias que têm amplitude térmica superior a 10ºC.

dicionario_mais_de_10 = {}

for i in range(len(arr_amp_max)):
    if arr_amp_max[i] > 10:
        dicionario_mais_de_10[datas_tem_max[i]] = arr_amp_max[i]

# Nos ultimos 2 meses não existe amplitude térmica superior a 10ºC

