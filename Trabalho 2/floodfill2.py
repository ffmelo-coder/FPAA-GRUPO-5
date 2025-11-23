from collections import deque
from typing import List, Tuple, Dict, Optional


def colorir_regiao(grid: List[List[int]], start: Tuple[int, int], color: int) -> bool:
    """
    Preenche a região conectada (4-direções) de células com valor 0 a partir de 'start'
    com o valor 'color'. Retorna True se preenchimento ocorreu, False caso o ponto
    de início não seja uma célula navegável (0).
    """
    linhas = len(grid)
    if linhas == 0:
        return False
    colunas = len(grid[0])
    r0, c0 = start
    if not (0 <= r0 < linhas and 0 <= c0 < colunas):
        return False
    if grid[r0][c0] != 0:
        return False

    dq = deque()
    dq.append((r0, c0))
    grid[r0][c0] = color
    while dq:
        r, c = dq.popleft()
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < linhas and 0 <= nc < colunas and grid[nr][nc] == 0:
                grid[nr][nc] = color
                dq.append((nr, nc))
    return True


def colorir_todas_regioes(grid: List[List[int]], inicio: Optional[Tuple[int, int]] = None,
                           primeiro_cor: int = 2) -> Dict[int, List[Tuple[int, int]]]:
    """
    Percorre o grid e coloriza todas as regiões navegáveis (valores 0), começando
    pela região que contém 'inicio' (se fornecido e for 0). Cada região recebe
    uma cor incremental (2,3,4,...). Retorna dicionário mapeando cor -> lista de
    coordenadas preenchidas por essa cor.

    Observações:
    - Células com valor 1 são obstáculos e não são alteradas.
    - Células com valor >=2 são consideradas já coloridas e preservadas.
    """
    linhas = len(grid)
    if linhas == 0:
        return {}
    colunas = len(grid[0])

    # Função auxiliar para procurar próxima célula 0
    def encontrar_proximo_zero() -> Optional[Tuple[int, int]]:
        for i in range(linhas):
            for j in range(colunas):
                if grid[i][j] == 0:
                    return (i, j)
        return None

    resultados: Dict[int, List[Tuple[int, int]]] = {}
    cor_atual = primeiro_cor

    # Se inicio especificado e é 0, primeiro preenche a partir dele
    if inicio is not None:
        r0, c0 = inicio
        if 0 <= r0 < linhas and 0 <= c0 < colunas and grid[r0][c0] == 0:
            # coleciona coordenadas preenchidas para registro
            # preenchimento coloca a cor nas células
            colorir_regiao(grid, inicio, cor_atual)
            # recolher coords preenchidas (varredura simples)
            coords = []
            for i in range(linhas):
                for j in range(colunas):
                    if grid[i][j] == cor_atual:
                        coords.append((i, j))
            resultados[cor_atual] = coords
            cor_atual += 1

    # Preenche as demais regiões até não restarem zeros
    while True:
        proximo = encontrar_proximo_zero()
        if proximo is None:
            break
        colorir_regiao(grid, proximo, cor_atual)
        coords = []
        for i in range(linhas):
            for j in range(colunas):
                if grid[i][j] == cor_atual:
                    coords.append((i, j))
        resultados[cor_atual] = coords
        cor_atual += 1

    return resultados


def imprimir_grid(grid: List[List[int]]):
    for linha in grid:
        print(" ".join(str(x) for x in linha))


if __name__ == "__main__":
    # Demo rápido com os exemplos do enunciado
    exemplo1 = [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 0, 1],
        [0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0],
    ]
    print("Exemplo 1 - Entrada:")
    imprimir_grid(exemplo1)
    colorir_todas_regioes(exemplo1, inicio=(0, 0), primeiro_cor=2)
    print("Exemplo 1 - Saída:")
    imprimir_grid(exemplo1)

    print("\nExemplo 2 - Entrada:")
    exemplo2 = [
        [0, 1, 0, 0, 1],
        [0, 1, 0, 0, 1],
        [0, 1, 1, 1, 1],
        [0, 0, 0, 1, 0],
    ]
    imprimir_grid(exemplo2)
    colorir_todas_regioes(exemplo2, inicio=(0, 2), primeiro_cor=2)
    print("Exemplo 2 - Saída:")
    imprimir_grid(exemplo2)
