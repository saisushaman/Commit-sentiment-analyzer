"""
Regenerate visualizations from the 200-commit analysis
"""
from commit_analyzer import CommitFetcher
from sentiment_analyzer import SentimentAnalyzer
from visualizer import SentimentVisualizer

print("="*70)
print("REGENERATING VISUALIZATIONS WITH 200 COMMITS")
print("="*70)

# Fetch 200 commits
print("\n[1/3] Fetching 200 commits...")
fetcher = CommitFetcher('microsoft', 'vscode')
commits = fetcher.fetch_commits(limit=200)
print(f"    ✓ Fetched {len(commits)} commits")

# Analyze
print("\n[2/3] Analyzing sentiment...")
analyzer = SentimentAnalyzer()
df = analyzer.analyze_commits(commits)
summary = analyzer.get_summary(df)
print(f"    ✓ Analyzed {summary['total_commits']} commits")
print(f"    Positive: {summary['positive_count']} ({summary['positive_percentage']:.1f}%)")
print(f"    Neutral:  {summary['neutral_count']} ({summary['neutral_percentage']:.1f}%)")
print(f"    Negative: {summary['negative_count']} ({summary['negative_percentage']:.1f}%)")

# Generate visualizations
print("\n[3/3] Generating visualizations...")
visualizer = SentimentVisualizer()
visualizer.plot_sentiment_timeline(df, output_file='sentiment_analysis.png')
visualizer.plot_sentiment_distribution(df, output_file='sentiment_distribution.png')
print("    ✓ Visualizations regenerated with 200 commits")

print("\n" + "="*70)
print("VERIFICATION:")
print(f"  Total commits in DataFrame: {len(df)}")
print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
print("="*70)
