from pathfinder import PathFinder


def validar_labirinto(labirinto):
    if not labirinto:
        raise ValueError("Labirinto vazio")

    largura = len(labirinto[0])
    for linha in labirinto:
        if len(linha) != largura:
            raise ValueError("Todas as linhas devem ter o mesmo tamanho")

    return True


def ler_labirinto():
    print("Digite o labirinto (matriz 2D):")
    print("Use: 0 (livre), 1 (obstaculo), S (inicio), E (fim)")
    print("Digite cada linha separada por espacos, linha vazia para terminar:")

    labirinto = []
    while True:
        try:
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
                    try:
                        valor = int(v)
                        if valor not in [0, 1, 2, 3]:
                            raise ValueError(f"Valor invalido: {v}")
                        linha_labirinto.append(valor)
                    except ValueError:
                        raise ValueError(f"Valor invalido: {v}")

            labirinto.append(linha_labirinto)
        except ValueError as e:
            print(f"Erro na entrada: {e}")
            return None

    return labirinto


def main():
    try:
        labirinto = ler_labirinto()

        if labirinto is None:
            return

        validar_labirinto(labirinto)

        print("\nDeseja permitir movimentacao diagonal? (s/n): ", end="")
        diagonal_input = input().strip().lower()
        diagonal = diagonal_input == "s"

        pathfinder = PathFinder(labirinto, diagonal=diagonal)

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

    except ValueError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


if __name__ == "__main__":
    main()
