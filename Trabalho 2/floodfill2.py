from collections import deque
from typing import List, Tuple, Dict, Optional
import copy


def colorir_regiao(grid: List[List[int]], start: Tuple[int, int], color: int) -> bool:
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


def colorir_regiao_history(
    grid: List[List[int]],
    start: Tuple[int, int],
    color: int,
    history: List[List[List[int]]],
) -> bool:
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
    history.append(copy.deepcopy(grid))
    while dq:
        r, c = dq.popleft()
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < linhas and 0 <= nc < colunas and grid[nr][nc] == 0:
                grid[nr][nc] = color
                dq.append((nr, nc))
                history.append(copy.deepcopy(grid))
    return True


def colorir_todas_regioes(
    grid: List[List[int]],
    inicio: Optional[Tuple[int, int]] = None,
    primeiro_cor: int = 2,
    record_history: bool = False,
) -> Dict[int, List[Tuple[int, int]]]:
    linhas = len(grid)
    if linhas == 0:
        return {}
    colunas = len(grid[0])

    def encontrar_proximo_zero() -> Optional[Tuple[int, int]]:
        for i in range(linhas):
            for j in range(colunas):
                if grid[i][j] == 0:
                    return (i, j)
        return None

    resultados: Dict[int, List[Tuple[int, int]]] = {}
    cor_atual = primeiro_cor

    history: List[List[List[int]]] = [] if record_history else None

    if inicio is not None:
        r0, c0 = inicio
        if 0 <= r0 < linhas and 0 <= c0 < colunas and grid[r0][c0] == 0:
            if record_history:
                colorir_regiao_history(grid, inicio, cor_atual, history)
            else:
                colorir_regiao(grid, inicio, cor_atual)
            coords = []
            for i in range(linhas):
                for j in range(colunas):
                    if grid[i][j] == cor_atual:
                        coords.append((i, j))
            resultados[cor_atual] = coords
            cor_atual += 1

    while True:
        proximo = encontrar_proximo_zero()
        if proximo is None:
            break
        if record_history:
            colorir_regiao_history(grid, proximo, cor_atual, history)
        else:
            colorir_regiao(grid, proximo, cor_atual)
        coords = []
        for i in range(linhas):
            for j in range(colunas):
                if grid[i][j] == cor_atual:
                    coords.append((i, j))
        resultados[cor_atual] = coords
        cor_atual += 1

    if record_history:
        resultados[-1] = history

    return resultados


def imprimir_grid(grid: List[List[int]]):
    for linha in grid:
        print(" ".join(str(x) for x in linha))
