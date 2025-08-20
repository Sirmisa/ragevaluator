import pandas as pd
from typing import List, Dict, Any
from .scorers.base_scorer import BaseScorer

class EvaluationManager:
    """Class to manage the evaluation process and generate reports."""
    
    def __init__(self, scorers: List[BaseScorer]):
        """
        Initialize the evaluation manager.
        
        Args:
            scorers (List[BaseScorer]): List of scoring methods to use
        """
        self.scorers = scorers

    def evaluate_response(self, reference: str, candidate: str) -> Dict[str, float]:
        """
        Evaluate a single response using all scoring methods.
        
        Args:
            reference (str): The ground truth text
            candidate (str): The text to evaluate
            
        Returns:
            Dict[str, float]: Dictionary mapping score names to values
        """
        results = {}
        for scorer in self.scorers:
            score = scorer.calculate_score(reference, candidate)
            results[scorer.get_score_name()] = score
        return results

    def update_csv(self, input_file: str, output_file: str, responses: Dict[str, str]) -> None:
        """
        Update CSV file with responses and scores.
        
        Args:
            input_file (str): Path to input CSV with ground truth
            output_file (str): Path where to save the results
            responses (Dict[str, str]): Dictionary mapping queries to responses
        """
        # Read the ground truth CSV
        df = pd.read_csv(input_file)
        
        # Add responses column
        df['actual_response'] = df['query'].map(responses)
        
        # Calculate scores for each scoring method
        for scorer in self.scorers:
            score_name = scorer.get_score_name()
            df[score_name] = df.apply(
                lambda row: scorer.calculate_score(row['ground_truth'], row['actual_response'])
                if pd.notnull(row['actual_response']) else None,
                axis=1
            )
        
        # Calculate average scores
        score_columns = [scorer.get_score_name() for scorer in self.scorers]
        df['average_score'] = df[score_columns].mean(axis=1)
        
        # Save to new CSV
        df.to_csv(output_file, index=False)
