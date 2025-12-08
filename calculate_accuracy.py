from sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()

# All 48 test cases from test_validation.py
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

print("Calculating accuracy for 48 test cases...\n")

for msg, expected in test_cases:
    result = analyzer.analyze_message(msg)
    actual = result['sentiment']
    score = result['compound']
    
    if actual == expected:
        correct += 1
    else:
        mismatches.append((msg, expected, actual, score))

accuracy = (correct / total) * 100

print(f"Total test cases: {total}")
print(f"Correct classifications: {correct}")
print(f"Incorrect classifications: {len(mismatches)}")
print(f"\nAccuracy: {correct}/{total} = {accuracy:.1f}%")
print(f"\nMisclassified cases ({len(mismatches)}):")
for msg, exp, act, sc in mismatches:
    print(f"  '{msg}'")
    print(f"    Expected: {exp}, Got: {act}, Score: {sc:.3f}")

# Write to file
with open('accuracy_result.txt', 'w') as f:
    f.write(f"Total test cases: {total}\n")
    f.write(f"Correct classifications: {correct}\n")
    f.write(f"Incorrect classifications: {len(mismatches)}\n")
    f.write(f"\nAccuracy: {correct}/{total} = {accuracy:.1f}%\n")
    f.write(f"\nMisclassified cases ({len(mismatches)}):\n")
    for msg, exp, act, sc in mismatches:
        f.write(f"  '{msg}'\n")
        f.write(f"    Expected: {exp}, Got: {act}, Score: {sc:.3f}\n")
