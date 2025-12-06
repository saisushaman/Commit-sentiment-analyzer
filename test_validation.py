"""
Test and Validation Script
Tests the sentiment analyzer with sample data and validates results.
"""

from commit_analyzer import CommitFetcher
from sentiment_analyzer import SentimentAnalyzer
from validator import ResultValidator
import pandas as pd


def test_sentiment_analyzer():
    """Test sentiment analyzer with known test cases."""
    print("="*60)
    print("SENTIMENT ANALYZER TEST CASES")
    print("="*60)
    
    analyzer = SentimentAnalyzer()
    
    # Test cases with expected sentiment
    test_cases = [
        ("Fixed critical bug", "negative"),  # Should be negative
        ("Added amazing new feature", "positive"),  # Should be positive
        ("Update documentation", "neutral"),  # Should be neutral
        ("Fix broken tests and improve performance", "positive"),  # Mixed
        ("This is terrible, completely broken", "negative"),  # Clearly negative
        ("Great! Everything works perfectly now", "positive"),  # Clearly positive
        ("Merge pull request #123", "neutral"),  # Neutral
    ]
    
    print("\nTesting individual messages:\n")
    correct = 0
    total = len(test_cases)
    
    for message, expected in test_cases:
        result = analyzer.analyze_message(message)
        sentiment = result['sentiment']
        compound = result['compound']
        
        # Check if sentiment matches (allow some flexibility)
        status = "✓" if sentiment == expected else "✗"
        if status == "✓":
            correct += 1
        
        print(f"{status} Message: '{message[:50]}'")
        print(f"   Expected: {expected}, Got: {sentiment}, Score: {compound:.3f}")
        print()
    
    print(f"Accuracy: {correct}/{total} ({correct/total*100:.1f}%)")
    print("="*60 + "\n")
    
    return correct == total


def test_with_real_repo(owner: str = "octocat", repo: str = "Hello-World", limit: int = 10):
    """
    Test with a real GitHub repository and validate results.
    
    Args:
        owner: Repository owner
        repo: Repository name
        limit: Number of commits to fetch
    """
    print("="*60)
    print(f"TESTING WITH REAL REPOSITORY: {owner}/{repo}")
    print("="*60)
    
    # Fetch commits
    fetcher = CommitFetcher(owner, repo)
    commits = fetcher.fetch_commits(limit=limit)
    
    if not commits:
        print("ERROR: Could not fetch commits. Skipping real repo test.")
        return False
    
    # Analyze
    analyzer = SentimentAnalyzer()
    df = analyzer.analyze_commits(commits)
    summary = analyzer.get_summary(df)
    
    # Validate
    validator = ResultValidator()
    is_valid = validator.validate_all(commits, df, summary)
    
    return is_valid


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print("="*60)
    print("EDGE CASE TESTING")
    print("="*60)
    
    analyzer = SentimentAnalyzer()
    
    edge_cases = [
        ("", "Empty message"),  # Empty
        ("a", "Single character"),  # Very short
        ("!" * 100, "Only punctuation"),  # Special chars
        (" " * 50, "Only whitespace"),  # Whitespace
        ("Test" * 100, "Very long message"),  # Very long
        ("1234567890", "Only numbers"),  # Numbers only
        ("Fix\n\n\nMultiple\nLines", "Multiline"),  # Multiline
    ]
    
    print("\nTesting edge cases:\n")
    all_valid = True
    
    for message, description in edge_cases:
        try:
            result = analyzer.analyze_message(message)
            # Check that result has all required keys
            required_keys = ['compound', 'positive', 'neutral', 'negative', 'sentiment']
            has_all_keys = all(key in result for key in required_keys)
            
            # Check score ranges
            valid_range = (-1.0 <= result['compound'] <= 1.0)
            
            status = "✓" if (has_all_keys and valid_range) else "✗"
            if status == "✗":
                all_valid = False
            
            print(f"{status} {description}")
            print(f"   Message: '{message[:30]}...' (len={len(message)})")
            print(f"   Sentiment: {result['sentiment']}, Score: {result['compound']:.3f}")
            print()
        except Exception as e:
            print(f"✗ {description} - ERROR: {e}")
            all_valid = False
            print()
    
    print("="*60 + "\n")
    return all_valid


def run_all_tests():
    """Run all validation tests."""
    print("\n" + "="*70)
    print("RUNNING COMPREHENSIVE VALIDATION TESTS")
    print("="*70)
    
    results = []
    
    # Test 1: Sentiment analyzer with known cases
    print("\n[TEST 1/4] Sentiment Analyzer Test Cases")
    result1 = test_sentiment_analyzer()
    results.append(("Sentiment Analyzer", result1))
    
    # Test 2: Edge cases
    print("\n[TEST 2/4] Edge Case Testing")
    result2 = test_edge_cases()
    results.append(("Edge Cases", result2))
    
    # Test 3: Real repository (small test)
    print("\n[TEST 3/4] Real Repository Test")
    result3 = test_with_real_repo("octocat", "Hello-World", limit=5)
    results.append(("Real Repository", result3))
    
    # Test 4: Data validation
    print("\n[TEST 4/4] Data Validation Test")
    result4 = test_data_validation()
    results.append(("Data Validation", result4))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
    print("="*70 + "\n")
    
    return all(passed for _, passed in results)


def test_data_validation():
    """Test data validation with synthetic data."""
    print("\nTesting data validation with synthetic data...")
    
    analyzer = SentimentAnalyzer()
    validator = ResultValidator()
    
    # Create synthetic commit data
    test_commits = [
        {
            'sha': 'abc1234',
            'message': 'Fix bug in authentication',
            'date': '2024-01-15T10:30:00Z',
            'author': 'Test User'
        },
        {
            'sha': 'def5678',
            'message': 'Add amazing new feature',
            'date': '2024-01-16T11:00:00Z',
            'author': 'Test User'
        },
        {
            'sha': 'ghi9012',
            'message': 'Update README',
            'date': '2024-01-17T12:00:00Z',
            'author': 'Test User'
        },
    ]
    
    df = analyzer.analyze_commits(test_commits)
    summary = analyzer.get_summary(df)
    
    is_valid = validator.validate_all(test_commits, df, summary)
    
    return is_valid


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)

