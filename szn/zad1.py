import numpy as np
import random

def generuj_tablice(p_1, rozmiar, liczby_1):
    tab = np.random.binomial(1, p_1, rozmiar)
    while np.count_nonzero(tab == 1) != liczby_1:
        tab = np.random.binomial(1, p_1, rozmiar)
    return tab

def losuj_pare(tab):
    a, b = random.randint(0, len(tab) - 1), random.randint(0, len(tab) - 1)
    kierunek = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
    a1 = max(0, min(a + kierunek[0], len(tab) - 1))
    b1 = max(0, min(b + kierunek[1], len(tab) - 1))
    return a, b, a1, b1

def sprawdz_id(a, a1, tab):
    dl_tab = len(tab)
    if a1 < 0 or a1 >= dl_tab:
        a1 = (a + 1) % dl_tab if a1 < 0 else (a - 1) % dl_tab
    return a, a1

def sznajd_pionowy(a, b, a1, tab, war):
    rozmiar = len(tab)
    wspolrzedne = [(a + i, b + j) for i in range(-1, 2) for j in range(-1, 2)]
    for i, j in wspolrzedne:
        if 0 <= i < rozmiar and 0 <= j < rozmiar:
            tab[i, j] = war
    return tab

def sznajd_poziomy(a, b, b1, tab, war):
    rozmiar = len(tab)
    wspolrzedne = [(a + i, b + j) for i in range(-1, 2) for j in range(-1, 2)]
    for i, j in wspolrzedne:
        if 0 <= i < rozmiar and 0 <= j < rozmiar:
            tab[i, j] = war
    return tab

def Glowny_sznajd(a, b, a1, b1, tab):
    pkt1, pkt2 = tab[a, b], tab[a1, b1]
    if pkt1 == pkt2:
        if a == a1:
            poczatek_b, koniec_b = sorted([b, b1])
            sznajd_poziomy(a, poczatek_b, koniec_b, tab, pkt1)
        elif b == b1:
            poczatek_a, koniec_a = sorted([a, a1])
            sznajd_pionowy(poczatek_a, b, koniec_a, tab, pkt1)
    return tab

def wypisz(a, b, a1, b1, tab, g):
    print(f"\nwynik {g+1} losu ")
    print("ilosc wartosci 1-TAK wynosi:", np.count_nonzero(tab == 1))
    print("para wspolrzednych:", (a, b), (a1, b1))
    print("para wartosci:", tab[a, b], ",", tab[a1, b1])
    print("\n", tab)
    print("------------------------------------\n")

tab_rozm = (10, 10)
nowa_tab = generuj_tablice(0.5, tab_rozm, 50)

print(nowa_tab)
for g in range(10):
    a, b, a1, b1 = losuj_pare(nowa_tab)
    a, a1 = sprawdz_id(a, a1, nowa_tab)
    b, b1 = sprawdz_id(b, b1, nowa_tab)
    Glowny_sznajd(a, b, a1, b1, nowa_tab)
    wypisz(a, b, a1, b1, nowa_tab, g)
