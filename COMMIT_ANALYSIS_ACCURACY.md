# Accuracy for Commit Analysis (200 Commits from microsoft/vscode)

## Two Types of Accuracy

### 1. **Test Case Accuracy: 90.0% (43/48)**
- **What it measures**: Accuracy on curated test cases with known expected classifications
- **Location**: `test_validation.py` - `test_sentiment_analyzer()` function
- **Purpose**: Validates that the sentiment analyzer correctly classifies known examples

### 2. **Validation Accuracy: 100% (200/200)**
- **What it measures**: Data integrity and correctness of the analysis process
- **Location**: `validator.py` - `validate_all()` function
- **Purpose**: Ensures all commits were analyzed correctly and results are mathematically consistent

## Validation Accuracy for Commit Analysis

### Current Status: **100% Validation Pass Rate**

The paper states: *"Comprehensive validation achieved 100% pass rate across all tiers."*

### What Gets Validated:

#### 1. **Data Integrity (100% Pass)**
- ✅ All 200 commits have required fields (sha, message, date, author)
- ✅ No missing or null values
- ✅ SHA format correct (7 characters)
- ✅ Date formats valid and parseable
- ✅ No empty messages
- ✅ All sentiment values valid (positive/neutral/negative)

**Validation Code** (`validator.py` lines 127-179):
```python
def validate_data_integrity(self, commits, df):
    # Checks:
    # - Commit count matches DataFrame length
    # - All required fields present
    # - No null values
    # - Valid date formats
    # - Valid sentiment values
```

#### 2. **Sentiment Score Validation (100% Pass)**
- ✅ All compound scores within [-1.0, 1.0] range
- ✅ All positive/neutral/negative scores within [0, 1] range
- ✅ For each commit: positive + neutral + negative ≈ 1.0
- ✅ All classifications match threshold rules:
  - compound ≥ 0.05 → classified as positive ✓
  - compound ≤ -0.05 → classified as negative ✓
  - -0.05 < compound < 0.05 → classified as neutral ✓

**Validation Code** (`validator.py` lines 19-73):
```python
def validate_sentiment_scores(self, df):
    # Checks:
    # - Score ranges
    # - Score sums ≈ 1.0
    # - Classifications match thresholds
```

#### 3. **Summary Statistics Validation (100% Pass)**
- ✅ Total count matches: 200 commits
- ✅ Counts add up: 37 + 137 + 26 = 200 ✓
- ✅ Percentages sum to 100%: 18.5% + 68.5% + 13.0% = 100.0% ✓
- ✅ Average compound score matches calculated mean: +0.022 ✓
- ✅ All counts match DataFrame values

**Validation Code** (`validator.py` lines 75-125):
```python
def validate_summary(self, summary, df):
    # Checks:
    # - Total count matches
    # - Counts add up correctly
    # - Percentages sum to 100%
    # - Average matches calculated mean
```

## How Validation Accuracy is Calculated

### Process:

1. **Fetch 200 commits** from microsoft/vscode repository
2. **Analyze each commit** using VaderSentiment
3. **Run validation checks** on all 200 commits
4. **Calculate pass rate**: (Passed Checks / Total Checks) × 100%

### Validation Formula:

```
Validation Accuracy = (Number of Passed Validations / Total Validations) × 100%

For 200 commits:
- Data Integrity: 200/200 passed = 100%
- Sentiment Scores: 200/200 passed = 100%
- Summary Statistics: All checks passed = 100%

Overall Validation Rate: 100%
```

## Results for 200 Commits

### Analysis Results:
- **Total Commits**: 200
- **Positive**: 37 (18.5%)
- **Neutral**: 137 (68.5%)
- **Negative**: 26 (13.0%)
- **Mean Sentiment**: +0.022
- **P/N Ratio**: 1.42:1

### Validation Results:
- **Data Integrity**: ✅ 100% (200/200)
- **Sentiment Scores**: ✅ 100% (200/200)
- **Summary Statistics**: ✅ 100% (all checks passed)
- **Overall Validation Rate**: ✅ 100%

## Classification Accuracy vs Validation Accuracy

### Classification Accuracy (90% on test cases)
- Measures: How well the analyzer classifies sentiment
- Requires: Ground truth labels (known correct answers)
- Available for: 48 test cases with known classifications
- Result: 90.0% (43/48 correct)

### Validation Accuracy (100% on real commits)
- Measures: Whether the analysis process is correct and consistent
- Checks: Data integrity, score ranges, mathematical consistency
- Available for: All 200 real commits
- Result: 100% (all validation checks passed)

## Why We Can't Measure Classification Accuracy on Real Commits

For the 200 real commits from microsoft/vscode:
- ❌ We don't have ground truth labels (no one manually labeled them)
- ❌ We can't know the "correct" sentiment for each commit
- ✅ We can validate that the analysis process is correct (100% validation)

## How to Verify Commit Analysis Accuracy

### Method 1: Run Validation
```bash
python main.py microsoft vscode --limit 200 --validate
```

This will:
- Analyze 200 commits
- Run all validation checks
- Show validation report with 100% pass rate

### Method 2: Check Validation Results
The validator checks:
- All 200 commits have valid data
- All sentiment scores are in correct ranges
- All classifications follow threshold rules
- All statistics are mathematically correct

### Method 3: Manual Spot Check
You can manually review sample commits:
```bash
python show_commits.py
```

## Summary

| Metric | Value | What It Measures |
|--------|-------|------------------|
| **Test Case Accuracy** | 90.0% (43/48) | Classification correctness on known test cases |
| **Validation Accuracy** | 100% (200/200) | Data integrity and process correctness |
| **Validation Pass Rate** | 100% | All validation checks passed |

## Key Points

1. **Test Case Accuracy (90%)**: Measures how well the sentiment analyzer classifies known examples
2. **Validation Accuracy (100%)**: Ensures the analysis process is correct and consistent
3. **Real Commit Analysis**: We validate correctness (100%) but can't measure classification accuracy without ground truth labels
4. **Both are important**: Test cases validate the algorithm, validation ensures the process works correctly
