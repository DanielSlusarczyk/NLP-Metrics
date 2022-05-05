# Obliczanie funkcji ekspotencjalnej i logarytmów:
import math
# Wyrażenia regularne do wyszukiwania słów w tekście:
import re

tabs = '\t\t\t\t'
listOfNmbOfGrams = []
listOfResults = []

# Dzieli na listy wszystkie elementy listy
def splitList(inputList):
    mainList = []
    for element in inputList:
        mainList.append(element.split())
    return mainList

# Wyświetla informacje o tabeli
def describeTable(nRef):
    counter = 1
    print("n-GRAM" + tabs + "\t\t\tRef1", end='')
    for ref in range(1, nRef):
        counter = counter + 1
        print("\tRef" + str(counter), end='')

    print("\tMax Ref Count" + "\tClip Count" + "\tContribution")

# Definiuje liczbę rozpatrywanych n-gramów zależnie od przypisanych wag
def getNumberOfnGram(weights):
    n = len(weights)
    result = 0
    for i in range(1, n):
        if( weights[i - 1] == 0 ):
            break
        else:
            result = i
    return result + 1

# Zwraca liczbę wystąpień pattern w text - wyrażenia regularne
def getNumberOfOccurance(pattern, text):
    # "pattern"
    number = re.findall("^" + pattern + "$", text)
    # "pattern "
    number = number + re.findall("^" + pattern + " ", text)
    # " pattern "
    number = number + re.findall(" " + pattern + " ", text)
    # " pattern"
    number = number + re.findall(" " + pattern + "$", text)
    return len(number)

# Tworzy z inputList listę bez duplikatów
def makeUniqueList(inputList):
    unique_list = []
    for element in inputList:
        if element not in unique_list:
            unique_list.append(element)
    return unique_list

# Zwraca długość najdłuższej listy z listy
def getMaxLengthOflist(inputList):
    size = len (inputList[0])
    for element in inputList:
        if(size < len(element)):
            size = len(element)
    return size

# Oblicz karę za niedopasowanie długości
def lengthPenalty(refLength, canLength):
    result = math.exp(1-refLength/canLength)
    return result

# Oblicz końcową wartość wyniku i wyświetla
def calculateResult(bp, weights):
    if(len(listOfResults) == len (listOfNmbOfGrams)):
        sumOfLog = 0
        print("\nBLUE [" + str(len(listOfNmbOfGrams)) + "] = " + "{:.3f}".format(bp) + " exp( ", end ='')
        
        for con in range(0, len(listOfResults)):
            print( " ln( " + str(listOfResults[con]) + "/" + str(listOfNmbOfGrams[con]) + " )",end='')
            if(con != len(listOfResults) - 1):
                print(" +", end = '')
                
            sumOfLog = sumOfLog + weights[con] * math.log(listOfResults[con]/listOfNmbOfGrams[con])
        print(" ) = " + str(bp * math.exp(sumOfLog)))
        
        
def printTable(n, refNmb, candidate, references, canLength):        
    # Zmienne pomocnicze
    listOfNmbOfGrams.clear()
    listOfResults.clear()
    describeTable(refNmb)
    unique_candidate = makeUniqueList(candidate)

    # Pętla po liczbie n (liczbie rozpatrywanych n-gramów)
    for ngram in range(1, n + 1):

        # Suma wszystkich clipCount jednego n-gramu
        sumClipCount = 0
        counter = 1
        # Liczba n-gramów:
        if(ngram > 1):
            unique_candidate = candidate
        nmbOfGrams = len(unique_candidate) - ngram + 1

        # Pętla po liczbie n-gramów zależna od rozpatrywanego n-gramu
        for idOfPattern in range(0, nmbOfGrams):

            gram = unique_candidate[idOfPattern]
            # Pętla po liczbie słów do dodania aby otrzymać n-gram
            for idToAdd in range(1, ngram):
                gram = gram + ' ' + unique_candidate[idOfPattern + idToAdd]

            #Wypisanie początku wiersza tabeli
            print("{0:<4}".format(str(counter)+ ")"), end='')
            print("{0:<20}".format(gram), end='')
            print(tabs, end='')

            #Zmienne dla konkretnego n-gramu:
            counter = counter + 1
            maxRefCount = 0
            count = 0
            candidateWithSpace = ' '.join(map(str, candidate))
            count = getNumberOfOccurance(gram, candidateWithSpace)

            # Sprawdzanie wystąpień n-gramu w referencjach
            for reference in references:
                referenceWithSpace = ' '.join(map(str, reference))
                # Sprawdzenie wystąpienia konkretnego n-gramu w danej referencji
                if(gram in referenceWithSpace):
                    gramOccurrances = getNumberOfOccurance(gram, referenceWithSpace)
                    print(str(gramOccurrances) + '\t', end='')
                    maxRefCount = max(maxRefCount, gramOccurrances)
                else:
                    print("0" + '\t', end='')

            # Obliczanie wartości sumClipCount
            sumClipCount = sumClipCount + min(maxRefCount, count)

            #Wypisywanie maxRefCount i Coun
            if(idOfPattern != nmbOfGrams - 1):
                print(str(maxRefCount) + '\t' + str(count) + '\t' + str(min(maxRefCount, count)))
            else:
                print(str(maxRefCount) + '\t' + str(count) + '\t' + str(min(maxRefCount, count)), end ='')

        #Zapisanie wkładu danego n-gramu do oceny
        if(ngram == 1):
            listOfNmbOfGrams.append(canLength)
        else:
            listOfNmbOfGrams.append(nmbOfGrams)
        listOfResults.append(sumClipCount)
        print("\t\t" + str(listOfResults[-1]) + "\\" + str(listOfNmbOfGrams[-1]) + "\n")