from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer
from rouge_score import rouge_scorer
from .base_scorer import BaseScorer

class CosineScorer(BaseScorer):
    """Scorer that uses cosine similarity with TF-IDF vectors."""
    
    def __init__(self):
        self.stemmer = SnowballStemmer('spanish')
        self.vectorizer = TfidfVectorizer(tokenizer=self.stemmed_tokenizer)

    def stemmed_tokenizer(self, text):
        return [self.stemmer.stem(word) for word in text.split()]  # Simple split; use nltk.word_tokenize for better

    def calculate_score(self, reference: str, candidate: str) -> float:
        """Calculate cosine similarity between reference and candidate texts."""
        # Fit and transform the texts to TF-IDF vectors
        tfidf_matrix = self.vectorizer.fit_transform([reference, candidate])
        return float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])

    def get_score_name(self) -> str:
        return "cosine_similarity"

class RougeScorer(BaseScorer):
    """Scorer that uses ROUGE-L score."""
    
    def __init__(self):
        self.stemmer = SnowballStemmer('spanish')
        self.scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=False)  # Disable default

    def calculate_score(self, reference: str, candidate: str) -> float:
        # Apply stemming manually
        ref_stemmed = ' '.join(self.stemmer.stem(w) for w in reference.split())
        cand_stemmed = ' '.join(self.stemmer.stem(w) for w in candidate.split())
        scores = self.scorer.score(ref_stemmed, cand_stemmed)
        return scores['rougeL'].fmeasure
    def get_score_name(self) -> str:
        return "rouge_l_score"
