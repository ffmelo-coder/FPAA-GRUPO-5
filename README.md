# PathFinder - Resolvendo o Labirinto 2D com o Algoritmo A\*

## Contexto

Este projeto implementa o Algoritmo A\* para encontrar o menor caminho entre dois pontos em um labirinto 2D, evitando obstáculos.

O robô parte de um ponto inicial **S** (start) e precisa chegar ao ponto final **E** (end), movendo-se apenas entre células livres, sem colidir com obstáculos.

## Objetivo

Implementar o Algoritmo A\* para encontrar o menor caminho em um labirinto 2D entre dois pontos, considerando os custos dos movimentos e usando a heurística de Manhattan.

## Como executar

### Requisitos

- Python 3.x instalado

### Execução

```bash
python main.py
```

### Entrada

O programa solicitará que você digite o labirinto linha por linha:

- **0**: Célula livre (onde o robô pode se mover)
- **1**: Obstáculo (onde o robô não pode passar)
- **S ou 2**: Ponto inicial (start)
- **E ou 3**: Ponto final (end)

Digite cada linha separada por espaços e pressione Enter. Quando terminar, pressione Enter em uma linha vazia.

### Exemplo de entrada:

```
S 0 1 0 0
0 0 1 0 1
1 0 1 0 0
1 0 0 E 1
```

Após inserir o labirinto, o programa perguntará:

```
Deseja permitir movimentacao diagonal? (s/n):
```

Digite `s` para permitir movimentação diagonal ou `n` para apenas 4 direções.

### Saída

O programa retorna:

1. O menor caminho em formato de coordenadas: `[(0, 0), (1, 0), (1, 1), (2, 1), ...]`
2. O labirinto com o caminho destacado usando `*`

## Estrutura do projeto

```
FPAA GRUPO/
├── main.py          # Programa principal com entrada de dados
├── pathfinder.py    # Implementação do algoritmo A*
```

## Algoritmo A\*

O algoritmo A\* combina:

- **g(n)**: Custo real do caminho do início até o nó atual
- **h(n)**: Heurística (estimativa) da distância do nó atual até o destino
- **f(n) = g(n) + h(n)**: Função de avaliação total

### Heurística de Manhattan (4 direções)

```
h(n) = |x_atual - x_final| + |y_atual - y_final|
```

Esta heurística estima a distância entre dois pontos somando as diferenças absolutas de suas coordenadas.

### Heurística Euclidiana (movimentação diagonal)

Quando a movimentação diagonal está habilitada, o algoritmo usa a distância euclidiana:

```
h(n) = √((x_atual - x_final)² + (y_atual - y_final)²)
```

Esta heurística fornece uma estimativa mais precisa quando movimentos diagonais são permitidos.

### Custos de Movimento

- Movimentação horizontal/vertical: custo = 1
- Movimentação diagonal: custo = √2 ≈ 1.414

## Primeira Entrega

Esta primeira versão inclui:

- ✅ Leitura do labirinto via entrada do usuário
- ✅ Identificação automática dos pontos S e E
- ✅ Implementação da heurística de Manhattan
- ✅ Implementação da heurística Euclidiana para movimento diagonal
- ✅ Algoritmo A\* básico funcional
- ✅ Movimentação nas 4 direções (cima, baixo, esquerda, direita)
- ✅ Movimentação diagonal opcional (8 direções)
- ✅ Validação se S e E existem no labirinto
- ✅ Validação de unicidade de S e E
- ✅ Validação de formato do labirinto (matriz retangular)
- ✅ Tratamento de erros de entrada inválida
- ✅ Exibição do caminho encontrado
- ✅ Visualização do labirinto com caminho destacado
- ✅ Sistema de custos diferenciados (1 para reto, √2 para diagonal)

## Autores

Filipe Faria Melo

Augusto Fuscaldi Cerezo
