"""
Quick script to show commit data fetched from GitHub
"""

from commit_analyzer import CommitFetcher
from sentiment_analyzer import SentimentAnalyzer
import sys

if len(sys.argv) < 3:
    print("Usage: python show_commits.py <owner> <repo> [limit]")
    print("Example: python show_commits.py facebook react 10")
    sys.exit(1)

owner = sys.argv[1]
repo = sys.argv[2]
limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10

print(f"\n{'='*80}")
print(f"COMMIT MESSAGES FROM: {owner}/{repo}")
print(f"{'='*80}\n")

# Fetch commits
fetcher = CommitFetcher(owner, repo)
commits = fetcher.fetch_commits(limit=limit)

if not commits:
    print("No commits found!")
    sys.exit(1)

# Analyze sentiment
analyzer = SentimentAnalyzer()

print(f"{'SHA':<10} {'Sentiment':<12} {'Score':<8} {'Message'}")
print("-" * 80)

for commit in commits:
    sentiment_data = analyzer.analyze_message(commit['message'])
    sha = commit['sha']
    message = commit['message'].split('\n')[0][:60]  # First line, max 60 chars
    sentiment = sentiment_data['sentiment']
    score = sentiment_data['compound']
    
    # Color coding (simple text indicators)
    sentiment_icon = {
        'positive': '😊',
        'negative': '😞',
        'neutral': '😐'
    }.get(sentiment, '❓')
    
    print(f"{sha:<10} {sentiment_icon} {sentiment:<10} {score:>6.3f}  {message}")

print("\n" + "="*80)

