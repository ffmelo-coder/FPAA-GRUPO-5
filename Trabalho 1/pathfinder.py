import heapq
import math
from typing import List, Tuple, Optional, Dict
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.patheffects as path_effects


class PathFinder:
    # Inicialização da classe PathFinder
    def __init__(self, labirinto: List[List[int]], diagonal: bool = False):
        self.labirinto = labirinto
        self.linhas = len(labirinto)
        self.colunas = len(labirinto[0]) if labirinto else 0
        self.inicio = None
        self.fim = None
        self.diagonal = diagonal

    # Encontra as posições de início (S) e fim (E) no labirinto
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

    # Calcula a distância heurística até o ponto final
    def heuristica(self, atual: Tuple[int, int]) -> float:
        if self.fim is None:
            return 0
        dx = abs(atual[0] - self.fim[0])
        dy = abs(atual[1] - self.fim[1])
        if self.diagonal:
            return math.sqrt(dx * dx + dy * dy)
        return dx + dy

    # Retorna os vizinhos válidos de uma posição
    def vizinhos_validos(
        self, pos: Tuple[int, int]
    ) -> List[Tuple[Tuple[int, int], float]]:
        x, y = pos
        vizinhos = []
        direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        if self.diagonal:
            direcoes.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.linhas and 0 <= ny < self.colunas:
                if self.labirinto[nx][ny] != 1:
                    custo = math.sqrt(2) if abs(dx) + abs(dy) == 2 else 1
                    vizinhos.append(((nx, ny), custo))
        return vizinhos

    # Algoritmo A* para encontrar o caminho mais curto
    def a_estrela(self, visualizar=False, salvar_gif=False) -> Optional[List[Tuple[int, int]]]:
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
                custos_visitados = {pos: custo_g[pos] for pos in visitados}
                na_fila = [pos for _, pos in fila_prioridade]
                posicoes_fila = {pos: idx + 1 for idx, pos in enumerate(na_fila)}
                historico_exploracao.append(
                    (
                        atual,
                        set(visitados.copy()),
                        custos_visitados,
                        set(na_fila),
                        posicoes_fila,
                    )
                )
            if atual == self.fim:
                caminho = self.reconstruir_caminho(veio_de)
                if visualizar:
                    self.visualizar_busca(historico_exploracao, caminho, True, salvar_gif)
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
            self.visualizar_busca(historico_exploracao, None, False, salvar_gif)
        return None

    # Reconstrói o caminho a partir do dicionário de predecessores
    def reconstruir_caminho(self, veio_de: dict) -> List[Tuple[int, int]]:
        caminho = [self.fim]
        atual = self.fim
        while atual in veio_de:
            atual = veio_de[atual]
            caminho.append(atual)
        caminho.reverse()
        return caminho

    # Exibe o labirinto com o caminho encontrado no console
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

    # Cria animação visual da busca A*
    def visualizar_busca(self, historico_exploracao, caminho_final, tem_solucao, salvar_gif=False):

        self.ultima_animacao = None

        fig, ax = plt.subplots(figsize=(10, 10))
        try:
            mng = plt.get_current_fig_manager()
            try:
                mng.window.state("zoomed")
            except Exception:
                try:
                    mng.full_screen_toggle()
                except Exception:
                    try:
                        mng.window.showMaximized()
                    except Exception:
                        pass
        except Exception:
            pass

        # Parameters for text caching / eviction
        TOP_K = 50
        MAX_CACHE = 100

        cmap = ListedColormap(
            ["white", "black", "green", "red", "#87CEFA", "#FFD700", "#FF69B4"]
        )
        legend_elements = [
            mpatches.Patch(color="green", label="Start (S)"),
            mpatches.Patch(color="red", label="End (E)"),
            mpatches.Patch(color="#87CEFA", label="Visited"),
            mpatches.Patch(color="#FF69B4", label="In queue"),
            mpatches.Patch(color="#FFD700", label="Final path"),
        ]
        ax.legend(
            handles=legend_elements,
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            borderaxespad=0.0,
            frameon=True,
        )

        base = np.array(self.labirinto, dtype=float)
        img = ax.imshow(
            base, cmap=cmap, vmin=0, vmax=6, alpha=0.9, animated=True, zorder=1
        )
        (path_line,) = ax.plot(
            [],
            [],
            color="#FFD700",
            linewidth=2.5,
            marker="o",
            markersize=4,
            animated=True,
            zorder=3,
        )
        path_line.set_visible(False)

        ax.set_xticks(np.arange(self.colunas))
        ax.set_yticks(np.arange(self.linhas))
        ax.set_xticklabels([str(i) for i in range(self.colunas)], fontsize=8)
        ax.set_yticklabels([str(i) for i in range(self.linhas)], fontsize=8)
        ax.xaxis.tick_top()
        ax.set_xlim(-0.5, self.colunas - 0.5)
        ax.set_ylim(self.linhas - 0.5, -0.5)
        ax.set_xticks(np.arange(-0.5, self.colunas, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, self.linhas, 1), minor=True)
        ax.grid(which="minor", color="gray", linewidth=0.3, alpha=0.5)

        # textos maps position -> (Text artist, last_cost)
        textos: Dict[Tuple[int, int], Tuple[plt.Text, float]] = {}

        # Formata custo para exibição (inteiro ou 1 casa decimal)
        def formatar_custo(custo):
            if abs(custo - round(custo)) < 1e-9:
                return f"{int(round(custo))}"
            return f"{custo:.1f}"

        total_frames = len(historico_exploracao) + 62

        # Seleciona quais custos exibir na visualização
        def selecionar_subconjunto_de_custos(custos_dict, final_frame, caminho_final):
            # Se for frame final com solução: mostra custos do caminho final
            # Caso contrário: mostra até TOP_K nós visitados com maior custo
            if not custos_dict:
                return {}
            if final_frame and tem_solucao and caminho_final:
                subset = {
                    pos: custos_dict[pos] for pos in caminho_final if pos in custos_dict
                }
                return subset
            items = sorted(custos_dict.items(), key=lambda x: x[1], reverse=True)
            if len(items) <= TOP_K:
                return dict(items)
            return dict(items[:TOP_K])

        # Mantém cache de textos em MAX_CACHE removendo custos menores não protegidos
        def evict_remove_smallest_costs(protected_positions: set):
            if not textos:
                return
            # Enquanto acima da capacidade, remove menores não protegidos
            while len(textos) > MAX_CACHE:
                candidates = [
                    (pos, data[1])
                    for pos, data in textos.items()
                    if pos not in protected_positions
                ]
                if not candidates:
                    break
                pos_to_remove = min(candidates, key=lambda kv: kv[1])[0]
                text_artist, _ = textos.pop(pos_to_remove, (None, None))
                if text_artist is not None:
                    try:
                        text_artist.remove()
                    except Exception:
                        try:
                            text_artist.set_visible(False)
                        except Exception:
                            pass

        # Atualiza cada frame da animação
        def atualizar_frame(frame):
            matriz_visual = base.copy()
            if frame < len(historico_exploracao):
                _, visitados, custos_visitados, na_fila, posicoes_fila = (
                    historico_exploracao[frame]
                )
                final_frame = False
            else:
                _, visitados, custos_visitados, na_fila, posicoes_fila = (
                    historico_exploracao[-1]
                )
                final_frame = True

            for r, c in visitados:
                if matriz_visual[r, c] == 0:
                    matriz_visual[r, c] = 4
            for r, c in na_fila:
                if matriz_visual[r, c] == 0:
                    matriz_visual[r, c] = 6

            if final_frame and tem_solucao and caminho_final:
                for r, c in caminho_final:
                    if matriz_visual[r, c] not in [2, 3]:
                        matriz_visual[r, c] = 5
                coords = np.array(caminho_final)
                path_line.set_data(coords[:, 1], coords[:, 0])
                path_line.set_visible(True)
            else:
                path_line.set_data([], [])
                path_line.set_visible(False)

            img.set_data(matriz_visual)

            # Escolhe subconjunto de custos para exibir (seleção estável)
            subset_custos = selecionar_subconjunto_de_custos(
                custos_visitados, final_frame, caminho_final
            )

            novos = set(subset_custos.keys())
            existentes = set(textos.keys())

            artistas_texto = []

            # Atualiza artistas existentes e cria novos quando necessário
            for pos in novos:
                r, c = pos
                custo_atual = subset_custos[pos]
                label = formatar_custo(custo_atual)
                if pos in textos:
                    text_artist, _ = textos[pos]
                    # Update text and mark visible (don't recreate artist)
                    text_artist.set_text(label)
                    text_artist.set_visible(True)
                    textos[pos] = (text_artist, custo_atual)
                else:
                    text_artist = ax.text(
                        c,
                        r,
                        label,
                        ha="center",
                        va="center",
                        color="black",
                        fontsize=7,
                        animated=True,
                        zorder=5,
                    )
                    text_artist.set_path_effects(
                        [path_effects.withStroke(linewidth=1, foreground="white")]
                    )
                    textos[pos] = (text_artist, custo_atual)
                artistas_texto.append(textos[pos][0])

            # Esconde artistas não no subconjunto atual (mas mantém em cache para reutilização)
            for pos in existentes - novos:
                text_artist, last_cost = textos.get(pos, (None, None))
                if text_artist is not None:
                    text_artist.set_visible(False)

            # Protege exibidos atualmente e caminho final para evitar remoção
            protected = set(novos)
            if final_frame and tem_solucao and caminho_final:
                protected.update(caminho_final)

            # Remove custos menores mantendo posições protegidas
            evict_remove_smallest_costs(protected)

            if final_frame and not tem_solucao:
                titulo = f"A* - SEM SOLUÇÃO - Frame {frame + 1}/{total_frames}"
            else:
                titulo = f"A* - Frame {frame + 1}/{total_frames}"
            ax.set_title(titulo, fontsize=14)

            artists = [img, path_line, ax.title] + artistas_texto
            return artists

        try:
            anim = animation.FuncAnimation(
                fig,
                atualizar_frame,
                frames=total_frames,
                interval=80,
                blit=True,
                repeat=True,
            )
        except Exception:
            anim = animation.FuncAnimation(
                fig,
                atualizar_frame,
                frames=total_frames,
                interval=80,
                blit=False,
                repeat=True,
            )
        
        self.ultima_animacao = anim
        
        fig.subplots_adjust(right=0.82)
        try:
            fig.tight_layout(rect=[0, 0, 1, 0.90])
        except Exception:
            plt.tight_layout()
        
        plt.show()
    
    def salvar_ultima_animacao(self):
        if self.ultima_animacao is None:
            print("Nenhuma animacao disponivel para salvar.")
            return
        
        print("Salvando animacao como GIF (isso pode demorar)...")
        try:
            self.ultima_animacao.save('astar_animation.gif', writer='pillow', fps=12, dpi=80)
            print("GIF salvo como 'astar_animation.gif'")
        except Exception as e:
            print(f"Erro ao salvar GIF: {e}")
            print("Certifique-se de ter o Pillow instalado: pip install pillow")
