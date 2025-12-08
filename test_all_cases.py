"""Test all cases and get actual classifications"""
from sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()

# All 48 test cases
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
total = len(test_cases)
mismatches = []

print("Testing all 48 cases...\n")
for msg, expected in test_cases:
    result = analyzer.analyze_message(msg)
    actual = result['sentiment']
    score = result['compound']
    
    if actual == expected:
        correct += 1
    else:
        mismatches.append((msg, expected, actual, score))

accuracy = correct / total * 100

print(f"Accuracy: {correct}/{total} ({accuracy:.1f}%)")
print(f"\nMismatches ({len(mismatches)}):")
for msg, exp, act, sc in mismatches:
    print(f"  '{msg}'")
    print(f"    Expected: {exp}, Got: {act}, Score: {sc:.3f}")

# Write results
with open('test_accuracy_results.txt', 'w') as f:
    f.write(f"Test Accuracy: {correct}/{total} ({accuracy:.1f}%)\n\n")
    f.write("Mismatches:\n")
    for msg, exp, act, sc in mismatches:
        f.write(f"  '{msg}': Expected {exp}, Got {act} (score: {sc:.3f})\n")

print(f"\nResults saved to test_accuracy_results.txt")

