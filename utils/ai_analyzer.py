import spacy
import nltk
from textblob import TextBlob
from typing import Dict, List
import re

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

class AIAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def generate_summary(self, text: str) -> str:
        sentences = nltk.sent_tokenize(text)
        return ' '.join(sentences[:3])  # First 3 sentences
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        doc = self.nlp(text)
        entities = {}
        for ent in doc.ents:
            etype = ent.label_
            if etype not in entities:
                entities[etype] = []
            if ent.text not in entities[etype]:
                entities[etype].append(ent.text)
        return entities
    
    def analyze_sentiment(self, text: str) -> str:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        return 'positive' if polarity > 0.1 else 'negative' if polarity < -0.1 else 'neutral'
    
    def analyze(self, text: str) -> Dict:
        if not text or len(text) < 10:
            return {"summary": "No content", "entities": {}, "sentiment": "neutral", "confidence": 0.5}
        
        summary = self.generate_summary(text)
        entities = self.extract_entities(text)
        sentiment = self.analyze_sentiment(text)
        confidence = 0.8
        
        return {
            "summary": summary,
            "entities": entities,
            "sentiment": sentiment,
            "confidence": confidence
        }