import numpy as np
import random
import pygame
from board import Sudoku

# Configurações
GRID_SIZE = 9
POP_SIZE = 100
MUTATION_RATE = 0.9
NUM_GENERATIONS = 2000
ELITISM_COUNT = 5
BEST_SOLUTION = 3 * GRID_SIZE * GRID_SIZE

BLUE = (0, 0, 255)
WHITE = (0, 0, 0)
RED = (255, 0, 0)

# Inicialização do Pygame
pygame.init()
WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")
FONT = pygame.font.Font(None, 36)


# Tabuleiro inicial
SUDOKU_BASE = Sudoku.random(0.7)

FIXED_MASK = np.array(SUDOKU_BASE) != 0  # Máscara para números fixos


def fill_board_randomly(board):
    """Preenche as células vazias do tabuleiro com números válidos"""
    for row in range(GRID_SIZE):
        # Encontra os números já presentes na linha
        existing_numbers = set(board[row])
        missing_numbers = set(range(1, 10)) - existing_numbers
        missing_numbers = list(missing_numbers)
        random.shuffle(missing_numbers)  # Embaralha os números que faltam

        # Preenche as células vazias com os números faltantes
        for col in range(GRID_SIZE):
            if board[row, col] == 0:  # Somente preenche as células vazias
                board[row, col] = missing_numbers.pop()

    return board


def initialize_population_valid():
    """Inicializa a população de forma válida, seguindo as regras básicas"""
    population = []

    for _ in range(POP_SIZE):
        # Copia o tabuleiro base para garantir que os números fixos são mantidos
        new_board = np.copy(SUDOKU_BASE)

        # Preenche o tabuleiro respeitando as regras básicas de linha e coluna
        filled_board = fill_board_randomly(new_board)

        # Aplica uma reparação nas subgrades para garantir validade total
        repaired_board = repair_subgrids(filled_board)

        # Adiciona à população
        population.append(repaired_board)

    return population


def repair_subgrids(board):
    # Reparar subgrades
    for r in range(0, GRID_SIZE, 3):
        for c in range(0, GRID_SIZE, 3):
            subgrid = board[r : r + 3, c : c + 3].flatten()
            missing_numbers = set(range(1, 10)) - set(subgrid)
            repeated_numbers = [num for num in subgrid if list(subgrid).count(num) > 1]

            for repeat_num in repeated_numbers:
                row_idx, col_idx = np.where(board[r : r + 3, c : c + 3] == repeat_num)
                actual_row, actual_col = r + row_idx[0], c + col_idx[0]
                if not FIXED_MASK[actual_row, actual_col]:
                    # Apenas altera se não for um número fixo
                    if missing_numbers:
                        board[actual_row, actual_col] = missing_numbers.pop()
    return board


def fitness(board):
    row_penalty = 0
    col_penalty = 0
    subgrid_penalty = 0

    # Penaliza números repetidos em cada linha
    for i in range(GRID_SIZE):
        unique_values = set(board[i])
        row_penalty += GRID_SIZE - len(unique_values)  # Penaliza repetições

    # Penaliza números repetidos em cada coluna
    for i in range(GRID_SIZE):
        unique_values = set(board[:, i])
        col_penalty += GRID_SIZE - len(unique_values)  # Penaliza repetições

    # Penaliza números repetidos em cada subgrade 3x3
    for r in range(0, GRID_SIZE, 3):
        for c in range(0, GRID_SIZE, 3):
            subgrid = board[r : r + 3, c : c + 3].flatten()
            unique_values = set(subgrid)
            subgrid_penalty += GRID_SIZE - len(unique_values)  # Penaliza repetições

    # O fitness total é a soma das penalidades invertida, queremos minimizar as penalidades
    total_penalty = row_penalty + col_penalty + subgrid_penalty
    max_fitness = (
        3 * GRID_SIZE * GRID_SIZE
    )  # O máximo que podemos atingir, caso não haja repetições

    return max_fitness - total_penalty


def crossover(parent1, parent2):
    """Realiza o crossover trocando subgrades 3x3 entre dois pais"""
    child = np.copy(parent1)
    for i in range(3):
        for j in range(3):
            if random.random() > 0.5:  # Troca a subgrade com 50% de chance
                child[i * 3 : (i + 1) * 3, j * 3 : (j + 1) * 3] = parent2[
                    i * 3 : (i + 1) * 3, j * 3 : (j + 1) * 3
                ]
    return child


def tournament_selection(population, k=3):
    """Realiza a seleção por torneio para escolher um indivíduo"""
    tournament = random.sample(population, k)
    return max(tournament, key=fitness)


def mutate(board):
    """Aplica mutação trocando dois números dentro de uma subgrade 3x3"""
    if random.random() < MUTATION_RATE:
        subgrid_row = random.randint(0, 2) * 3
        subgrid_col = random.randint(0, 2) * 3

        available_positions = [
            (r, c)
            for r in range(subgrid_row, subgrid_row + 3)
            for c in range(subgrid_col, subgrid_col + 3)
            if not FIXED_MASK[r, c]
        ]

        if len(available_positions) >= 2:
            pos1, pos2 = random.sample(available_positions, 2)
            board[pos1], board[pos2] = board[pos2], board[pos1]

    return board


def select_population(population):
    """Seleciona os melhores indivíduos e adiciona diversidade"""
    population.sort(key=fitness, reverse=True)
    top_half = population[: POP_SIZE // 2]
    bottom_half = random.sample(population[POP_SIZE // 2 :], POP_SIZE // 4)
    return top_half + bottom_half


def find_repeated_numbers(board):
    """Encontra números repetidos em linhas, colunas e subgrades"""
    repeated = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)

    # Verifica repetições nas linhas
    for row in range(GRID_SIZE):
        unique, counts = np.unique(board[row], return_counts=True)
        repeated_in_row = unique[counts > 1]
        for num in repeated_in_row:
            repeated[row] |= board[row] == num

    # Verifica repetições nas colunas
    for col in range(GRID_SIZE):
        unique, counts = np.unique(board[:, col], return_counts=True)
        repeated_in_col = unique[counts > 1]
        for num in repeated_in_col:
            repeated[:, col] |= board[:, col] == num

    return repeated


def draw_sudoku(board):
    """Desenha o tabuleiro Sudoku na tela com números repetidos em vermelho"""
    block_size = WIDTH // GRID_SIZE
    SCREEN.fill((255, 255, 255))
    repeated = find_repeated_numbers(board)

    for i in range(GRID_SIZE + 1):
        line_width = 4 if i % 3 == 0 else 1
        pygame.draw.line(
            SCREEN, WHITE, (i * block_size, 0), (i * block_size, HEIGHT), line_width
        )
        pygame.draw.line(
            SCREEN, WHITE, (0, i * block_size), (WIDTH, i * block_size), line_width
        )

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = board[row, col]
            if num != 0:
                if FIXED_MASK[row, col]:
                    color = BLUE
                elif repeated[row, col]:
                    color = RED
                else:
                    color = WHITE
                value = FONT.render(str(num), True, color)
                SCREEN.blit(value, (col * block_size + 20, row * block_size + 10))

    pygame.display.flip()


def draw_progress_bar(generation, total_generations):
    """Desenha uma barra de progresso na parte inferior da tela"""
    progress = generation / total_generations
    pygame.draw.rect(
        SCREEN, (0, 255, 0), (50, HEIGHT - 30, progress * (WIDTH - 100), 20)
    )
    pygame.draw.rect(SCREEN, WHITE, (50, HEIGHT - 30, WIDTH - 100, 20), 2)


def main():
    """Função principal para rodar o algoritmo genético"""
    population = initialize_population_valid()

    for generation in range(NUM_GENERATIONS):
        population = sorted(population, key=fitness, reverse=True)
        best_board = population[0]

        print(f"Generation {generation}: Best fitness = {fitness(best_board)}")
        draw_sudoku(best_board)

        if fitness(best_board) == BEST_SOLUTION:
            print(f"Solução perfeita encontrada na geração {generation}")
            break
        # Seleção e crossover
        new_population = select_population(population)
        if fitness(best_board) > 0:
            new_population = [
                crossover(
                    tournament_selection(new_population),
                    tournament_selection(new_population),
                )
                for _ in range(POP_SIZE - ELITISM_COUNT)
            ]

        # Mantém o melhor da geração anterior
        new_population.insert(0, best_board)
        population = new_population

        # Aplicação de mutação nos indivíduos
        population = [mutate(ind) for ind in population]

        # Tratamento de eventos do Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

    while True:
        draw_sudoku(best_board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


if __name__ == "__main__":
    main()
