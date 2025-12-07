"""
Run vscode analysis and print results immediately
"""
import sys
from commit_analyzer import CommitFetcher
from sentiment_analyzer import SentimentAnalyzer
from visualizer import SentimentVisualizer
import pandas as pd

print("="*70)
print("RUNNING ANALYSIS: microsoft/vscode - 200 COMMITS")
print("="*70)

try:
    # Fetch
    print("\n[1/4] Fetching 200 commits from microsoft/vscode...")
    fetcher = CommitFetcher('microsoft', 'vscode')
    commits = fetcher.fetch_commits(limit=200)
    print(f"    ✓ Fetched {len(commits)} commits")
    
    if len(commits) < 200:
        print(f"    ⚠ Only {len(commits)} commits available")
    
    # Analyze
    print("\n[2/4] Analyzing sentiment...")
    analyzer = SentimentAnalyzer()
    df = analyzer.analyze_commits(commits)
    summary = analyzer.get_summary(df)
    
    # Calculate stats
    min_score = float(df['compound'].min())
    max_score = float(df['compound'].max())
    std_dev = float(df['compound'].std())
    median_score = float(df['compound'].median())
    
    # Print results
    print("\n[3/4] RESULTS:")
    print("-"*70)
    print(f"Repository: microsoft/vscode")
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
    
    # Calculate P/N ratio
    if summary['negative_count'] > 0:
        pn_ratio = summary['positive_count'] / summary['negative_count']
        print(f"\nPositive/Negative Ratio: {pn_ratio:.2f}:1")
    
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
        if summary['negative_count'] > 0:
            f.write(f"\nPositive/Negative Ratio: {pn_ratio:.2f}:1\n")
    
    print("    ✓ Saved to FINAL_RESULTS.txt")
    
    # Generate visualizations
    print("    ✓ Generating visualizations...")
    visualizer = SentimentVisualizer()
    visualizer.plot_sentiment_timeline(df, output_file='sentiment_analysis.png')
    visualizer.plot_sentiment_distribution(df, output_file='sentiment_distribution.png')
    print("    ✓ Visualizations saved")
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70)
    
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
