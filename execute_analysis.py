"""Execute analysis and save to file"""
import sys
import traceback

try:
    from commit_analyzer import CommitFetcher
    from sentiment_analyzer import SentimentAnalyzer
    from visualizer import SentimentVisualizer
    import pandas as pd
    
    output_lines = []
    output_lines.append("="*70)
    output_lines.append("ANALYZING microsoft/vscode - 200 COMMITS")
    output_lines.append("="*70)
    
    # Fetch
    output_lines.append("\n[1/4] Fetching commits...")
    fetcher = CommitFetcher('microsoft', 'vscode')
    commits = fetcher.fetch_commits(limit=200)
    output_lines.append(f"    ✓ Fetched {len(commits)} commits")
    
    # Analyze
    output_lines.append("\n[2/4] Analyzing sentiment...")
    analyzer = SentimentAnalyzer()
    df = analyzer.analyze_commits(commits)
    summary = analyzer.get_summary(df)
    
    min_score = float(df['compound'].min())
    max_score = float(df['compound'].max())
    std_dev = float(df['compound'].std())
    median_score = float(df['compound'].median())
    pn_ratio = summary['positive_count'] / summary['negative_count'] if summary['negative_count'] > 0 else 0
    
    # Results
    output_lines.append("\n[3/4] RESULTS:")
    output_lines.append("-"*70)
    output_lines.append(f"Repository: microsoft/vscode")
    output_lines.append(f"Total Commits: {summary['total_commits']}")
    output_lines.append(f"\nSentiment Distribution:")
    output_lines.append(f"  Positive: {summary['positive_count']:3d} ({summary['positive_percentage']:5.1f}%)")
    output_lines.append(f"  Neutral:  {summary['neutral_count']:3d} ({summary['neutral_percentage']:5.1f}%)")
    output_lines.append(f"  Negative: {summary['negative_count']:3d} ({summary['negative_percentage']:5.1f}%)")
    output_lines.append(f"\nScore Statistics:")
    output_lines.append(f"  Average: {summary['average_compound']:7.3f}")
    output_lines.append(f"  Median:  {median_score:7.3f}")
    output_lines.append(f"  Min:     {min_score:7.3f}")
    output_lines.append(f"  Max:     {max_score:7.3f}")
    output_lines.append(f"  Std Dev: {std_dev:7.3f}")
    output_lines.append(f"  P/N Ratio: {pn_ratio:.2f}:1")
    
    # Save to FINAL_RESULTS.txt
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
        f.write(f"  P/N Ratio: {pn_ratio:.2f}:1\n")
    
    # Generate visualizations
    output_lines.append("\n[4/4] Generating visualizations...")
    visualizer = SentimentVisualizer()
    visualizer.plot_sentiment_timeline(df, output_file='sentiment_analysis.png')
    visualizer.plot_sentiment_distribution(df, output_file='sentiment_distribution.png')
    output_lines.append("    ✓ Complete!")
    
    # Print and save
    output_text = "\n".join(output_lines)
    print(output_text)
    
    with open('ANALYSIS_OUTPUT.txt', 'w') as f:
        f.write(output_text)
    
except Exception as e:
    error_msg = f"ERROR: {e}\n{traceback.format_exc()}"
    print(error_msg)
    with open('ANALYSIS_ERROR.txt', 'w') as f:
        f.write(error_msg)

