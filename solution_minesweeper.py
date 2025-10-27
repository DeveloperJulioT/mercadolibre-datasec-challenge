# Mercado Libre DataSec Technical Challenge
# Versión de Python utilizada: 3.12.3

from typing import List

def minesweeper_count_neighbours(board: List[List[int]]) -> List[List[int]]:
    if not board or not board[0]:
        # Manejo de casos límite: tablero vacío o de 0 columnas
        return []

    R = len(board)       # Número de filas
    C = len(board[0])    # Número de columnas

    # Inicializar el tablero de resultados con ceros.
    # Usamos una comprensión de lista para crear una copia limpia.
    result_board = [[0 for _ in range(C)] for _ in range(R)]

    # 8 posibles direcciones de desplazamiento (horizontal, vertical, diagonal)
    # (dr, dc) = (fila_delta, columna_delta)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Recorrido de doble bucle sobre cada celda (r, c) del tablero
    for r in range(R):
        for c in range(C):
            
            # 1. Procesar la celda actual (r, c)
            if board[r][c] == 1:
                # Si la celda actual es una mina, se marca con 9 en el resultado. 
                result_board[r][c] = 9
            else:
                # Si la celda actual es un espacio vacío (0), se cuenta el número de minas vecinas.
                mine_count = 0
                
                # 2. Recorrer los 8 vecinos para contar las minas
                for dr, dc in directions:
                    # Coordenadas de la celda vecina (nr, nc)
                    nr, nc = r + dr, c + dc
                    
                    # 3. Validación de límites y conteo
                    # Asegurarse de que el vecino esté dentro de los límites del tablero
                    is_in_bounds = (0 <= nr < R) and (0 <= nc < C)
                    
                    if is_in_bounds and board[nr][nc] == 1:
                        # Si el vecino está dentro de los límites Y es una mina (1) en el tablero original
                        mine_count += 1
                
                # Asignar la cuenta de minas vecinas a la celda vacía en el tablero de resultados
                result_board[r][c] = mine_count

    return result_board

# Este bloque ejecuta un caso de prueba para verificar la función minesweeper_count_neighbours.
if __name__ == "__main__":
    
    # Ejemplo de entrada
    INPUT_BOARD = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 1, 0, 0]
    ]

    # Resultado esperado.
    EXPECTED_OUTPUT = [
        [1, 9, 2, 1],
        [2, 3, 9, 2],
        [3, 9, 4, 9],
        [9, 9, 3, 1]
    ]

    # Ejecución y verificación
    calculated_output = minesweeper_count_neighbours(INPUT_BOARD)

    # Función auxiliar para imprimir el resultado de forma legible
    def print_board(board_to_print):
        print("[" + "\n".join([f"  {row}," for row in board_to_print])[:-1] + "]")

    print("--- Tablero de Entrada ---")
    print_board(INPUT_BOARD)

    print("\n--- Tablero Calculado (Salida) ---")
    print_board(calculated_output)

    print("\n--- Verificación ---")
    if calculated_output == EXPECTED_OUTPUT:
        print("¡El resultado coincide con la salida esperada!")
    else:
        print("¡El resultado NO coincide con la salida esperada!")
        print("\nEsperado:")
        print_board(EXPECTED_OUTPUT)