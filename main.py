import random


class Sudoku():
    def __init__(self, tamanho_populacao, taxa_mutacao, taxa_crossover, limite_geracao):
        self.__tabuleiro = [[0 for i in range(9)] for j in range(9)]
        self.__tamanho_populacao = tamanho_populacao
        self.__taxa_mutacao = taxa_mutacao
        self.__taxa_crossover = taxa_crossover
        self.__limite_geracao = limite_geracao
        self.__populacao = []
        self.__melhor = []
        self.__variaveis = self.__tabuleiro == 0

    def __validate_placing(self, row: int, column: int, value: int):
        return self.__validate_placing_row(row, column, value) and \
                self.__validate_placing_column(row, column, value) and \
                self.__validate_placing_small_matrix(row, column, value)

    def __get_small_matrix_cells(self, row: int, column: int):
        row_inicio, col_inicio = 3 * (row // 3), 3 * (column // 3)
        return (self.__tabuleiro[i][j] for i in range(row_inicio, row_inicio + 3) for j in range(col_inicio, col_inicio + 3))

    def __validate_placing_row(self, row: int, column: int, value: int) -> bool:
        if value in self.__tabuleiro[row]:
            return False
        return True

    def __validate_placing_column(self, row: int, column: int, value: int) -> bool:
        if value in [self.__tabuleiro[row][column] for i in range(9)]:
            return False
        return True

    def __validate_placing_small_matrix(self, row: int, column: int, value: int) -> bool:
        return value not in self.__get_small_matrix_cells(row, column)

    def preencher(self, dicas: int = 0):
        dicas_colocadas = 0
        while dicas_colocadas < dicas:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.__tabuleiro[row][col] == 0:
                num = random.randint(1, 9)
                if self.__validate_placing(row, col, num):
                    self.__tabuleiro[row][col] = num
                    dicas_colocadas += 1

    def __str__(self):
        tabuleiro = ""
        for i, linha in enumerate(self.__tabuleiro):
            linha_str = "| "
            if i % 3 == 0:
                tabuleiro += "-" * 37 + "\n"
            for j, valor in enumerate(linha, 1):
                if valor == 0:
                    linha_str += "."
                else:
                    linha_str += str(valor)
                if j % 3 == 0:
                    linha_str += " | "
                else:
                    linha_str += "   "
            linha_str += "\n"
            tabuleiro += linha_str
        tabuleiro += "-" * 37 + "\n"
        return tabuleiro


def fitness_function(X):
    board = X.reshape(9, 9).astype(int)
    score = 0

    # Calculate row uniqueness
    for row in board:
        score += len(set(row))  # More unique values = higher score

    # Calculate column uniqueness
    for col in board.T:
        score += len(set(col))

    # Calculate subgrid uniqueness
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            subgrid = board[row:row + 3, col:col + 3].flatten()
            score += len(set(subgrid))

    # Subtract penalties for duplicate values
    max_score = 9 * 3 * 9  # Maximum possible score if everything is perfect
    return max_score - score  # Minimize penalties


def main():
    print("This is the sudoku game.")
    sudoku = Sudoku(300, 0.2, 0.9, 1000)
    sudoku.preencher(10)
    print(sudoku)


if __name__ == "__main__":
    main()
