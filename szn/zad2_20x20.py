import numpy as np
import random
from matplotlib import pyplot

def generuj_tablice(prawdopodobienstwo_1, tab_rozmiar, procent_1):
    liczby_1 = int(np.prod(tab_rozmiar) * procent_1 / 100)
    while True:
        wygenerowana_tab = np.random.binomial(1, prawdopodobienstwo_1, tab_rozmiar)
        if np.count_nonzero(wygenerowana_tab == 1) == liczby_1:
            break
    return wygenerowana_tab

def Glowny_sznajd(a, b, a1, b1, aktualna_tab):
    pkt1, pkt2 = aktualna_tab[a, b], aktualna_tab[a1, b1]
    if pkt1 == pkt2:
        if a == a1:
            poczatek_b, koniec_b = sorted([b, b1])
            sznajd_poziomy(a, poczatek_b, koniec_b, aktualna_tab, pkt1)
        elif b == b1:
            poczatek_a, koniec_a = sorted([a, a1])
            sznajd_pionowy(poczatek_a, b, koniec_a, aktualna_tab, pkt1)

def losuj_pare(aktualna_tab):
    a, b = random.randint(0, len(aktualna_tab)-1), random.randint(0, len(aktualna_tab)-1)
    kierunek = random.choice([(-1,0), (1,0), (0,-1), (0,1)]) 
    a1 = max(0, min(a + kierunek[0], len(aktualna_tab)-1))
    b1 = max(0, min(b + kierunek[1], len(aktualna_tab)-1))
    return a, b, a1, b1

def sznajd_pionowy(a, b, a1, aktualna_tab, war):
    rozmiar = len(aktualna_tab)
    wspolrzedne = [(i, j) for i in range(-1, 2) for j in range(-1, 2)]
    for i, j in wspolrzedne:
        new_a1, new_b = a1 + i, b + j
        if 0 <= new_a1 < rozmiar and 0 <= new_b < rozmiar:
            aktualna_tab[new_a1, new_b] = war

def sznajd_poziomy(a, b, b1, aktualna_tab, war):
    rozmiar = len(aktualna_tab)
    wspolrzedne = [(a+i, b+j) for i in range(-1,2) for j in range(-1,2)]
    for w in wspolrzedne:
        i, j = w
        if 0<= i < rozmiar and 0 <=j <rozmiar:
            aktualna_tab[i,j]=war

def sprawdz_id_a(a, a1, aktualna_tab):
    dl_tab = len(aktualna_tab)
    if a1 < 0 or a1 >= dl_tab:
        a1 = (a + 1) % dl_tab if a1 < 0 else (a - 1) % dl_tab
    return a, a1

def sprawdz_id_b(b, b1, aktualna_tab):
    dl_tab = len(aktualna_tab)
    if b1 < 0 or b1 >= dl_tab:
        b1 = (b + 1) % dl_tab if b1 < 0 else (b - 1) % dl_tab
    return b, b1

# Generowanie tablic
tab_rozm = (20, 20)
procenty = [15, 35, 55, 75, 95]

tablice = [generuj_tablice(pr/100, tab_rozm, pr) for pr in procenty]
czasy = [[] for _ in range(len(procenty))]
wartosci_p = [[] for _ in range(len(procenty))]

for tablica, czas_symulacji, wartosci_p_symulacji in zip(tablice, czasy, wartosci_p):
    for g in range(10**5):
        a_id, b_id, a1_id, b1_id = losuj_pare(tablica)
        a_id, a1_id = sprawdz_id_a(a_id, a1_id, tablica)
        b_id, b1_id = sprawdz_id_b(b_id, b1_id, tablica)
        Glowny_sznajd(a_id, b_id, a1_id, b1_id, tablica)
        g += 1
        czas_symulacji.append(g)
        wartosci_p_symulacji.append(np.count_nonzero(tablica == 1) / np.prod(tab_rozm) * 100)

# Wykres funkcji
colors = ['blue', 'green', 'red', 'yellow', 'pink']
labels = [f'{p}% wartości 1' for p in procenty]

for czas_symulacji, wartosci_p_symulacji, color, label in zip(czasy, wartosci_p, colors, labels):
    pyplot.plot(czas_symulacji, wartosci_p_symulacji, label=label, color=color)

pyplot.xlabel('Odstep czasowy')
pyplot.ylabel("% wartosci '1' ")
pyplot.legend()
pyplot.show()
