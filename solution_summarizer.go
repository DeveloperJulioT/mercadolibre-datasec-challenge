// Mercado Libre DataSec Technical Challenge
// Go CLI - Text Summarizer with GenAI (HuggingFace API)
// Go versión: 1.20+
// Ejemplo de ejecución:
//   go run solution_summarizer.go --file texto.txt --type bullet
//   go run solution_summarizer.go --text "Texto de ejemplo" --type short
// Requiere variable de entorno: HUGGINGFACE_API_KEY

package main

import (
	"bytes"
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"time"
)

// ==========================
// CONFIGURACIÓN DE CONSTANTES
// ==========================

const (
	hfModelEndpoint = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
	defaultTimeout  = 25 * time.Second
)

// ==========================
// ESTRUCTURAS DE DATOS
// ==========================

type hfRequest struct {
	Inputs string `json:"inputs"`
}

type hfResponse struct {
	SummaryText string `json:"summary_text"`
}

// ==========================
// FUNCIÓN PRINCIPAL
// ==========================

func main() {
	// Flags CLI
	filePath := flag.String("file", "", "Ruta al archivo de texto a resumir")
	textInput := flag.String("text", "", "Texto directo a resumir")
	summaryType := flag.String("type", "short", "Tipo de resumen: short | medium | bullet")
	flag.Parse()

	if *filePath == "" && *textInput == "" {
		fmt.Println("Error: debe usar --file <ruta> o --text \"texto a resumir\"")
		os.Exit(1)
	}

	// Obtener texto
	var text string
	if *filePath != "" {
		data, err := os.ReadFile(*filePath)
		if err != nil {
			fmt.Printf("Error leyendo archivo: %v\n", err)
			os.Exit(1)
		}
		text = string(data)
	} else {
		text = *textInput
	}

	apiKey := os.Getenv("HUGGINGFACE_API_KEY")
	if apiKey == "" {
		fmt.Println("Error: falta la variable de entorno HUGGINGFACE_API_KEY")
		os.Exit(1)
	}

	// Crear contexto con timeout
	ctx, cancel := context.WithTimeout(context.Background(), defaultTimeout)
	defer cancel()

	// Ejecutar resumen
	summary, err := summarizeWithHuggingFace(ctx, text, *summaryType, apiKey)
	if err != nil {
		fmt.Printf("Error llamando a la API de HuggingFace: %v\n", err)
		fmt.Println("Se usará un resumen local simplificado (fallback).")
		summary = localFallbackSummary(text, *summaryType)
	}

	fmt.Println("\n=== Resumen ===")
	fmt.Println(summary)
}

// ==========================
// FUNCIÓN PRINCIPAL DE RESUMEN (API)
// ==========================

func summarizeWithHuggingFace(ctx context.Context, text string, kind string, apiKey string) (string, error) {
    if strings.TrimSpace(text) == "" {
        return "", fmt.Errorf("texto vacío")
    }

    prompt := adjustPrompt(text, kind)

    payload := hfRequest{Inputs: prompt}
    body, _ := json.Marshal(payload)

    req, err := http.NewRequestWithContext(ctx, http.MethodPost, hfModelEndpoint, bytes.NewReader(body))
    if err != nil {
        return "", err
    }

    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", apiKey))

    client := &http.Client{Timeout: defaultTimeout}
    resp, err := client.Do(req)
    if err != nil {
        fmt.Println("Error en la llamada HTTP:", err)
        return "", err
    }
    defer resp.Body.Close()

    // 👇 Nuevo bloque de debug
    fmt.Println("Código de respuesta:", resp.StatusCode)
    if resp.StatusCode < 200 || resp.StatusCode >= 300 {
        b, _ := io.ReadAll(resp.Body)
        fmt.Println("Error en respuesta de API:", string(b))
        return "", fmt.Errorf("respuesta inválida de API (%d): %s", resp.StatusCode, string(b))
    }

    var result []hfResponse
    if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
        b, _ := io.ReadAll(resp.Body)
        fmt.Println("Error decodificando JSON:", err)
        fmt.Println("recibido:", string(b))
        return "", fmt.Errorf("error decodificando respuesta: %v | contenido: %s", err, string(b))
    }

    if len(result) == 0 {
        fmt.Println("La respuesta JSON está vacía")
        return "", fmt.Errorf("respuesta vacía de la API")
    }

    fmt.Println("Respuesta procesada correctamente.")
    return strings.TrimSpace(result[0].SummaryText), nil
}


// ==========================
// PROMPT Y FALLBACK LOCAL
// ==========================

func adjustPrompt(text string, kind string) string {
	switch strings.ToLower(kind) {
	case "bullet":
		return "Resume el siguiente texto en formato de viñetas:\n\n" + text
	case "medium":
		return "Resume el siguiente texto en dos o tres oraciones:\n\n" + text
	default:
		return "Resume brevemente el siguiente texto:\n\n" + text
	}
}

// Resumen local simple por fallback
func localFallbackSummary(text string, kind string) string {
	lines := strings.Split(text, ".")
	if len(lines) == 0 {
		return text
	}
	switch strings.ToLower(kind) {
	case "bullet":
		var out strings.Builder
		for i, l := range lines {
			trimmed := strings.TrimSpace(l)
			if trimmed == "" {
				continue
			}
			out.WriteString(fmt.Sprintf("- %s\n", trimmed))
			if i > 3 { // limitar a 4 bullets
				break
			}
		}
		return out.String()
	case "medium":
		return strings.Join(lines[:min(2, len(lines))], ". ") + "."
	default:
		return lines[0] + "."
	}
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
