"""
Main Application
Commit Message Sentiment Analyzer - Entry Point
"""

import argparse
import sys
from commit_analyzer import CommitFetcher
from sentiment_analyzer import SentimentAnalyzer
from visualizer import SentimentVisualizer
from validator import ResultValidator


def print_summary(summary: dict):
    """Print summary statistics to console."""
    print("\n" + "="*60)
    print("SENTIMENT ANALYSIS SUMMARY")
    print("="*60)
    print(f"Total Commits Analyzed: {summary['total_commits']}")
    print(f"\nSentiment Breakdown:")
    print(f"  Positive: {summary['positive_count']} ({summary['positive_percentage']:.1f}%)")
    print(f"  Neutral:  {summary['neutral_count']} ({summary['neutral_percentage']:.1f}%)")
    print(f"  Negative: {summary['negative_count']} ({summary['negative_percentage']:.1f}%)")
    print(f"\nAverage Sentiment Score: {summary['average_compound']:.3f}")
    print("  (Range: -1.0 to +1.0, where 0 is neutral)")
    print("="*60 + "\n")


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description='Analyze sentiment of GitHub commit messages',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py microsoft vscode
  python main.py facebook react --limit 100
  python main.py tensorflow tensorflow --limit 200 --output my_results.png
        """
    )
    
    parser.add_argument('owner', help='GitHub repository owner (username or organization)')
    parser.add_argument('repo', nargs='?', help='Repository name (optional, can be part of owner/repo)')
    parser.add_argument('--limit', type=int, default=200, 
                       help='Maximum number of commits to analyze (default: 200)')
    parser.add_argument('--output', type=str, default='sentiment_analysis.png',
                       help='Output file name for visualization (default: sentiment_analysis.png)')
    parser.add_argument('--validate', action='store_true',
                       help='Run validation checks on results')
    
    args = parser.parse_args()
    
    # Handle case where repo might be in owner (owner/repo format)
    if '/' in args.owner:
        parts = args.owner.split('/')
        owner = parts[0]
        repo = parts[1] if len(parts) > 1 else args.repo
    else:
        owner = args.owner
        repo = args.repo
    
    if not repo:
        print("Error: Repository name is required.")
        print("Usage: python main.py <owner> <repo>")
        print("   or: python main.py owner/repo")
        sys.exit(1)
    
    # Initialize components
    fetcher = CommitFetcher(owner, repo)
    analyzer = SentimentAnalyzer()
    visualizer = SentimentVisualizer()
    
    # Fetch commits
    commits = fetcher.fetch_commits(limit=args.limit)
    
    if not commits:
        print("No commits found or error occurred.")
        sys.exit(1)
    
    # Analyze sentiment
    print("Analyzing sentiment...")
    df = analyzer.analyze_commits(commits)
    
    # Get summary
    summary = analyzer.get_summary(df)
    print_summary(summary)
    
    # Run validation if requested
    if args.validate:
        validator = ResultValidator()
        validator.validate_all(commits, df, summary)
    
    # Create visualizations
    print("Generating visualizations...")
    visualizer.plot_sentiment_timeline(df, output_file=args.output)
    visualizer.plot_sentiment_distribution(df, output_file='sentiment_distribution.png')
    
    print("\n✅ Analysis complete!")
    print(f"📊 Timeline chart: {args.output}")
    print(f"📊 Distribution chart: sentiment_distribution.png")
    
    if args.validate:
        print("✅ Validation checks completed")


if __name__ == '__main__':
    main()

