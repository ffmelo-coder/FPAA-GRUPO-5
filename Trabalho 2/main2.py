from floodfill2 import colorir_todas_regioes, imprimir_grid


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


if __name__ == "__main__":
    exemplo_execucao()
