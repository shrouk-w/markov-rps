import numpy as np

import time

import matplotlib.pyplot as plt



# możliwe ruchy przeciwnika

t1 = ['P', 'St', 'Sc']   # P = papier, St = stone/kamień, Sc = scissors/nożyce



# macierz przejść:

# wiersz = poprzedni ruch przeciwnika

# kolumna = kolejny ruch przeciwnika

wyst = np.array([

    [1, 0, 0],   # po P

    [0, 1, 0],   # po St

    [0, 0, 1]    # po Sc

], dtype=float)



# prawdziwy rozkład ruchów przeciwnika (symulacja)

prob_op = np.array([0.1, 0.55, 0.35])   # P, St, Sc



print("Macierz początkowa:")

print(wyst)

print()



# historia wyniku

kasa = []

stankasy = 0



n = 30

state = 'P'   # zakładamy, że ostatni ruch przeciwnika na początku to P



# mapowanie ruchu na indeks

idx = {'P': 0, 'St': 1, 'Sc': 2}



# jaki ruch wygrywa z przewidywanym ruchem przeciwnika

# jeśli przewidujemy:

# P  -> gramy Sc

# St -> gramy P

# Sc -> gramy St

counter_move = {

    'P': 'Sc',

    'St': 'P',

    'Sc': 'St'

}



def result(our_move, op_move):

    """Zwraca wynik rundy:

    +1 = wygrana

     0 = remis

    -1 = przegrana

    """

    if our_move == op_move:

        return 0



    wins = {

        ('Sc', 'P'),   # nożyce wygrywają z papierem

        ('P', 'St'),   # papier wygrywa z kamieniem

        ('St', 'Sc')   # kamień wygrywa z nożycami

    }



    if (our_move, op_move) in wins:

        return 1

    else:

        return -1



for i in range(n):

    row = idx[state]



    # przewidywanie następnego ruchu przeciwnika

    probs = wyst[row] / np.sum(wyst[row])

    pred = np.random.choice(t1, p=probs)



    # wybieramy ruch, który powinien wygrać z przewidywanym ruchem przeciwnika

    our_move = counter_move[pred]



    # rzeczywisty ruch przeciwnika (losowany z jego "prawdziwego" rozkładu)

    op_akc = np.random.choice(t1, p=prob_op)



    # wynik rundy

    punkt = result(our_move, op_akc)

    stankasy += punkt

    kasa.append(stankasy)



    # uczenie:

    # skoro poprzedni ruch przeciwnika był "state",

    # a teraz wykonał "op_akc", to zwiększamy odpowiednie przejście

    wyst[row, idx[op_akc]] += 1



    # wypisanie informacji

    print(f"Runda {i+1}")

    print(f"Poprzedni stan przeciwnika: {state}")

    print(f"Prawdopodobieństwa z wiersza: {np.round(probs, 3)}")

    print(f"Przewidywany ruch przeciwnika: {pred}")

    print(f"Nasz ruch: {our_move}")

    print(f"Rzeczywisty ruch przeciwnika: {op_akc}")

    print(f"Wynik rundy: {punkt}")

    print(f"Stan kasy: {stankasy}")

    print("Aktualna macierz wyst:")

    print(wyst)

    print("-" * 40)



    # nowy stan = ostatni rzeczywisty ruch przeciwnika

    state = op_akc



    time.sleep(0.1)



# wykres wyniku

plt.figure(figsize=(10, 5))

plt.plot(range(1, n+1), kasa, marker='o')

plt.xlabel("Numer rundy")

plt.ylabel("Stan kasy")

plt.title("Wynik gracza w czasie")

plt.grid(True)

plt.show()