# Wyrażenia regularne do wyszukiwania słów w tekście:
import re
# Obliczanie funkcji ekspotencjalnej i logarytmów:
import math
# Znaki interpunkcyjne
import string

# Usuwanie znaków interpunkcyjnych ze zdania
def deletePunctuation(sentence):
    newSentence = ""
    for character in sentence:
        if (character not in string.punctuation):
            newSentence = newSentence + character
    return newSentence

class Bleu:

    def __init__(self, weights, references, candidate, verbose = False):
        self.weights = weights
        self.references = references
        self.candidate = candidate
        self.references = self.splitList(self.references)
        self.candidate = self.candidate.split()
        self.verbose = verbose
        self.error = False
        
        self.analizeData()
        self.prepareData()
        self.calculateBP()
        self.calculateResult()
        self.printer = Printer(self)

    # Dzielenie na listy wszystkich elementów listy
    def splitList(self, inputList):
        return [item.split() for item in inputList]

    # Definiowanie liczby rozpatrywanych n-gramów zależnie od przypisanych wag
    def getNumberOfnGram(self):
        n = len(self.weights)
        result = 0
        for i in range(1, n):
            if(self.weights[i - 1] == 0):
                break
            else:
                result = i
        return result + 1

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
        return len(number)

    # Tworzenie z inputList listy bez duplikatów
    def makeUniqueList(self, inputList):
        unique_list = []
        for element in inputList:
            if element not in unique_list:
                unique_list.append(element)
        return unique_list

    # Zwracanie długość najdłuższej listy z listy
    def getMinLengthOflist(self, inputList):
        size = len (inputList[0])
        for element in inputList:
            if(size > len(element)):
                size = len(element)
        return size
    
    def getIndexOfMin(self, inputList):
        index = 0
        minValue = inputList[0]
        for i in range(0, len(inputList)):
            if(abs(inputList[i]) <= abs(minValue)):
                if(abs(inputList[i]) != abs(minValue)):
                    minValue = inputList[i]
                    index = i
                else:
                    if(inputList[i] < minValue):
                        minValue = inputList[i]
                        index = i
        return index

    # Zwracanie najbardziej zbliżonej długości do kandydata wśród referencji
    def getClosestLength(self):
        referenceLengths = [len(ref) - len(self.candidate) for ref in self.references]
        return len(self.candidate) + referenceLengths[self.getIndexOfMin(referenceLengths)]

    # Analiza otrzymanych danych
    def analizeData(self):
        # Ilość analizowanych n-gramów
        self.n = self.getNumberOfnGram()
        # Liczba referencji
        self.refNmb = len(self.references)
        # Najbliższa długość wzorca
        self.refMinLength = self.getClosestLength()
        # Długość kandydata
        self.canLength = len(self.candidate)
        # Unikalne słowa kandydata 
        self.uniqueCandidate = self.makeUniqueList(self.candidate)
      
    def prepareData(self):        
        # Zmienne pomocnicze
        self.listOfNmbOfGrams = []
        self.listOfResults = []
        self.data = []
        self.listOfNGrams = []
        uniqueCandidate = self.makeUniqueList(self.candidate)

        # Pętla po liczbie n (liczbie rozpatrywanych n-gramów)
        for ngram in range(1, self.n + 1):

            # Suma wszystkich clipCount jednego n-gramu
            sumClipCount = 0
            # Liczba n-gramów:
            if(ngram > 1):
                uniqueCandidate = self.candidate
            nmbOfGrams = len(uniqueCandidate) - ngram + 1

            # Pętla po liczbie n-gramów zależna od rozpatrywanego n-gramu
            for idOfPattern in range(0, nmbOfGrams):
                dataLine = []

                gram = uniqueCandidate[idOfPattern]
                # Pętla po liczbie słów do dodania aby otrzymać n-gram
                for idToAdd in range(1, ngram):
                    gram = gram + ' ' + uniqueCandidate[idOfPattern + idToAdd]
                
                # Nierozpatrywanie kilka razy tego samego n-gramu
                if(gram in self.listOfNGrams):
                    continue
                    
                self.listOfNGrams.append(gram)
                # Zmienne dla konkretnego n-gramu:
                maxRefCount = 0
                candidateWithSpace = ' '.join(map(str, self.candidate))
                count = self.getNumberOfOccurance(gram, candidateWithSpace)
                
                # Sprawdzanie wystąpień n-gramu w referencjach
                for reference in self.references:
                    referenceWithSpace = ' '.join(map(str, reference))
                    # Sprawdzenie wystąpienia konkretnego n-gramu w danej referencji
                    gramOccurrances = 0
                    if(gram in referenceWithSpace):
                        gramOccurrances = self.getNumberOfOccurance(gram, referenceWithSpace)
                        maxRefCount = max(maxRefCount, gramOccurrances)
                    dataLine.append(gramOccurrances)

                # Obliczanie wartości sumClipCount
                sumClipCount = sumClipCount + min(maxRefCount, count)

                # Zapis danych do tabeli
                dataLine.append(maxRefCount)
                dataLine.append(count)
                dataLine.append(min(maxRefCount, count))
                self.data.append(dataLine)

            # Zapisanie wkładu danego n-gramu do oceny
            if(ngram == 1):
                self.listOfNmbOfGrams.append(self.canLength)
            else:
                self.listOfNmbOfGrams.append(nmbOfGrams)
            self.listOfResults.append(sumClipCount)
    
    # Obliczanie kary za niedopasowanie długości
    def calculateBP(self):
        self.canLength = len(self.candidate)
        self.bp = math.exp(1-(self.refMinLength/self.canLength))
        if(self.bp > 1):
            self.bp = 1
    
    # Obliczanie końcowowej wartość wyniku
    def calculateResult(self):
        sumOfLogs = 0
        if(len(self.listOfResults) == len (self.listOfNmbOfGrams)):
            for con in range(0, len(self.listOfResults)):
                try:
                    sumOfLogs = sumOfLogs + self.weights[con] * math.log(self.listOfResults[con]/self.listOfNmbOfGrams[con])
                except:
                    if(self.verbose):
                        print("[Uwaga]Zerowa wartość wpływu n-gramu - rozważ zmianę wag")
                    self.error = True
                    self.result = 0
                    return
        self.result = self.bp * math.exp(sumOfLogs)

    def showAnalizedData(self):
        self.printer.showAnalizedData()

    def showTable(self):
        self.printer.showTable()
    
    def showBP(self):
        self.printer.showBP()
    
    def showResult(self):
        self.printer.showResult()

class Printer:

    def __init__(self, bleu):
        self.bleu = bleu
        # 5 | 50 | 10 | ... | 10 | 10 | 10 | 30
        self.col1 = "{0:<5}"            # Kolumna liczba porządkowych
        self.col2 = "{0:<50}"           # Kolumna n-gramów
        self.col3 = "{0:<10}"           # Kolumna poszczególnych zdań referencyjnych
        self.col4 = "{0:<10}"           # Kolumna Max Ref
        self.col5 = "{0:<10}"           # Kolumna Count
        self.col6 = "{0:<10}"           # Kolumna Clip Count
        self.col7 = "{0:>20}"           # Kolumna Contribution
    
    def showAnalizedData(self):
        print("{0:<50}".format("Liczba rozpatrywanych n-gramów: ")                  + str(self.bleu.n))
        print("{0:<50}".format("Liczba tłumaczeń referencyjnych (wzorcowych): ")    + str(self.bleu.refNmb))
        print("{0:<50}".format("Maksymalna długość wzorca: ")                       + str(self.bleu.refMinLength))
        print("{0:<50}".format("Maksymalna długość kandydata: ")                    + str(self.bleu.canLength))
        print("{0:<50}".format("Tłumaczenie kandydujące: ")                         + str(self.bleu.candidate))
        print("{0:<50}".format("Tłumaczenie kandydujące bez powtórzeń: ")           + str(self.bleu.uniqueCandidate))
        print("\n")

    def showTable(self):
        self.showHeadline()
        self.showData()
    
    def showHeadline(self):
        self.printt(self.col1.format("Lp") + self.col2.format("n-GRAM"))
        for ref in range(0, self.bleu.refNmb):
            self.printt(self.col3.format("Ref" + str(ref + 1)))
        print(self.col4.format("Max Ref") + self.col5.format("Count") + self.col6.format("Clip Count") + self.col7.format("Contribution"))

    def showData(self):
        n = 0
        for lp in range(0, len(self.bleu.data)):
            dataLine = self.bleu.data[lp]
            actualN = len(self.bleu.listOfNGrams[lp].split())
            if(n != actualN):
                con = str(self.bleu.listOfResults[n]) + "/" + str(self.bleu.listOfNmbOfGrams[n])
                self.printDataLine(lp + 1, self.bleu.listOfNGrams[lp], dataLine, contribution = con)
                n = actualN
            else:
                self.printDataLine(lp + 1, self.bleu.listOfNGrams[lp], dataLine)
        print("\n")

    def showBP(self):
        print("Najbliższa długość tłumaczenia wzorcowego: "     + str(self.bleu.refMinLength))
        print("Długość tłumaczenia kandydującego: "             + str(self.bleu.canLength))
        print("BP: "                                            + str(self.bleu.bp) + "\n")
    
    def showResult(self):
        self.printt("BLUE [" + str(len(self.bleu.weights)) + "] = " + "{:.3f}".format(self.bleu.bp) + " exp( ")
        
        for con in range(0, len(self.bleu.listOfResults)):
            self.printt( str( self.bleu.weights[con]) + " ln( " + str(self.bleu.listOfResults[con]) + "/" + str(self.bleu.listOfNmbOfGrams[con]) + " )")
            if(con != len(self.bleu.listOfResults) - 1):
                self.printt(" + ")
        print(" ) = " + str(self.bleu.result))       
    
    def printDataLine(self, lp, gram, dataLine, contribution = ''):
        self.printt(self.col1.format(str(lp) + ")") + self.col2.format(gram))
        for ref in range(0, self.bleu.refNmb):
            self.printt(self.col3.format(dataLine[ref]))
        print(self.col4.format(dataLine[-3]) + self.col5.format(dataLine[-2]) + self.col6.format(dataLine[-1]) + self.col7.format(contribution))

    def printt(self, text):
        print(text, end='' )
