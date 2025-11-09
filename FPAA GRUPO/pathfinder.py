import heapq
import math
from typing import List, Tuple, Optional
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import numpy as np


class PathFinder:
    def __init__(self, labirinto: List[List[int]], diagonal: bool = False):
        self.labirinto = labirinto
        self.linhas = len(labirinto)
        self.colunas = len(labirinto[0]) if labirinto else 0
        self.inicio = None
        self.fim = None
        self.diagonal = diagonal

    def encontrar_posicoes(self) -> bool:
        count_inicio = 0
        count_fim = 0

        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.labirinto[i][j] == 2:
                    self.inicio = (i, j)
                    count_inicio += 1
                elif self.labirinto[i][j] == 3:
                    self.fim = (i, j)
                    count_fim += 1

        if count_inicio > 1 or count_fim > 1:
            raise ValueError("Labirinto deve ter apenas um ponto S e um ponto E")

        return self.inicio is not None and self.fim is not None

    def heuristica(self, atual: Tuple[int, int]) -> float:
        if self.fim is None:
            return 0
        dx = abs(atual[0] - self.fim[0])
        dy = abs(atual[1] - self.fim[1])

        if self.diagonal:
            return math.sqrt(dx * dx + dy * dy)
        return dx + dy

    def vizinhos_validos(
        self, pos: Tuple[int, int]
    ) -> List[Tuple[Tuple[int, int], float]]:
        x, y = pos
        vizinhos = []

        direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        if self.diagonal:
            direcoes_diagonais = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            direcoes.extend(direcoes_diagonais)

        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.linhas and 0 <= ny < self.colunas:
                if self.labirinto[nx][ny] != 1:
                    custo = math.sqrt(2) if abs(dx) + abs(dy) == 2 else 1
                    vizinhos.append(((nx, ny), custo))

        return vizinhos

    def a_estrela(self, visualizar=False) -> Optional[List[Tuple[int, int]]]:
        if not self.encontrar_posicoes():
            return None

        fila_prioridade = []
        heapq.heappush(fila_prioridade, (0, self.inicio))

        veio_de = {}
        custo_g = {self.inicio: 0}
        visitados = set()
        historico_exploracao = [] if visualizar else None

        while fila_prioridade:
            _, atual = heapq.heappop(fila_prioridade)

            if atual in visitados:
                continue

            visitados.add(atual)

            if visualizar:
                historico_exploracao.append((atual, set(visitados.copy())))

            if atual == self.fim:
                caminho = self.reconstruir_caminho(veio_de)
                if visualizar:
                    self.visualizar_busca(historico_exploracao, caminho, True)
                return caminho

            for vizinho, custo_movimento in self.vizinhos_validos(atual):
                if vizinho in visitados:
                    continue

                novo_custo = custo_g[atual] + custo_movimento

                if vizinho not in custo_g or novo_custo < custo_g[vizinho]:
                    custo_g[vizinho] = novo_custo
                    f = novo_custo + self.heuristica(vizinho)
                    heapq.heappush(fila_prioridade, (f, vizinho))
                    veio_de[vizinho] = atual

        if visualizar and historico_exploracao:
            self.visualizar_busca(historico_exploracao, None, False)

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

    def visualizar_busca(self, historico_exploracao, caminho_final, tem_solucao):
        fig, ax = plt.subplots(figsize=(10, 10))
        cmap = ListedColormap(["white", "black", "green", "red", "lightblue", "yellow"])

        def atualizar_frame(frame):
            ax.clear()
            matriz_visual = np.array(self.labirinto, dtype=float)

            if frame < len(historico_exploracao):
                _, visitados = historico_exploracao[frame]
                for pos in visitados:
                    if matriz_visual[pos[0]][pos[1]] == 0:
                        matriz_visual[pos[0]][pos[1]] = 4
            else:
                _, visitados = historico_exploracao[-1]
                for pos in visitados:
                    if matriz_visual[pos[0]][pos[1]] == 0:
                        matriz_visual[pos[0]][pos[1]] = 4

                if tem_solucao and caminho_final:
                    for pos in caminho_final:
                        if matriz_visual[pos[0]][pos[1]] not in [2, 3]:
                            matriz_visual[pos[0]][pos[1]] = 5

            ax.imshow(matriz_visual, cmap=cmap, vmin=0, vmax=5)

            if frame >= len(historico_exploracao) and not tem_solucao:
                titulo = f"A* - SEM SOLUCAO - Frame {frame + 1}/{len(historico_exploracao) + 10}"
            else:
                titulo = f"A* - Frame {frame + 1}/{len(historico_exploracao) + 10}"

            ax.set_title(
                titulo, fontsize=14, fontweight="bold" if not tem_solucao else "normal"
            )
            ax.grid(True, which="both", color="gray", linewidth=0.5)
            ax.set_xticks(np.arange(-0.5, self.colunas, 1))
            ax.set_yticks(np.arange(-0.5, self.linhas, 1))
            ax.set_xticklabels([])
            ax.set_yticklabels([])

        total_frames = len(historico_exploracao) + 10
        anim = animation.FuncAnimation(
            fig, atualizar_frame, frames=total_frames, interval=20, repeat=True
        )

        plt.tight_layout()
        plt.show()
