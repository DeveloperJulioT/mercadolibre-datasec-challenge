#Archivo de pruebas unitarias para solution_best_in_genre.py
#Versión de Python: 3.12.3

from unittest.mock import patch
import requests
from solution_best_in_genre import bestInGenre, fetch_page

# Caso 1: Selección correcta de la mejor serie 
@patch("solution_best_in_genre.fetch_page")
def test_best_in_genre_returns_highest_rating(mock_fetch_page):
    """Verifica que devuelve la mejor serie con rating mayor y desempate alfabético."""
    # Simulamos la respuesta paginada de la API
    mock_api_page_1 = {
        "page": 1,
        "total_pages": 2,
        "data": [
            {"name": "Alpha Show", "genre": "Drama, Action", "imdb_rating": 9.1},
            {"name": "Beta Series", "genre": "Comedy", "imdb_rating": 8.5},
        ],
    }

    mock_api_page_2 = {
        "page": 2,
        "total_pages": 2,
        "data": [
            {"name": "Omega Drama", "genre": "Drama", "imdb_rating": 9.1},
            {"name": "Gamma Show", "genre": "Drama", "imdb_rating": 8.9},
        ],
    }

    # Configuramos el mock para que devuelva las dos páginas
    mock_fetch_page.side_effect = [mock_api_page_1, mock_api_page_2]

    result = bestInGenre("Drama")

    # Ambas Alpha y Omega tienen rating 9.1, pero Alpha gana por nombre alfabético
    assert result == "Alpha Show"

# Caso 2: Género inexistente
@patch("solution_best_in_genre.fetch_page")
def test_best_in_genre_handles_no_results(mock_fetch_page):
    """Verifica el manejo de un género inexistente."""
    mock_fetch_page.return_value = {
        "page": 1,
        "total_pages": 1,
        "data": [
            {"name": "Alpha Show", "genre": "Comedy", "imdb_rating": 8.0},
        ],
    }

    result = bestInGenre("Horror")
    assert "No se encontró" in result

#  Caso 3: Error de red controlado 
@patch("solution_best_in_genre.requests.get")
def test_fetch_page_network_error(mock_get):
    """Verifica que fetch_page() maneje errores de red correctamente."""
    # Simulamos un fallo real de conexión de la librería requests
    mock_get.side_effect = requests.exceptions.RequestException("Connection failed")

    result = fetch_page(1)
    # La función debe manejar el error y retornar None sin lanzar excepción
    assert result is None
