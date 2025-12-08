"""Get actual vscode statistics"""
from commit_analyzer import CommitFetcher
from sentiment_analyzer import SentimentAnalyzer
import pandas as pd

print("Starting analysis...")
fetcher = CommitFetcher('microsoft', 'vscode')
commits = fetcher.fetch_commits(limit=200)
print(f"Fetched {len(commits)} commits")

analyzer = SentimentAnalyzer()
df = analyzer.analyze_commits(commits)
summary = analyzer.get_summary(df)

min_score = float(df['compound'].min())
max_score = float(df['compound'].max())
std_dev = float(df['compound'].std())
median_score = float(df['compound'].median())
pn_ratio = summary['positive_count'] / summary['negative_count'] if summary['negative_count'] > 0 else 0

results = f"""VSCODE_ACTUAL_RESULTS
{'='*70}
Repository: microsoft/vscode
Total Commits: {summary['total_commits']}

Sentiment Distribution:
  Positive: {summary['positive_count']} ({summary['positive_percentage']:.1f}%)
  Neutral:  {summary['neutral_count']} ({summary['neutral_percentage']:.1f}%)
  Negative: {summary['negative_count']} ({summary['negative_percentage']:.1f}%)

Score Statistics:
  Average: {summary['average_compound']:.3f}
  Median:  {median_score:.3f}
  Min:     {min_score:.3f}
  Max:     {max_score:.3f}
  Std Dev: {std_dev:.3f}
  P/N Ratio: {pn_ratio:.2f}:1
{'='*70}
"""

print(results)

with open('VSCODE_ACTUAL_RESULTS.txt', 'w') as f:
    f.write(results)

print("\nResults saved to VSCODE_ACTUAL_RESULTS.txt")

