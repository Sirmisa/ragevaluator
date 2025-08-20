from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseScorer(ABC):
    """Abstract base class for implementing different scoring metrics."""
    
    @abstractmethod
    def calculate_score(self, reference: str, candidate: str) -> float:
        """
        Calculate the similarity score between reference and candidate texts.
        
        Args:
            reference (str): The ground truth text
            candidate (str): The text to evaluate
            
        Returns:
            float: Similarity score between 0 and 1
        """
        pass

    @abstractmethod
    def get_score_name(self) -> str:
        """
        Get the name of the scoring metric.
        
        Returns:
            str: Name of the scoring metric
        """
        pass

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get additional metadata about the scoring method.
        
        Returns:
            Dict[str, Any]: Dictionary containing metadata about the scoring method
        """
        return {
            "name": self.get_score_name(),
            "type": self.__class__.__name__
        }
