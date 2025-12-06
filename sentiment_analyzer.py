"""
Sentiment Analysis Module
Analyzes commit messages using VaderSentiment.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List
import pandas as pd
from datetime import datetime


class SentimentAnalyzer:
    """Analyzes sentiment of text using VaderSentiment."""
    
    def __init__(self):
        """Initialize the sentiment analyzer."""
        self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze_message(self, message: str) -> Dict:
        """
        Analyze sentiment of a single message.
        
        Args:
            message: Commit message text
            
        Returns:
            Dictionary with sentiment scores and classification
        """
        scores = self.analyzer.polarity_scores(message)
        
        # Classify as positive, negative, or neutral
        compound = scores['compound']
        if compound >= 0.05:
            sentiment = 'positive'
        elif compound <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'compound': compound,
            'positive': scores['pos'],
            'neutral': scores['neu'],
            'negative': scores['neg'],
            'sentiment': sentiment
        }
    
    def analyze_commits(self, commits: List[Dict]) -> pd.DataFrame:
        """
        Analyze sentiment for a list of commits.
        
        Args:
            commits: List of commit dictionaries
            
        Returns:
            DataFrame with commits and their sentiment scores
        """
        results = []
        
        for commit in commits:
            sentiment_data = self.analyze_message(commit['message'])
            
            result = {
                'sha': commit['sha'],
                'message': commit['message'],
                'date': pd.to_datetime(commit['date']),
                'author': commit['author'],
                'compound': sentiment_data['compound'],
                'positive': sentiment_data['positive'],
                'neutral': sentiment_data['neutral'],
                'negative': sentiment_data['negative'],
                'sentiment': sentiment_data['sentiment']
            }
            results.append(result)
        
        df = pd.DataFrame(results)
        return df
    
    def get_summary(self, df: pd.DataFrame) -> Dict:
        """
        Generate summary statistics from sentiment analysis.
        
        Args:
            df: DataFrame with sentiment analysis results
            
        Returns:
            Dictionary with summary statistics
        """
        total = len(df)
        
        summary = {
            'total_commits': total,
            'positive_count': len(df[df['sentiment'] == 'positive']),
            'neutral_count': len(df[df['sentiment'] == 'neutral']),
            'negative_count': len(df[df['sentiment'] == 'negative']),
            'average_compound': df['compound'].mean(),
            'positive_percentage': (len(df[df['sentiment'] == 'positive']) / total * 100) if total > 0 else 0,
            'neutral_percentage': (len(df[df['sentiment'] == 'neutral']) / total * 100) if total > 0 else 0,
            'negative_percentage': (len(df[df['sentiment'] == 'negative']) / total * 100) if total > 0 else 0,
        }
        
        return summary

