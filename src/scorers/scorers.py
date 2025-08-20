from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.translate.meteor_score import meteor_score
from rouge_score import rouge_scorer
import unicodedata
from abc import ABC, abstractmethod

# --- Base Class (for context) ---
class BaseScorer(ABC):
    @abstractmethod
    def calculate_score(self, reference: str, candidate: str) -> float:
        """Calculates a score between a reference and candidate string."""
        pass

    @abstractmethod
    def get_score_name(self) -> str:
        """Returns the name of the score."""
        pass

# --- Helper Function for Standardized Tokenization & Stemming ---
def _tokenize_and_stem(text: str, stemmer: SnowballStemmer) -> List[str]:
    """
    Tokenizes text using NLTK's robust tokenizer, converts to lowercase,
    and applies a provided stemmer.
    """
    tokens = word_tokenize(text.lower(), language='spanish')
    return [stemmer.stem(token) for token in tokens]

# --- Corrected Scorer Classes ---

class CosineScorer(BaseScorer):
    """
    Scorer that uses cosine similarity with TF-IDF vectors.

    NOTE: This scorer calculates TF-IDF based ONLY on the two documents
    being compared (reference and candidate). This makes it easy to use but
    limits the effectiveness of the IDF component, as it can't assess
    word rarity against a larger corpus. The score will heavily reflect
    term frequency (TF) overlap.
    """
    def __init__(self):
        self.stemmer = SnowballStemmer('spanish')
        # The tokenizer is now defined as an inner function for encapsulation
        def stemmed_tokenizer(text):
            tokens = word_tokenize(text.lower(), language='spanish')
            return [self.stemmer.stem(token) for token in tokens]
        
        self.vectorizer = TfidfVectorizer(tokenizer=stemmed_tokenizer)

    def calculate_score(self, reference: str, candidate: str) -> float:
        """Calculate cosine similarity by fitting the vectorizer on the fly."""
        # Fit and transform the texts to TF-IDF vectors for just these two docs
        try:
            tfidf_matrix = self.vectorizer.fit_transform([reference, candidate])
            return float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
        except ValueError:
            # This can happen if both texts are empty after processing stop words, etc.
            return 0.0

    def get_score_name(self) -> str:
        return "cosine_similarity"


class RougeScorer(BaseScorer):
    """Scorer that uses ROUGE-L F-measure with Spanish stemming."""
    def __init__(self):
        self.stemmer = SnowballStemmer('spanish')
        # Disable the default English stemmer to apply our own
        self.scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=False)

    def calculate_score(self, reference: str, candidate: str) -> float:
        # Pre-process text with robust tokenization and Spanish stemming
        ref_processed = ' '.join(_tokenize_and_stem(reference, self.stemmer))
        cand_processed = ' '.join(_tokenize_and_stem(candidate, self.stemmer))
        scores = self.scorer.score(ref_processed, cand_processed)
        return scores['rougeL'].fmeasure

    def get_score_name(self) -> str:
        return "rouge_l_score"

class ExactMatchScorer(BaseScorer):
    """Scorer that checks for exact match after robust normalization."""
    def calculate_score(self, reference: str, candidate: str) -> float:
        def normalize(text: str) -> str:
            """Lowercase, remove accents, and strip whitespace."""
            return unicodedata.normalize('NFD', text.lower())\
                              .encode('ascii', 'ignore')\
                              .decode('utf-8').strip()
        return 1.0 if normalize(reference) == normalize(candidate) else 0.0

    def get_score_name(self) -> str:
        return "exact_match"

class F1Scorer(BaseScorer):
    """Calculates a token-level F1 score based on word overlap."""
    def calculate_score(self, reference: str, candidate: str) -> float:
        ref_tokens = set(word_tokenize(reference.lower(), language='spanish'))
        cand_tokens = set(word_tokenize(candidate.lower(), language='spanish'))
        
        if not ref_tokens or not cand_tokens:
            return 0.0
            
        common_tokens = ref_tokens.intersection(cand_tokens)
        
        precision = len(common_tokens) / len(cand_tokens)
        recall = len(common_tokens) / len(ref_tokens)
        
        if precision + recall == 0:
            return 0.0
            
        f1 = 2 * (precision * recall) / (precision + recall)
        return f1

    def get_score_name(self) -> str:
        return "token_f1"

class MeteorScorer(BaseScorer):
    """
    Scorer that uses the METEOR score.
    
    NOTE: NLTK's METEOR implementation relies on the English WordNet for synonym
    matching. This feature will not work for Spanish, so the score will primarily
    be based on stemmed word matches and word order.
    """
    def __init__(self):
        self.stemmer = SnowballStemmer('spanish')

    def calculate_score(self, reference: str, candidate:str) -> float:
        ref_tokens = _tokenize_and_stem(reference, self.stemmer)
        cand_tokens = _tokenize_and_stem(candidate, self.stemmer)
        
        # meteor_score expects a list of reference token lists
        return meteor_score([ref_tokens], cand_tokens)

    def get_score_name(self) -> str:
        return "meteor_score"