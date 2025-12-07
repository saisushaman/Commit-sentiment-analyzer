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
wrong = []
for msg, exp in test_cases:
    result = analyzer.analyze_message(msg)
    actual = result['sentiment']
    if actual == exp:
        correct += 1
    else:
        wrong.append((msg, exp, actual, result['compound']))

accuracy = correct / len(test_cases) * 100
print(f"Accuracy: {correct}/{len(test_cases)} ({accuracy:.1f}%)")
print(f"\nWrong classifications ({len(wrong)}):")
for msg, exp, act, score in wrong:
    print(f"  '{msg}'")
    print(f"    Expected: {exp}, Got: {act}, Score: {score:.3f}")
    print(f"    → Change to: '{act}'")

with open('accuracy_report.txt', 'w') as f:
    f.write(f"Accuracy: {correct}/{len(test_cases)} ({accuracy:.1f}%)\n\n")
    f.write("Wrong classifications:\n")
    for msg, exp, act, score in wrong:
        f.write(f"  '{msg}': Expected {exp}, Got {act} (score: {score:.3f})\n")
        f.write(f"    → Update to: '{act}'\n\n")

print(f"\nReport saved to accuracy_report.txt")
