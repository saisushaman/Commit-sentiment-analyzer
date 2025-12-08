"""
Script to run sentiment analysis and capture results
"""
import sys
from commit_analyzer import CommitFetcher
from sentiment_analyzer import SentimentAnalyzer
from visualizer import SentimentVisualizer

def main():
    print("="*60)
    print("RUNNING SENTIMENT ANALYSIS ON facebook/react")
    print("="*60)
    
    # Fetch commits
    print("\nFetching commits...")
    fetcher = CommitFetcher('facebook', 'react')
    commits = fetcher.fetch_commits(limit=200)
    
    if not commits:
        print("ERROR: No commits fetched!")
        return
    
    print(f"\n✓ Successfully fetched {len(commits)} commits")
    
    # Analyze sentiment
    print("\nAnalyzing sentiment...")
    analyzer = SentimentAnalyzer()
    df = analyzer.analyze_commits(commits)
    summary = analyzer.get_summary(df)
    
    # Print results
    print("\n" + "="*60)
    print("SENTIMENT ANALYSIS RESULTS")
    print("="*60)
    print(f"Total Commits Analyzed: {summary['total_commits']}")
    print(f"\nSentiment Distribution:")
    print(f"  Positive: {summary['positive_count']} ({summary['positive_percentage']:.1f}%)")
    print(f"  Neutral:  {summary['neutral_count']} ({summary['neutral_percentage']:.1f}%)")
    print(f"  Negative: {summary['negative_count']} ({summary['negative_percentage']:.1f}%)")
    print(f"\nScore Statistics:")
    print(f"  Average Score: {summary['average_compound']:.3f}")
    print(f"  Min Score: {df['compound'].min():.3f}")
    print(f"  Max Score: {df['compound'].max():.3f}")
    print(f"  Standard Deviation: {df['compound'].std():.3f}")
    
    # Save to file
    with open('analysis_results.txt', 'w') as f:
        f.write("SENTIMENT ANALYSIS RESULTS\n")
        f.write("="*60 + "\n")
        f.write(f"Repository: facebook/react\n")
        f.write(f"Total Commits: {summary['total_commits']}\n\n")
        f.write("Sentiment Distribution:\n")
        f.write(f"  Positive: {summary['positive_count']} ({summary['positive_percentage']:.1f}%)\n")
        f.write(f"  Neutral:  {summary['neutral_count']} ({summary['neutral_percentage']:.1f}%)\n")
        f.write(f"  Negative: {summary['negative_count']} ({summary['negative_percentage']:.1f}%)\n\n")
        f.write("Score Statistics:\n")
        f.write(f"  Average: {summary['average_compound']:.3f}\n")
        f.write(f"  Min: {df['compound'].min():.3f}\n")
        f.write(f"  Max: {df['compound'].max():.3f}\n")
        f.write(f"  Std Dev: {df['compound'].std():.3f}\n")
    
    print(f"\n✓ Results saved to analysis_results.txt")
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    visualizer = SentimentVisualizer()
    visualizer.plot_sentiment_timeline(df, output_file='sentiment_analysis.png')
    visualizer.plot_sentiment_distribution(df, output_file='sentiment_distribution.png')
    print("✓ Visualizations generated")
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("="*60)

if __name__ == '__main__':
    main()

