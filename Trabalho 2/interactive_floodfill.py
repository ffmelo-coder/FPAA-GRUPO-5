import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import ListedColormap
from floodfill2 import colorir_regiao_history
import copy


class InteractiveFloodFill:
    def __init__(self, linhas, colunas, modo_desenho=True):
        self.linhas = linhas
        self.colunas = colunas
        self.grid = [[0 for _ in range(colunas)] for _ in range(linhas)]
        self.original_grid = None
        self.cor_atual = 2
        self.modo_desenho = modo_desenho
        self.animacao_concluida = False
        self.fig, self.ax = plt.subplots(figsize=(10, 10))

        manager = plt.get_current_fig_manager()
        try:
            manager.window.state("zoomed")
        except:
            try:
                manager.full_screen_toggle()
            except:
                try:
                    manager.window.showMaximized()
                except:
                    pass

        self.setup_colors()
        self.setup_plot()
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.fig.canvas.mpl_connect("key_press_event", self.on_key)

    def setup_colors(self):
        base_colors = ["white", "black", "red", "blue", "orange", "yellow", "green"]
        extra_colors = [
            (0.5, 0, 0.5),
            (0, 0.5, 0.5),
            (1, 0.75, 0.8),
            (0.6, 0.4, 0.2),
            (0.5, 0.5, 0.5),
            (0.4, 0, 0.8),
            (0.8, 0.4, 0),
            (0, 0.6, 0.3),
            (0.7, 0.3, 0.7),
            (0.3, 0.7, 0.7),
            (0.9, 0.6, 0.1),
            (0.2, 0.8, 0.2),
            (0.8, 0.2, 0.2),
            (0.2, 0.2, 0.8),
            (0.6, 0.6, 0),
            (0, 0.6, 0.6),
            (0.6, 0, 0.6),
            (0.8, 0.8, 0.4),
            (0.4, 0.8, 0.8),
            (0.8, 0.4, 0.8),
        ]
        self.color_list = base_colors + extra_colors

    def setup_plot(self):
        self.ax.clear()
        self.ax.set_xlim(-0.5, self.colunas - 0.5)
        self.ax.set_ylim(-0.5, self.linhas - 0.5)
        self.ax.set_aspect("equal")
        self.ax.invert_yaxis()

        for i in range(self.linhas):
            for j in range(self.colunas):
                color_idx = self.grid[i][j]
                if color_idx < len(self.color_list):
                    color = self.color_list[color_idx]
                else:
                    color = self.color_list[-1]

                rect = patches.Rectangle(
                    (j - 0.5, i - 0.5),
                    1,
                    1,
                    linewidth=1,
                    edgecolor="gray",
                    facecolor=color,
                )
                self.ax.add_patch(rect)

        self.ax.set_xticks(range(self.colunas))
        self.ax.set_yticks(range(self.linhas))
        self.ax.grid(True, alpha=0.3)

        if self.modo_desenho:
            self.ax.set_title(
                "MODO DESENHO: Clique para alternar célula (livre/obstáculo)\n"
                "Pressione ENTER para iniciar o Flood Fill",
                fontsize=12,
                pad=20,
            )

        self.fig.canvas.draw()

    def on_click(self, event):
        if event.inaxes != self.ax:
            return

        if self.animacao_concluida:
            return

        col = int(round(event.xdata))
        row = int(round(event.ydata))

        if 0 <= row < self.linhas and 0 <= col < self.colunas:
            if self.modo_desenho:
                if self.grid[row][col] == 0:
                    self.grid[row][col] = 1
                    print(f"({row}, {col}) → Obstáculo")
                elif self.grid[row][col] == 1:
                    self.grid[row][col] = 0
                    print(f"({row}, {col}) → Livre")
                self.setup_plot()

    def on_key(self, event):
        if event.key == "enter":
            if self.modo_desenho:
                self.modo_desenho = False
                self.original_grid = copy.deepcopy(self.grid)
                print("\n=== INICIANDO ANIMAÇÃO AUTOMÁTICA ===")
                self.preencher_tudo_animado()
        elif event.key == "r":
            if self.original_grid is not None:
                self.grid = copy.deepcopy(self.original_grid)
                self.cor_atual = 2
                self.modo_desenho = True
                self.animacao_concluida = False
                self.setup_plot()
                print("\n✓ Grid resetado! Voltando ao modo desenho...")
        elif event.key == "escape":
            plt.close(self.fig)
            print("\n✓ Saindo...")

    def preencher_tudo_animado(self):
        self.ax.set_title(
            "Preenchendo automaticamente...",
            fontsize=12,
            pad=20,
        )
        self.fig.canvas.draw()
        plt.pause(0.5)

        regioes_preenchidas = 0

        while True:
            posicao_zero = None
            for i in range(self.linhas):
                for j in range(self.colunas):
                    if self.grid[i][j] == 0:
                        posicao_zero = (i, j)
                        break
                if posicao_zero:
                    break

            if not posicao_zero:
                print(f"Nenhuma célula vazia encontrada. Finalizando...")
                break

            row, col = posicao_zero
            print(
                f"\nPreenchendo região {self.cor_atual - 1} a partir de ({row}, {col})"
            )

            history = []
            grid_copy = copy.deepcopy(self.grid)
            sucesso = colorir_regiao_history(
                grid_copy, start=(row, col), color=self.cor_atual, history=history
            )

            if sucesso and len(history) > 0:
                num_celulas = len(history)
                print(f"✓ Região {self.cor_atual - 1}: {num_celulas} células")
                regioes_preenchidas += 1

                for frame_idx, frame in enumerate(history):
                    self.grid = copy.deepcopy(frame)
                    self.setup_plot()
                    self.ax.set_title(
                        f"Preenchendo região {self.cor_atual - 1}... ({frame_idx + 1}/{len(history)} células)",
                        fontsize=12,
                        pad=20,
                    )
                    self.fig.canvas.draw()
                    plt.pause(0.05)

                self.cor_atual += 1

                self.setup_plot()
                self.ax.set_title(
                    f"Preenchendo... ({regioes_preenchidas} regiões encontradas)",
                    fontsize=12,
                    pad=20,
                )
                self.fig.canvas.draw()
                plt.pause(0.5)

        self.ax.set_title(
            f"✓ Concluído! {regioes_preenchidas} {'região' if regioes_preenchidas == 1 else 'regiões'} {'preenchida' if regioes_preenchidas == 1 else 'preenchidas'}\n"
            f"Pressione R para resetar ou ESC para sair",
            fontsize=12,
            pad=20,
        )
        self.animacao_concluida = True
        self.fig.canvas.draw()
        print(f"\n=== CONCLUÍDO ===")
        print(f"Total de regiões: {regioes_preenchidas}")
        print("Pressione R para resetar ou ESC para sair")

    def show(self):
        plt.show()


def criar_grid_exemplo(tipo="medio"):
    if tipo == "pequeno":
        return [
            [0, 0, 1, 0, 0],
            [0, 1, 1, 0, 1],
            [0, 0, 1, 1, 1],
            [1, 1, 0, 0, 0],
        ]
    elif tipo == "medio":
        return [
            [0, 1, 0, 0, 1, 0, 0],
            [0, 1, 0, 1, 1, 0, 1],
            [0, 0, 0, 1, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 1, 0, 0],
        ]
    elif tipo == "grande":
        return [
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
            [0, 1, 0, 1, 1, 0, 1, 1, 0, 1],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
        ]
    else:
        return [[0, 0, 1, 0, 0]]


if __name__ == "__main__":
    print("=== Flood Fill Interativo ===")
    print("\nEscolha o modo:")
    print("1. Desenhar grid personalizado (recomendado)")
    print("2. Usar grid pré-definido")

    modo = input("\nOpção (1-2): ").strip()

    if modo == "1":
        print("\nDefina o tamanho do grid:")
        linhas = int(input("Número de linhas (ex: 5): "))
        colunas = int(input("Número de colunas (ex: 5): "))

        print("\n=== Instruções ===")
        print("MODO DESENHO:")
        print(
            "  • Clique nas células para alternar entre livre (branco) e obstáculo (preto)"
        )
        print("  • Pressione ENTER para iniciar a animação automática")
        print("\nAPÓS A ANIMAÇÃO:")
        print("  • Pressione R para resetar e redesenhar")
        print("  • Pressione ESC para sair")
        print("\nIniciando interface gráfica...")

        app = InteractiveFloodFill(linhas, colunas, modo_desenho=True)
        app.show()
    else:
        print("\nEscolha o tamanho do grid:")
        print("1. Pequeno (4x5)")
        print("2. Médio (7x7)")
        print("3. Grande (10x10)")

        escolha = input("\nOpção (1-3): ").strip()

        if escolha == "1":
            grid = criar_grid_exemplo("pequeno")
        elif escolha == "2":
            grid = criar_grid_exemplo("medio")
        elif escolha == "3":
            grid = criar_grid_exemplo("grande")
        else:
            grid = criar_grid_exemplo("medio")

        print("\n=== Instruções ===")
        print("• Pressione ENTER para iniciar a animação automática")
        print("• Pressione R para resetar")
        print("• Pressione ESC para sair")
        print("\nIniciando interface gráfica...")

        linhas = len(grid)
        colunas = len(grid[0])
        app = InteractiveFloodFill(linhas, colunas, modo_desenho=False)
        app.grid = grid
        app.original_grid = copy.deepcopy(grid)
        app.setup_plot()
        app.show()
