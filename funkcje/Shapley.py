import math

class ShapleyValue:
    def __init__(self, players, player):
        self.players = players
        self.player = player
        self.listOfNewPlayers = []
        self.listOfTeamsWithPlayer = []
        self.listOfTeamsWithoutPlayer = []
        self.listOfMarCon = []
        self.listOfSV = []
        self.result = 0
        self.relativeResult = 0
    
        self.printer = Printer(self)
        self.calculateShapley()

# Obliczanie wartości Shapleya dla player w zbiorze players
    def calculateShapley(self):
        
        # player - > indkes gracza
        try:
            playerIndex = self.players.index(self.player)
        except:
            print("Nie znaleziono gracza!")
            return
        
        # Liczba graczy -> n
        n = len(self.players)

        # Lista indeksów niezawierających indeksu liczonego ngramu -> subset
        subset = list(range(0, n))
        del subset[playerIndex]
        
        # Lista wszystkich unikalnych permutacji indeksów (0, n -1) - elementowych -> listOfPermutation
        listOfPermutation = []
        listOfPermutation.append([])
        for per in range(1, n):
            listOfPermutation = listOfPermutation + self.subsetsOfGivenSize(subset, per)
        
        # Pętla po wszystkich możliwościach
        for indexes in (listOfPermutation):
            # indexes -> newPlayers (zamiana indeksów na graczy)
            newPlayers = []
            for index in indexes:
                newPlayers.append(self.players[index])
            # Obliczenia bez analizowanego gracza
            self.listOfNewPlayers.append(newPlayers)
            self.listOfTeamsWithoutPlayer.append(self.calValue(newPlayers))

            # Dodanie analizowanego gracza
            newPlayers.append(self.players[playerIndex])

            # Obliczenia z analizowanych graczem
            self.listOfTeamsWithPlayer.append(self.calValue(newPlayers))

            # Wkład marginalny
            # Różnica pomiędzy wartością funkcji koalicyjnej z analizowanym graczem i bez analizowanego gracza
            self.listOfMarCon.append(self.listOfTeamsWithPlayer[-1] - self.listOfTeamsWithoutPlayer[-1])

            # Wartość shapleya dla koalicji
            self.listOfSV.append(self.calShapleyValue(len(self.listOfNewPlayers[-1]) - 1, n, self.listOfMarCon[-1]))
            
            # Wynik
            self.result = sum(self.listOfSV)
            self.relativeResult = round((sum(self.listOfSV)/self.calValue(self.players)) * 100, 2)

    # Obliczanie wartości zbioru graczy players - funkcja koalicyjna
    # Wzór zdefiniowany w przykładzie - kwadrat sumy graczy
    def calValue(self, players):
        return pow(sum(players), 2)

    # Obliczanie wartości Shapleya zgodnie ze wzorem dla jednego przypadku i
    # SV_i = ( ( |S_i|! (n - |S_i| - 1)! )/n! ) * WkładMarginalny dla przypadku i
    def calShapleyValue(self, S, n, marInflu):
        return((self.calFactorial(S) * self.calFactorial(n - S - 1))/self.calFactorial(n)) * marInflu

    # Obliczanie silni dla n
    def calFactorial(self, n):
        return math.prod(i for i in range(1, n + 1))

    # Funkcja pomocnicza dla obliczania podzbiorów rozmiaru n
    def subsets(self, numbers):
        if numbers == []:
            return [[]]
        x = self.subsets(numbers[1:])
        return x + [[numbers[0]] + y for y in x]
 
    # Zwracanie listy podzbiorów zbioru numbers o rozmiarze n
    def subsetsOfGivenSize(self, numbers, n):
        return [x for x in self.subsets(numbers) if len(x) == n]
    
    # Wyświetlanie poszczególnych przypadków w formie tabeli
    def showTable(self):
        self.printer.showTable()
        
class Printer:

    def __init__(self, shapley):
        self.shapley = shapley
        # 5 | 30 | 20 | 20 | 20 | 20
        self.col1 = "{0:<5}"            # Kolumna liczb porządkowych
        self.col2 = "{0:<30}"           # Kolumna kombinacji
        self.col3 = "{0:<20}"           # Kolumna wartości bez gracza
        self.col4 = "{0:<20}"           # Kolumna wartości z graczem
        self.col5 = "{0:<20}"           # Kolumna wkładu marginalnego
        self.col6 = "{0:<20}"           # Kolumna skalowanego wkładu marginalnego

    def showTable(self):
        self.showHeadline()
        self.showData()
        self.showResult()
        
    def showHeadline(self):
        self.printt(self.col1.format("Lp") + self.col2.format("Kombinacja"))
        self.printt(self.col3.format("Wartość bez gracza"))
        print(self.col4.format("Wartość z graczem") + self.col5.format("Wkład marginalny") + self.col6.format("Wartość Shapleya"))
        
    def showData(self):
        for i in range(0, len(self.shapley.listOfNewPlayers)):
            self.printt(self.col1.format(str(i + 1) + ")"))
            self.printt(self.col2.format(str(self.shapley.listOfNewPlayers[i])))
            self.printt(self.col3.format(self.shapley.listOfTeamsWithoutPlayer[i]))
            self.printt(self.col4.format(self.shapley.listOfTeamsWithPlayer[i]))
            self.printt(self.col5.format(round(self.shapley.listOfMarCon[i], 2)))
            self.printt(self.col6.format(round(self.shapley.listOfSV[i], 2)))
            print()
            
    def showResult(self):
        print()
        print("Wartość shapleya dla " + str(self.shapley.player) + ": " + str(self.shapley.result))
        print("Wkład procentowy w wielką koalicję: " + str(self.shapley.relativeResult) + "%")
        
    def printt(self, text):
        print(text, end='' )