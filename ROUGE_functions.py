# Wyrażenia regularne do wyszukiwania słów w tekście:
import re

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
    if(len(number) > 0):
        return 1
    return 0

# Tworzy z inputList listę bez duplikatów
def makeUniqueList(inputList):
    unique_list = []
    for element in inputList:
        if element not in unique_list:
            unique_list.append(element)
    return unique_list

def calculateRecall(ngram, reference, candidate):
    # Zmienne pomocnicze
    unique_reference = makeUniqueList(reference)
    tabs = '\t\t\t\t'
    sumOfGram = 0

    # Liczba n-gramów:
    if(ngram > 1):
        unique_reference = reference
    nmbOfGrams = len(unique_reference) - ngram + 1
    counter = 1

    # Pętla po liczbie n-gramów zależna od rozpatrywanego n-gramu
    for idOfPattern in range(0, nmbOfGrams):

        gram = unique_reference[idOfPattern]

        # Pętla po liczbie słów do dodania aby otrzymać n-gram
        for idToAdd in range(1, ngram):
            gram = gram + ' ' + unique_reference[idOfPattern + idToAdd]

        #Wypisanie początku wiersza tabeli
        print("{0:<4}".format(str(counter)+ ")"), end='')
        print("{0:<20}".format(gram), end='')
        print(tabs, end='')

        #Zmienne dla konkretnego n-gramu:
        counter = counter + 1
        candidateWithSpace = ' '.join(map(str, candidate))

        # Sprawdzenie wystąpienia konkretnego n-gramu w referencji
        gramOccurrances = getNumberOfOccurance(gram, candidateWithSpace)
        sumOfGram = sumOfGram + gramOccurrances
        print(str(gramOccurrances))

    recall = sumOfGram/len(unique_reference)
    return recall