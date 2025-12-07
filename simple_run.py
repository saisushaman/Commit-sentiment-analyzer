#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("Importing modules...")
from commit_analyzer import CommitFetcher
from sentiment_analyzer import SentimentAnalyzer
from visualizer import SentimentVisualizer
import pandas as pd

print("="*70)
print("ANALYZING microsoft/vscode - 200 COMMITS")
print("="*70)

# Fetch
print("\n[1/4] Fetching commits from GitHub...")
fetcher = CommitFetcher('microsoft', 'vscode')
commits = fetcher.fetch_commits(limit=200)
print(f"    ✓ Fetched {len(commits)} commits")

if len(commits) < 200:
    print(f"    ⚠ Warning: Only {len(commits)} commits available (requested 200)")

# Analyze
print("\n[2/4] Analyzing sentiment...")
analyzer = SentimentAnalyzer()
df = analyzer.analyze_commits(commits)
summary = analyzer.get_summary(df)

# Stats
min_score = float(df['compound'].min())
max_score = float(df['compound'].max())
std_dev = float(df['compound'].std())
median_score = float(df['compound'].median())

# Results
print("\n[3/4] Results:")
print("-"*70)
print(f"Total Commits: {summary['total_commits']}")
print(f"\nSentiment Distribution:")
print(f"  Positive: {summary['positive_count']:3d} ({summary['positive_percentage']:5.1f}%)")
print(f"  Neutral:  {summary['neutral_count']:3d} ({summary['neutral_percentage']:5.1f}%)")
print(f"  Negative: {summary['negative_count']:3d} ({summary['negative_percentage']:5.1f}%)")
print(f"\nScore Statistics:")
print(f"  Average: {summary['average_compound']:7.3f}")
print(f"  Median:  {median_score:7.3f}")
print(f"  Min:     {min_score:7.3f}")
print(f"  Max:     {max_score:7.3f}")
print(f"  Std Dev: {std_dev:7.3f}")

# Save
print("\n[4/4] Saving results...")
with open('FINAL_RESULTS.txt', 'w') as f:
    f.write("="*70 + "\n")
    f.write("SENTIMENT ANALYSIS - microsoft/vscode\n")
    f.write("="*70 + "\n\n")
    f.write(f"Total Commits: {summary['total_commits']}\n\n")
    f.write("Sentiment Distribution:\n")
    f.write(f"  Positive: {summary['positive_count']} ({summary['positive_percentage']:.1f}%)\n")
    f.write(f"  Neutral:  {summary['neutral_count']} ({summary['neutral_percentage']:.1f}%)\n")
    f.write(f"  Negative: {summary['negative_count']} ({summary['negative_percentage']:.1f}%)\n\n")
    f.write("Score Statistics:\n")
    f.write(f"  Average: {summary['average_compound']:.3f}\n")
    f.write(f"  Median:  {median_score:.3f}\n")
    f.write(f"  Min:     {min_score:.3f}\n")
    f.write(f"  Max:     {max_score:.3f}\n")
    f.write(f"  Std Dev: {std_dev:.3f}\n")

print("    ✓ Saved to FINAL_RESULTS.txt")

# Visualizations
print("    ✓ Generating visualizations...")
visualizer = SentimentVisualizer()
visualizer.plot_sentiment_timeline(df, output_file='sentiment_analysis.png')
visualizer.plot_sentiment_distribution(df, output_file='sentiment_distribution.png')
print("    ✓ Visualizations saved")

print("\n" + "="*70)
print("ANALYSIS COMPLETE!")
print("="*70)
