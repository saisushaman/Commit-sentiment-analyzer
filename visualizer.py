"""
Visualization Module
Creates charts and graphs for sentiment analysis results.
"""

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from typing import Optional
import numpy as np


class SentimentVisualizer:
    """Creates visualizations for sentiment analysis data."""
    
    def __init__(self, figsize=(12, 6)):
        """
        Initialize the visualizer.
        
        Args:
            figsize: Figure size tuple (width, height)
        """
        self.figsize = figsize
        # Use a compatible matplotlib style
        try:
            plt.style.use('seaborn-v0_8-darkgrid')
        except:
            try:
                plt.style.use('seaborn-darkgrid')
            except:
                plt.style.use('default')
    
    def plot_sentiment_timeline(self, df: pd.DataFrame, output_file: str = 'sentiment_analysis.png'):
        """
        Create a timeline visualization of sentiment trends.
        
        Args:
            df: DataFrame with commit data and sentiment scores
            output_file: Output file path for the chart
        """
        # Sort by date
        df_sorted = df.sort_values('date').copy()
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 1, figsize=self.figsize, sharex=True)
        
        # Plot 1: Sentiment over time (scatter)
        ax1 = axes[0]
        colors = df_sorted['sentiment'].map({
            'positive': 'green',
            'neutral': 'gray',
            'negative': 'red'
        })
        
        scatter = ax1.scatter(
            df_sorted['date'],
            df_sorted['compound'],
            c=colors,
            alpha=0.6,
            s=50
        )
        
        # Add moving average line
        df_sorted['moving_avg'] = df_sorted['compound'].rolling(window=5, min_periods=1).mean()
        ax1.plot(df_sorted['date'], df_sorted['moving_avg'], 'b-', linewidth=2, label='Moving Average (5 commits)')
        
        ax1.axhline(y=0, color='black', linestyle='--', alpha=0.3)
        ax1.set_ylabel('Sentiment Score', fontsize=12)
        ax1.set_title('Commit Message Sentiment Over Time', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Daily sentiment distribution
        ax2 = axes[1]
        df_sorted['date_only'] = df_sorted['date'].dt.date
        
        # Count sentiments per day
        daily_sentiment = df_sorted.groupby(['date_only', 'sentiment']).size().unstack(fill_value=0)
        
        if not daily_sentiment.empty:
            daily_sentiment.plot(kind='area', ax=ax2, stacked=True, 
                                color={'positive': 'green', 'neutral': 'gray', 'negative': 'red'},
                                alpha=0.6)
        
        ax2.set_ylabel('Number of Commits', fontsize=12)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_title('Daily Sentiment Distribution', fontsize=14, fontweight='bold')
        ax2.legend(title='Sentiment', loc='upper left')
        ax2.grid(True, alpha=0.3)
        
        # Format x-axis dates
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Chart saved to: {output_file}")
        plt.close()
    
    def plot_sentiment_distribution(self, df: pd.DataFrame, output_file: str = 'sentiment_distribution.png'):
        """
        Create a pie chart showing sentiment distribution.
        
        Args:
            df: DataFrame with commit data and sentiment scores
            output_file: Output file path for the chart
        """
        sentiment_counts = df['sentiment'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        colors = {'positive': 'green', 'neutral': 'gray', 'negative': 'red'}
        labels = sentiment_counts.index.tolist()
        sizes = sentiment_counts.values.tolist()
        plot_colors = [colors.get(label, 'blue') for label in labels]
        
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            colors=plot_colors,
            startangle=90,
            textprops={'fontsize': 12, 'fontweight': 'bold'}
        )
        
        ax.set_title('Overall Sentiment Distribution', fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Distribution chart saved to: {output_file}")
        plt.close()

