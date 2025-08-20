# Herramienta de Evaluación de Respuestas RAG

Esta herramienta ayuda a evaluar las respuestas de un sistema RAG (Generación Aumentada por Recuperación) comparándolas con respuestas de referencia predefinidas utilizando múltiples métricas de puntuación. Automatiza el proceso de envío de consultas a través de una interfaz web y genera informes de evaluación completos.

## Características

- Automatización web usando Playwright para interactuar con la interfaz del sistema RAG
- Múltiples métricas de puntuación (ver guía detallada abajo):
  - Similitud de Coseno (usando TF-IDF)
  - Puntuación ROUGE-L
  - Coincidencia Exacta
  - Puntuación F1 de Tokens
  - Puntuación METEOR
- Arquitectura modular para fácil adición de nuevos métodos de puntuación
- Entrada y salida basada en CSV para fácil gestión de datos
- Informes de evaluación detallados con múltiples métricas
- Soporte para idioma español con tokenización y stemming adecuados

## Guía de Métodos de Puntuación

Esta sección proporciona información detallada sobre cada método de puntuación disponible en la herramienta de evaluación. Comprender estas métricas te ayudará a interpretar los resultados y elegir el enfoque de evaluación más adecuado para tu sistema RAG.

### 1. Similitud de Coseno (`cosine_similarity`)

**Propósito**: Mide la similitud semántica entre textos usando vectorización TF-IDF.

**Cómo funciona**:
- Convierte ambos textos (referencia y candidato) en vectores TF-IDF
- Calcula el coseno del ángulo entre estos vectores
- Usa tokenización y stemming en español para mayor precisión

**Rango de Puntuación**: 0.0 a 1.0
- **1.0**: Similitud semántica perfecta
- **0.8-0.9**: Alta similitud, probablemente buena coincidencia
- **0.6-0.7**: Similitud moderada, coincidencia parcial
- **0.3-0.5**: Baja similitud, contenido diferente
- **0.0-0.2**: Muy baja similitud, contenido no relacionado

**Mejor para**: Evaluar cercanía semántica cuando no se requiere coincidencia exacta de palabras.

**Limitaciones**:
- El TF-IDF se calcula solo sobre los dos documentos comparados, limitando la efectividad del IDF
- Puede no capturar relaciones semánticas complejas

### 2. Puntuación ROUGE-L (`rouge_l_score`)

**Propósito**: Mide la subsecuencia común más larga (LCS) entre los textos de referencia y candidato.

**Cómo funciona**:
- Encuentra la subsecuencia común más larga de palabras entre los textos
- Calcula la medida F basada en precisión y recall de la LCS
- Usa stemming en español para manejar variaciones de palabras

**Rango de Puntuación**: 0.0 a 1.0
- **1.0**: Coincidencia perfecta en orden y contenido
- **0.8-0.9**: Excelente solapamiento y buen orden de palabras
- **0.6-0.7**: Buen solapamiento, algunas diferencias en el orden
- **0.4-0.5**: Solapamiento moderado, diferencias significativas
- **0.0-0.3**: Poco solapamiento, contenido muy diferente

**Mejor para**: Evaluar fluidez y preservación del orden de palabras, especialmente importante para resúmenes.

**Limitaciones**:
- Se enfoca en el orden de palabras, puede penalizar respuestas semánticamente correctas pero estructuradas de forma diferente
- Menos efectivo para textos cortos

### 3. Coincidencia Exacta (`exact_match`)

**Propósito**: Verifica si los textos son idénticos tras la normalización.

**Cómo funciona**:
- Normaliza ambos textos (minúsculas, elimina acentos, espacios)
- Devuelve 1.0 si los textos coinciden exactamente, 0.0 en caso contrario

**Rango de Puntuación**: Binario (0.0 o 1.0)
- **1.0**: Coincidencia perfecta tras normalización
- **0.0**: Cualquier diferencia en el contenido

**Mejor para**:
- Preguntas fácticas con una sola respuesta correcta
- Evaluar precisión en recuperación de información específica
- Control de calidad para información crítica

**Limitaciones**:
- Muy estricto, no considera parafraseo o sinónimos
- No apto para preguntas abiertas

### 4. Puntuación F1 de Tokens (`token_f1`)

**Propósito**: Mide el solapamiento a nivel de palabras usando precisión y recall.

**Cómo funciona**:
- Tokeniza ambos textos en palabras individuales
- Calcula precisión (tokens comunes / tokens del candidato)
- Calcula recall (tokens comunes / tokens de referencia)
- Calcula F1 como media armónica de precisión y recall

**Rango de Puntuación**: 0.0 a 1.0
- **1.0**: Solapamiento perfecto de palabras
- **0.8-0.9**: Alto solapamiento, respuesta completa
- **0.6-0.7**: Buen solapamiento, contenido mayormente correcto
- **0.4-0.5**: Solapamiento moderado, faltan términos clave
- **0.0-0.3**: Poco solapamiento, vocabulario muy diferente

**Mejor para**:
- Evaluar cobertura de vocabulario
- Medir completitud de la información
- Balancear precisión y recall en la evaluación de contenido

**Limitaciones**:
- No considera el orden de palabras ni relaciones semánticas
- Trata todas las palabras por igual, sin importar su importancia

### 5. Puntuación METEOR (`meteor_score`)

**Propósito**: Métrica avanzada que considera coincidencias por raíz y orden de palabras.

**Cómo funciona**:
- Coincide palabras por raíz (maneja variaciones)
- Considera el orden de palabras mediante alineación
- Penaliza diferencias en el orden
- Usa stemming en español para mayor precisión

**Rango de Puntuación**: 0.0 a 1.0
- **1.0**: Coincidencia perfecta con orden óptimo
- **0.8-0.9**: Excelente contenido y buena estructura
- **0.6-0.7**: Buen contenido, algunas diferencias estructurales
- **0.4-0.5**: Coincidencia moderada, diferencias notables
- **0.0-0.3**: Coincidencia pobre, contenido o estructura muy diferente

**Mejor para**:
- Evaluación integral considerando contenido y estructura
- Manejo de variaciones de palabras mediante stemming
- Evaluación más matizada que el simple solapamiento de palabras

**Limitaciones**:
- La coincidencia de sinónimos de WordNet no funciona para español (usa coincidencia por raíz)
- Más compleja y computacionalmente intensiva

## Guía de Interpretación

### Combinaciones de Puntuaciones
- **Puntuaciones altas en todas las métricas**: Excelente calidad de respuesta
- **Alta Coseno + ROUGE, baja Coincidencia Exacta**: Buena coincidencia semántica con diferente redacción
- **Alta F1 de Tokens, baja ROUGE**: Buen vocabulario pero mal orden de palabras
- **Alta Coincidencia Exacta, otras variables**: Precisión fáctica perfecta con presentación variable

### Elección de Métricas según el Caso de Uso

**Para preguntas fácticas**: Priorizar Coincidencia Exacta y F1 de Tokens
**Para resúmenes**: Enfocarse en ROUGE-L y METEOR
**Para búsqueda semántica**: Enfatizar Similitud de Coseno y METEOR
**Para evaluación integral**: Usar todas las métricas y analizar patrones

### Recomendaciones de Umbrales
- **Excelente**: Puntuación media > 0.8
- **Bueno**: Puntuación media 0.6-0.8
- **Aceptable**: Puntuación media 0.4-0.6
- **Pobre**: Puntuación media < 0.4

Recuerda que el umbral ideal depende de tu caso de uso, dominio y requisitos de calidad.

## Instalación

1. Clona este repositorio:
```bash
git clone <repository-url>
cd rag_evaluation
```

2. Crea un entorno virtual y actívalo:
```bash
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
```

3. Instala los paquetes requeridos:
```bash
pip install -r requirements.txt
```

4. Instala los navegadores de Playwright:
```bash
playwright install
```

## Uso

1. Prepara tu archivo CSV de entrada con consultas y respuestas de referencia. El archivo debe tener dos columnas:
   - `query`: La pregunta a realizar
   - `ground_truth`: La respuesta esperada

   Ejemplo:
   ```csv
   query,ground_truth
   "¿Cuál es la capital de Francia?","París es la ciudad capital de Francia."
   ```

2. Ejecuta el script de evaluación:
```bash
python main.py --url "https://tu-sistema-rag.com" \
               --input "data/queries.csv" \
               --output "data/results.csv" \
               --input-selector "#query-input" \
               --submit-selector "#submit-button"
```
```bash
python main.py --url "http://localhost:8000/" --input "data/sample_queries.csv" --output "data/results.csv" --input-selector "#query-input" --submit-selector "#submit-button"
```

### Argumentos de Línea de Comandos

- `--url`: URL de la interfaz web del sistema RAG
- `--input`: Ruta al archivo CSV de entrada con consultas y respuestas de referencia
- `--output`: Ruta donde guardar el CSV de resultados
- `--input-selector`: Selector CSS para el campo de entrada de consulta
- `--submit-selector`: Selector CSS para el botón de envío

## Añadir Nuevos Métodos de Puntuación

Para añadir un nuevo método de puntuación:

1. Crea una nueva clase en `src/scorers/scorers.py` que herede de `BaseScorer`
2. Implementa los métodos requeridos:
   - `calculate_score(self, reference: str, candidate: str) -> float`
   - `get_score_name(self) -> str`

Ejemplo:
```python
from .base_scorer import BaseScorer

class MiNuevoScorer(BaseScorer):
    def calculate_score(self, reference: str, candidate: str) -> float:
        """
        Calcula tu puntuación personalizada entre referencia y candidato.
        
        Args:
            reference: Texto de referencia
            candidate: Texto de respuesta generada
            
        Returns:
            float: Puntuación entre 0.0 y 1.0
        """
        # Implementa tu lógica aquí
        if not reference or not candidate:
            return 0.0
        score = len(set(reference) & set(candidate)) / len(set(reference) | set(candidate))
        return score

    def get_score_name(self) -> str:
        return "mi_nueva_puntuacion"
```

3. Añade tu scorer al gestor de evaluación. La implementación actual incluye todos los scorers disponibles por defecto.

### Buenas Prácticas para Scorers Personalizados

- **Devuelve puntuaciones normalizadas**: Siempre valores entre 0.0 y 1.0
- **Maneja casos límite**: Verifica cadenas vacías, valores None, etc.
- **Documenta limitaciones**: Añade docstrings claros explicando cuándo usar tu scorer
- **Considera el idioma**: Si trabajas con texto en español, usa tokenización adecuada
- **Rendimiento**: Cachea operaciones costosas si el scorer se usará repetidamente

## Formato de Salida

La herramienta genera un archivo CSV con las siguientes columnas:
- Columnas originales del archivo de entrada (`query`, `ground_truth`)
- `actual_response`: La respuesta recibida del sistema RAG
- Columnas de puntuación individual:
  - `cosine_similarity`: Similitud semántica basada en TF-IDF (0.0-1.0)
  - `rouge_l_score`: Medida F ROUGE-L para solapamiento de texto (0.0-1.0)
  - `exact_match`: Coincidencia exacta tras normalización (0.0 o 1.0)
  - `token_f1`: Puntuación F1 a nivel de tokens (0.0-1.0)
  - `meteor_score`: Puntuación METEOR con stemming en español (0.0-1.0)
- `average_score`: Promedio de todas las métricas

### Ejemplo de Salida

```csv
query,ground_truth,actual_response,cosine_similarity,rouge_l_score,exact_match,token_f1,meteor_score,average_score
"¿Cuál es la capital de Francia?","París","París es la ciudad capital de Francia.",0.85,0.92,0.0,0.75,0.88,0.68
```

### Análisis de Resultados

- **Métricas individuales**: Usa puntuaciones específicas para entender diferentes aspectos de la calidad de la respuesta
- **Puntuación promedio**: Proporciona una evaluación general, pero considera las métricas individuales para un análisis detallado
- **Patrones**: Busca fortalezas/debilidades consistentes en diferentes tipos de consultas
- **Atípicos**: Investiga casos donde las métricas difieren significativamente

## Contribuir

1. Haz un fork del repositorio
2. Crea una rama de funcionalidad
3. Haz commit de tus cambios
4. Haz push a la rama
5. Crea un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.
