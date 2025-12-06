# Commit Message Sentiment Analyzer

A text analysis project that analyzes commit messages from GitHub repositories to understand developer behavior, workload, and project health.

## Features

- 🔍 Collects commit messages from any public GitHub repository
- 😊 Analyzes sentiment using VaderSentiment (positive, negative, neutral)
- 📊 Visualizes sentiment trends over time
- 📈 Provides insights into team morale and project activity

## Installation

1. Clone or download this project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python main.py <owner> <repo>
```

Example:
```bash
python main.py facebook react
```

This will analyze commit messages from the facebook/react repository.

### Advanced Options

```bash
python main.py <owner> <repo> --limit 100 --output results.png --validate
```

- `--limit`: Number of commits to analyze (default: 50)
- `--output`: Output file name for the visualization (default: sentiment_analysis.png)
- `--validate`: Run validation checks on the results (recommended)

## How It Works

1. **Fetch Commits**: Uses GitHub API to retrieve commit messages
2. **Sentiment Analysis**: Uses VaderSentiment to classify each message
3. **Trend Analysis**: Groups commits by date and calculates sentiment scores
4. **Visualization**: Creates charts showing sentiment trends over time

## Output

The tool generates:
- Console output with summary statistics
- A visualization chart saved as PNG file
- Breakdown of positive, negative, and neutral commits

## Requirements

- Python 3.7+
- Internet connection (for GitHub API access)
- GitHub repository must be public (or requires authentication)

## Example Output

```
Analyzing commits from facebook/react...
Found 50 commits

Sentiment Summary:
- Positive: 25 (50.0%)
- Neutral: 20 (40.0%)
- Negative: 5 (10.0%)

Average Sentiment Score: 0.15
Chart saved to: sentiment_analysis.png
```

## Validation

The project includes comprehensive validation to ensure results are accurate:

### Run Validation Tests

```bash
python test_validation.py
```

This will run:
- Sentiment analyzer test cases with known examples
- Edge case testing (empty messages, special characters, etc.)
- Real repository testing
- Data integrity validation

### Validate Results During Analysis

Add the `--validate` flag to your analysis command:

```bash
python main.py facebook react --validate
```

The validator checks:
- ✅ Sentiment scores are within valid ranges (-1 to 1)
- ✅ Percentages add up correctly to 100%
- ✅ Summary statistics match the actual data
- ✅ Data integrity (no missing values, valid formats)
- ✅ Sentiment classifications match compound scores
- ✅ Date formats and ranges are valid

## License

MIT License

