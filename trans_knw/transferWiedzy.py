import numpy as np
import matplotlib.pyplot as plt

# Constants
L = 5
K = 4
time_steps = 50
probabilities = [0.9, 0.7, 0.5, 0.3]
R = 50

# budowa macierzy
def initialize_matrix(L, p):
    matrix = np.random.rand(L, L, K) < p
    return matrix.astype(int)

# helikalne warunki brzegowe
def apply_helicoidal_boundaries(matrix):
    L = matrix.shape[0]
    extended_matrix = np.zeros((L+2, L+2, K), dtype=int)
    extended_matrix[1:-1, 1:-1] = matrix
    extended_matrix[0, 1:-1] = matrix[-1, :]
    extended_matrix[-1, 1:-1] = matrix[0, :]
    extended_matrix[1:-1, 0] = matrix[:, -1]
    extended_matrix[1:-1, -1] = matrix[:, 0]
    extended_matrix[0, 0] = matrix[-1, -1]
    extended_matrix[0, -1] = matrix[-1, 0]
    extended_matrix[-1, 0] = matrix[0, -1]
    extended_matrix[-1, -1] = matrix[0, 0]
    return extended_matrix

# aktualizacja macierzy
def update_matrix(matrix):
    L = matrix.shape[0]
    extended_matrix = apply_helicoidal_boundaries(matrix)
    new_matrix = matrix.copy()

    for i in range(L):
        for j in range(L):
            neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
            for k in range(K):
                if matrix[i, j, k] == 0:
                    for ni, nj in neighbors:
                        ni = (ni + L) % L
                        nj = (nj + L) % L
                        if extended_matrix[ni+1, nj+1, k] == 1 and np.sum(extended_matrix[ni+1, nj+1]) == np.sum(matrix[i, j]) + 1:
                            new_matrix[i, j, k] = 1
                            break
    return new_matrix

# symulacja dla pojedynczego agenta
def run_simulation_for_cell(p, time_steps):
    results_K2 = np.zeros(time_steps)
    results_K4 = np.zeros(time_steps)
    
    for r in range(R):
        matrix = initialize_matrix(L, p)
        for t in range(time_steps):
            counts_K2 = np.sum(np.sum(matrix, axis=2) == 2)
            counts_K4 = np.sum(np.sum(matrix, axis=2) == 4)
            results_K2[t] += counts_K2
            results_K4[t] += counts_K4
            matrix = update_matrix(matrix)
    
    avg_K2 = results_K2 / R
    avg_K4 = results_K4 / R
    
    return avg_K2, avg_K4

# glowna funkcja
def main():
    results_K2 = {}
    results_K4 = {}
    
    for p in probabilities:
        avg_K2, avg_K4 = run_simulation_for_cell(p, time_steps)
        results_K2[p] = avg_K2
        results_K4[p] = avg_K4
    
    # wykres
    plot_results(results_K2, 'Liczba agentów z wiedzą K=2 w czasie')
    plot_results(results_K4, 'Liczba agentów z wiedzą K=4 w czasie')
    
    # wyniki
    save_results_to_file(results_K2, 'wyniki_K2.txt')
    save_results_to_file(results_K4, 'wyniki_K4.txt')

def plot_results(results, title):
    plt.figure(figsize=(10, 6))
    for p, result in results.items():
        plt.plot(result, label=f'p={p}')
    plt.xlabel('Krok czasowy')
    plt.ylabel('Liczba agentów')
    plt.title(title)
    plt.legend()
    plt.ylim(0, 25)
    plt.show()

def save_results_to_file(results, filename):
    with open(filename, 'w') as file:
        for p, result in results.items():
            file.write(f'p={p}\n')
            for t, value in enumerate(result):
                file.write(f'Krok czasowy {t}: {value}\n')
            file.write('\n')

if __name__ == "__main__":
    main()
