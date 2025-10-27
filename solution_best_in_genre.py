# Mercado Libre DataSec Technical Challenge
# Versión de Python utilizada: 3.12.3

import requests
from typing import List, Dict, Any, Optional

# Constante de la API
BASE_URL = "https://jsonmock.hackerrank.com/api/tvseries"

# Función para realizar la petición GET a una página específica de la API.
def fetch_page(page_number: int, url: str = BASE_URL) -> Optional[Dict[str, Any]]:
    try:
        # 1. Definición de parámetros para la paginación
        params = {'page': page_number}
        
        # 2. Petición GET con un timeout para evitar esperas infinitas
        response = requests.get(url, params=params, timeout=15)
        
        # 3. Verificación de errores HTTP (status codes 4xx o 5xx)
        response.raise_for_status() 
        
        # 4. Retorno de la respuesta JSON
        return response.json()
        
    except requests.exceptions.RequestException as e:
        # Manejo de errores de red (conexión, DNS, timeout, HTTP error, etc.)
        print(f"Error al obtener la página {page_number} de la API: {e}")
        return None

def bestInGenre(genre: str) -> str:
    # Inicialización de variables para seguimiento de la mejor serie
    best_series_name: Optional[str] = None
    max_rating: float = -1.0 # Una calificación inicial imposiblemente baja
    current_page: int = 1
    total_pages: int = 1 # Se actualizará en la primera llamada

    # Bucle de paginación: se detiene cuando se han recorrido todas las páginas
    while current_page <= total_pages:
        
        # Obtener datos de la página actual
        response_data = fetch_page(current_page)
        
        if not response_data:
            # Si hay un error en la API, salimos del bucle para evitar un ciclo infinito.
            break 

        # Actualizar el número total de páginas - propiedad 'total_pages' en el JSON
        total_pages = response_data.get('total_pages', total_pages)
        series_list: List[Dict[str, Any]] = response_data.get('data', [])

        # Procesar la lista de series de la página actual
        for series in series_list:
            series_name = series.get('name')
            series_genre = series.get('genre', '')
            rating = series.get('imdb_rating')

            # Validación de datos y Filtrado por Género
            # Se busca la subcadena de género
            if series_name and rating is not None and genre.lower() in series_genre.lower():
                
                # 1. Aplicar Criterio Principal: Mayor imdb_rating
                if rating > max_rating:
                    max_rating = rating
                    best_series_name = series_name
                
                # 2. Aplicar Criterio de Desempate: Nombre alfabéticamente menor
                elif rating == max_rating and best_series_name:
                    # Comparar strings alfabéticamente
                    if series_name < best_series_name:
                        best_series_name = series_name
        
        current_page += 1 # Avanzar a la siguiente página

    # Si se encontró una serie, retorna su nombre; si no, retorna una cadena vacía.
    return best_series_name if best_series_name else "No se encontró ninguna serie para el género especificado."

# Bloque de Ejecución y Pruebas
if __name__ == "__main__":
    print("Desafío 2: Mejor Serie por Género")
    
    # Ejemplo de prueba
    TEST_GENRE = "Drama" 
    print(f"\nBuscando la mejor serie para el género: '{TEST_GENRE}'...")
    
    # Ejecución de la función
    result = bestInGenre(TEST_GENRE)
    
    print(f"\nLa mejor serie en el género '{TEST_GENRE}' es: \n>>> {result} <<<")
