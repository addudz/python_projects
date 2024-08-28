import numpy as np

# Inicjalizacja siatki 20x20 z trzema opiniami
opinie = ['czerwona', 'zielona', 'niebieska']
siatka = np.random.choice(opinie, size=(20, 20))

# Parametry
alpha = 3

# Funkcja obliczająca wpływ społeczny
def wplyw_spoleczny(i, j):
    wpływ = np.zeros(3)
    for k in range(3):
        for l in range(20):
            for m in range(20):
                if (l, m) != (i, j):
                    dystans = np.sqrt((i - l)**2 + (j - m)**2)
                    wpływ[k] += 4 / (1 + dystans**alpha) * (siatka[l, m] == opinie[k])
    return wpływ

# Symulacja dla kolejnych chwil czasowych
html_output = ''
for t in range(1, 11):
    nowa_siatka = np.copy(siatka)
    for i in range(20):
        for j in range(20):
            wpływ = wplyw_spoleczny(i, j)
            nowa_siatka[i, j] = opinie[np.argmax(wpływ)]
    siatka = nowa_siatka

    # Generowanie HTML dla tablicy opinii w danej chwili czasowej
    html_output += f'<h2>Chwila czasowa t={t}</h2>'
    html_output += '<table border="1" style="border-collapse: collapse; width: auto;">'
    for row in siatka:
        html_output += '<tr>'
        for cell in row:
            color = 'red' if cell == 'czerwona' else ('green' if cell == 'zielona' else 'blue')
            html_output += f'<td style="width: 30px; height: 30px; background-color:{color};"></td>'
        html_output += '</tr>'
    html_output += '</table>'

# Zapisanie HTML do pliku
with open('output.html', 'w') as f:
    f.write(html_output)
