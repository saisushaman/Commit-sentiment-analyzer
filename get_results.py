"""
Comprehensive script to run analysis and save detailed results
"""
import sys
import traceback
from datetime import datetime

try:
    from commit_analyzer import CommitFetcher
    from sentiment_analyzer import SentimentAnalyzer
    from visualizer import SentimentVisualizer
    import pandas as pd
    
    print("Starting analysis...")
    
    # Initialize
    fetcher = CommitFetcher('facebook', 'react')
    analyzer = SentimentAnalyzer()
    visualizer = SentimentVisualizer()
    
    # Fetch commits
    print("Fetching 200 commits...")
    commits = fetcher.fetch_commits(limit=200)
    
    if not commits:
        print("ERROR: No commits fetched!")
        sys.exit(1)
    
    print(f"Fetched {len(commits)} commits")
    
    # Analyze
    print("Analyzing sentiment...")
    df = analyzer.analyze_commits(commits)
    summary = analyzer.get_summary(df)
    
    # Calculate additional stats
    min_score = df['compound'].min()
    max_score = df['compound'].max()
    std_dev = df['compound'].std()
    median_score = df['compound'].median()
    
    # Write detailed results
    results = f"""
================================================================================
SENTIMENT ANALYSIS RESULTS - facebook/react
================================================================================
Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Repository: facebook/react
Total Commits Analyzed: {summary['total_commits']}

SENTIMENT DISTRIBUTION:
  Positive: {summary['positive_count']} commits ({summary['positive_percentage']:.1f}%)
  Neutral:  {summary['neutral_count']} commits ({summary['neutral_percentage']:.1f}%)
  Negative: {summary['negative_count']} commits ({summary['negative_percentage']:.1f}%)

SCORE STATISTICS:
  Average Compound Score: {summary['average_compound']:.3f}
  Median Score: {median_score:.3f}
  Minimum Score: {min_score:.3f}
  Maximum Score: {max_score:.3f}
  Standard Deviation: {std_dev:.3f}

SENTIMENT CATEGORY STATISTICS:
  Mean Positive Score: {df[df['sentiment']=='positive']['compound'].mean():.3f}
  Mean Neutral Score: {df[df['sentiment']=='neutral']['compound'].mean():.3f}
  Mean Negative Score: {df[df['sentiment']=='negative']['compound'].mean():.3f}

VALIDATION:
  Total commits: {len(df)}
  Positive + Neutral + Negative = {summary['positive_count'] + summary['neutral_count'] + summary['negative_count']}
  Percentages sum: {summary['positive_percentage'] + summary['neutral_percentage'] + summary['negative_percentage']:.1f}%
  
================================================================================
"""
    
    print(results)
    
    # Save to file
    with open('analysis_results.txt', 'w', encoding='utf-8') as f:
        f.write(results)
    
    print("Results saved to analysis_results.txt")
    
    # Generate visualizations
    print("Generating visualizations...")
    visualizer.plot_sentiment_timeline(df, output_file='sentiment_analysis.png')
    visualizer.plot_sentiment_distribution(df, output_file='sentiment_distribution.png')
    print("Visualizations saved!")
    
    # Also save a CSV for reference
    df.to_csv('commits_data.csv', index=False)
    print("Data saved to commits_data.csv")
    
except Exception as e:
    error_msg = f"ERROR: {str(e)}\n{traceback.format_exc()}"
    print(error_msg)
    with open('analysis_error.txt', 'w') as f:
        f.write(error_msg)
    sys.exit(1)

