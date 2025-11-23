import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import datetime
import os
from floodfill2 import colorir_todas_regioes


def animate_history(history, save_gif=False, out_path=None, interval=200):
    if not history:
        print("Nenhum histórico recebido para animar.")
        return

    arr0 = np.array(history[0])
    linhas, colunas = arr0.shape

    fig, ax = plt.subplots(figsize=(6, 6))

    from matplotlib.colors import ListedColormap

    cores_base = ["white", "black", "red", "blue", "orange", "yellow", "green"]
    cores_extras = [
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
    cores = cores_base + cores_extras
    cmap = ListedColormap(cores)

    img = ax.imshow(arr0, cmap=cmap, vmin=0, vmax=6, animated=True)
    ax.set_xticks(np.arange(colunas))
    ax.set_yticks(np.arange(linhas))
    ax.xaxis.tick_top()
    ax.grid(False)

    def atualizar(i):
        img.set_data(np.array(history[i]))
        ax.set_title(f"Frame {i+1}/{len(history)}")
        return [img]

    anim = animation.FuncAnimation(
        fig, atualizar, frames=len(history), interval=interval, blit=True
    )

    plt.tight_layout()
    if save_gif:
        if out_path is None:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = f"animation_{ts}.gif"
        try:
            anim.save(out_path, writer="pillow")
            print(f"GIF salvo em: {out_path}")
        except Exception as e:
            print(f"Erro ao salvar GIF: {e}")
    else:
        plt.show()


if __name__ == "__main__":
    grid = [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 0, 1],
        [0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0],
    ]
    print("Gerando histórico de preenchimento...")
    resultados = colorir_todas_regioes(
        grid, inicio=(0, 0), primeiro_cor=2, record_history=True
    )
    history = resultados.get(-1, [])
    if not history:
        print("Nenhum passo gravado.")
    else:
        imgs_dir = os.path.join(os.path.dirname(__file__), "imgs")
        os.makedirs(imgs_dir, exist_ok=True)
        out_path = os.path.join(imgs_dir, "floodfill_demo.gif")
        animate_history(history, save_gif=True, out_path=out_path, interval=250)
