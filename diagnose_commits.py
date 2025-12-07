"""
Diagnostic script to check what's actually being fetched
"""
from commit_analyzer import CommitFetcher
from sentiment_analyzer import SentimentAnalyzer
import pandas as pd

print("="*70)
print("DIAGNOSTIC: Checking Commit Fetching")
print("="*70)

# Fetch commits
print("\n[1] Fetching commits...")
fetcher = CommitFetcher('facebook', 'react')
commits = fetcher.fetch_commits(limit=200)

print(f"\n✓ Raw commits fetched: {len(commits)}")

if len(commits) < 200:
    print(f"⚠ WARNING: Only {len(commits)} commits fetched (requested 200)")

# Analyze
print("\n[2] Analyzing sentiment...")
analyzer = SentimentAnalyzer()
df = analyzer.analyze_commits(commits)

print(f"\n✓ DataFrame length: {len(df)} rows")
print(f"✓ DataFrame columns: {list(df.columns)}")

# Check for duplicates or missing data
print("\n[3] Data Quality Check:")
print(f"  Unique SHAs: {df['sha'].nunique()}")
print(f"  Duplicate SHAs: {len(df) - df['sha'].nunique()}")
print(f"  Missing dates: {df['date'].isna().sum()}")
print(f"  Missing messages: {df['message'].isna().sum()}")

# Date range
print("\n[4] Date Range:")
print(f"  Earliest commit: {df['date'].min()}")
print(f"  Latest commit: {df['date'].max()}")
print(f"  Date span: {(df['date'].max() - df['date'].min()).days} days")

# Daily counts
print("\n[5] Daily Commit Counts:")
df['date_only'] = df['date'].dt.date
daily_counts = df.groupby('date_only').size()
print(f"  Total days with commits: {len(daily_counts)}")
print(f"  Sum of daily counts: {daily_counts.sum()}")
print(f"  Max commits per day: {daily_counts.max()}")
print(f"  Average commits per day: {daily_counts.mean():.1f}")

# Show first few commits
print("\n[6] Sample Commits (first 5):")
for idx, row in df.head(5).iterrows():
    print(f"  {row['sha']}: {row['date'].strftime('%Y-%m-%d')} - {row['message'][:50]}...")

print("\n" + "="*70)
print("DIAGNOSIS COMPLETE")
print("="*70)

# Save detailed info
with open('diagnostic_results.txt', 'w') as f:
    f.write("DIAGNOSTIC RESULTS\n")
    f.write("="*70 + "\n\n")
    f.write(f"Raw commits fetched: {len(commits)}\n")
    f.write(f"DataFrame length: {len(df)}\n")
    f.write(f"Unique SHAs: {df['sha'].nunique()}\n")
    f.write(f"Date range: {df['date'].min()} to {df['date'].max()}\n")
    f.write(f"Total days: {len(daily_counts)}\n")
    f.write(f"Sum of daily counts: {daily_counts.sum()}\n\n")
    f.write("Daily breakdown:\n")
    for date, count in daily_counts.items():
        f.write(f"  {date}: {count} commits\n")

print("\n✓ Detailed results saved to diagnostic_results.txt")
