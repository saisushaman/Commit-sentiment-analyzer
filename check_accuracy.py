import sys
import os
from sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()

test_cases = [
    ("Added amazing new feature", "positive"),
    ("Great! Everything works perfectly now", "positive"),
    ("Implemented excellent solution", "positive"),
    ("Enhanced performance significantly", "positive"),
    ("Successfully completed major milestone", "positive"),
    ("Improved user experience", "positive"),
    ("Added wonderful new functionality", "positive"),
    ("Optimized code for better performance", "positive"),
    ("Resolved issue successfully", "negative"),
    ("Upgraded to latest version", "neutral"),
    ("Fixed critical bug", "negative"),
    ("This is terrible, completely broken", "negative"),
    ("Fixed error in authentication", "negative"),
    ("Resolved critical security vulnerability", "negative"),
    ("Fixed broken API endpoint", "negative"),
    ("Removed problematic code", "negative"),
    ("Fixed memory leak issue", "negative"),
    ("Resolved crash on startup", "negative"),
    ("Fixed data corruption bug", "negative"),
    ("Emergency fix for production issue", "negative"),
    ("Update documentation", "neutral"),
    ("Merge pull request #123", "neutral"),
    ("Refactor code structure", "neutral"),
    ("Update dependencies", "neutral"),
    ("Move files to new directory", "neutral"),
    ("Change configuration settings", "neutral"),
    ("Update version number", "neutral"),
    ("Modify build script", "neutral"),
    ("Rename variables for clarity", "neutral"),
    ("Reorganize project structure", "neutral"),
    ("Fix broken tests and improve performance", "negative"),
    ("Fixed critical bug and added new feature", "negative"),
    ("Resolved issue and optimized code", "negative"),
    ("Fixed error and improved error handling", "negative"),
    ("Implemented new API endpoint", "positive"),
    ("Fixed null pointer exception", "negative"),
    ("Added unit tests for module", "positive"),
    ("Resolved race condition", "neutral"),
    ("Optimized database query", "positive"),
    ("Fixed segmentation fault", "negative"),
    ("feat: add new authentication system", "positive"),
    ("fix: resolve memory leak in cache", "negative"),
    ("docs: update API documentation", "neutral"),
    ("refactor: improve code organization", "positive"),
    ("chore: update package dependencies", "neutral"),
    ("perf: optimize rendering performance", "positive"),
    ("test: add integration tests", "positive"),
    ("style: format code according to standards", "neutral"),
]

correct = 0
mismatches = []

for msg, expected in test_cases:
    result = analyzer.analyze_message(msg)
    actual = result['sentiment']
    if actual == expected:
        correct += 1
    else:
        mismatches.append((msg, expected, actual))

total = len(test_cases)
accuracy = (correct / total) * 100

output_file = os.path.join(os.path.dirname(__file__), 'accuracy_final.txt')
with open(output_file, 'w') as f:
    f.write(f"Total test cases: {total}\n")
    f.write(f"Correct: {correct}\n")
    f.write(f"Incorrect: {len(mismatches)}\n")
    f.write(f"Accuracy: {correct}/{total} = {accuracy:.1f}%\n")
    f.write(f"\nMisclassified ({len(mismatches)}):\n")
    for msg, exp, act in mismatches:
        f.write(f"  '{msg}' - Expected: {exp}, Got: {act}\n")

print(f"Accuracy: {correct}/{total} = {accuracy:.1f}%")
print(f"Results saved to: {output_file}")
