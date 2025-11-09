import heapq
from typing import List, Tuple, Optional


class PathFinder:
    def __init__(self, labirinto: List[List[int]]):
        self.labirinto = labirinto
        self.linhas = len(labirinto)
        self.colunas = len(labirinto[0]) if labirinto else 0
        self.inicio = None
        self.fim = None

    def encontrar_posicoes(self) -> bool:
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.labirinto[i][j] == 2:
                    self.inicio = (i, j)
                elif self.labirinto[i][j] == 3:
                    self.fim = (i, j)

        return self.inicio is not None and self.fim is not None

    def heuristica(self, atual: Tuple[int, int]) -> int:
        if self.fim is None:
            return 0
        return abs(atual[0] - self.fim[0]) + abs(atual[1] - self.fim[1])

    def vizinhos_validos(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = pos
        vizinhos = []
        direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.linhas and 0 <= ny < self.colunas:
                if self.labirinto[nx][ny] != 1:
                    vizinhos.append((nx, ny))

        return vizinhos

    def a_estrela(self) -> Optional[List[Tuple[int, int]]]:
        if not self.encontrar_posicoes():
            return None

        fila_prioridade = []
        heapq.heappush(fila_prioridade, (0, self.inicio))

        veio_de = {}
        custo_g = {self.inicio: 0}

        while fila_prioridade:
            _, atual = heapq.heappop(fila_prioridade)

            if atual == self.fim:
                return self.reconstruir_caminho(veio_de)

            for vizinho in self.vizinhos_validos(atual):
                novo_custo = custo_g[atual] + 1

                if vizinho not in custo_g or novo_custo < custo_g[vizinho]:
                    custo_g[vizinho] = novo_custo
                    f = novo_custo + self.heuristica(vizinho)
                    heapq.heappush(fila_prioridade, (f, vizinho))
                    veio_de[vizinho] = atual

        return None

    def reconstruir_caminho(self, veio_de: dict) -> List[Tuple[int, int]]:
        caminho = [self.fim]
        atual = self.fim

        while atual in veio_de:
            atual = veio_de[atual]
            caminho.append(atual)

        caminho.reverse()
        return caminho

    def mostrar_labirinto_com_caminho(self, caminho: List[Tuple[int, int]]):
        labirinto_visual = [linha[:] for linha in self.labirinto]

        for pos in caminho:
            if labirinto_visual[pos[0]][pos[1]] == 0:
                labirinto_visual[pos[0]][pos[1]] = "*"

        for i in range(self.linhas):
            linha_str = ""
            for j in range(self.colunas):
                celula = labirinto_visual[i][j]
                if celula == 2:
                    linha_str += "S "
                elif celula == 3:
                    linha_str += "E "
                elif celula == "*":
                    linha_str += "* "
                else:
                    linha_str += str(celula) + " "
            print(linha_str)
