# Validation Guide

This guide explains how to validate the results of the Commit Message Sentiment Analyzer.

## What is Validated?

The validation system checks multiple aspects of the analysis:

### 1. **Data Integrity**
- ✅ All required fields are present (sha, message, date, author)
- ✅ No missing or null values in critical fields
- ✅ SHA format is correct (7 characters)
- ✅ Date formats are valid and parseable
- ✅ Message content is not empty
- ✅ Sentiment values are valid (positive/neutral/negative)

### 2. **Sentiment Score Validation**
- ✅ Compound scores are within [-1.0, 1.0] range
- ✅ Positive, neutral, negative scores are within [0, 1] range
- ✅ Positive + neutral + negative ≈ 1.0 for each commit
- ✅ Sentiment classification matches compound score thresholds
  - compound ≥ 0.05 → positive
  - compound ≤ -0.05 → negative
  - -0.05 < compound < 0.05 → neutral

### 3. **Summary Statistics Validation**
- ✅ Total commit count matches DataFrame length
- ✅ Sentiment counts add up to total
- ✅ Percentages add up to 100%
- ✅ Average compound score matches calculated mean
- ✅ Counts match actual DataFrame values

### 4. **Additional Checks**
- ✅ Date range information
- ✅ Score distribution statistics (min, max, std dev)

## How to Use Validation

### Option 1: Validate During Analysis

Add the `--validate` flag when running analysis:

```bash
python main.py facebook react --validate
```

This will run validation checks after analysis and display a detailed report.

### Option 2: Run Standalone Tests

Run the comprehensive test suite:

```bash
python test_validation.py
```

This runs:
- **Test Case Validation**: Tests sentiment analyzer with known examples
- **Edge Case Testing**: Tests with empty messages, special characters, etc.
- **Real Repository Test**: Validates with actual GitHub data
- **Data Validation**: Tests data integrity with synthetic data

### Option 3: Use Validator Programmatically

```python
from commit_analyzer import CommitFetcher
from sentiment_analyzer import SentimentAnalyzer
from validator import ResultValidator

# Fetch and analyze
fetcher = CommitFetcher("owner", "repo")
commits = fetcher.fetch_commits(limit=50)

analyzer = SentimentAnalyzer()
df = analyzer.analyze_commits(commits)
summary = analyzer.get_summary(df)

# Validate
validator = ResultValidator()
is_valid = validator.validate_all(commits, df, summary)
```

## Understanding Validation Output

### Success Example

```
============================================================
VALIDATION REPORT
============================================================

1. Data Integrity Check...
   ✓ PASSED

2. Sentiment Score Validation...
   ✓ PASSED - All scores within valid ranges

3. Summary Statistics Validation...
   ✓ PASSED - Summary matches data

4. Additional Checks...
   ✓ Date range: 30 days
   ✓ Oldest commit: 2024-01-15 10:30:00
   ✓ Newest commit: 2024-02-14 15:45:00

   Score Statistics:
   - Compound: min=-0.542, max=0.636, std=0.234
   - Positive: mean=0.342, std=0.245
   - Neutral:  mean=0.521, std=0.198
   - Negative: mean=0.137, std=0.156

============================================================
✓ ALL VALIDATIONS PASSED
============================================================
```

### Error Example

```
============================================================
VALIDATION REPORT
============================================================

1. Data Integrity Check...
   ✓ PASSED

2. Sentiment Score Validation...
   ✗ ERROR: Found 2 commits with compound scores outside [-1, 1] range
   ✗ ERROR: Found 1 misclassified commits
     - SHA abc1234: compound=0.125, classified as 'neutral'

3. Summary Statistics Validation...
   ✗ ERROR: Percentages don't add up to 100% (sum = 99.8%)

============================================================
✗ SOME VALIDATIONS FAILED - Please review errors above
============================================================
```

## Common Validation Issues

### Issue: Misclassified Sentiments
**Cause**: Classification thresholds might be off by a tiny amount
**Solution**: This is usually a rounding issue. The validator checks within tolerance.

### Issue: Percentages Don't Add Up to 100%
**Cause**: Rounding errors in percentage calculations
**Solution**: Validator allows small tolerance (±0.1%). Larger differences indicate actual bugs.

### Issue: Missing Data
**Cause**: GitHub API might return incomplete data
**Solution**: Check repository accessibility and API response format.

## Best Practices

1. **Always validate** when testing new features
2. **Run tests** before deploying or sharing results
3. **Check warnings** - they may indicate data quality issues
4. **Review errors** - they indicate actual problems that need fixing

## Validator Methods

The `ResultValidator` class provides these methods:

- `validate_sentiment_scores(df)` - Validates score ranges and classifications
- `validate_summary(summary, df)` - Validates summary statistics
- `validate_data_integrity(commits, df)` - Validates data completeness
- `validate_all(commits, df, summary)` - Runs all validations

Each method returns `(is_valid: bool, issues: List[str])`.

