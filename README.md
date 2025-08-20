# RAG Response Evaluation Tool

This tool helps evaluate responses from a RAG (Retrieval-Augmented Generation) system by comparing them against predefined ground truth answers using multiple scoring metrics. It automates the process of sending queries through a web interface and generates comprehensive evaluation reports.

## Features

- Web automation using Playwright for interacting with RAG system UI
- Multiple scoring metrics:
  - Cosine Similarity (using TF-IDF)
  - ROUGE-L Score
- Modular architecture for easy addition of new scoring methods
- CSV-based input and output for easy data management
- Detailed evaluation reports with multiple metrics

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd rag_evaluation
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

## Usage

1. Prepare your input CSV file with queries and ground truth answers. The file should have two columns:
   - `query`: The question to ask
   - `ground_truth`: The expected answer

   Example:
   ```csv
   query,ground_truth
   "What is the capital of France?","Paris is the capital city of France."
   ```

2. Run the evaluation script:
```bash
python main.py --url "https://your-rag-system.com" \
               --input "data/queries.csv" \
               --output "data/results.csv" \
               --input-selector "#query-input" \
               --submit-selector "#submit-button"
```
```bash
python main.py --url "http://localhost:8000/" --input "data/sample_queries.csv" --output "data/results.csv" --input-selector "#query-input" --submit-selector "#submit-button"
```

### Command Line Arguments

- `--url`: URL of the RAG system's web interface
- `--input`: Path to input CSV file with queries and ground truth
- `--output`: Path where to save the results CSV
- `--input-selector`: CSS selector for the query input field
- `--submit-selector`: CSS selector for the submit button

## Adding New Scoring Methods

To add a new scoring method:

1. Create a new class in `src/scorers/scorers.py` that inherits from `BaseScorer`
2. Implement the required methods:
   - `calculate_score(self, reference: str, candidate: str) -> float`
   - `get_score_name(self) -> str`

Example:
```python
from .base_scorer import BaseScorer

class MyNewScorer(BaseScorer):
    def calculate_score(self, reference: str, candidate: str) -> float:
        # Implement your scoring logic here
        pass

    def get_score_name(self) -> str:
        return "my_new_score"
```

3. Add your scorer to the list in `main.py`:
```python
scorers = [CosineScorer(), RougeScorer(), MyNewScorer()]
```

## Output Format

The tool generates a CSV file with the following columns:
- Original columns from input file (`query`, `ground_truth`)
- `actual_response`: The response received from the RAG system
- Individual score columns (e.g., `cosine_similarity`, `rouge_l_score`)
- `average_score`: Average of all scoring metrics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
