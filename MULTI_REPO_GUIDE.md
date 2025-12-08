# Multi-Repository Sentiment Analysis Guide

## Overview

You can analyze multiple GitHub repositories for sentiment analysis. This enables:
- **Comparative Studies**: Compare sentiment patterns across different projects
- **Cross-Repository Analysis**: Identify trends across multiple codebases
- **Research Applications**: Study how different project types, languages, or organizations differ in commit message sentiment

## Methods to Analyze Multiple Repositories

### Method 1: Run Multiple Times (Current Approach)

Analyze each repository separately:

```bash
# Analyze first repository
python main.py microsoft vscode --limit 200

# Analyze second repository
python main.py facebook react --limit 200

# Analyze third repository
python main.py tensorflow tensorflow --limit 200
```

**Pros:**
- Simple, uses existing code
- Each analysis is independent
- Can use different limits per repository

**Cons:**
- Manual comparison needed
- No automated comparison table
- Results saved separately

### Method 2: Use Multi-Repository Script (New)

Use the `analyze_multiple_repos.py` script for automated comparison:

```bash
# Analyze multiple repos at once
python analyze_multiple_repos.py microsoft/vscode facebook/react tensorflow/tensorflow

# With custom limit
python analyze_multiple_repos.py microsoft/vscode facebook/react --limit 100

# Save comparison to file
python analyze_multiple_repos.py microsoft/vscode facebook/react --output comparison.txt
```

**Features:**
- ✅ Automated comparison table
- ✅ Statistical summary across repositories
- ✅ Save results to file
- ✅ Side-by-side comparison

**Example Output:**
```
Repository                      Total    Pos%     Neu%     Neg%     Avg      P/N     
----------------------------------------------------------------------
microsoft/vscode               200      18.5%    68.5%    13.0%    0.022    1.42
facebook/react                 200      25.0%    60.0%    15.0%    0.045    1.67
tensorflow/tensorflow          200      20.0%    65.0%    15.0%    0.030    1.33

STATISTICAL SUMMARY
Average Positive: 21.2%
Average Neutral:  64.5%
Average Negative: 14.3%
Average Compound Score: 0.033
```

## Use Cases for Multi-Repository Analysis

### 1. **Comparative Research**
Compare sentiment patterns across:
- Different programming languages
- Open-source vs. proprietary projects
- Large vs. small projects
- Different organizational structures

### 2. **Project Health Monitoring**
Track sentiment trends across:
- Multiple projects in an organization
- Related projects (e.g., framework ecosystem)
- Projects at different maturity levels

### 3. **Research Studies**
- Cross-repository sentiment analysis
- Identifying common patterns
- Statistical comparisons

## Implementation Details

### Current Architecture

The system is designed to handle one repository at a time:
- `CommitFetcher`: Fetches from one repository
- `SentimentAnalyzer`: Analyzes commits (works with any commits)
- `SentimentVisualizer`: Creates visualizations (one per repository)

### Multi-Repository Support

The new `analyze_multiple_repos.py` script:
1. Loops through multiple repositories
2. Analyzes each independently
3. Collects results
4. Generates comparison table
5. Calculates aggregate statistics

## Example: Analyzing 3 Repositories

```bash
python analyze_multiple_repos.py \
    microsoft/vscode \
    facebook/react \
    tensorflow/tensorflow \
    --limit 200 \
    --output multi_repo_comparison.txt
```

This will:
1. Analyze 200 commits from each repository
2. Display results for each
3. Show comparison table
4. Save detailed results to file

## Limitations

1. **API Rate Limits**: 
   - Unauthenticated: 60 requests/hour
   - Analyzing multiple repos will use more API calls
   - Consider using authenticated access for large-scale analysis

2. **Time Requirements**:
   - Each repository takes time to fetch and analyze
   - Multiple repos = longer total time

3. **Visualization**:
   - Current visualizer creates one chart per repository
   - For comparison, you'd need to create separate charts or modify the visualizer

## Future Enhancements

The paper mentions this in Future Work (line 201):
> **Multi-Repository Comparison:** Extending analysis to multiple repositories would enable comparative studies across different project types, sizes, and development cultures.

Potential improvements:
- Side-by-side comparison visualizations
- Statistical significance testing
- Correlation analysis across repositories
- Time-series comparison charts

## Best Practices

1. **Start Small**: Test with 2-3 repositories first
2. **Use Similar Limits**: Use the same `--limit` for fair comparison
3. **Consider Rate Limits**: Space out requests if analyzing many repos
4. **Save Results**: Use `--output` to save comparison data
5. **Validate**: Use `--validate` flag to ensure data quality

## Example Research Questions

With multi-repository analysis, you can answer:
- Do different project types have different sentiment patterns?
- How does project size affect sentiment distribution?
- Are there cultural differences in commit message sentiment?
- Do open-source projects differ from corporate projects?
- How does programming language affect sentiment?
