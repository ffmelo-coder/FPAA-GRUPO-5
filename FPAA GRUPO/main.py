from pathfinder import PathFinder


def ler_labirinto():
    print("Digite o labirinto (matriz 2D):")
    print("Use: 0 (livre), 1 (obstaculo), 2 (inicio S), 3 (fim E)")
    print("Digite cada linha separada por espacos, linha vazia para terminar:")

    labirinto = []
    while True:
        linha = input()
        if not linha.strip():
            break

        valores = linha.split()
        linha_labirinto = []
        for v in valores:
            if v.upper() == "S":
                linha_labirinto.append(2)
            elif v.upper() == "E":
                linha_labirinto.append(3)
            else:
                linha_labirinto.append(int(v))

        labirinto.append(linha_labirinto)

    return labirinto


def main():
    labirinto = ler_labirinto()

    if not labirinto:
        print("Labirinto vazio!")
        return

    pathfinder = PathFinder(labirinto)

    if not pathfinder.encontrar_posicoes():
        print("Sem solucao")
        return

    caminho = pathfinder.a_estrela()

    if caminho is None:
        print("Sem solucao")
    else:
        print("\nMenor caminho (em coordenadas):")
        print(caminho)

        print("\nLabirinto com o caminho destacado:")
        pathfinder.mostrar_labirinto_com_caminho(caminho)


if __name__ == "__main__":
    main()
