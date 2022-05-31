# Wyrażenia regularne do wyszukiwania słów w tekście:
from calendar import c
import re

class Rouge:
    def __init__(self, candidate, reference, ngram = 1):
        self.candidate = candidate.split()
        self.reference = reference.split()
        self.ngram = ngram

        self.sumOfGram = 0
        self.nmbOfGrams = 0
        self.nmbOfCandidateGrams = 0
        self.lcs = 0
        self.listOfNGrams = []
        self.listOfOccurance = []

        self.recall = 0
        self.precision = 0
        self.f1 = 0
        self.recallL = 0
        self.precisionL = 0
        self.f1L = 0
        self.printer = Printer(self)

        self.prepareNGram()
        self.longestCommonSubsequence(self.candidate, self.reference)
        self.calculateRecall()
        self.calculatePrecision()
        self.calculateF1()


    # Zwracanie liczby wystąpień pattern w text - wyrażenia regularne
    def getNumberOfOccurance(self, pattern, text):
        # "pattern"
        number = re.findall("^" + pattern + "$", text)
        # "pattern "
        number = number + re.findall("^" + pattern + " ", text)
        # " pattern "
        number = number + re.findall(" " + pattern + " ", text)
        # " pattern"
        number = number + re.findall(" " + pattern + "$", text)
        if(len(number) > 0):
            return 1
        return 0

    # Tworzenie z inputList listy bez duplikatów
    def makeUniqueList(self, inputList):
        unique_list = []
        for element in inputList:
            if element not in unique_list:
                unique_list.append(element)
        return unique_list

    # Obliczanie wspólnych n-gramów
    def prepareNGram(self):
        # Obliczenie ilości n-gramów kandydata
        self.nmbOfCandidateGrams = len(self.makeUniqueList(self.candidate))
        if(self.ngram > 1):
            self.nmbOfCandidateGrams = len(self.candidate) - self.ngram + 1

        # Zmienne pomocnicze
        unique_reference = self.makeUniqueList(self.reference)

        # Liczba n-gramów:
        if(self.ngram > 1):
            unique_reference = self.reference
        self.nmbOfGrams = len(unique_reference) - self.ngram + 1
        counter = 1

        # Pętla po liczbie n-gramów zależna od rozpatrywanego n-gramu
        for idOfPattern in range(0, self.nmbOfGrams):

            gram = unique_reference[idOfPattern]

            # Pętla po liczbie słów do dodania aby otrzymać n-gram
            for idToAdd in range(1, self.ngram):
                gram = gram + ' ' + unique_reference[idOfPattern + idToAdd]

            self.listOfNGrams.append(gram)    

            #Zmienne dla konkretnego n-gramu:
            counter = counter + 1
            candidateWithSpace = ' '.join(map(str, self.candidate))

            # Sprawdzenie wystąpienia konkretnego n-gramu w referencji
            gramOccurrances = self.getNumberOfOccurance(gram, candidateWithSpace)
            self.sumOfGram = self.sumOfGram + gramOccurrances
            self.listOfOccurance.append(gramOccurrances)


    # Obliczanie miary Recall
    def calculateRecall(self):
        self.recallL = self.lcs/len(self.makeUniqueList(self.reference))
        self.recall = self.sumOfGram/self.nmbOfGrams

    # Obliczanie miary Precision
    def calculatePrecision(self):
        self.precisionL = self.lcs/len(self.makeUniqueList(self.candidate))
        self.precision = self.sumOfGram/self.nmbOfCandidateGrams

    # Obliczanie miary F1 Score
    def calculateF1(self):
        self.f1L = 2 * (self.recallL * self.precisionL)/(self.precisionL + self.recallL)
        self.f1 = 2 * (self.recall * self.precision)/(self.precision + self.recall)

    # Definiuje liczbę rozpatrywanych n-gramów zależnie od przypisanych wag
    def getNumberOfnGram(self, weights):
        result = 0
        for i in range(1, len(weights)):
            if( weights[i - 1] == 0 ):
                break
            else:
                result = i
        return result + 1

    # Zwracanie długości najdłuższego wspólnego podłańcucha
    def longestCommonSubsequence(self, text1 , text2):
        m = len(text1)
        n = len(text2)
        matrix = [[0]*(n+1) for i in range(m+1)] 
        for i in range(m+1):
            for j in range(n+1):
                if i==0 or j==0:
                    matrix[i][j] = 0
                elif text1[i-1] == text2[j-1]:
                    matrix[i][j] = 1 + matrix[i-1][j-1]
                else:
                    matrix[i][j] = max(matrix[i-1][j] , matrix[i][j-1])
        self.lcs = matrix[-1][-1]

    def showRecall(self):
        self.printer.showTable()
        self.printer.showRecall()

    def showPrecision(self):
        self.printer.showTable()
        self.printer.showPrecision()

    def showRouge(self):
        self.printer.showF1()

    def showRougeL(self):
        self.printer.showRougeL()


class Printer:

    def __init__(self, rouge):
        self.rouge = rouge
        # 5 | 30 | 10
        self.col1 = "{0:<5}"            # Kolumna liczb porządkowych
        self.col2 = "{0:<30}"           # Kolumna n-gramów
        self.col3 = "{0:<10}"           # Kolumna poszczególnych zdań referencyjnych
    
    def showTable(self):
        self.showHeadline()
        self.showData()
    
    def showHeadline(self):
        self.printt(self.col1.format("Lp"))
        self.printt(self.col2.format("n-gram"))
        print(self.col3.format("Wystąpienie"))
    
    def showData(self):
        for lp in range(0, len(self.rouge.listOfNGrams)):
            self.printt(self.col1.format(str(lp + 1) + ")"))
            self.printt(self.col2.format(self.rouge.listOfNGrams[lp]))
            print(self.col3.format(self.rouge.listOfOccurance[lp]))

    def showRecall(self):
        print("\nrecall = " + str(self.rouge.sumOfGram) + "/" + str(self.rouge.nmbOfGrams))
        print("\nWartość miary recall: " + str(self.rouge.recall))

    def showPrecision(self):
        print("\nprecision = " + str(self.rouge.sumOfGram) + "/" + str(self.rouge.nmbOfCandidateGrams))
        print("\nWartość miary precision: " + str(self.rouge.precision))

    def showF1(self):
        self.printt("\nF1 = 2 * ( " + str(self.rouge.recall) + " * " + str(self.rouge.precision) + " ) ")
        print("/ (" + str(self.rouge.recall) + " + " + str(self.rouge.precision) + ")")
        print("\nWartość miary F1 (Rouge): " + str(self.rouge.f1))

    def showRougeL(self):
        print("[ Rouge-L ] NWP: " + str(self.rouge.lcs))
        print("[ Rouge-L ] Wartość miary recall: " + str(self.rouge.recallL))
        print("[ Rouge-L ] Wartość miary precision: " + str(self.rouge.precisionL))
        print("[ Rouge-L ] Wartość miary F1: " + str(self.rouge.f1L))

    def printt(self, text):
        print(text, end='' )
