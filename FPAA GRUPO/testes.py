from pathfinder import PathFinder


def teste_1_simples_sem_diagonal():
    print("=== Teste 1: Labirinto simples (SEM diagonal) ===")
    labirinto = [[2, 0, 1, 0, 0], [0, 0, 0, 0, 1], [0, 1, 0, 0, 0], [1, 0, 0, 3, 1]]

    pathfinder = PathFinder(labirinto, diagonal=False)
    caminho = pathfinder.a_estrela()

    if caminho:
        print(f"Caminho encontrado com {len(caminho)} passos: {caminho}")
        pathfinder.mostrar_labirinto_com_caminho(caminho)
    else:
        print("Sem solucao")
    print()


def teste_2_sem_solucao_sem_diagonal():
    print("=== Teste 2: Labirinto sem solucao (SEM diagonal) ===")
    labirinto = [[2, 0, 1, 0, 0], [0, 0, 1, 0, 1], [1, 1, 1, 1, 1], [1, 0, 0, 3, 1]]

    pathfinder = PathFinder(labirinto, diagonal=False)
    caminho = pathfinder.a_estrela()

    if caminho:
        print(f"Caminho encontrado: {caminho}")
    else:
        print("Sem solucao")
    print()


def teste_3_grande_sem_diagonal():
    print("=== Teste 3: Labirinto maior (SEM diagonal) ===")
    labirinto = [
        [2, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 3],
    ]

    pathfinder = PathFinder(labirinto, diagonal=False)
    caminho = pathfinder.a_estrela()

    if caminho:
        print(f"Caminho encontrado com {len(caminho)} passos")
        pathfinder.mostrar_labirinto_com_caminho(caminho)
    else:
        print("Sem solucao")
    print()


def teste_4_direto_sem_diagonal():
    print("=== Teste 4: Caminho direto (SEM diagonal) ===")
    labirinto = [[2, 0, 0, 0, 3]]

    pathfinder = PathFinder(labirinto, diagonal=False)
    caminho = pathfinder.a_estrela()

    if caminho:
        print(f"Caminho encontrado com {len(caminho)} passos: {caminho}")
        pathfinder.mostrar_labirinto_com_caminho(caminho)
    else:
        print("Sem solucao")
    print()


def teste_5_simples_com_diagonal():
    print("=== Teste 5: Labirinto simples (COM diagonal) ===")
    labirinto = [[2, 0, 1, 0, 0], [0, 0, 1, 0, 1], [1, 0, 1, 0, 0], [1, 0, 0, 3, 1]]

    pathfinder = PathFinder(labirinto, diagonal=True)
    caminho = pathfinder.a_estrela()

    if caminho:
        print(f"Caminho encontrado com {len(caminho)} passos: {caminho}")
        pathfinder.mostrar_labirinto_com_caminho(caminho)
    else:
        print("Sem solucao")
    print()


def teste_6_com_solucao_com_diagonal():
    print("=== Teste 6: Labirinto que tem solucao diagonal (COM diagonal) ===")
    labirinto = [[2, 0, 1, 0, 0], [0, 0, 1, 0, 1], [1, 1, 0, 1, 1], [1, 0, 1, 3, 1]]

    pathfinder = PathFinder(labirinto, diagonal=True)
    caminho = pathfinder.a_estrela()

    if caminho:
        print(f"Caminho encontrado com {len(caminho)} passos: {caminho}")
        pathfinder.mostrar_labirinto_com_caminho(caminho)
    else:
        print("Sem solucao")
    print()


def teste_7_grande_com_diagonal():
    print("=== Teste 7: Labirinto maior (COM diagonal) ===")
    labirinto = [
        [2, 0, 0, 0, 0, 0, 0, 1],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 3],
    ]

    pathfinder = PathFinder(labirinto, diagonal=True)
    caminho = pathfinder.a_estrela()

    if caminho:
        print(f"Caminho encontrado com {len(caminho)} passos")
        pathfinder.mostrar_labirinto_com_caminho(caminho)
    else:
        print("Sem solucao")
    print()


def teste_8_direto_com_diagonal():
    print("=== Teste 8: Caminho direto diagonal (COM diagonal) ===")
    labirinto = [[2, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 3]]

    pathfinder = PathFinder(labirinto, diagonal=True)
    caminho = pathfinder.a_estrela()

    if caminho:
        print(f"Caminho encontrado com {len(caminho)} passos: {caminho}")
        pathfinder.mostrar_labirinto_com_caminho(caminho)
    else:
        print("Sem solucao")
    print()


def executar_todos_testes():
    print("========================================")
    print("EXECUTANDO TESTES DO PATHFINDER")
    print("========================================\n")

    print("*** TESTES SEM MOVIMENTO DIAGONAL ***\n")
    teste_1_simples_sem_diagonal()
    teste_2_sem_solucao_sem_diagonal()
    teste_3_grande_sem_diagonal()
    teste_4_direto_sem_diagonal()

    print("\n*** TESTES COM MOVIMENTO DIAGONAL ***\n")
    teste_5_simples_com_diagonal()
    teste_6_com_solucao_com_diagonal()
    teste_7_grande_com_diagonal()
    teste_8_direto_com_diagonal()

    print("========================================")
    print("TESTES CONCLUIDOS - 8 TESTES EXECUTADOS")
    print("========================================")


if __name__ == "__main__":
    executar_todos_testes()
