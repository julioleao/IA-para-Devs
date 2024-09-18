# Tech Challenge II

## Desafio

Resolver um problema real utilizando algoritmo genético

## Problema escolhido

Resolver um Sudoku 9x9 com diferentes níveis de dificuldade

## Como começar?

- Requisitos mínimos

  - Python 3.10+
  - Virtualenv

- Clone o repositório e acesse o diretório do projeto

```bash
git clone https://github.com/julioleao/IA-para-Devs.git

cd 02-tech-challenge
```

- Crie um ambiente virtual Python

```bash
virtualenv venv

#Windows
venv\Script\activate

#Linux
source venv/bin/activate
```

- Agora instale as dependencias com

```bash
pip install -r requirements
```

## Configurando e executando o código

Abra o arquivo `sudoku.py` e ajustes as configurações conforme necessário

| Constante       | Valor padrão       | Descrição                                                                                                                                                                                                                                                               |
| --------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| POP_SIZE        | 100                | Tamanho da população gerada                                                                                                                                                                                                                                             |
| MUTATE_RATE     | 0.9                | A taxa de mutação (1.0 sempre soferá mutação)                                                                                                                                                                                                                           |
| NUM_GENERATIONS | 2000               | O tamanho máximo de gerações para que o algoritmo encerre caso não encontre um resultado perfeito                                                                                                                                                                       |
| ELITISM_COUNT   | 5                  | O número das melhores populações (selecionada por elitismo) que serão usadas no cruzamento                                                                                                                                                                              |
| SUDOKU_BASE     | Sudoku.random(0.7) | Utiliza a classe Sudoku para gerar o tabuleiro inicial com base na dificuldade informada<br><br> - Sudoku.easy()<br> - Sudoku.medium()<br> - Sudoku.hard()<br> - Sudoku.evil()<br> - Sudoku.random(difficulty: float) <br><br> Valor 0 gera um tabuleiro já solucionado |

Feito a configuração, basta executar o arquivo `sudoku.py`

```bash
python sudoku.py
```
