"""
Check the REAL number of commits being fetched and visualized
"""
import sys
from commit_analyzer import CommitFetcher
from sentiment_analyzer import SentimentAnalyzer
from visualizer import SentimentVisualizer
import pandas as pd

print("="*70)
print("CHECKING REAL COMMIT COUNT")
print("="*70)

# Fetch
print("\nFetching commits...")
fetcher = CommitFetcher('facebook', 'react')
commits = fetcher.fetch_commits(limit=200)

print(f"\n✓ ACTUAL commits fetched from API: {len(commits)}")
print(f"  (Requested: 200)")

if len(commits) < 200:
    print(f"\n⚠ ISSUE FOUND: Only {len(commits)} commits were fetched!")
    print(f"  Possible reasons:")
    print(f"  1. GitHub API rate limiting")
    print(f"  2. Repository doesn't have 200 recent commits")
    print(f"  3. Pagination stopped early")

# Analyze
analyzer = SentimentAnalyzer()
df = analyzer.analyze_commits(commits)

print(f"\n✓ Commits in DataFrame: {len(df)}")

# Check daily counts (what visualization shows)
df_sorted = df.sort_values('date').copy()
df_sorted['date_only'] = df_sorted['date'].dt.date
daily_sentiment = df_sorted.groupby(['date_only', 'sentiment']).size().unstack(fill_value=0)
daily_totals = daily_sentiment.sum(axis=1)

print(f"\n✓ Daily commit totals (what bottom chart shows):")
print(f"  Sum of all daily counts: {daily_totals.sum()}")
print(f"  Number of days: {len(daily_totals)}")

# Count scatter points (what top chart shows)
print(f"\n✓ Scatter plot points (what top chart shows):")
print(f"  Number of data points: {len(df_sorted)}")

print("\n" + "="*70)
print("CONCLUSION:")
if len(commits) == 200 and len(df) == 200:
    print("✓ 200 commits were fetched and analyzed")
    print("  If visualization shows fewer, it's a display issue")
elif len(commits) < 200:
    print(f"⚠ Only {len(commits)} commits were actually fetched")
    print("  This explains why visualization shows fewer commits")
    print("  Need to investigate why API didn't return 200 commits")
print("="*70)

# Save to file
with open('REAL_COUNT.txt', 'w') as f:
    f.write(f"REAL COMMIT COUNT CHECK\n")
    f.write("="*70 + "\n\n")
    f.write(f"Commits fetched from API: {len(commits)}\n")
    f.write(f"Commits in DataFrame: {len(df)}\n")
    f.write(f"Sum of daily counts: {daily_totals.sum()}\n")
    f.write(f"Scatter plot points: {len(df_sorted)}\n")

print("\n✓ Results saved to REAL_COUNT.txt")
