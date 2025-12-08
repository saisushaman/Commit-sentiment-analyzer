"""
Analyze sentiment for multiple GitHub repositories
Supports batch analysis and comparison
"""
import argparse
import sys
from commit_analyzer import CommitFetcher
from sentiment_analyzer import SentimentAnalyzer
from visualizer import SentimentVisualizer
import pandas as pd
from typing import List, Dict, Tuple


def analyze_repository(owner: str, repo: str, limit: int = 200) -> Dict:
    """
    Analyze a single repository and return summary.
    
    Args:
        owner: Repository owner
        repo: Repository name
        limit: Number of commits to analyze
        
    Returns:
        Dictionary with analysis results
    """
    print(f"\n{'='*70}")
    print(f"Analyzing: {owner}/{repo}")
    print(f"{'='*70}")
    
    try:
        # Fetch commits
        fetcher = CommitFetcher(owner, repo)
        commits = fetcher.fetch_commits(limit=limit)
        
        if not commits:
            print(f"⚠️  No commits found for {owner}/{repo}")
            return None
        
        # Analyze sentiment
        analyzer = SentimentAnalyzer()
        df = analyzer.analyze_commits(commits)
        summary = analyzer.get_summary(df)
        
        # Add repository info
        result = {
            'repository': f"{owner}/{repo}",
            'total_commits': summary['total_commits'],
            'positive_count': summary['positive_count'],
            'neutral_count': summary['neutral_count'],
            'negative_count': summary['negative_count'],
            'positive_percentage': summary['positive_percentage'],
            'neutral_percentage': summary['neutral_percentage'],
            'negative_percentage': summary['negative_percentage'],
            'average_compound': summary['average_compound'],
            'pn_ratio': summary['positive_count'] / summary['negative_count'] if summary['negative_count'] > 0 else 0,
            'std_dev': df['compound'].std(),
            'min_score': df['compound'].min(),
            'max_score': df['compound'].max(),
        }
        
        print(f"✓ Analyzed {len(commits)} commits")
        print(f"  Positive: {result['positive_count']} ({result['positive_percentage']:.1f}%)")
        print(f"  Neutral:  {result['neutral_count']} ({result['neutral_percentage']:.1f}%)")
        print(f"  Negative: {result['negative_count']} ({result['negative_percentage']:.1f}%)")
        print(f"  Average: {result['average_compound']:.3f}")
        
        return result
        
    except Exception as e:
        print(f"✗ Error analyzing {owner}/{repo}: {e}")
        return None


def compare_repositories(results: List[Dict]):
    """
    Compare results from multiple repositories.
    
    Args:
        results: List of analysis result dictionaries
    """
    if not results:
        print("No results to compare")
        return
    
    print(f"\n{'='*70}")
    print("COMPARATIVE ANALYSIS")
    print(f"{'='*70}")
    
    # Create comparison table
    print(f"\n{'Repository':<30} {'Total':<8} {'Pos%':<8} {'Neu%':<8} {'Neg%':<8} {'Avg':<8} {'P/N':<8}")
    print("-" * 70)
    
    for result in results:
        if result:
            print(f"{result['repository']:<30} "
                  f"{result['total_commits']:<8} "
                  f"{result['positive_percentage']:>6.1f}% "
                  f"{result['neutral_percentage']:>6.1f}% "
                  f"{result['negative_percentage']:>6.1f}% "
                  f"{result['average_compound']:>7.3f} "
                  f"{result['pn_ratio']:>7.2f}")
    
    # Statistical summary
    print(f"\n{'='*70}")
    print("STATISTICAL SUMMARY")
    print(f"{'='*70}")
    
    avg_pos = sum(r['positive_percentage'] for r in results if r) / len([r for r in results if r])
    avg_neu = sum(r['neutral_percentage'] for r in results if r) / len([r for r in results if r])
    avg_neg = sum(r['negative_percentage'] for r in results if r) / len([r for r in results if r])
    avg_compound = sum(r['average_compound'] for r in results if r) / len([r for r in results if r])
    
    print(f"Average Positive: {avg_pos:.1f}%")
    print(f"Average Neutral:  {avg_neu:.1f}%")
    print(f"Average Negative: {avg_neg:.1f}%")
    print(f"Average Compound Score: {avg_compound:.3f}")


def main():
    """Main entry point for multi-repository analysis."""
    parser = argparse.ArgumentParser(
        description='Analyze sentiment for multiple GitHub repositories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze multiple repos
  python analyze_multiple_repos.py microsoft/vscode facebook/react tensorflow/tensorflow
  
  # With custom limit
  python analyze_multiple_repos.py microsoft/vscode facebook/react --limit 100
  
  # Save comparison to file
  python analyze_multiple_repos.py microsoft/vscode facebook/react --output comparison.txt
        """
    )
    
    parser.add_argument('repositories', nargs='+', 
                       help='Repository names in format owner/repo (e.g., microsoft/vscode)')
    parser.add_argument('--limit', type=int, default=200,
                       help='Number of commits to analyze per repository (default: 200)')
    parser.add_argument('--output', type=str,
                       help='Output file to save comparison results')
    parser.add_argument('--validate', action='store_true',
                       help='Run validation checks for each repository')
    
    args = parser.parse_args()
    
    # Parse repository names
    repos_to_analyze = []
    for repo_str in args.repositories:
        if '/' in repo_str:
            parts = repo_str.split('/')
            if len(parts) == 2:
                repos_to_analyze.append((parts[0], parts[1]))
            else:
                print(f"⚠️  Invalid repository format: {repo_str}")
        else:
            print(f"⚠️  Repository must be in format owner/repo: {repo_str}")
    
    if not repos_to_analyze:
        print("Error: No valid repositories provided")
        sys.exit(1)
    
    print(f"\n{'='*70}")
    print(f"ANALYZING {len(repos_to_analyze)} REPOSITORY(IES)")
    print(f"{'='*70}")
    
    # Analyze each repository
    results = []
    for owner, repo in repos_to_analyze:
        result = analyze_repository(owner, repo, limit=args.limit)
        if result:
            results.append(result)
    
    # Compare results
    if len(results) > 1:
        compare_repositories(results)
    
    # Save to file if requested
    if args.output and results:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write("MULTI-REPOSITORY SENTIMENT ANALYSIS\n")
            f.write("="*70 + "\n\n")
            
            for result in results:
                f.write(f"Repository: {result['repository']}\n")
                f.write(f"Total Commits: {result['total_commits']}\n")
                f.write(f"Positive: {result['positive_count']} ({result['positive_percentage']:.1f}%)\n")
                f.write(f"Neutral:  {result['neutral_count']} ({result['neutral_percentage']:.1f}%)\n")
                f.write(f"Negative: {result['negative_count']} ({result['negative_percentage']:.1f}%)\n")
                f.write(f"Average Score: {result['average_compound']:.3f}\n")
                f.write(f"P/N Ratio: {result['pn_ratio']:.2f}\n")
                f.write("-"*70 + "\n\n")
            
            if len(results) > 1:
                f.write("COMPARATIVE SUMMARY\n")
                f.write("="*70 + "\n")
                avg_pos = sum(r['positive_percentage'] for r in results) / len(results)
                avg_neu = sum(r['neutral_percentage'] for r in results) / len(results)
                avg_neg = sum(r['negative_percentage'] for r in results) / len(results)
                avg_compound = sum(r['average_compound'] for r in results) / len(results)
                f.write(f"Average Positive: {avg_pos:.1f}%\n")
                f.write(f"Average Neutral:  {avg_neu:.1f}%\n")
                f.write(f"Average Negative: {avg_neg:.1f}%\n")
                f.write(f"Average Compound Score: {avg_compound:.3f}\n")
        
        print(f"\n✓ Results saved to {args.output}")
    
    print(f"\n✅ Analysis complete! Analyzed {len(results)} repository(ies)")


if __name__ == '__main__':
    main()
