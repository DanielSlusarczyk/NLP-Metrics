import nltk.translate.bleu_score as bleu

# Obliczanie wartości Shapleya dla player w zbiorze players
def shapley(players, player):
    
    # player - > indkes gracza
    player = getPlayerIndex(players, player)
    
    # Liczba graczy -> n
    n = len(players)
    listOfResults = []
    listOfPermutation = []
    
    # Lista indeksów niezawierających indeksu liczonego ngramu -> subset
    subset = list(range(0, n))
    del subset[player]
    
    # Lista wszystkich unikalnych permutacji indeksów (0, n -1) - elementowych -> listOfPermutation
    listOfPermutation.append([])
    for per in range(1, n):
        listOfPermutation = listOfPermutation + subsetsOfGivenSize(subset, per)
    
    listOfNewPlayers = []
    listOfTeamWithPlayer = []
    listOfTeamWithoutPlayer = []
    for indexes in list(listOfPermutation):
        newPlayers = []
        for index in indexes:
            newPlayers.append(players[index])    
        listOfNewPlayers.append(newPlayers)
        listOfTeamWithoutPlayer.append(calValue(newPlayers))
        newPlayers.append(players[player])
        listOfTeamWithPlayer.append(calValue(newPlayers))
        del newPlayers[-1]
    printShapleyTable(players[player], listOfNewPlayers, listOfTeamWithPlayer, listOfTeamWithoutPlayer, n, players)

# Obliczanie wartości zbioru graczy players - funkcja koalicyjna    
def calValue(players):
    return pow(sum(players), 2)

# Obliczanie wartości Shaplya zgodnie ze wzorem
def calShapleyValue(S, n, marInflu):
    return((calFactorial(S) * calFactorial(n - S - 1))/calFactorial(n)) * marInflu

# Obliczanie silni dla n
def calFactorial(n):
    res = 1
    for i in range(1, n + 1):
        res = res * i
    return res

# Funkcja pomocnicza dla obliczania podzbiorów rozmiaru n
def subsets(numbers):
    if numbers == []:
        return [[]]
    x = subsets(numbers[1:])
    return x + [[numbers[0]] + y for y in x]
 
# Zwracającanie listy podzbiorów zbioru numbers o rozmiarze n
def subsetsOfGivenSize(numbers, n):
    return [x for x in subsets(numbers) if len(x) == n]

# Wypisywanie tabeli i obliczanie wartości Shapleya
def printShapleyTable(player, listOfPlayers, listOfTeamsWithPlayer, listOfTeamsWithoutPlayer, n, players):
    print("TABELA DLA: " + str(player))
    print("Nr:" + "\t Kombinacja:" + "\t\t\tBez gracza:" + "\t\tZ graczem:" + "\t\tWkład marginalny:" + "\tSkalowany wkład marginalny:")
    counter = 1
    listOfSV = []
    for i in range(0, len(listOfPlayers)):
        print("{0:<9}".format(str(counter)+ ")"), end='')
        counter = counter + 1
        print("{0:<31}".format(str( listOfPlayers[i] )), end='')
        print("{0:<24}".format(str( listOfTeamsWithoutPlayer[i] )), end='')
        print("{0:<24}".format(str( listOfTeamsWithPlayer[i] )), end='')
        marInflu = listOfTeamsWithPlayer[i] - listOfTeamsWithoutPlayer[i]
        print("{0:<24}".format(str( marInflu )), end='')
        sv = calShapleyValue(len(listOfPlayers[i]), n, marInflu)
        listOfSV.append(sv)
        print("{0:<20}".format(str( round(sv*100)/100 )))
    print("\nWartość Shapleya dla " + str(player) + ": " + str(sum(listOfSV)))
    print("Wkład procentowy: " + "{:.3f}".format((sum(listOfSV)/calValue(players))*100) + "%")

# Zwracanie indeksu player w liście players
def getPlayerIndex(players, player):
    index = 0;
    for p in players:
        if(p == player):
            break
        index = index + 1
    return index