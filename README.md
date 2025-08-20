# RAG Response Evaluation Tool

This tool helps evaluate responses from a RAG (Retrieval-Augmented Generation) system by comparing them against predefined ground truth answers using multiple scoring metrics. It automates the process of sending queries through a web interface and generates comprehensive evaluation reports.

## Features

- Web automation using Playwright for interacting with RAG system UI
- Multiple scoring metrics (see detailed guide below):
  - Cosine Similarity (using TF-IDF)
  - ROUGE-L Score
  - Exact Match
  - Token F1 Score
  - METEOR Score
- Modular architecture for easy addition of new scoring methods
- CSV-based input and output for easy data management
- Detailed evaluation reports with multiple metrics
- Spanish language support with proper tokenization and stemming

## Scoring Methods Guide

This section provides detailed information about each scoring method available in the evaluation tool. Understanding these metrics will help you interpret the results and choose the most appropriate evaluation approach for your RAG system.

### 1. Cosine Similarity (`cosine_similarity`)

**Purpose**: Measures semantic similarity between texts using TF-IDF vectorization.

**How it works**: 
- Converts both reference and candidate texts into TF-IDF vectors
- Calculates the cosine of the angle between these vectors
- Uses Spanish tokenization and stemming for better language-specific accuracy

**Score Range**: 0.0 to 1.0
- **1.0**: Perfect semantic similarity
- **0.8-0.9**: High similarity, likely good match
- **0.6-0.7**: Moderate similarity, partial match
- **0.3-0.5**: Low similarity, different content
- **0.0-0.2**: Very low similarity, unrelated content

**Best for**: Evaluating semantic closeness when exact wording isn't required.

**Limitations**: 
- TF-IDF is calculated only on the two documents being compared, limiting IDF effectiveness
- May not capture complex semantic relationships

### 2. ROUGE-L Score (`rouge_l_score`)

**Purpose**: Measures longest common subsequence (LCS) between reference and candidate texts.

**How it works**:
- Finds the longest common subsequence of words between texts
- Calculates F-measure based on precision and recall of the LCS
- Uses Spanish stemming to handle word variations

**Score Range**: 0.0 to 1.0
- **1.0**: Perfect word order and content match
- **0.8-0.9**: Excellent overlap with good word order preservation
- **0.6-0.7**: Good overlap, some word order differences
- **0.4-0.5**: Moderate overlap, significant differences
- **0.0-0.3**: Poor overlap, very different content

**Best for**: Evaluating fluency and word order preservation, especially important for summaries.

**Limitations**: 
- Focuses on word order, may penalize semantically correct but differently structured answers
- Less effective for short texts

### 3. Exact Match (`exact_match`)

**Purpose**: Checks if texts are identical after normalization.

**How it works**:
- Normalizes both texts (lowercase, removes accents, strips whitespace)
- Returns 1.0 if texts match exactly, 0.0 otherwise

**Score Range**: Binary (0.0 or 1.0)
- **1.0**: Perfect match after normalization
- **0.0**: Any difference in content

**Best for**: 
- Factual questions with single correct answers
- Evaluating precision in specific information retrieval
- Quality control for critical information

**Limitations**: 
- Very strict, doesn't account for paraphrasing or synonyms
- Not suitable for open-ended questions

### 4. Token F1 Score (`token_f1`)

**Purpose**: Measures word-level overlap using precision and recall.

**How it works**:
- Tokenizes both texts into individual words
- Calculates precision (common tokens / candidate tokens)
- Calculates recall (common tokens / reference tokens)
- Computes F1 score as harmonic mean of precision and recall

**Score Range**: 0.0 to 1.0
- **1.0**: Perfect word overlap
- **0.8-0.9**: High word overlap, comprehensive answer
- **0.6-0.7**: Good word overlap, mostly correct content
- **0.4-0.5**: Moderate overlap, missing some key terms
- **0.0-0.3**: Poor overlap, significantly different vocabulary

**Best for**: 
- Evaluating vocabulary coverage
- Measuring information completeness
- Balancing precision and recall in content evaluation

**Limitations**: 
- Doesn't consider word order or semantic relationships
- Treats all words equally regardless of importance

### 5. METEOR Score (`meteor_score`)

**Purpose**: Advanced metric considering stemmed matches and word order.

**How it works**:
- Matches words based on stems (handles word variations)
- Considers word order through alignment
- Penalizes differences in word order
- Uses Spanish stemming for language-specific accuracy

**Score Range**: 0.0 to 1.0
- **1.0**: Perfect match with optimal word order
- **0.8-0.9**: Excellent content with good structure
- **0.6-0.7**: Good content, some structural differences
- **0.4-0.5**: Moderate match, notable differences
- **0.0-0.3**: Poor match, very different content or structure

**Best for**: 
- Comprehensive evaluation considering both content and structure
- Handling word variations through stemming
- More nuanced evaluation than simple word overlap

**Limitations**: 
- WordNet synonym matching doesn't work for Spanish (falls back to stem matching)
- More complex and computationally intensive

## Interpretation Guidelines

### Score Combinations
- **High scores across all metrics**: Excellent response quality
- **High Cosine + ROUGE, low Exact Match**: Good semantic match with different wording
- **High Token F1, low ROUGE**: Good vocabulary but poor word order
- **High Exact Match, others varying**: Perfect factual accuracy with varying presentation

### Choosing Metrics for Your Use Case

**For Factual Q&A**: Prioritize Exact Match and Token F1
**For Summarization**: Focus on ROUGE-L and METEOR
**For Semantic Search**: Emphasize Cosine Similarity and METEOR
**For Comprehensive Evaluation**: Use all metrics and analyze patterns

### Threshold Recommendations
- **Excellent**: Average score > 0.8
- **Good**: Average score 0.6-0.8
- **Acceptable**: Average score 0.4-0.6
- **Poor**: Average score < 0.4

Remember that the ideal threshold depends on your specific use case, domain, and quality requirements.

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
        """
        Calculate your custom score between reference and candidate.
        
        Args:
            reference: Ground truth text
            candidate: Generated response text
            
        Returns:
            float: Score between 0.0 and 1.0
        """
        # Implement your scoring logic here
        # Example: Simple character-based similarity
        if not reference or not candidate:
            return 0.0
        
        # Your custom logic here
        score = len(set(reference) & set(candidate)) / len(set(reference) | set(candidate))
        return score

    def get_score_name(self) -> str:
        return "my_new_score"
```

3. Add your scorer to the evaluation manager. The current implementation includes all available scorers by default.

### Best Practices for Custom Scorers

- **Return normalized scores**: Always return values between 0.0 and 1.0
- **Handle edge cases**: Check for empty strings, None values, etc.
- **Document limitations**: Add clear docstrings explaining when to use your scorer
- **Consider language**: If working with Spanish text, use appropriate tokenization
- **Performance**: Cache expensive operations if the scorer will be used repeatedly

## Output Format

The tool generates a CSV file with the following columns:
- Original columns from input file (`query`, `ground_truth`)
- `actual_response`: The response received from the RAG system
- Individual score columns:
  - `cosine_similarity`: TF-IDF based semantic similarity (0.0-1.0)
  - `rouge_l_score`: ROUGE-L F-measure for text overlap (0.0-1.0)
  - `exact_match`: Binary exact match after normalization (0.0 or 1.0)
  - `token_f1`: Token-level F1 score (0.0-1.0)
  - `meteor_score`: METEOR score with Spanish stemming (0.0-1.0)
- `average_score`: Average of all scoring metrics

### Example Output

```csv
query,ground_truth,actual_response,cosine_similarity,rouge_l_score,exact_match,token_f1,meteor_score,average_score
"What is the capital of France?","Paris","Paris is the capital city of France.",0.85,0.92,0.0,0.75,0.88,0.68
```

### Analyzing Results

- **Individual Metrics**: Use specific scores to understand different aspects of response quality
- **Average Score**: Provides overall assessment but consider individual metrics for detailed analysis
- **Patterns**: Look for consistent strengths/weaknesses across different types of queries
- **Outliers**: Investigate cases where metrics disagree significantly

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
