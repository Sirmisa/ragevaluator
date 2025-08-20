from src.web_interface import WebInterface
from src.evaluation_manager import EvaluationManager
from src.scorers.scorers import CosineScorer, RougeScorer, ExactMatchScorer, F1Scorer, MeteorScorer
import pandas as pd
import argparse
from typing import List, Dict

def load_queries(input_file: str) -> List[str]:
    """
    Load queries from CSV file.
    
    Args:
        input_file (str): Path to CSV file containing queries
        
    Returns:
        List[str]: List of queries to evaluate
    """
    df = pd.read_csv(input_file)
    return df['query'].tolist()

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Evaluate RAG system responses')
    parser.add_argument('--url', required=True, help='URL of the RAG system web interface')
    parser.add_argument('--input', required=True, help='Input CSV file with queries and ground truth')
    parser.add_argument('--output', required=True, help='Output CSV file for results')
    parser.add_argument('--input-selector', required=True, help='CSS selector for input field')
    parser.add_argument('--submit-selector', required=True, help='CSS selector for submit button')
    args = parser.parse_args()

    # Initialize components
    web_interface = WebInterface(args.url)
    scorers = [CosineScorer(), RougeScorer(), ExactMatchScorer(), F1Scorer(), MeteorScorer()]
    evaluator = EvaluationManager(scorers)

    try:
        # Start the web interface
        web_interface.start()

        # Load queries
        queries = load_queries(args.input)

        # Collect responses
        responses: Dict[str, str] = {}
        for query in queries:
            response = web_interface.send_query(
                query, 
                args.input_selector,
                args.submit_selector
            )
            if response:
                responses[query] = response
            else:
                print(f"Warning: No response received for query: {query}")

        # Update CSV with responses and scores
        evaluator.update_csv(args.input, args.output, responses)
        print(f"Evaluation complete. Results saved to {args.output}")

    finally:
        # Cleanup
        web_interface.close()

if __name__ == "__main__":
    main()
