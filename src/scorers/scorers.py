from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from .base_scorer import BaseScorer

class CosineScorer(BaseScorer):
    """Scorer that uses cosine similarity with TF-IDF vectors."""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def calculate_score(self, reference: str, candidate: str) -> float:
        """Calculate cosine similarity between reference and candidate texts."""
        # Fit and transform the texts to TF-IDF vectors
        tfidf_matrix = self.vectorizer.fit_transform([reference, candidate])
        return float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])

    def get_score_name(self) -> str:
        return "cosine_similarity"


class BleuScorer(BaseScorer):
    """Scorer that uses BLEU score."""
    
    def __init__(self):
        self.smoothing = SmoothingFunction().method1

    def calculate_score(self, reference: str, candidate: str) -> float:
        """Calculate BLEU score between reference and candidate texts."""
        reference_tokens = reference.split()
        candidate_tokens = candidate.split()
        return sentence_bleu([reference_tokens], candidate_tokens, 
                           smoothing_function=self.smoothing)

    def get_score_name(self) -> str:
        return "bleu_score"


class RougeScorer(BaseScorer):
    """Scorer that uses ROUGE-L score."""
    
    def __init__(self):
        self.scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)

    def calculate_score(self, reference: str, candidate: str) -> float:
        """Calculate ROUGE-L score between reference and candidate texts."""
        scores = self.scorer.score(reference, candidate)
        return scores['rougeL'].fmeasure

    def get_score_name(self) -> str:
        return "rouge_l_score"
