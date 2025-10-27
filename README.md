# 🧠 Mercado Libre DataSec Technical Challenge

Este repositorio contiene la solución completa de **Mercado Libre DataSec Technical Challenge**, desarrollado en **Python 3.12.3** y **Go 1.25.3**, con prácticas de ingeniería segura, pruebas unitarias y uso de inteligencia artificial (Hugging Face Inference API).

---

## 📁 Estructura del Proyecto

```
mercadolibre-datasec-challenge/
│
├── solution_minesweeper.py        # Punto 1: Lógica de Buscaminas
│── solution_best_in_genre.py      # Punto 2: API de series y mejor género
│── solution_ad_failures.sql       # Punto 3: Consulta SQL con validación
│── validate_sql_solution.py       # Punto 3: Script para validar la consulta
│── solution_summarizer.go         # Punto 4: CLI con HuggingFace API
│── tests/                         # Carpeta de pruebas unitarias (pytest)
│
└── README.md
```

---

## ⚙️ Requisitos Previos

### 🔹 Python
- Versión: **3.12.3**
- Librerías:
  ```bash
  pip install requests pytest pandas
  ```

### 🔹 Go
- Versión mínima: **1.20**
- Variable de entorno obligatoria para el punto 4:
  ```bash
  setx HUGGINGFACE_API_KEY "hf_tuTokenGenerado123456"
  ```
  *(Reinicia la terminal después de configurarla).*

---

## 🚀 Ejecución por Puntos

### 🧩 **Punto 1 — Minesweeper**
Calcula el número de minas vecinas en un tablero estilo “Buscaminas”.

```bash
python solution_minesweeper.py
```

**Salida esperada:**
```
¡El resultado coincide con la salida esperada!
```

---

### 🎬 **Punto 2 — Best In Genre**
Obtiene la mejor serie por género usando la API pública de Hackerrank.

```bash
python solution_best_in_genre.py
```

**Ejemplo:**
```
Buscando la mejor serie para el género: 'Drama'...
La mejor serie en el género 'Drama' es: Breaking Bad
```

---

### 🧮 **Punto 3 — SQL Ad Failures**
Consulta SQL para obtener el cliente con más campañas fallidas.

1. Archivo principal: `solution_ad_failures.sql`
2. Validación:
   ```bash
   python validate_sql_solution.py
   ```

**Salida esperada:**
```
=== Resultado de la consulta SQL ===
         customer  failures
0  Whitney Ferrero         6

Validación exitosa: la consulta devuelve el resultado esperado.
```

---

### 🤖 **Punto 4 — Go CLI: Text Summarizer con HuggingFace**
CLI en Go que genera resúmenes con la Inference API de Hugging Face (`facebook/bart-large-cnn`).

**Ejecución desde archivo:**
```bash
go run solution_summarizer.go --file texto.txt --type bullet
```

**Ejecución con texto directo:**
```bash
go run solution_summarizer.go --text "La IA está transformando la industria tecnológica" --type short
```

Tipos de resumen:
- `short` → breve
- `medium` → intermedio
- `bullet` → formato con viñetas

**Ejemplo de salida:**
```
✅ Código de respuesta: 200
✅ Respuesta procesada correctamente.

=== Resumen ===
- La inteligencia artificial transforma la industria tecnológica.
- Automatiza procesos y mejora la eficiencia.
```

---

## 🧪 Ejecución de Pruebas Unitarias

Las pruebas automatizadas están implementadas con **pytest** en la carpeta `tests/`.

### 📋 Comando recomendado (desde el entorno virtual):

```bash
python -m pytest -v
```

O directamente (si pytest está en PATH):
```bash
pytest -v
```

**Salida esperada:**
```
collected 10 items
tests/test_best_in_genre.py::test_best_in_genre_returns_highest_rating PASSED
tests/test_minesweeper.py::test_minesweeper_example_case PASSED
...
=================== 10 passed in 0.37s ===================
```

---

## 🧰 Tecnologías Utilizadas

| Tecnología | Propósito |
|-------------|------------|
| **Python 3.12.3** | Lógica, consultas y validaciones |
| **Go 1.25.3** | CLI con conexión a Hugging Face |
| **pytest** | Pruebas unitarias |
| **SQLite / SQL** | Validación y ejecución de consultas |
| **Hugging Face API** | Generación de resúmenes con IA |

---

## 🧑‍💻 Autor
**Julio Tarquino**  
Software engineer expert in cybersecurity and information security
📍 Colombia 🇨🇴  
[LinkedIn](https://www.linkedin.com/in/julio-david-tarquino-calderon-cyber-dev-ops/) | [GitHub](https://github.com/DeveloperJulioT)
