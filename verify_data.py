"""
Verify the actual data being used for visualization
"""
from commit_analyzer import CommitFetcher
from sentiment_analyzer import SentimentAnalyzer
import pandas as pd

print("="*70)
print("VERIFYING DATA FOR VISUALIZATION")
print("="*70)

# Fetch and analyze
fetcher = CommitFetcher('facebook', 'react')
commits = fetcher.fetch_commits(limit=200)
analyzer = SentimentAnalyzer()
df = analyzer.analyze_commits(commits)

print(f"\nTotal commits in DataFrame: {len(df)}")
print(f"Expected: 200")

# Check daily grouping (this is what the visualization uses)
df_sorted = df.sort_values('date').copy()
df_sorted['date_only'] = df_sorted['date'].dt.date

# Count by day (this is what the bottom chart uses)
daily_sentiment = df_sorted.groupby(['date_only', 'sentiment']).size().unstack(fill_value=0)
daily_totals = daily_sentiment.sum(axis=1)

print(f"\nDaily grouping results:")
print(f"  Number of days: {len(daily_totals)}")
print(f"  Sum of daily totals: {daily_totals.sum()}")
print(f"  This should equal: {len(df)}")

if daily_totals.sum() != len(df):
    print(f"\n⚠ PROBLEM: Daily sum ({daily_totals.sum()}) doesn't match DataFrame length ({len(df)})")
else:
    print(f"\n✓ Daily grouping is correct")

# Check scatter plot data (top chart)
print(f"\nScatter plot data:")
print(f"  Number of rows in df_sorted: {len(df_sorted)}")
print(f"  Unique dates: {df_sorted['date'].nunique()}")
print(f"  Date range: {df_sorted['date'].min()} to {df_sorted['date'].max()}")

# Show some sample daily counts
print(f"\nSample daily counts (first 10 days):")
for date, count in daily_totals.head(10).items():
    print(f"  {date}: {count} commits")

print(f"\n" + "="*70)
print("If daily_totals.sum() = DataFrame length, visualization should show all commits")
print("="*70)
