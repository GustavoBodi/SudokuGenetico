import numpy as np
from geneticalgorithm import geneticalgorithm as ga


class OitoRainhas():
    def __init__(self, tamanho_populacao, taxa_mutacao, taxa_crossover, limite_geracao):
        self.__tabuleiro = np.zeros((8, 8), dtype=int)
        self.__tamanho_populacao = tamanho_populacao
        self.__taxa_mutacao = taxa_mutacao
        self.__taxa_crossover = taxa_crossover
        self.__limite_geracao = limite_geracao
        self.__populacao = []
        self.__melhor = []

    def __fitness_function(self, posicoes):
        conflitos = 0
        n = len(posicoes)
        # Conflitos de coluna
        conflitos += n - len(np.unique(posicoes))
        # Conflitos diagonais
        for i in range(n):
            for j in range(i + 1, n):
                if abs(posicoes[i] - posicoes[j]) == abs(i - j):
                    conflitos += 1
        return conflitos

    def resolver(self):
        varbound = np.array([[0, 7]] * 8)  # Limites para cada rainha (colunas 0 a 7)
        algoritmo_param = {
            'max_num_iteration': self.__limite_geracao,
            'population_size': self.__tamanho_populacao,
            'mutation_probability': self.__taxa_mutacao,
            'elit_ratio': 0.02,
            'crossover_probability': self.__taxa_crossover,
            'parents_portion': 0.3,
            'crossover_type': 'uniform',
            'mutation_type': 'uniform_by_range',
            'selection_type': 'roulette',
            'max_iteration_without_improv': None
        }

        modelo = ga(
            function=self.__fitness_function,
            dimension=8,
            variable_type='int',
            variable_boundaries=varbound,
            algorithm_parameters=algoritmo_param
        )

        modelo.run()

        solucao = modelo.output_dict['variable'].astype(int)
        fitness = modelo.output_dict['function']

        self.__set_rainhas(solucao)

        if fitness == 0:
            print("Uma solucao valida foi encontrada!")
            print(self)
        else:
            print("Nenhuma solucao valida encontrada dentro do limite de geracoes.")
            print(f"Melhor fitness (numero de conflitos): {fitness}")
            print(self)

    def __set_rainhas(self, posicoes):
        self.__tabuleiro = np.zeros((8, 8), dtype=int)
        for linha, coluna in enumerate(posicoes):
            self.__tabuleiro[linha, coluna] = 1

    def __str__(self):
        tabuleiro_str = "Tabuleiro:\n"
        for linha in self.__tabuleiro:
            linha_str = ''
            for celula in linha:
                if celula == 1:
                    linha_str += ' Q '
                else:
                    linha_str += ' . '
            tabuleiro_str += linha_str + '\n'
        return tabuleiro_str


def main():
    print("Resolucao do problema das 8 Rainhas usando algoritmo genetico.")
    oito_rainhas = OitoRainhas(tamanho_populacao=200, taxa_mutacao=0.2, taxa_crossover=0.8, limite_geracao=50)
    oito_rainhas.resolver()


if __name__ == "__main__":
    main()

