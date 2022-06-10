# Projekt Indywidualny
Repozytorium _Projekt Indywidualny_ jest wynikiem pracy przeprowadzanej przez cały semestr 2022L w ramach przedmiotu projektowego. Początek realizacji projektu przypada na: 02.03.2022, zaś koniec: 07.06.2022.

### Autor: Daniel Ślusarczyk
### Opiekun projektu: mgr inż. Mateusz Bartosiewicz

## Cel Projektu
Celem projektu było opracowanie teoretyczne metryk znajdujących zastosowanie w ewaluacji napisów, oraz innych narzędzi do analizy NLP. Praca porusza również takie zagadnienia jak: szczegółowe działanie poszczególnych metryk, gotowe pakiety języka programowania Python 3.0 znajdujące zastosowanie w omawianej tematyce i inne aspekty związane z danymi narzędziami.

## Poruszana Tematyka
### Metryki:
- BLEU - Opis danej metryki, działanie, problemy, zastosowanie dla języka polskiego, przykłady obliczenia metryki. Dodatkowo została przygotowana przykładowa implementacja obliczania metryki BLEU dla zdań referencyjnych i zdania ocenianego, której celem jest wizualizacja sposobu obliczania poszczególnych wartości.

- METEOR - Opis danej metryki, działanie, problemy, zastosowanie dla języka polskiego, przykłady obliczenia metryki.

- ROUGE (ROUGE-N i ROUGE-L) - Opis danej metryki, działanie, problemy, zastosowanie dla języka polskiego, przykłady obliczenia metryki. Dodatkowo sekcja ta zawiera przykładową implementację obliczania metryki, która pozwala obliczyć wynik dla zdania ocenianego i jednego zdania referencyjnego.

- WMD - Opis danej metryki, działanie, problemy, zastosowanie dla języka polskiego, przykłady obliczenia metryki

- CIDEr - Opis danej metryki, działanie, problemy, zastosowanie dla języka polskiego, przykłady obliczenia metryki

- SPICE - Opis danej metryki, działanie, problemy, zastosowanie dla języka polskiego, przykłady obliczenia metryki

### Macierz Pomyłek
Teoretyczne przedstawienie macierzy pomyłek, sposób odczytywania najważniejszych miar bezpośrednio z macierzy pomyłek, zastosowanie macierzy pomyłek w problemach z większą ilościa klas.
### Wartości Shapleya
Teoretyczne przedstawienie wartości shapleya, zastosowanie wartość shapleya w problemach uczenia maszynowego, przykłady obliczania wartości, gotowy pakiet umożliwiający analizę zbioru. Sekcja ta zawiera również gotową implementację liczenia wartości shapleya dla przykładowego problemu, który ułatwia zrozumienie tematyki.
### Zbiór COCO
Przedstawienie zbioru COCO i jego zastosowania. Użycie zbioru do przeprowadzenia analizy poprawności wyników własnej implementacji BLEU.

## Użycie Przygotowanej Implementacji (Python 3.0)
Kody źródłowe poszczególnych implementacji znajdują się w folderze: "funkcje". Omawiane poniżej przykłady zostałe opracowane w podejściu obiektowym. Dodatkowo, w dokumencie "Projekt.ipynb" znajduje się wiele przykładów użycia poniższych metod.

### BLEU - Bleu.py
Tworzenie nowego obiektu:
  - bleu = Bleu(weights, references, candidate)

Wypisanie analizy wczytanych danych:
  - bleu.showAnalizedData()

Wypisanie tabeli z analizą poszczególnych n-gramów:
  - bleu.showTable()
  
Wypisanie kary za niedopasowanie długości (z ang. Brevity Penalty):
  - bleu.showBP()

Wypisanie końcowego wyniku i gotowego podstawienia do wzoru:
  - bleu.showResult()

### ROUGE - Rouge.py
Tworzenie nowego obiektu dla ROUGE-N:
  - rouge = Rouge(candidate, reference, ngram)

Wypisanie miary Recall z listą n-gramów użytych do analizy i sposobu obliczenia:
  - rouge.showRecall()

Wypisanie miary Precision z listą n-gramów użytych do analizy i sposobu obliczenia:
  - rouge.showPrecision()

Wypisanie miary F1 Score (Rouge - N) ze sposobem obliczania:
  - rouge.showRouge()

Tworzenie nowego obiektu dla ROUGE-L:
  - rouge = Rouge(candidate, reference)

Wypisanie miary ROUGE-L z miarą recall, precision i F1 Score zgodnej z wariantem ROUGE-L
  - rouge.showRougeL()

### Wartości Shapleya - Shapley.py
Tworzenie nowego obiektu dla wartości shapleya:
  - sv = ShapleyValue(players, player)

Wypisanie tabeli z pełną analizą dla 'player' w zbiorze 'players'
  - sv.showTable()

