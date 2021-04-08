from collections import Counter
from collections.abc import Iterable
import locale

# EXERCÍCIO 1

# Defina uma função sem_pontuacao que remova toda a pontuação de uma string.


def sem_pontuacao(txt):

    str_curada = ""

    lista_pontuacao = ['.', ',', ';', ':', '?', '!', '"', '-','(',')','[',']']

    for c in txt:
        if c not in lista_pontuacao:
            str_curada += c

    return str_curada


print(sem_pontuacao('Olá mundo! Vou começar a programar Python.'))


# EXERCÍCIO 2

# Defina uma função palavras que retorna a lista de palavras presentes
# numa string.

def palavras(str):

    str_curada1 = sem_pontuacao(str)

    lista_palavras = str_curada1.split()

    return lista_palavras


print(palavras('Olá mundo\nVou começar a programar Python'))


# EXERCÍCIO 4

# Defina uma função minusculas que converte uma lista de palavras em minúsculas.

def minusculas(lista):

    txt_lower = []

    for word in lista:
        txt_lower.append(word.lower())

    return txt_lower


print(minusculas(['Olá', 'mundo', 'VOU',
      'começar', 'a', 'programar', 'Python']))


# EXERCÍCIO 3

# Defina uma função conta que recebe uma string e uma palavra, e conta quantas
# vezes uma palavra ocorre na string, ignorando maiúsculas e minúsculas:

def conta(str, lista):

    string_curada = minusculas(palavras(str))
    palavra_curada = lista.lower()
    ocorrencias = 0

    for word in string_curada:
        if palavra_curada == word:
            ocorrencias += 1

    return ocorrencias


print(conta('Olá mundo do python\nVou começar a programar Python', 'Python'))


# TAREFA 1

# Faça download para uma pasta local do ficheiro lusiadas.txt, que contém o texto
# integral da obra Os Lusíadas de Luís Vaz de Camões.

# Leia o conteúdo do ficheiro lusiadas.txt para uma string.

lusiadas = open('lusiadas.txt', 'r').read()

# Neste momento temos uma string chamada 'lusiadas' que tem o conteúdo do ficheiro
# lusiadas.txt lá 'dentro'


lu_sem_punc = sem_pontuacao(lusiadas)

# Neste momento temos o conteudo do ficheiro, mas sem pontuação, que facilitará a
# sua análise daqui em diante


lu_lista_linhas = lu_sem_punc.split('\n')

# Agora temos uma lista, cujo cada elemento é uma linha do ficheiro lusiadas.txt
# mas ainda com elementos vazios ('') porque temos no ficheiro original linhas de
# intervalo

lu_curado = []

for frase in lu_lista_linhas:
    if frase != '':
        lu_curado.append(frase)

# lu_curado é agora uma lista que tem como elementos cada linha sem linhas vazias


# EXERCÍCIO 5

# Conte quantas vezes a palavra 'Portugal' aparece em todo o texto.

print('Portugal aparece', conta(lu_sem_punc, 'Portugal'), 'vezes.')


# TAREFA 2

# Escreva num ficheiro indice.txt um índice de cantos e estrofes para linhas no
# ficheiro original (repare no alinhamento vertical; as
# linhas impressas no ecrã devem ter todas o mesmo comprimento, mas os números
# exatos de espaços ou hífens por linha ficam ao critério dos alunos).

lista_cantos = ['Primeiro', 'Segundo', 'Terceiro', 'Quarto',
                'Quinto', 'Sexto', 'Sétimo', 'Oitavo', 'Nono', 'Décimo']

file_indice = open('indice.txt', 'w')

# uso o lu_lista_linhas, porque para o índice tem importância as linhas em branco
for i in range(len(lu_lista_linhas)):

    for canto in lista_cantos:

        if ('Canto ' + canto) == lu_lista_linhas[i]:

            string_imp = lu_lista_linhas[i] + str(i+1)

            comp_linha = 30 - len(string_imp)

            file_indice.write(
                'Canto ' + canto + ' ' + comp_linha*'-' + ' ' + str(i+1) + '\n')

    if (lu_lista_linhas[i].isnumeric()):

        string_imp = lu_lista_linhas[i] + str(i+1)

        comp_linha = 30 - len(string_imp)

        file_indice.write(
            str(int(lu_lista_linhas[i])) + ' ' + comp_linha*'-' + ' ' + str((i+1)) + '\n')

file_indice.close()


# TAREFA 3

# Defina uma função organiza que organiza o texto original numa lista de cantos,
# em que cada canto é uma lista de estrofes, cada estrofe é uma lista versos e
# cada verso é uma lista de palavras.

def organiza(txt):

    textoSemPontuacao = sem_pontuacao(txt)

    listaDasFrases = textoSemPontuacao.split('\n')
    livro = []

    for i in range(len(listaDasFrases)):
        if listaDasFrases[i] != '':
            livro.append(listaDasFrases[i])

            # neste momento tenho os lusiadas numa lista cujos elementos são linhas

    lista_cantos = []
    lista_final = []

    currentCanto = -1

    for frase in livro:
        if frase.startswith('Canto'):  # começou um novo canto
            currentCanto += 1
            lista_cantos.append([])
        if (currentCanto >= 0) and (not(frase.startswith('Canto'))):
            lista_cantos[currentCanto].append(frase)

    numCantos = len(lista_cantos)

    for i in range(numCantos):
        lista_final.append([])
        estrofe_counter = -1
        for j in range(len(lista_cantos[i])):

            if lista_cantos[i][j].isnumeric():

                estrofe_counter += 1

                lista_final[i].append([])

            if (estrofe_counter >= 0) and (not(lista_cantos[i][j].isnumeric())):

                lista_final[i][estrofe_counter].append(
                    lista_cantos[i][j].split())

    return lista_final


lusiadas_organizado = organiza(lusiadas)


# TAREFA 4

# Defina uma função que retorna um tuplo com os números totais de estrofes,
# versos e palavras.

# Defina uma função que retorna um tuplo com o comprimento médio de palavras
# por verso, por estrofe, por canto e em todo o texto.

# Nota: Quando existe mais do que um elemento do mesmo tipo (o texto tem por
# exemplo mais do que um verso), deve calcular a média por cada elemento, e de
# seguida a média das médias de cada elemento.


def numEVP(lista):

    # Nota: consideram-se palavras apenas as que constituem as estrofes

    numEstrofes = 0
    numPalavras = 0

    for i in range(len(lista)):

        numEstrofes += len(lista[i])

        # o nº de versos por estrofe é constante (8)
        numVersos = 8 * numEstrofes

        for j in range(len(lista[i])):

            for k in range(len(lista[i][j])):

                numPalavras += len(lista[i][j])

    return (numEstrofes, numVersos, numPalavras)


print(numEVP(lusiadas_organizado))




def media_texto_total(lista):

    lista_de_versos = []

    # Não queremos nem o nome do autor nem o título da obra para este cálculo
    for i in range(2, len(lu_curado)):
        if not(lu_curado[i].startswith('Canto') or lu_curado[i].isnumeric()):

            lista_de_versos.append(lu_curado[i])


# lu_curado é uma lista de frases

    lista_de_versos_em_palavras = []

    for verso in lista_de_versos:

        lista_de_versos_em_palavras.append(palavras(verso))

    contador_de_versos = 0
    soma_medias_versos = 0

    for i in range(len(lista_de_versos_em_palavras)):

        contador_de_versos += 1
        soma_comprimento_palavras = 0

        for palavra in lista_de_versos_em_palavras[i]:

            soma_comprimento_palavras += len(palavra)

        media_por_verso = soma_comprimento_palavras / \
            len(lista_de_versos_em_palavras[i])
        soma_medias_versos += media_por_verso

    media_versos_todos = soma_medias_versos/contador_de_versos

    current_canto = -1
    lista_cantos = []

    for frase in lista:
        if frase.startswith('Canto'):  # começou um novo canto
            current_canto += 1
            lista_cantos.append([])
        if (current_canto >= 0) and (not(frase.startswith('Canto'))):
            lista_cantos[current_canto].append(frase)

    # lista_cantos é uma lista com 10 elementos em que cada elemento é
    # o conteúdo de um canto

    lista_cantos_sem_numeros = []

    for i in range(len(lista_cantos)):

        lista_cantos_sem_numeros.append([])

        for verso in lista_cantos[i]:
            if not(verso.isnumeric()):
                lista_cantos_sem_numeros[i].append(verso)

    lista_cantos_em_palavras = []

    for verso in lista_cantos_sem_numeros:
        lista_cantos_em_palavras.append(palavras(verso))

    soma_comprimento_palavras = 0

    for i in range(len(lista_cantos_em_palavras)):
        for j in range(len(lista_cantos_em_palavras[i])):
            soma_comprimento_palavras += len(lista_cantos_em_palavras[i][j])
    # print(soma_comprimento_palavras)
    media_por_texto = soma_comprimento_palavras / 70528

    soma_medias_cantos = 0

    for i in range(len(lista_cantos_em_palavras)):
        soma_comprimento_palavras = 0
        for j in range(len(lista_cantos_em_palavras[i])):
            soma_comprimento_palavras += len(lista_cantos_em_palavras[i][j])

        media_por_canto = soma_comprimento_palavras / \
            len(lista_cantos_em_palavras[i])
        soma_medias_cantos += media_por_canto

    media_cantos_todos = soma_medias_cantos/len(lista_cantos_em_palavras)

    return (media_por_texto, media_cantos_todos, media_versos_todos)




# EXERCÍCIO 6

# Quais as 3 palavras mais usadas?

# Qual é a estrofe que mais vezes utiliza a palavra mais utilizada no livro
# inteiro?

# Conte quantas vezes as palavras 'Rei' e 'Pátria' aparecem na mesma estrofe.

# Conte quantas vezes palavras com mais de 3 letras aparecem repetidas numa
# estrofe.

# Encontre o maior palíndrono. Quantos caracteres tem?


tudoEmPalavras = minusculas(palavras(sem_pontuacao(lusiadas)))

Counter = Counter(tudoEmPalavras)

maisFrequentes = Counter.most_common(3)

primeiraMaisFreq = maisFrequentes[0][0]
segundaMaisFreq = maisFrequentes[1][0]
terceiraMaisFreq = maisFrequentes[2][0]

lista_das_estrofes_que_tem_palavra_mais_freq = []

for i in range(len(lusiadas_organizado)):
    lista_das_estrofes_que_tem_palavra_mais_freq.append([])
    for j in range(len(lusiadas_organizado[i])):
        for k in range(len(lusiadas_organizado[i][j])):
            for h in range(len(lusiadas_organizado[i][j][k])):
                if lusiadas_organizado[i][j][k][h] == primeiraMaisFreq:
                    lista_das_estrofes_que_tem_palavra_mais_freq[i].append(j)

def most_frequent(List):
    counter = 0
    num = List[0]
      
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
  
    return num

lst = []

for i in range(len(lista_das_estrofes_que_tem_palavra_mais_freq)):
    elemento_mais_freq = most_frequent(lista_das_estrofes_que_tem_palavra_mais_freq[i])
    
    lst.append(elemento_mais_freq)


lst2 = []
lst3 = []
for i in range(len(lista_das_estrofes_que_tem_palavra_mais_freq)):

    lst2.append(conta(str(lista_das_estrofes_que_tem_palavra_mais_freq[i]),str(lst[i])))
    lst3.append(lst[i])
    
maximo = max(lst2)

lst4 = []
for i in range(len(lst2)):
    tupulo = (lst2[i],lst3[i])
    lst4.append(tupulo)




lst5 = []

for i in range(len(lst2)):
    if lst4[i][0] == maximo:
        lst5.append(lst4[i])
    else:
        lst5.append((0,0))



lst6 = []

for i in range(len(lst5)):
    if lst5[i][0] != 0:

        lst6.append((lst5[i][1],(i+1)))

print('As estrofes', lst6[0][0],',',lst6[1][0],'e',lst6[2][0],'dos cantos',lst6[0][1],',', lst6[1][1]
,'e',lst6[2][1],',respetivamente, são as estrofes em que aparecem mais vezes a palavra mais frequente')


lista_de_estrofes_onde_aparece = []
for i in range(len(lusiadas_organizado)):
    lista_de_estrofes_onde_aparece.append([])
    for j in range(len(lusiadas_organizado[i])):
        for k in range(len(lusiadas_organizado[i][j])):
            for h in range(len(lusiadas_organizado[i][j][k])):
                if (lusiadas_organizado[i][j][k][h] == 'Rei' or lusiadas_organizado[i][j][k][h] == 'Pátria'):
                    lista_de_estrofes_onde_aparece[i].append(j)



lst8 = []
for i in range(len(lista_de_estrofes_onde_aparece)):
    for j in range(len(lista_de_estrofes_onde_aparece[i])):
        if (conta(str(lista_de_estrofes_onde_aparece[i]),str(lista_de_estrofes_onde_aparece[i][j]))==2):
            lst8.append((i+1,lista_de_estrofes_onde_aparece[i][j]))


lst9 = []

for i in range(0, len(lst8),2):
    lst9.append(lst8[i])

print('Aparecem', len(lst9),'vezes na mesma estrofe')

lista_com_palavras_mais_de_tres = []  
for i in range(len(lusiadas_organizado)):
    lista_com_palavras_mais_de_tres.append([])
    for j in range(len(lusiadas_organizado[i])):
        lista_com_palavras_mais_de_tres[i].append([])
        for k in range(len(lusiadas_organizado[i][j])):
            for h in range(len(lusiadas_organizado[i][j][k])):
                if (len(lusiadas_organizado[i][j][k][h]) > 3):
                    lista_com_palavras_mais_de_tres[i][j].append(lusiadas_organizado[i][j][k][h])



#print(lista_com_palavras_mais_de_tres[0][0])
lista_de_tupulos = []
for i in range(len(lista_com_palavras_mais_de_tres)):
   for j in range(len(lista_com_palavras_mais_de_tres[i])):
       for k in range(len(lista_com_palavras_mais_de_tres[i][j])):
           if lista_com_palavras_mais_de_tres[i][j].count(lista_com_palavras_mais_de_tres[i][j][k]) >= 2:

               tupulo = (i+1,j+1,lista_com_palavras_mais_de_tres[i][j][k])
               lista_de_tupulos.append(tupulo)

#print(lista_de_tupulos)

lista_de_tupulos_final = []

for i in range(len(lista_de_tupulos)):
    if lista_de_tupulos[i] not in lista_de_tupulos_final:
        lista_de_tupulos_final.append(lista_de_tupulos[i])

#print(lista_de_tupulos_final)

lista_final = []
for i in range(len(lista_de_tupulos_final)):
    if lista_de_tupulos_final[i][1] not in lista_final:
        lista_final.append(lista_de_tupulos_final[i][1])

print('Palavras com mais de 3 letras aparecem repetidas numa estrofe',len(lista_final),'vezes')


def inverter(txt):
    I=''
    for i in range(1,len(txt)+1):
        I=I+txt[-i]
    return I


def isPalindrome(str):

    if (not str or len(str)<2):
        return False
    if inverter(str) == str.lower():
        return True
    
    return False
 

lista_de_palindromes = []  
for i in range(len(lusiadas_organizado)):
    for j in range(len(lusiadas_organizado[i])):
        for k in range(len(lusiadas_organizado[i][j])):
            for h in range(len(lusiadas_organizado[i][j][k])):
                if (isPalindrome(lusiadas_organizado[i][j][k][h])):
                    lista_de_palindromes.append(lusiadas_organizado[i][j][k][h])

lista_de_palindromes_final = []

for i in range(len(lista_de_palindromes)):
    if lista_de_palindromes[i] not in lista_de_palindromes_final:
        lista_de_palindromes_final.append(lista_de_palindromes[i])

lista_de_palindromes_final = sorted(lista_de_palindromes_final, key=len)

print('O maior palíndrono é \'',lista_de_palindromes_final[-1],'\', que tem',len(lista_de_palindromes_final[-1]),'caractéres.')



# TAREFA 5

# Faça download para uma pasta local do ficheiro palavras.txt, que contém uma lista exaustiva de 
# palavras presentes na língua Portuguesa após o último acordo ortográfico.

# Leia o conteúdo do ficheiro palavras.txt para um set de palavras.


texto_gigante = open('palavras.txt','r').read()

conjunto_palavras = set(texto_gigante.split('\n'))



# TAREFA 6

# Retorne uma lista de palavras nos Lusíadas com mais de 3 letras, sem repetidos e excluindo 
# nomes (ou seja, palavras que começam por maiúsculas) que não obedecem à ortografia atual 
# (ou seja, que não se encontram no set de palavras acima construído). Esta lista deve estar 
# ordenada alfabeticamente, considerando acentos. Por exemplo, a palavra 'útil' deverá aparecer 
# depois de 'utilizar' e antes de 'verdade'.

#print(lista_com_palavras_mais_de_tres)

def deepflat(lista):
    for elemento in lista:
        if isinstance(elemento, Iterable) and not isinstance(elemento, (str, bytes)):
            yield from deepflat(elemento)
        else:
            yield elemento

lista_palavras_lusiadas = deepflat(lista_com_palavras_mais_de_tres)

def comecaMaiuscula (str):
    if not(str):
        return False
    if str < 'a':
        return True
    return False


def obedeceAOrtografia (str):
    # executar logica
    if not(str):
        return False
    if str.lower() in conjunto_palavras:
        return True

    # return resultado
    return False


set_palavras_lusiadas_mais_de_tres = set()

for elemento in lista_palavras_lusiadas:
    if not( comecaMaiuscula(elemento) and not(obedeceAOrtografia(elemento)) ):
        set_palavras_lusiadas_mais_de_tres.add(elemento)
        
locale.setlocale(locale.LC_ALL, "pt_PT")

lista_final_palavras_lusiadas_mais_de_tres = sorted(list(set_palavras_lusiadas_mais_de_tres), key=locale.strxfrm)

print(lista_final_palavras_lusiadas_mais_de_tres)



