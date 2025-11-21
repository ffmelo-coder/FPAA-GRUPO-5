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


def gerar_labirinto_aleatorio(linhas, colunas, densidade_obstaculos=0.3, numero_fins=1):
    if linhas < 2 or colunas < 2:
        raise ValueError("Labirinto deve ter no minimo 2x2")
    total_setores = numero_fins + 1
    if linhas * colunas < 4 * total_setores:
        raise ValueError(
            "Area do labirinto insuficiente para o numero de fins (X * Y >= 4 * (N + 1))"
        )
    if densidade_obstaculos > 0.8:
        densidade_obstaculos = 0.8
        print("Aviso: Densidade ajustada para 0.8 (maximo permitido)")
    labirinto = [[0 for _ in range(colunas)] for _ in range(linhas)]
    grid_cols = int(np.ceil(np.sqrt(total_setores)))
    grid_rows = int(np.ceil(total_setores / grid_cols))
    setores = list(range(total_setores))
    inicio_setor = np.random.randint(0, total_setores)
    fins_setores = [s for s in setores if s != inicio_setor]
    for setor in setores:
        setor_row = setor // grid_cols
        setor_col = setor % grid_cols
        start_row = (setor_row * linhas) // grid_rows
        end_row = ((setor_row + 1) * linhas) // grid_rows - 1
        start_col = (setor_col * colunas) // grid_cols
        end_col = ((setor_col + 1) * colunas) // grid_cols - 1
        if end_row < start_row:
            end_row = start_row
        if end_col < start_col:
            end_col = start_col
        r = np.random.randint(start_row, end_row + 1)
        c = np.random.randint(start_col, end_col + 1)
        if setor == inicio_setor:
            labirinto[r][c] = 2
        else:
            labirinto[r][c] = 3
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
        numero_fins = 1
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
                if algoritmo == "2":
                    try:
                        numero_fins_input = input(
                            "Digite o numero de fins desejados (inteiro >=1, padrao 1): "
                        ).strip()
                        if numero_fins_input:
                            numero_fins = int(numero_fins_input)
                            if numero_fins < 1:
                                print("Erro: numero de fins deve ser >= 1")
                                return
                    except ValueError:
                        print("Erro: numero de fins invalido")
                        return
                labirinto = gerar_labirinto_aleatorio(
                    linhas, colunas, densidade, numero_fins
                )
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
                    print("\nDeseja salvar a animacao como GIF? (s/n): ", end="")
                    salvar_gif_input = input().strip().lower()
                    if salvar_gif_input == "s":
                        pathfinder.salvar_ultima_animacao()
        else:
            floodfill = FloodFill(labirinto)
            if not floodfill.encontrar_posicoes():
                print("Sem solucao")
                return
            caminhos = floodfill.buscar_caminho(visualizar=visualizar)
            if not caminhos:
                print("Sem solucao")
            else:
                total_fins = len(floodfill.fins)
                caminhos_possiveis = len(caminhos)
                caminhos_impossiveis = total_fins - caminhos_possiveis
                print(f"\nCaminhos Possíveis: {caminhos_possiveis}")
                print(f"Caminhos Impossíveis: {caminhos_impossiveis}")
                print("\n[Flood Fill] Fins encontrados e caminhos:")
                for fim_pos, caminho in caminhos.items():
                    print(f"Fim {fim_pos}: comprimento {len(caminho)}")
                    print(caminho)
                if not visualizar:
                    print("\nLabirinto com o caminho destacado:")
                    floodfill.mostrar_labirinto_com_caminho(caminhos)
                else:
                    print("\nDeseja salvar a animacao como GIF? (s/n): ", end="")
                    salvar_gif_input = input().strip().lower()
                    if salvar_gif_input == "s":
                        floodfill.salvar_ultima_animacao()
    except ValueError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


if __name__ == "__main__":
    main()
