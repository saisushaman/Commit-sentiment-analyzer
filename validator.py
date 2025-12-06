"""
Validation Module
Validates data integrity and analysis results.
"""

import pandas as pd
from typing import Dict, List, Tuple
import sys


class ResultValidator:
    """Validates analysis results for correctness and integrity."""
    
    def __init__(self):
        """Initialize the validator."""
        self.errors = []
        self.warnings = []
    
    def validate_sentiment_scores(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate that sentiment scores are within expected ranges.
        
        Args:
            df: DataFrame with sentiment analysis results
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check compound score range (-1 to 1)
        invalid_compound = df[(df['compound'] < -1.0) | (df['compound'] > 1.0)]
        if len(invalid_compound) > 0:
            errors.append(f"ERROR: Found {len(invalid_compound)} commits with compound scores outside [-1, 1] range")
        
        # Check positive, neutral, negative scores (should be 0 to 1)
        invalid_pos = df[(df['positive'] < 0) | (df['positive'] > 1)]
        invalid_neu = df[(df['neutral'] < 0) | (df['neutral'] > 1)]
        invalid_neg = df[(df['negative'] < 0) | (df['negative'] > 1)]
        
        if len(invalid_pos) > 0:
            errors.append(f"ERROR: Found {len(invalid_pos)} commits with positive scores outside [0, 1] range")
        if len(invalid_neu) > 0:
            errors.append(f"ERROR: Found {len(invalid_neu)} commits with neutral scores outside [0, 1] range")
        if len(invalid_neg) > 0:
            errors.append(f"ERROR: Found {len(invalid_neg)} commits with negative scores outside [0, 1] range")
        
        # Check that pos + neu + neg ≈ 1 (within 0.01 tolerance)
        score_sum = df['positive'] + df['neutral'] + df['negative']
        invalid_sum = df[abs(score_sum - 1.0) > 0.01]
        if len(invalid_sum) > 0:
            errors.append(f"ERROR: Found {len(invalid_sum)} commits where pos+neu+neg ≠ 1.0")
        
        # Validate sentiment classification matches compound score
        misclassified = []
        for _, row in df.iterrows():
            compound = row['compound']
            sentiment = row['sentiment']
            
            if compound >= 0.05 and sentiment != 'positive':
                misclassified.append((row['sha'], compound, sentiment))
            elif compound <= -0.05 and sentiment != 'negative':
                misclassified.append((row['sha'], compound, sentiment))
            elif -0.05 < compound < 0.05 and sentiment != 'neutral':
                misclassified.append((row['sha'], compound, sentiment))
        
        if misclassified:
            errors.append(f"ERROR: Found {len(misclassified)} misclassified commits")
            # Show first 3 examples
            for sha, comp, sent in misclassified[:3]:
                errors.append(f"  - SHA {sha}: compound={comp:.3f}, classified as '{sent}'")
        
        return len(errors) == 0, errors
    
    def validate_summary(self, summary: Dict, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate summary statistics match the data.
        
        Args:
            summary: Summary dictionary
            df: DataFrame with sentiment analysis results
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check total count matches
        if summary['total_commits'] != len(df):
            errors.append(f"ERROR: Summary total_commits ({summary['total_commits']}) doesn't match DataFrame length ({len(df)})")
        
        # Check count totals
        total_counted = (summary['positive_count'] + 
                        summary['neutral_count'] + 
                        summary['negative_count'])
        
        if total_counted != summary['total_commits']:
            errors.append(f"ERROR: Sentiment counts don't add up to total ({total_counted} != {summary['total_commits']})")
        
        # Check percentages add up to ~100%
        total_percentage = (summary['positive_percentage'] + 
                           summary['neutral_percentage'] + 
                           summary['negative_percentage'])
        
        if abs(total_percentage - 100.0) > 0.1:
            errors.append(f"ERROR: Percentages don't add up to 100% (sum = {total_percentage:.1f}%)")
        
        # Check average compound score
        actual_avg = df['compound'].mean()
        if abs(summary['average_compound'] - actual_avg) > 0.001:
            errors.append(f"ERROR: Average compound score mismatch ({summary['average_compound']:.6f} vs {actual_avg:.6f})")
        
        # Verify counts match DataFrame
        actual_pos = len(df[df['sentiment'] == 'positive'])
        actual_neu = len(df[df['sentiment'] == 'neutral'])
        actual_neg = len(df[df['sentiment'] == 'negative'])
        
        if summary['positive_count'] != actual_pos:
            errors.append(f"ERROR: Positive count mismatch ({summary['positive_count']} vs {actual_pos})")
        if summary['neutral_count'] != actual_neu:
            errors.append(f"ERROR: Neutral count mismatch ({summary['neutral_count']} vs {actual_neu})")
        if summary['negative_count'] != actual_neg:
            errors.append(f"ERROR: Negative count mismatch ({summary['negative_count']} vs {actual_neg})")
        
        return len(errors) == 0, errors
    
    def validate_data_integrity(self, commits: List[Dict], df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate data integrity between fetched commits and analysis results.
        
        Args:
            commits: Original list of commits
            df: DataFrame with analysis results
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        warnings = []
        
        # Check count matches
        if len(commits) != len(df):
            errors.append(f"ERROR: Commit count mismatch ({len(commits)} commits vs {len(df)} rows)")
        
        # Check required fields
        required_fields = ['sha', 'message', 'date', 'author']
        for field in required_fields:
            if field not in df.columns:
                errors.append(f"ERROR: Missing required column '{field}'")
        
        # Check for missing/null values
        for field in required_fields:
            null_count = df[field].isna().sum()
            if null_count > 0:
                errors.append(f"ERROR: Found {null_count} null values in '{field}' column")
        
        # Check for empty messages
        empty_messages = df[df['message'].str.strip() == '']
        if len(empty_messages) > 0:
            warnings.append(f"WARNING: Found {len(empty_messages)} commits with empty messages")
        
        # Check date format
        try:
            pd.to_datetime(df['date'])
        except:
            errors.append("ERROR: Invalid date format in 'date' column")
        
        # Verify SHA format (should be 7 characters)
        invalid_shas = df[df['sha'].str.len() != 7]
        if len(invalid_shas) > 0:
            warnings.append(f"WARNING: Found {len(invalid_shas)} commits with non-standard SHA format")
        
        # Check sentiment values are valid
        valid_sentiments = {'positive', 'neutral', 'negative'}
        invalid_sentiments = df[~df['sentiment'].isin(valid_sentiments)]
        if len(invalid_sentiments) > 0:
            errors.append(f"ERROR: Found {len(invalid_sentiments)} commits with invalid sentiment values")
        
        return len(errors) == 0, errors + warnings
    
    def validate_all(self, commits: List[Dict], df: pd.DataFrame, summary: Dict) -> bool:
        """
        Run all validation checks.
        
        Args:
            commits: Original list of commits
            df: DataFrame with analysis results
            summary: Summary dictionary
            
        Returns:
            True if all validations pass, False otherwise
        """
        print("\n" + "="*60)
        print("VALIDATION REPORT")
        print("="*60)
        
        all_valid = True
        
        # Data integrity
        print("\n1. Data Integrity Check...")
        valid, issues = self.validate_data_integrity(commits, df)
        if valid:
            print("   ✓ PASSED")
        else:
            all_valid = False
            for issue in issues:
                if issue.startswith("ERROR"):
                    print(f"   ✗ {issue}")
                else:
                    print(f"   ⚠ {issue}")
        
        # Sentiment scores
        print("\n2. Sentiment Score Validation...")
        valid, errors = self.validate_sentiment_scores(df)
        if valid:
            print("   ✓ PASSED - All scores within valid ranges")
        else:
            all_valid = False
            for error in errors:
                print(f"   ✗ {error}")
        
        # Summary statistics
        print("\n3. Summary Statistics Validation...")
        valid, errors = self.validate_summary(summary, df)
        if valid:
            print("   ✓ PASSED - Summary matches data")
        else:
            all_valid = False
            for error in errors:
                print(f"   ✗ {error}")
        
        # Additional checks
        print("\n4. Additional Checks...")
        
        # Check date range
        if len(df) > 0:
            date_range = (df['date'].max() - df['date'].min()).days
            print(f"   ✓ Date range: {date_range} days")
            print(f"   ✓ Oldest commit: {df['date'].min()}")
            print(f"   ✓ Newest commit: {df['date'].max()}")
        
        # Score distribution stats
        if len(df) > 0:
            print(f"\n   Score Statistics:")
            print(f"   - Compound: min={df['compound'].min():.3f}, max={df['compound'].max():.3f}, std={df['compound'].std():.3f}")
            print(f"   - Positive: mean={df['positive'].mean():.3f}, std={df['positive'].std():.3f}")
            print(f"   - Neutral:  mean={df['neutral'].mean():.3f}, std={df['neutral'].std():.3f}")
            print(f"   - Negative: mean={df['negative'].mean():.3f}, std={df['negative'].std():.3f}")
        
        print("\n" + "="*60)
        if all_valid:
            print("✓ ALL VALIDATIONS PASSED")
        else:
            print("✗ SOME VALIDATIONS FAILED - Please review errors above")
        print("="*60 + "\n")
        
        return all_valid

