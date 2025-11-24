import tkinter as tk
from tkinter import messagebox, simpledialog
import numpy as np
import time
from pathfinder import PathFinder
from floodfill import FloodFill


class TkLabirintoApp:
    # Classe principal da interface Tkinter para busca de caminhos
    def __init__(self, root):
        # Inicializa a interface e variáveis principais
        self.root = root
        self.root.title("Sistema de Busca de Caminhos - Tkinter")
        self.algoritmo = tk.StringVar(value="1")
        self.linhas = 10
        self.colunas = 10
        self.grid = None
        self.inicio = None
        self.fins = []
        self.canvas = None
        self.canvas_frame = None
        self.h_scroll = None
        self.v_scroll = None
        self.cell_size = 24
        self.visualizar = tk.BooleanVar(value=True)
        self.diagonal = tk.BooleanVar(value=False)
        self.last_draw_state = None
        self.diag_check = None
        # performance helpers
        self.cell_items = (
            None  # lista 2D armazenando os IDs dos itens do canvas para cada célula
        )
        self.path_cells = set()  # conjunto de (i,j) marcados como caminho (valor 5)
        self._last_drag_time = 0
        self._build_interface()

    def _build_interface(self):
        # Monta os widgets e controles da interface
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(frame, text="Algoritmo:").pack(side=tk.LEFT)
        tk.Radiobutton(
            frame,
            text="A* (diagonal)",
            variable=self.algoritmo,
            value="1",
            command=self.on_algoritmo_change,
        ).pack(side=tk.LEFT)
        tk.Radiobutton(
            frame,
            text="Flood Fill (ortogonal)",
            variable=self.algoritmo,
            value="2",
            command=self.on_algoritmo_change,
        ).pack(side=tk.LEFT)
        tk.Button(frame, text="Novo Grid", command=self.novo_grid_dialog).pack(
            side=tk.LEFT
        )
        tk.Button(frame, text="Aleatório", command=self.gerar_aleatorio).pack(
            side=tk.LEFT
        )
        tk.Button(frame, text="Executar", command=self.executar_algoritmo).pack(
            side=tk.LEFT
        )
        tk.Button(frame, text="Limpar", command=self.limpar_grid).pack(side=tk.LEFT)
        tk.Checkbutton(frame, text="Visualizar", variable=self.visualizar).pack(
            side=tk.LEFT
        )
        self.diag_check = tk.Checkbutton(frame, text="Diagonal", variable=self.diagonal)
        self.diag_check.pack(side=tk.LEFT)

        # Slider de Zoom (tamanho da célula)
        self.zoom_scale = tk.Scale(
            frame,
            label="Tamanho célula",
            from_=4,
            to=64,
            orient=tk.HORIZONTAL,
            command=self.on_zoom_change,
            showvalue=True,
            length=150,
        )
        self.zoom_scale.set(self.cell_size)
        self.zoom_scale.pack(side=tk.LEFT)

        # Cria o label de status apenas uma vez
        self.status = tk.Label(
            self.root,
            text="Clique para desenhar obstáculos. Botão direito: início. Shift+Clique: fim.",
        )
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Cria o grid padrão ao abrir
        self.novo_grid(self.linhas, self.colunas)
        self.on_algoritmo_change()

    def zoom_in(self):
        # Aumenta o tamanho das células (máx 64)
        if self.cell_size < 64:
            self.cell_size = min(64, self.cell_size + 4)
            if hasattr(self, "zoom_scale"):
                self.zoom_scale.set(self.cell_size)
            # invalidate items so they are recreated with the new cell size
            self.cell_items = None
            self.redesenhar_com_novo_zoom()

    def zoom_out(self):
        # Diminui o tamanho das células (mín 8)
        if self.cell_size > 4:
            self.cell_size = max(4, self.cell_size - 4)
            if hasattr(self, "zoom_scale"):
                self.zoom_scale.set(self.cell_size)
            # invalidate items so they are recreated with the new cell size
            self.cell_items = None
            self.redesenhar_com_novo_zoom()

    def on_zoom_change(self, val):
        # Handler para o slider de zoom: atualiza cell_size e redesenha
        try:
            size = int(float(val))
        except Exception:
            return
        size = max(4, min(64, size))
        if size != self.cell_size:
            self.cell_size = size
            # invalidate existing canvas items so they will be recreated
            self.cell_items = None
            self.redesenhar_com_novo_zoom()

    def redesenhar_com_novo_zoom(self):
        # Redesenha o grid mantendo o estado, ajustando o tamanho do canvas e scrollbars
        self._criar_canvas_com_scroll()
        self.desenhar_grid()

    def on_algoritmo_change(self):
        # Atualiza opções ao trocar algoritmo (A* ou Flood Fill)
        if self.algoritmo.get() == "1":
            self.diag_check.config(state=tk.NORMAL)
        else:
            self.diag_check.config(state=tk.DISABLED)
            self.diagonal.set(False)

    def novo_grid_dialog(self):
        # Abre diálogo para definir novo tamanho do grid
        linhas = simpledialog.askinteger(
            "Linhas",
            "Digite o número de linhas:",
            parent=self.root,
            initialvalue=self.linhas,
        )
        colunas = simpledialog.askinteger(
            "Colunas",
            "Digite o número de colunas:",
            parent=self.root,
            initialvalue=self.colunas,
        )
        if linhas and colunas and linhas > 1 and colunas > 1:
            self.novo_grid(linhas, colunas)

    def novo_grid(self, linhas, colunas):
        # Cria um novo grid vazio com o tamanho especificado
        self.linhas = linhas
        self.colunas = colunas
        self.grid = [[0 for _ in range(colunas)] for _ in range(linhas)]
        self.inicio = None
        self.fins = []
        self.last_draw_state = None
        # reiniciar performance helpers
        self.cell_items = None
        self.path_cells.clear()
        self._criar_canvas_com_scroll()
        self.desenhar_grid()

    def _criar_canvas_com_scroll(self):
        # Cria o canvas com barras de rolagem (centralizado e redimensionável)
        if self.canvas:
            self.canvas.destroy()
        if self.h_scroll:
            self.h_scroll.destroy()
        if self.v_scroll:
            self.v_scroll.destroy()
        if self.canvas_frame:
            self.canvas_frame.destroy()

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.h_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(
            self.canvas_frame,
            bg="white",
            xscrollcommand=self.h_scroll.set,
            yscrollcommand=self.v_scroll.set,
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.h_scroll.config(command=self.canvas.xview)
        self.v_scroll.config(command=self.canvas.yview)

        # When recreating the canvas, invalidate existing cell items
        self.cell_items = None

        self.offset_x = 0
        self.offset_y = 0

        total_w = self.colunas * self.cell_size
        total_h = self.linhas * self.cell_size
        self.canvas.config(scrollregion=(0, 0, total_w, total_h))

        self.canvas.bind("<Configure>", lambda e: self.desenhar_grid())

        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<B1-Motion>", self.on_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_release)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<Shift-Button-1>", self.on_shift_left_click)

    def desenhar_grid(self):
        # Desenha o grid e as células no canvas, centralizado
        total_width = self.colunas * self.cell_size
        total_height = self.linhas * self.cell_size

        canvas_width = max(1, self.canvas.winfo_width())
        canvas_height = max(1, self.canvas.winfo_height())

        self.offset_x = max(0, (canvas_width - total_width) // 2)
        self.offset_y = max(0, (canvas_height - total_height) // 2)

        # If cell items not created yet (or grid size changed), create them once.
        need_create = (
            not self.cell_items
            or len(self.cell_items) != self.linhas
            or (self.cell_items and len(self.cell_items[0]) != self.colunas)
        )

        if need_create:
            # clear canvas and recreate items
            self.canvas.delete("all")
            self.cell_items = [
                [None for _ in range(self.colunas)] for _ in range(self.linhas)
            ]
            for i in range(self.linhas):
                for j in range(self.colunas):
                    x0 = j * self.cell_size + self.offset_x
                    y0 = i * self.cell_size + self.offset_y
                    x1 = x0 + self.cell_size
                    y1 = y0 + self.cell_size
                    cor = "white"
                    if self.grid[i][j] == 1:
                        cor = "black"
                    elif self.grid[i][j] == 2:
                        cor = "green"
                    elif self.grid[i][j] == 3:
                        cor = "red"
                    elif self.grid[i][j] == 5:
                        cor = "yellow"
                    item = self.canvas.create_rectangle(
                        x0, y0, x1, y1, fill=cor, outline="gray"
                    )
                    self.cell_items[i][j] = item
        else:
            # Update existing items' positions and colors
            for i in range(self.linhas):
                for j in range(self.colunas):
                    item = self.cell_items[i][j]
                    if item is None:
                        continue
                    x0 = j * self.cell_size + self.offset_x
                    y0 = i * self.cell_size + self.offset_y
                    x1 = x0 + self.cell_size
                    y1 = y0 + self.cell_size
                    cor = "white"
                    if self.grid[i][j] == 1:
                        cor = "black"
                    elif self.grid[i][j] == 2:
                        cor = "green"
                    elif self.grid[i][j] == 3:
                        cor = "red"
                    elif self.grid[i][j] == 5:
                        cor = "yellow"
                    # update geometry and color
                    try:
                        self.canvas.coords(item, x0, y0, x1, y1)
                        self.canvas.itemconfig(item, fill=cor)
                    except tk.TclError:
                        # item might have been deleted; ignore
                        pass

        # Update scrollregion (total grid size)
        self.canvas.config(scrollregion=(0, 0, total_width, total_height))

    def on_left_click(self, event):
        # Manipula clique esquerdo: desenha/remove obstáculos e limpa caminho
        x_canvas = self.canvas.canvasx(event.x) - getattr(self, "offset_x", 0)
        y_canvas = self.canvas.canvasy(event.y) - getattr(self, "offset_y", 0)
        i, j = int(y_canvas // self.cell_size), int(x_canvas // self.cell_size)

        # Limpa Caminho anterior
        if self.path_cells:
            for px, py in list(self.path_cells):
                if 0 <= px < self.linhas and 0 <= py < self.colunas:
                    self.grid[px][py] = 0
                    if (
                        self.cell_items
                        and 0 <= px < len(self.cell_items)
                        and 0 <= py < len(self.cell_items[0])
                    ):
                        try:
                            self.canvas.itemconfig(
                                self.cell_items[px][py], fill="white"
                            )
                        except tk.TclError:
                            pass
            self.path_cells.clear()

        if 0 <= i < self.linhas and 0 <= j < self.colunas:
            if self.grid[i][j] == 0:
                self.grid[i][j] = 1
                self.last_draw_state = 1
            elif self.grid[i][j] == 1:
                self.grid[i][j] = 0
                self.last_draw_state = 0
            else:
                self.last_draw_state = None

            if (i, j) in self.fins and self.grid[i][j] != 3:
                try:
                    self.fins.remove((i, j))
                except ValueError:
                    pass

            if (
                self.cell_items
                and 0 <= i < len(self.cell_items)
                and 0 <= j < len(self.cell_items[0])
            ):
                item = self.cell_items[i][j]
                if item:
                    color = "black" if self.grid[i][j] == 1 else "white"
                    try:
                        self.canvas.itemconfig(item, fill=color)
                    except tk.TclError:
                        pass

    def on_left_drag(self, event):
        # Manipula arrasto com botão esquerdo: desenha/remover obstáculos
        # Throttle drag events to avoid excessive updates
        now = time.time()
        if now - self._last_drag_time < 0.02:
            return
        self._last_drag_time = now

        x_canvas = self.canvas.canvasx(event.x) - getattr(self, "offset_x", 0)
        y_canvas = self.canvas.canvasy(event.y) - getattr(self, "offset_y", 0)
        i, j = int(y_canvas // self.cell_size), int(x_canvas // self.cell_size)

        # Only clear path cells once (they are cleared on first drag/click)
        if self.path_cells:
            for px, py in list(self.path_cells):
                if 0 <= px < self.linhas and 0 <= py < self.colunas:
                    self.grid[px][py] = 0
                    item = None
                    if (
                        self.cell_items
                        and 0 <= px < len(self.cell_items)
                        and 0 <= py < len(self.cell_items[0])
                    ):
                        item = self.cell_items[px][py]
                    if item:
                        try:
                            self.canvas.itemconfig(item, fill="white")
                        except tk.TclError:
                            pass
            self.path_cells.clear()

        if (
            0 <= i < self.linhas
            and 0 <= j < self.colunas
            and self.last_draw_state is not None
        ):
            if self.grid[i][j] in [0, 1] and self.grid[i][j] != self.last_draw_state:
                self.grid[i][j] = self.last_draw_state
                # update only the affected cell
                if (i, j) in self.fins and self.grid[i][j] != 3:
                    try:
                        self.fins.remove((i, j))
                    except ValueError:
                        pass
                if (
                    self.cell_items
                    and 0 <= i < len(self.cell_items)
                    and 0 <= j < len(self.cell_items[0])
                ):
                    item = self.cell_items[i][j]
                    if item:
                        color = "black" if self.grid[i][j] == 1 else "white"
                        try:
                            self.canvas.itemconfig(item, fill=color)
                        except tk.TclError:
                            pass

    def on_left_release(self, event):
        # Finaliza arrasto do mouse
        self.last_draw_state = None

    def on_right_click(self, event):
        # Define a posição inicial (S) com clique direito
        x_canvas = self.canvas.canvasx(event.x) - getattr(self, "offset_x", 0)
        y_canvas = self.canvas.canvasy(event.y) - getattr(self, "offset_y", 0)
        i, j = int(y_canvas // self.cell_size), int(x_canvas // self.cell_size)
        if 0 <= i < self.linhas and 0 <= j < self.colunas:
            if self.inicio:
                old_i, old_j = self.inicio
                if self.grid[old_i][old_j] == 2:
                    self.grid[old_i][old_j] = 0
                    # update old start cell
                    if (
                        self.cell_items
                        and 0 <= old_i < len(self.cell_items)
                        and 0 <= old_j < len(self.cell_items[0])
                    ):
                        try:
                            self.canvas.itemconfig(
                                self.cell_items[old_i][old_j], fill="white"
                            )
                        except tk.TclError:
                            pass
            self.inicio = (i, j)
            self.grid[i][j] = 2
            # update new start cell
            if (
                self.cell_items
                and 0 <= i < len(self.cell_items)
                and 0 <= j < len(self.cell_items[0])
            ):
                try:
                    self.canvas.itemconfig(self.cell_items[i][j], fill="green")
                except tk.TclError:
                    pass

    def on_shift_left_click(self, event):
        # Adiciona ou remove posição final (E) com Shift+Clique esquerdo
        x_canvas = self.canvas.canvasx(event.x) - getattr(self, "offset_x", 0)
        y_canvas = self.canvas.canvasy(event.y) - getattr(self, "offset_y", 0)
        i, j = int(y_canvas // self.cell_size), int(x_canvas // self.cell_size)
        if 0 <= i < self.linhas and 0 <= j < self.colunas:
            if (i, j) in self.fins:
                # remove final
                self.fins.remove((i, j))
                if self.grid[i][j] == 3:
                    self.grid[i][j] = 0
                    if (
                        self.cell_items
                        and 0 <= i < len(self.cell_items)
                        and 0 <= j < len(self.cell_items[0])
                    ):
                        try:
                            self.canvas.itemconfig(self.cell_items[i][j], fill="white")
                        except tk.TclError:
                            pass
            else:
                # add final (no modal message)
                self.fins.append((i, j))
                self.grid[i][j] = 3
                if (
                    self.cell_items
                    and 0 <= i < len(self.cell_items)
                    and 0 <= j < len(self.cell_items[0])
                ):
                    try:
                        self.canvas.itemconfig(self.cell_items[i][j], fill="red")
                    except tk.TclError:
                        pass

    def limpar_grid(self):
        # Limpa o grid atual (mantém tamanho)
        self.novo_grid(self.linhas, self.colunas)

    def gerar_aleatorio(self):
        # Gera obstáculos aleatórios no grid
        densidade = simpledialog.askfloat(
            "Densidade",
            "Densidade de obstáculos (0.0 a 1.0):",
            parent=self.root,
            initialvalue=0.3,
            minvalue=0.0,
            maxvalue=1,
        )
        if densidade is None:
            return
        for i in range(self.linhas):
            for j in range(self.colunas):
                if np.random.rand() < densidade:
                    self.grid[i][j] = 1
                else:
                    self.grid[i][j] = 0
        self.inicio = None
        self.fins = []
        self.desenhar_grid()

    def executar_algoritmo(self):
        # Executa o algoritmo selecionado (A* ou Flood Fill) e mostra o resultado
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.grid[i][j] == 5:
                    self.grid[i][j] = 0
        self.desenhar_grid()
        actual_fins = []
        found_start = None
        for ii in range(self.linhas):
            for jj in range(self.colunas):
                if self.grid[ii][jj] == 3:
                    actual_fins.append((ii, jj))
                elif self.grid[ii][jj] == 2 and found_start is None:
                    found_start = (ii, jj)
        self.fins = actual_fins
        self.inicio = found_start

        if not self.inicio or not self.fins:
            self.status.config(
                text="Defina início (botão direito) e fim (shift+clique)!"
            )
            return
        if self.algoritmo.get() == "1":
            if len(self.fins) != 1:
                messagebox.showinfo(
                    "A*", "A* requer exatamente 1 fim!", parent=self.root
                )
                self.status.config(text="A* requer exatamente 1 fim!")
                return
            pathfinder = PathFinder(self.grid, diagonal=self.diagonal.get())
            if not pathfinder.encontrar_posicoes():
                self.status.config(text="Sem solução!")
                return
            caminho = pathfinder.a_estrela(visualizar=self.visualizar.get())
            elapsed_ms = getattr(pathfinder, "last_elapsed_ms", 0.0)
            if caminho is None:
                self.status.config(text="Sem solução!")
                print(f"\nA* execution time: {elapsed_ms:.3f} ms")
            else:
                for i, j in caminho:
                    if self.grid[i][j] not in [2, 3]:
                        self.grid[i][j] = 5
                        self.path_cells.add((i, j))
                        if (
                            self.cell_items
                            and 0 <= i < len(self.cell_items)
                            and 0 <= j < len(self.cell_items[0])
                        ):
                            try:
                                self.canvas.itemconfig(
                                    self.cell_items[i][j], fill="yellow"
                                )
                            except tk.TclError:
                                pass
                self.status.config(
                    text=f"Caminho encontrado! Tamanho: {len(caminho)} | Tempo total: {elapsed_ms:.3f} ms"
                )
                self.desenhar_grid()
                print(f"\nA* execution time: {elapsed_ms:.3f} ms")
                # Mostra o caminho no terminal
                print("\nCaminho encontrado (A*):")
                print(caminho)
        else:
            floodfill = FloodFill(self.grid)
            if not floodfill.encontrar_posicoes():
                self.status.config(text="Sem solução!")
                return
            caminhos = floodfill.buscar_caminho(
                visualizar=self.visualizar.get(), todos_encontrados=True
            )
            elapsed_ms = getattr(floodfill, "last_elapsed_ms", 0.0)
            if not caminhos:
                self.status.config(text="Sem solução!")
                print(f"\nFlood Fill execution time: {elapsed_ms:.3f} ms")
            else:
                for caminho in caminhos.values():
                    for i, j in caminho:
                        if self.grid[i][j] not in [2, 3]:
                            self.grid[i][j] = 5
                            self.path_cells.add((i, j))
                            if (
                                self.cell_items
                                and 0 <= i < len(self.cell_items)
                                and 0 <= j < len(self.cell_items[0])
                            ):
                                try:
                                    self.canvas.itemconfig(
                                        self.cell_items[i][j], fill="yellow"
                                    )
                                except tk.TclError:
                                    pass
                resumo_tamanhos = " | ".join(
                    [
                        f"{idx+1} - {len(caminho)}"
                        for idx, (_fim, caminho) in enumerate(caminhos.items())
                    ]
                )
                self.status.config(
                    text=f"Caminhos encontrados: {len(caminhos)} | {resumo_tamanhos} | Tempo total: {elapsed_ms:.3f} ms"
                )
                self.desenhar_grid()
                print(f"\nFlood Fill execution time: {elapsed_ms:.3f} ms")
                # Mostra os caminhos no terminal
                print("\nCaminhos encontrados (Flood Fill):")
                resumo_tamanhos = [
                    f"{idx+1} - {len(caminho)}"
                    for idx, (_fim, caminho) in enumerate(caminhos.items())
                ]
                if resumo_tamanhos:
                    print(" | ".join(resumo_tamanhos))
                for fim, caminho in caminhos.items():
                    print(f"Fim {fim}: {caminho}")

    def reset_grid(self):
        # Reseta o grid ao trocar modo/algoritmo
        self.novo_grid(self.linhas, self.colunas)
