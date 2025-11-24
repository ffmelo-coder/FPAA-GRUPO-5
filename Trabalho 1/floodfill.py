from collections import deque
from typing import List, Tuple, Dict
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.patheffects as path_effects


class FloodFill:
    # Inicialização da classe FloodFill
    def __init__(self, labirinto: List[List[int]]):
        self.labirinto = labirinto
        self.linhas = len(labirinto)
        self.colunas = len(labirinto[0]) if labirinto else 0
        self.inicio = None
        self.fins: List[Tuple[int, int]] = []
        self.last_elapsed_ms: float = 0.0

    # Encontra as posições de início (S) e fim (E) no labirinto
    def encontrar_posicoes(self) -> bool:
        self.inicio = None
        self.fins = []
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.labirinto[i][j] == 2:
                    self.inicio = (i, j)
                elif self.labirinto[i][j] == 3:
                    self.fins.append((i, j))
        return self.inicio is not None

    # Busca o caminho usando algoritmo Flood Fill (BFS)
    def buscar_caminho(
        self, visualizar=False, todos_encontrados: bool = False, salvar_gif=False
    ) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
        if not self.encontrar_posicoes():
            return {}
        start_time = time.perf_counter()
        viz_time = 0.0

        fila = deque([self.inicio])
        visitados = {self.inicio}
        veio_de = {self.inicio: None}
        dist = {self.inicio: 0}

        direcoes = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        historico_exploracao = [] if visualizar else None

        fins_set = set(self.fins)
        caminhos_encontrados: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}

        while fila:
            atual = fila.popleft()

            if visualizar:
                t_v0 = time.perf_counter()
                custos_visitados = {pos: dist[pos] for pos in visitados}
                historico_exploracao.append(
                    (atual, set(visitados.copy()), custos_visitados)
                )
                viz_time += time.perf_counter() - t_v0

            if atual in self.fins and atual not in caminhos_encontrados:
                caminho = self.reconstruir_caminho(veio_de, atual)
                caminhos_encontrados[atual] = caminho
                if todos_encontrados and len(caminhos_encontrados) == len(fins_set):
                    total = (time.perf_counter() - start_time) - viz_time
                    self.last_elapsed_ms = total * 1000.0
                    if visualizar:
                        caminhos_lista = list(caminhos_encontrados.values())
                        self.visualizar_busca(
                            historico_exploracao, caminhos_lista, True
                        )
                    return caminhos_encontrados

            x, y = atual
            for dx, dy in direcoes:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < self.linhas
                    and 0 <= ny < self.colunas
                    and (nx, ny) not in visitados
                    and self.labirinto[nx][ny] != 1
                ):
                    fila.append((nx, ny))
                    visitados.add((nx, ny))
                    veio_de[(nx, ny)] = atual
                    dist[(nx, ny)] = dist[atual] + 1

        total = (time.perf_counter() - start_time) - viz_time
        self.last_elapsed_ms = total * 1000.0
        if visualizar and historico_exploracao:
            caminhos_lista = (
                list(caminhos_encontrados.values()) if caminhos_encontrados else None
            )
            tem_solucao = bool(caminhos_encontrados)
            self.visualizar_busca(
                historico_exploracao, caminhos_lista, tem_solucao, salvar_gif
            )
        return caminhos_encontrados

    # Reconstrói o caminho a partir do dicionário de predecessores
    def reconstruir_caminho(
        self, veio_de: dict, alvo: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        caminho = []
        atual = alvo
        while atual is not None:
            caminho.append(atual)
            atual = veio_de[atual]
        caminho.reverse()
        return caminho

    # Exibe o labirinto com o caminho encontrado no console
    def mostrar_labirinto_com_caminho(
        self, caminhos: Dict[Tuple[int, int], List[Tuple[int, int]]]
    ):
        labirinto_visual = [linha[:] for linha in self.labirinto]
        for caminho in caminhos.values():
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

    # Cria animação visual da busca Flood Fill
    def visualizar_busca(
        self, historico_exploracao, caminho_final, tem_solucao, salvar_gif=False
    ):

        from matplotlib.widgets import Button
        import datetime

        self.ultima_animacao = None

        TOP_K = 50
        MAX_CACHE = 100

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

        cmap = ListedColormap(
            ["white", "black", "green", "red", "#87CEFA", "#FFD700", "#FF69B4"]
        )

        legend_elements = [
            mpatches.Patch(color="green", label="Start (S)"),
            mpatches.Patch(color="red", label="End (E)"),
            mpatches.Patch(color="#87CEFA", label="Visited"),
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

        path_lines = []

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

        textos: Dict[Tuple[int, int], Tuple[plt.Text, float]] = {}

        # Formata custo para exibição (inteiro ou 1 casa decimal)
        def formatar_custo(custo):
            if abs(custo - round(custo)) < 1e-9:
                return f"{int(round(custo))}"
            return f"{custo:.1f}"

        total_frames = len(historico_exploracao) + 62

        # Seleciona quais custos exibir na visualização
        def selecionar_subconjunto_de_custos(
            custos_dict, frame_idx, final_frame, caminhos_finais
        ):
            if not custos_dict:
                return {}
            if final_frame and tem_solucao and caminhos_finais:
                protectect_positions = set()
                for caminho in caminhos_finais:
                    protectect_positions.update(caminho)
                subset = {
                    pos: custos_dict[pos]
                    for pos in custos_dict.keys()
                    if pos in protectect_positions
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
            nonlocal path_lines
            matriz_visual = base.copy()
            if frame < len(historico_exploracao):
                _, visitados, custos_visitados = historico_exploracao[frame]
                final_frame = False
            else:
                _, visitados, custos_visitados = historico_exploracao[-1]
                final_frame = True

            for r, c in visitados:
                if matriz_visual[r, c] == 0:
                    matriz_visual[r, c] = 4

            if not final_frame:
                for ln in path_lines:
                    try:
                        ln.remove()
                    except Exception:
                        try:
                            ln.set_visible(False)
                        except Exception:
                            pass
                path_lines = []
            if final_frame and tem_solucao and caminho_final:
                # caminho_final é lista de caminhos
                for caminho in caminho_final:
                    for r, c in caminho:
                        if matriz_visual[r, c] not in [2, 3]:
                            matriz_visual[r, c] = 5
                    coords = np.array(caminho)
                    # plota linha para esse caminho
                    (ln,) = ax.plot(
                        coords[:, 1],
                        coords[:, 0],
                        linewidth=2.5,
                        marker="o",
                        markersize=4,
                        zorder=3,
                    )
                    ln.set_color("#FFD700")
                    ln.set_visible(True)
                    path_lines.append(ln)

            img.set_data(matriz_visual)

            # Escolhe subconjunto de custos para exibir

            subset_custos = selecionar_subconjunto_de_custos(
                custos_visitados, frame, final_frame, caminho_final
            )

            novos = set(subset_custos.keys())
            existentes = set(textos.keys())

            artistas_texto = []

            for pos in novos:
                r, c = pos
                custo_atual = subset_custos[pos]
                label = formatar_custo(custo_atual)
                if pos in textos:
                    text_artist, _ = textos[pos]
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

            # Esconde artistas não exibidos atualmente
            for pos in existentes - novos:
                text_artist, _ = textos.get(pos, (None, None))
                if text_artist is not None:
                    text_artist.set_visible(False)

            # Protege posições exibidas e caminho final
            protected = set(novos)
            if final_frame and tem_solucao and caminho_final:
                for caminho in caminho_final:
                    protected.update(caminho)
            evict_remove_smallest_costs(protected)

            if final_frame and not tem_solucao:
                titulo = f"Flood Fill - SEM SOLUÇÃO - Frame {frame + 1}/{total_frames}"
            else:
                titulo = f"Flood Fill - Frame {frame + 1}/{total_frames}"
            ax.set_title(titulo, fontsize=14)

            artists = [img, ax.title] + artistas_texto + path_lines
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

        # Adiciona botão Salvar GIF
        ax_button = fig.add_axes([0.83, 0.05, 0.13, 0.06])
        btn = Button(ax_button, "Salvar GIF", color="#FFD700", hovercolor="#FFEC8B")

        def on_save_gif(event):
            if self.ultima_animacao is None:
                print("Nenhuma animacao disponivel para salvar.")
                return
            print("Salvando animacao como GIF (isso pode demorar)...")
            try:
                now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"floodfill_animation_{now}.gif"
                self.ultima_animacao.save(filename, writer="pillow", fps=12, dpi=80)
                print(f"GIF salvo como '{filename}'")
                # Aviso visual no Matplotlib
                ax.text(
                    0.5,
                    1.05,
                    "GIF SALVO",
                    transform=ax.transAxes,
                    fontsize=16,
                    color="green",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                    zorder=10,
                )
                fig.canvas.draw_idle()
            except Exception as e:
                print(f"Erro ao salvar GIF: {e}")
                print("Certifique-se de ter o Pillow instalado: pip install pillow")

        btn.on_clicked(on_save_gif)

        plt.show()
