import numpy as np
import math as mth
import webbrowser

# oznaczenia c-czerwony, z-zielony, n-niebieski
# definicja tablic
biezaca_tablica = np.array([('c', 'z', 'c'),('c', 'n', 'n'),('c', 'z', 'n')])
pozniejsza_tablica = np.array([('z', 'z', 'z'),('z', 'z', 'z'),('z', 'z', 'z')])
rodzaje_opinii = ['z', 'c', 'n']
s, p = [i / 10 for i in range(1, 10)], [(1 - i / 10) for i in range(1, 10)]
suma_s, suma_p, suma_kolejnego_p = [], [], []
t = 0
alpha = 2
csuma, zsuma, nsuma = [], [], []
cdystans, zdystans, ndystans = [], [], []
cd, zd, nd = [], [], []

def identyczne_stanowisko(dystans, elementy):
    odl = 0
    while odl < len(elementy):
        suma_elem = (s[elementy[odl]] / (1 + (dystans[odl] ** alpha)))
        suma_s.append(suma_elem)
        odl = odl + 1
    return suma_s
                    
def odmienne_stanowisko(dystans, elementy, suma):
    odl = 0
    while odl < len(elementy):
        p_elem = (p[elementy[odl]] / (1 + (dystans[odl] ** alpha)))
        suma.append(p_elem)
        odl = odl + 1
    return suma

#zbior liczacy sume dodana do macierzy
def idsuma(tab_id, tab, isuma):
    for i in range(0, len(tab_id)):
        isuma.append(((len(tab) * tab_id[i][0]) + tab_id[i][1]))
    return isuma

def jaki_dystans(a, b, tab):
    for x in range(len(tab)):
        for y in range(len(tab)):
            if tab[x][y] == "c":
                cdystans.append(mth.sqrt((a - x) ** 2 + (b - y) ** 2))
                dodana = [x, y]
                cd.append(dodana)
            elif tab[x][y] == "z":
                zdystans.append(mth.sqrt((a - x) ** 2 + (b - y) ** 2))
                dodana = [x, y]
                zd.append(dodana)
            else:
                ndystans.append(mth.sqrt((a - x) ** 2 + (b - y) ** 2))
                dodana = [x, y]
                nd.append(dodana)
    #print("wyniki obliczen")
    return cdystans, zdystans, ndystans

# funkcja do generowania HTML dla komorek
def generate_html_cell(color):
    return f'<td style="background-color:{color};"></td>'

# funkcja do generowania calej tabeli HTML
def generate_html_table(tables, all_values):
    html = ''
    for i, (table, values) in enumerate(zip(tables, all_values)):
        html += f'<h2>Tablica dla t= {i}</h2>'
        html += '<table border="1" style="border-collapse: collapse; width: auto;">'
        for row in table:
            #for col in table:
            html += '<tr>'
            for cell in row:
                color = 'red' if cell == 'c' else ('green' if cell == 'z' else 'blue')
                html += f'<td style="width: 30px; height: 30px; background-color:{color};"></td>'
            html += '</tr>'
        html += '</table>'
        # wybierz ostatni zestaw wartosci dla kazdej komorki
        last_values = values[-1]
        identycznosc, odmiennosc, odmiennosc_kolejnego = last_values
        html += f'<p>CZERWONY: {round(identycznosc,2)}, ZIELONY: {round(odmiennosc,2)} and NIEBIESKI: {round(odmiennosc_kolejnego,2)}</p>'
        html += f'<p>MAX wynik: {round(max(identycznosc, odmiennosc, odmiennosc_kolejnego),2)}</p>'
        html += '<br>'
    return html


# glowna czesc programu
tables = []
all_values = []
for t in range(10):
    tables.append(biezaca_tablica.copy())
    values_for_iteration = []
    for i in range(0, len(biezaca_tablica)):
        for j in range(0, len(biezaca_tablica)):
            csuma, zsuma, nsuma = [], [], []
            cdystans, zdystans, ndystans = [], [], []
            cd, zd, nd = [], [], []
            jaki_dystans(i, j, biezaca_tablica)
            if biezaca_tablica[i][j] == "n":
                idsuma(cd, biezaca_tablica, csuma)
                idsuma(zd, biezaca_tablica, zsuma)
                idsuma(nd, biezaca_tablica, nsuma)
                identyczne_stanowisko(ndystans, nsuma)
                identycznosc = 4 * sum(suma_s)
                odmienne_stanowisko(zdystans, zsuma, suma_p)
                odmiennosc = 4 * sum(suma_p)
                odmienne_stanowisko(cdystans, csuma, suma_kolejnego_p)
                odmiennosc_kolejnego = 4 * sum(suma_kolejnego_p)
                max_wynik = max(identycznosc, odmiennosc, odmiennosc_kolejnego)
                values_for_iteration.append((identycznosc, odmiennosc, odmiennosc_kolejnego))

                if max_wynik == identycznosc:
                    pozniejsza_tablica[i][j] = "n"
                elif max_wynik == odmiennosc:
                    pozniejsza_tablica[i][j] = "z"
                else:
                    pozniejsza_tablica[i][j] = "c"
                suma_s.clear()
                suma_p.clear()
                suma_kolejnego_p.clear()
                max_wynik = 0
            elif biezaca_tablica[i][j] == "z":
                idsuma(cd, biezaca_tablica, csuma)
                idsuma(zd, biezaca_tablica, zsuma)
                idsuma(nd, biezaca_tablica, nsuma)
                identyczne_stanowisko(zdystans, zsuma)
                identycznosc = 4 * sum(suma_s)
                odmienne_stanowisko(ndystans, nsuma, suma_p)
                odmiennosc = 4 * sum(suma_p)
                odmienne_stanowisko(cdystans, csuma, suma_kolejnego_p)
                odmiennosc_kolejnego = 4 * sum(suma_kolejnego_p)
                max_wynik = max(identycznosc, odmiennosc, odmiennosc_kolejnego)
                values_for_iteration.append((identycznosc, odmiennosc, odmiennosc_kolejnego))
                if max_wynik == identycznosc:
                    pozniejsza_tablica[i][j] = "z"
                elif max_wynik == odmiennosc:
                    pozniejsza_tablica[i][j] = "n"
                else:
                    pozniejsza_tablica[i][j] = "c"
                suma_s.clear()
                suma_p.clear()
                suma_kolejnego_p.clear()
                max_wynik = 0
            elif biezaca_tablica[i][j] == "c":
                idsuma(cd, biezaca_tablica, csuma)
                idsuma(zd, biezaca_tablica, zsuma)
                idsuma(nd, biezaca_tablica, nsuma)
                identyczne_stanowisko(cdystans, csuma)
                identycznosc = 4 * sum(suma_s)
                odmienne_stanowisko(ndystans, nsuma, suma_p)
                odmiennosc = 4 * sum(suma_p)
                odmienne_stanowisko(zdystans, zsuma, suma_kolejnego_p)
                odmiennosc_kolejnego = 4 * sum(suma_kolejnego_p)
                max_wynik = max(identycznosc, odmiennosc, odmiennosc_kolejnego)
                values_for_iteration.append((identycznosc, odmiennosc, odmiennosc_kolejnego))
                if max_wynik == identycznosc:
                    pozniejsza_tablica[i][j] = "c"
                elif max_wynik == odmiennosc:
                    pozniejsza_tablica[i][j] = "n"
                else:
                    pozniejsza_tablica[i][j] = "z"
                suma_s.clear()
                suma_p.clear()
                suma_kolejnego_p.clear()
                max_wynik = 0
    all_values.append(values_for_iteration)
    for i in range(len(biezaca_tablica)):
        for j in range(len(biezaca_tablica)):
            biezaca_tablica[i][j] = pozniejsza_tablica[i][j]
           
# na koncu zapisujemy wszystkie tabele na raz
html_output = generate_html_table(tables, all_values)
with open('output.html', 'w') as f:
    f.write(html_output)

# otwieramy plik HTML
webbrowser.open('output.html')



