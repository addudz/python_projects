import numpy as np 
import random
from plotly import graph_objects as go

def generuj_tablice(a, b, c, p):
    """
    Generuje tablicę o wymiarach b x c, gdzie p jest ilością jedynek,
    a jest prawdopodobieństwem dla rozkładu binomialnego.
    """
    while True:
        wygenerowana_tab = np.random.binomial(1, a, (b, c))
        if np.count_nonzero(wygenerowana_tab == 1) == p: 
            break
    return wygenerowana_tab

def losuj_pare(rozmiar):
   
    a, b = random.randint(0, rozmiar - 1), random.randint(0, rozmiar - 1)
    kierunek = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)]) 
    a1 = max(0, min(a + kierunek[0], rozmiar - 1))
    b1 = max(0, min(b + kierunek[1], rozmiar - 1))
    return a, b, a1, b1

def sprawdz_id(id, id1, rozmiar):
   
    if id1 < 0 or id1 >= rozmiar:
        id1 = (id + 1) % rozmiar if id1 < 0 else (id - 1) % rozmiar
    return id, id1

def sznajd_pionowy(a, b, a1, aktualna_tab, war):

    rozmiar = len(aktualna_tab)
    for i in range(max(0, a-1), min(a1+2, rozmiar)):
        for j in range(max(0, b-1), min(b+2, rozmiar)):
            aktualna_tab[i, j] = war

def sznajd_poziomy(a, b, b1, aktualna_tab, war):
    
    rozmiar = len(aktualna_tab)
    for i in range(max(0, a-1), min(a+2, rozmiar)):
        for j in range(max(0, b-1), min(b1+2, rozmiar)):
            aktualna_tab[i, j] = war

def Glowny_sznajd(a, b, a1, b1, aktualna_tab):
 
    pkt1 = aktualna_tab[a, b]
    pkt2 = aktualna_tab[a1, b1]

    if pkt1 == pkt2:
        if a == a1:
            poczatek_b, koniec_b = sorted([b, b1])
            sznajd_poziomy(a, poczatek_b, koniec_b, aktualna_tab, pkt1)
        elif b == b1:
            poczatek_a, koniec_a = sorted([a, a1])
            sznajd_pionowy(poczatek_a, b, koniec_a, aktualna_tab, pkt1)
    return 0

def symulacja_wyniki(R, p, b, c, ilosc_jedynek):
  
    wyniki = []
    for _ in range(R):
        aktualna_tab = generuj_tablice(p, b, c, ilosc_jedynek)
        for _ in range(10 ** 3):
            id_a, id_b, id_a1, id_b1 = losuj_pare(len(aktualna_tab))
            id_b, id_b1 = sprawdz_id(id_b, id_b1, len(aktualna_tab))
            id_a, id_a1 = sprawdz_id(id_a, id_a1, len(aktualna_tab))
            Glowny_sznajd(id_a, id_b, id_a1, id_b1, aktualna_tab)
        wyniki.append(np.count_nonzero(aktualna_tab == 1))
    return wyniki

def oblicz_srednia_i_std(wyniki):
  
    srednia = np.nanmean(wyniki) / 400
    std = np.nanstd(wyniki) / 20
    srednia *=100
    return srednia, std

def generuj_dane_do_tabeli(R_values, p_values, b, c):
  
    dane = []
    for R in R_values:
        for p in p_values:
            wyniki = symulacja_wyniki(R, p, b, c, int(b * c * p))
            srednia, std = oblicz_srednia_i_std(wyniki)
            dane.append((R, p, srednia, std))
    return dane

def generuj_tabele(dane):
   
    dane_transponowane = list(zip(*dane))  # Transponujemy dane przed przekazaniem do tabeli
    fig = go.Figure(data=[go.Table(
        header=dict(values=["R", "p0", "p srednia", "p std"],
                    line_color='chocolate',
                    fill_color='beige',
                    align='center'),
        cells=dict(values=dane_transponowane,  # Przekazujemy transponowane dane
                   line_color='chocolate',
                   fill_color='white',
                   align='center')
    )])
    fig.update_layout(width=1300, height=800)
    fig.update_layout(title="Suma: 400 próbek dla kazdego przypadku")
    fig.show()


# Parametry
R_values = [10, 1000, 10000]
p_values = [0.25, 0.5, 0.75]
b = 20
c = 20

dane = generuj_dane_do_tabeli(R_values, p_values, b, c)
generuj_tabele(dane)
