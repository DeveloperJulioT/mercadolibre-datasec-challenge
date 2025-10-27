#Archivo de pruebas unitarias para solution_minesweeper.py
#Versión de Python: 3.12.3

from solution_minesweeper import minesweeper_count_neighbours

# CASO 1 — Ejemplo principal del challenge
def test_minesweeper_example_case():
    input_board = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 1, 0, 0],
    ]

    expected_output = [
        [1, 9, 2, 1],
        [2, 3, 9, 2],
        [3, 9, 4, 9],
        [9, 9, 3, 1],
    ]
    assert minesweeper_count_neighbours(input_board) == expected_output

# CASO 2 — Tablero vacío
def test_empty_board_returns_empty_list():
    assert minesweeper_count_neighbours([]) == []

# CASO 3 — Tablero 1x1 sin mina
def test_single_cell_no_mine():
    board = [[0]]
    expected = [[0]]
    assert minesweeper_count_neighbours(board) == expected

# CASO 4 — Tablero 1x1 con mina
def test_single_cell_with_mine():
    board = [[1]]
    expected = [[9]]
    assert minesweeper_count_neighbours(board) == expected

# CASO 5 — Tablero rectangular (no cuadrado)
def test_rectangular_board():
    board = [
        [1, 0, 0],
        [0, 1, 0],
    ]
    expected = [
        [9, 2, 1],
        [2, 9, 1],
    ]
    assert minesweeper_count_neighbours(board) == expected

#  CASO 6 — Validación de que no se altera el tablero original
def test_original_board_not_modified():
    board = [
        [0, 1],
        [1, 0],
    ]
    original_copy = [row[:] for row in board]  # copia profunda

    _ = minesweeper_count_neighbours(board)

    # Verificamos que el tablero original sigue igual
    assert board == original_copy

#  CASO 7 — Validación de consistencia del tamaño del tablero
def test_output_has_same_dimensions():
    board = [
        [0, 1, 0],
        [1, 0, 0],
    ]
    output = minesweeper_count_neighbours(board)

    assert len(output) == len(board)
    assert all(len(row) == len(board[0]) for row in output)
