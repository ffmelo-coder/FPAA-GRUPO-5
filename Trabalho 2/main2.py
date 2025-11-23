from floodfill2 import colorir_todas_regioes, imprimir_grid
from visualize2 import animate_history
import os
import copy


def exemplo_execucao():
    grid = [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 0, 1],
        [0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0],
    ]
    print("Grid inicial:")
    imprimir_grid(grid)
    resultados = colorir_todas_regioes(grid, inicio=(0, 0), primeiro_cor=2)
    print("\nGrid preenchido:")
    imprimir_grid(grid)
    print("\nRegiões preenchidas:")
    for cor, coords in resultados.items():
        print(f"Cor {cor}: {len(coords)} células")


def exemplo_com_visualizacao(grid, nome_arquivo, inicio=(0, 0)):
    print("Grid inicial:")
    imprimir_grid(grid)

    grid_copy = copy.deepcopy(grid)

    print("\nGerando histórico de preenchimento...")
    resultados = colorir_todas_regioes(
        grid_copy, inicio=inicio, primeiro_cor=2, record_history=True
    )

    print("\nGrid preenchido:")
    imprimir_grid(grid_copy)

    print("\nRegiões preenchidas:")
    num_regioes = 0
    for cor, coords in resultados.items():
        if cor != -1:
            print(f"Cor {cor}: {len(coords)} células")
            num_regioes += 1

    history = resultados.get(-1, [])
    if history:
        imgs_dir = os.path.join(os.path.dirname(__file__), "imgs")
        os.makedirs(imgs_dir, exist_ok=True)
        out_path = os.path.join(imgs_dir, nome_arquivo)
        animate_history(history, save_gif=True, out_path=out_path, interval=250)
        print(f"\nAnimação salva em: {out_path}")
    else:
        print("\nNenhum histórico foi gravado.")


def exemplo_1_regiao():
    grid = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    return grid


def exemplo_2_regioes():
    grid = [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
    ]
    return grid


def exemplo_3_regioes():
    grid = [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 0, 1],
        [0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0],
    ]
    return grid


def exemplo_4_regioes():
    grid = [
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
    ]
    return grid


def exemplo_5_regioes():
    grid = [
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
    ]
    return grid


if __name__ == "__main__":
    print("=== Exemplo básico ===")
    exemplo_execucao()

    print("\n\n=== Exemplo com 1 região ===")
    exemplo_com_visualizacao(exemplo_1_regiao(), "exemplo_1_regiao.gif")

    print("\n\n=== Exemplo com 2 regiões ===")
    exemplo_com_visualizacao(exemplo_2_regioes(), "exemplo_2_regioes.gif")

    print("\n\n=== Exemplo com 3 regiões ===")
    exemplo_com_visualizacao(exemplo_3_regioes(), "exemplo_3_regioes.gif")

    print("\n\n=== Exemplo com 4 regiões ===")
    exemplo_com_visualizacao(exemplo_4_regioes(), "exemplo_4_regioes.gif")

    print("\n\n=== Exemplo com 5 regiões ===")
    exemplo_com_visualizacao(exemplo_5_regioes(), "exemplo_5_regioes.gif")
