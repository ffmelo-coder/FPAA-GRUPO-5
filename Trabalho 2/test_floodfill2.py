import unittest
import copy
from floodfill2 import colorir_regiao, colorir_todas_regioes


class TestFloodFill(unittest.TestCase):

    def test_grid_vazio(self):
        grid = []
        resultado = colorir_todas_regioes(grid)
        self.assertEqual(resultado, {})

    def test_grid_sem_espacos_livres(self):
        grid = [[1, 1], [1, 1]]
        resultado = colorir_todas_regioes(grid)
        self.assertEqual(resultado, {})
        self.assertEqual(grid, [[1, 1], [1, 1]])

    def test_grid_todo_livre(self):
        grid = [[0, 0], [0, 0]]
        resultado = colorir_todas_regioes(grid, inicio=(0, 0), primeiro_cor=2)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(len(resultado[2]), 4)
        self.assertTrue(all(cell == 2 for row in grid for cell in row))

    def test_uma_regiao(self):
        grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        resultado = colorir_todas_regioes(grid, inicio=(0, 0), primeiro_cor=2)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(len(resultado[2]), 9)

    def test_duas_regioes_separadas(self):
        grid = [
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
        ]
        resultado = colorir_todas_regioes(grid, inicio=(0, 0), primeiro_cor=2)
        self.assertEqual(len(resultado), 2)
        self.assertEqual(len(resultado[2]), 4)
        self.assertEqual(len(resultado[3]), 4)

    def test_inicio_fora_dos_limites(self):
        grid = [[0, 0], [0, 0]]
        resultado = colorir_todas_regioes(grid, inicio=(5, 5), primeiro_cor=2)
        self.assertEqual(len(resultado), 1)
        self.assertIn(2, resultado)

    def test_inicio_em_obstaculo(self):
        grid = [[1, 0], [0, 0]]
        resultado = colorir_todas_regioes(grid, inicio=(0, 0), primeiro_cor=2)
        self.assertEqual(len(resultado), 1)
        self.assertIn(2, resultado)
        self.assertEqual(len(resultado[2]), 3)

    def test_inicio_none(self):
        grid = [[0, 1, 0]]
        resultado = colorir_todas_regioes(grid, inicio=None, primeiro_cor=2)
        self.assertEqual(len(resultado), 2)

    def test_grid_complexo_tres_regioes(self):
        grid = [
            [0, 0, 1, 0, 0],
            [0, 1, 1, 0, 1],
            [0, 0, 1, 1, 1],
            [1, 1, 0, 0, 0],
        ]
        resultado = colorir_todas_regioes(grid, inicio=(0, 0), primeiro_cor=2)
        self.assertEqual(len(resultado), 3)
        self.assertIn(2, resultado)
        self.assertIn(3, resultado)
        self.assertIn(4, resultado)

    def test_regiao_isolada_um_pixel(self):
        grid = [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1],
        ]
        resultado = colorir_todas_regioes(grid, inicio=(1, 1), primeiro_cor=2)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(len(resultado[2]), 1)
        self.assertEqual(grid[1][1], 2)

    def test_conectividade_4_direcoes(self):
        grid = [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0],
        ]
        resultado = colorir_todas_regioes(grid, inicio=(1, 1), primeiro_cor=2)
        self.assertEqual(len(resultado), 5)
        self.assertEqual(len(resultado[2]), 1)
        self.assertEqual(grid[1][1], 2)

    def test_grid_linha_unica(self):
        grid = [[0, 0, 1, 0]]
        resultado = colorir_todas_regioes(grid, inicio=(0, 0), primeiro_cor=2)
        self.assertEqual(len(resultado), 2)
        self.assertEqual(len(resultado[2]), 2)
        self.assertEqual(len(resultado[3]), 1)

    def test_grid_coluna_unica(self):
        grid = [[0], [0], [1], [0]]
        resultado = colorir_todas_regioes(grid, inicio=(0, 0), primeiro_cor=2)
        self.assertEqual(len(resultado), 2)
        self.assertEqual(len(resultado[2]), 2)
        self.assertEqual(len(resultado[3]), 1)

    def test_colorir_regiao_direta(self):
        grid = [[0, 0], [0, 0]]
        sucesso = colorir_regiao(grid, (0, 0), 5)
        self.assertTrue(sucesso)
        self.assertTrue(all(cell == 5 for row in grid for cell in row))

    def test_colorir_regiao_posicao_invalida(self):
        grid = [[0, 0], [0, 0]]
        sucesso = colorir_regiao(grid, (5, 5), 5)
        self.assertFalse(sucesso)
        self.assertTrue(all(cell == 0 for row in grid for cell in row))

    def test_colorir_regiao_obstaculo(self):
        grid = [[1, 0], [0, 0]]
        sucesso = colorir_regiao(grid, (0, 0), 5)
        self.assertFalse(sucesso)
        self.assertEqual(grid[0][0], 1)

    def test_preservar_regioes_ja_coloridas(self):
        grid = [[2, 0], [0, 0]]
        resultado = colorir_todas_regioes(grid, inicio=(0, 1), primeiro_cor=3)
        self.assertEqual(grid[0][0], 2)
        self.assertTrue(
            all(
                grid[i][j] == 3
                for i in range(2)
                for j in range(2)
                if not (i == 0 and j == 0)
            )
        )

    def test_record_history_presente(self):
        grid = [[0, 0], [0, 0]]
        resultado = colorir_todas_regioes(
            grid, inicio=(0, 0), primeiro_cor=2, record_history=True
        )
        self.assertIn(-1, resultado)
        self.assertIsInstance(resultado[-1], list)
        self.assertGreater(len(resultado[-1]), 0)

    def test_record_history_ausente(self):
        grid = [[0, 0], [0, 0]]
        resultado = colorir_todas_regioes(
            grid, inicio=(0, 0), primeiro_cor=2, record_history=False
        )
        self.assertNotIn(-1, resultado)

    def test_cinco_regioes(self):
        grid = [
            [0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
        ]
        resultado = colorir_todas_regioes(grid, inicio=(0, 0), primeiro_cor=2)
        self.assertEqual(len(resultado), 5)

    def test_grid_grande_performance(self):
        tamanho = 20
        grid = [[0 for _ in range(tamanho)] for _ in range(tamanho)]
        resultado = colorir_todas_regioes(grid, inicio=(0, 0), primeiro_cor=2)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(len(resultado[2]), tamanho * tamanho)


if __name__ == "__main__":
    unittest.main()
