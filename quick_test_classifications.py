"""Quick test to get actual classifications"""
from sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()

# Test the problematic cases
test_messages = [
    "Resolved issue successfully",
    "Upgraded to latest version", 
    "Fix broken tests and improve performance",
    "Fixed critical bug and added new feature",
    "Resolved issue and optimized code",
    "Fixed error and improved error handling",
    "Resolved race condition",
    "Implemented new API endpoint",
    "Added unit tests for module",
    "feat: add new authentication system",
    "refactor: improve code organization",
]

results = []
results.append("Actual Classifications:\n")
for msg in test_messages:
    result = analyzer.analyze_message(msg)
    line = f"'{msg}' -> {result['sentiment']:8s} (score: {result['compound']:7.3f})"
    results.append(line)
    print(line)

with open('quick_results.txt', 'w') as f:
    f.write('\n'.join(results))
