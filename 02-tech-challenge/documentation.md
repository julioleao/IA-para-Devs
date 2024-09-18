# Documentação do Código para Resolver Sudoku com Algoritmo Genético

## Configurações e Inicialização

### Constantes

- **`GRID_SIZE`**: `9`
  - Define o tamanho do tabuleiro do Sudoku (9x9).
- **`POP_SIZE`**: `200`
  - Tamanho da população na simulação do algoritmo genético.
- **`MUTATION_RATE`**: `0.1`
  - Taxa de mutação para o algoritmo genético, representando 10%.
- **`NUM_GENERATIONS`**: `2000`
  - Número total de gerações para o algoritmo genético.
- **`ELITISM_COUNT`**: `1`
  - Número de indivíduos da população que serão preservados para a próxima geração.

### Cores

- **`BLUE`**: `(0, 0, 255)`
  - Cor utilizada para números fixos no tabuleiro.
- **`WHITE`**: `(255, 255, 255)`
  - Cor utilizada para números comuns no tabuleiro.
- **`RED`**: `(255, 0, 0)`
  - Cor utilizada para números repetidos no tabuleiro.

### Inicialização do Pygame

- **`pygame.init()`**
  - Inicializa todos os módulos do Pygame necessários para a execução do jogo.
- **`WIDTH`**: `540`
  - Largura da janela de exibição.
- **`HEIGHT`**: `540`
  - Altura da janela de exibição.
- **`SCREEN`**: `pygame.display.set_mode((WIDTH, HEIGHT))`
  - Configura a tela de visualização com as dimensões especificadas.
- **`pygame.display.set_caption("Sudoku Solver")`**
  - Define o título da janela de visualização.
- **`FONT`**: `pygame.font.Font(None, 36)`
  - Define a fonte usada para renderizar os números no tabuleiro.

### Tabuleiro Inicial

- **`SUDOKU_BASE`**:

  ```python
  [
      [0, 0, 0, 3, 0, 0, 0, 0, 0],
      [2, 0, 6, 0, 0, 0, 0, 0, 0],
      [0, 7, 0, 6, 0, 2, 0, 0, 8],
      [0, 0, 0, 0, 0, 0, 5, 7, 0],
      [6, 0, 0, 2, 0, 0, 0, 0, 1],
      [0, 0, 0, 0, 0, 6, 0, 2, 4],
      [0, 0, 0, 0, 2, 0, 0, 8, 0],
      [0, 8, 5, 1, 0, 0, 0, 6, 0],
      [0, 0, 0, 0, 6, 0, 0, 0, 0]
  ]

- `SUDOKU_BASE` : Matriz representando o tabuleiro inicial do Sudoku, com zeros indicando células vazias.

- `FIXED_MASK` : Máscara que indica quais números são fixos e não devem ser alterados.

## Funções

### `initialize_population()`

Inicializa a população aleatória com base no tabuleiro inicial.

- **Retorno**: Lista de matrizes (soluções possíveis) onde os números fixos são mantidos e as células vazias são preenchidas com números aleatórios.

### `repair_solution(board)`

Repara a solução substituindo números duplicados em linhas, colunas e subgrades.

- **Parâmetros**:
  - `board` : Matriz representando um tabuleiro de Sudoku.
- **Retorno**: Matriz corrigida, onde números duplicados são substituídos por números que faltam em linhas, colunas e subgrades.

### `fitness(board)`

Calcula a aptidão de um tabuleiro, penalizando números repetidos.

- **Parâmetros**:
  - `board` : Matriz representando um tabuleiro de Sudoku.
- **Retorno**: Valor de aptidão do tabuleiro, que é maior para soluções que têm menos números repetidos e melhor preenchimento de subgrades.

### `crossover(parent1, parent2)`

Realiza o crossover entre dois pais para gerar um filho.

- **Parâmetros**:
  - `parent1` : Matriz representando o primeiro pai.
  - `parent2` : Matriz representando o segundo pai.
- **Retorno**: Matriz resultante do crossover, onde células são escolhidas aleatoriamente entre os dois pais.

### `mutate(board)`

Aplica mutação trocando dois números aleatórios em uma linha.

- **Parâmetros**:
  - `board` : Matriz representando um tabuleiro de Sudoku.
- **Retorno**: Matriz com uma linha aleatória alterada se a taxa de mutação é satisfeita.

### `select_population(population)`

Seleciona os melhores indivíduos e adiciona diversidade.

- **Parâmetros**:
  - `population` : Lista de matrizes representando a população atual.
- **Retorno**: Lista de matrizes representando a população selecionada para a próxima geração.

### `find_repeated_numbers(board)`

Encontra números repetidos em linhas, colunas e subgrades.

- **Parâmetros**:
  - `board` : Matriz representando um tabuleiro de Sudoku.
- **Retorno**: Matriz booleana onde `True` indica que o número na posição correspondente está repetido.

### `draw_sudoku(board)`

Desenha o tabuleiro Sudoku na tela com números repetidos em vermelho.

- **Parâmetros**:
  - `board` : Matriz representando um tabuleiro de Sudoku.
- **Retorno**: Nenhum. Desenha o tabuleiro na tela do Pygame e atualiza a visualização.

### `main()`

Função principal para rodar o algoritmo genético.

- **Processo**:
  1. Inicializa a população.
  2. Executa o loop para o número de gerações definido.
  3. Avalia a aptidão dos indivíduos e exibe o melhor tabuleiro.
  4. Realiza seleção, crossover e mutação para gerar a nova população.
  5. Desenha o tabuleiro atualizado na tela.
  6. Finaliza o Pygame se a janela for fechada.

## Execução

- **Função Principal**:

  ```python
  if __name__ == "__main__":
      main()
