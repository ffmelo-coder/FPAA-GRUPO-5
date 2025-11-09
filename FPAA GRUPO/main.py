from pathfinder import PathFinder
from floodfill import FloodFill
import numpy as np


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


def gerar_labirinto_aleatorio(linhas, colunas, densidade_obstaculos=0.3):
    if linhas < 2 or colunas < 2:
        raise ValueError("Labirinto deve ter no minimo 2x2")

    if densidade_obstaculos > 0.8:
        densidade_obstaculos = 0.8
        print("Aviso: Densidade ajustada para 0.8 (maximo permitido)")

    labirinto = [[0 for _ in range(colunas)] for _ in range(linhas)]

    tamanho_medio = (linhas + colunas) / 2
    distancia_minima = int(tamanho_medio * 0.6)

    tentativas = 0
    max_tentativas = 100

    while tentativas < max_tentativas:
        if tamanho_medio <= 5:
            inicio_x = np.random.randint(0, linhas)
            inicio_y = np.random.randint(0, colunas)
        else:
            quadrante_inicio = np.random.randint(0, 4)
            if quadrante_inicio == 0:
                inicio_x = np.random.randint(0, linhas // 2 + 1)
                inicio_y = np.random.randint(0, colunas // 2 + 1)
            elif quadrante_inicio == 1:
                inicio_x = np.random.randint(0, linhas // 2 + 1)
                inicio_y = np.random.randint(colunas // 2, colunas)
            elif quadrante_inicio == 2:
                inicio_x = np.random.randint(linhas // 2, linhas)
                inicio_y = np.random.randint(0, colunas // 2 + 1)
            else:
                inicio_x = np.random.randint(linhas // 2, linhas)
                inicio_y = np.random.randint(colunas // 2, colunas)

        if tamanho_medio <= 5:
            fim_x = np.random.randint(0, linhas)
            fim_y = np.random.randint(0, colunas)
        else:
            quadrantes_opostos = {0: 3, 1: 2, 2: 1, 3: 0}
            quadrante_fim = quadrantes_opostos.get(
                quadrante_inicio, np.random.randint(0, 4)
            )

            if quadrante_fim == 0:
                fim_x = np.random.randint(0, linhas // 2 + 1)
                fim_y = np.random.randint(0, colunas // 2 + 1)
            elif quadrante_fim == 1:
                fim_x = np.random.randint(0, linhas // 2 + 1)
                fim_y = np.random.randint(colunas // 2, colunas)
            elif quadrante_fim == 2:
                fim_x = np.random.randint(linhas // 2, linhas)
                fim_y = np.random.randint(0, colunas // 2 + 1)
            else:
                fim_x = np.random.randint(linhas // 2, linhas)
                fim_y = np.random.randint(colunas // 2, colunas)

        distancia_manhattan = abs(fim_x - inicio_x) + abs(fim_y - inicio_y)

        if distancia_manhattan >= distancia_minima:
            break

        tentativas += 1

    labirinto[inicio_x][inicio_y] = 2
    labirinto[fim_x][fim_y] = 3

    num_obstaculos = int(linhas * colunas * densidade_obstaculos)
    obstaculos_colocados = 0

    while obstaculos_colocados < num_obstaculos:
        x = np.random.randint(0, linhas)
        y = np.random.randint(0, colunas)

        if labirinto[x][y] == 0:
            labirinto[x][y] = 1
            obstaculos_colocados += 1

    return labirinto


def mostrar_labirinto(labirinto):
    for linha in labirinto:
        linha_str = ""
        for celula in linha:
            if celula == 2:
                linha_str += "S "
            elif celula == 3:
                linha_str += "E "
            else:
                linha_str += str(celula) + " "
        print(linha_str)


def main():
    try:
        print("=== Sistema de Busca de Caminhos ===\n")
        print("Escolha o algoritmo:")
        print("1 - A* (suporta movimento diagonal)")
        print("2 - Flood Fill (apenas movimentos ortogonais)")

        algoritmo = input("\nAlgoritmo: ").strip()

        if algoritmo not in ["1", "2"]:
            print("Opcao invalida!")
            return

        print("\nEscolha uma opcao:")
        print("1 - Digitar labirinto manualmente")
        print("2 - Gerar labirinto aleatorio")

        opcao = input("\nOpcao: ").strip()

        if opcao == "1":
            labirinto = ler_labirinto()
            if labirinto is None:
                return
        elif opcao == "2":
            try:
                linhas = int(input("\nDigite o numero de linhas (X): "))
                colunas = int(input("Digite o numero de colunas (Y): "))

                if linhas < 2 or colunas < 2:
                    print("Erro: Labirinto deve ter no minimo 2x2")
                    return

                densidade = input(
                    "Digite a densidade de obstaculos (0.0 a 0.8, padrao 0.3): "
                ).strip()
                if densidade:
                    densidade = float(densidade)
                    if densidade < 0 or densidade > 0.8:
                        print("Erro: Densidade deve estar entre 0.0 e 0.8")
                        return
                else:
                    densidade = 0.3

                labirinto = gerar_labirinto_aleatorio(linhas, colunas, densidade)
                print("\nLabirinto gerado:")
                mostrar_labirinto(labirinto)

            except ValueError as e:
                print(f"Erro na entrada: {e}")
                return
        else:
            print("Opcao invalida!")
            return

        validar_labirinto(labirinto)

        print("\nDeseja ver a visualizacao animada? (s/n): ", end="")
        visualizar_input = input().strip().lower()
        visualizar = visualizar_input == "s"

        if algoritmo == "1":
            print("\nDeseja permitir movimentacao diagonal? (s/n): ", end="")
            diagonal_input = input().strip().lower()
            diagonal = diagonal_input == "s"

            pathfinder = PathFinder(labirinto, diagonal=diagonal)

            if not pathfinder.encontrar_posicoes():
                print("Sem solucao")
                return

            caminho = pathfinder.a_estrela(visualizar=visualizar)

            if caminho is None:
                print("Sem solucao")
            else:
                print("\n[A*] Menor caminho (em coordenadas):")
                print(caminho)

                if not visualizar:
                    print("\nLabirinto com o caminho destacado:")
                    pathfinder.mostrar_labirinto_com_caminho(caminho)

        else:
            floodfill = FloodFill(labirinto)

            if not floodfill.encontrar_posicoes():
                print("Sem solucao")
                return

            caminho = floodfill.buscar_caminho(visualizar=visualizar)

            if caminho is None:
                print("Sem solucao")
            else:
                print("\n[Flood Fill] Menor caminho (em coordenadas):")
                print(caminho)

                if not visualizar:
                    print("\nLabirinto com o caminho destacado:")
                    floodfill.mostrar_labirinto_com_caminho(caminho)

    except ValueError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


if __name__ == "__main__":
    main()
