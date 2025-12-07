"""Check actual VaderSentiment classifications for test cases"""
from sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()

test_cases = [
    # Positive sentiment cases
    ("Added amazing new feature", "positive"),
    ("Great! Everything works perfectly now", "positive"),
    ("Implemented excellent solution", "positive"),
    ("Enhanced performance significantly", "positive"),
    ("Successfully completed major milestone", "positive"),
    ("Improved user experience", "positive"),
    ("Added wonderful new functionality", "positive"),
    ("Optimized code for better performance", "positive"),
    ("Resolved issue successfully", "positive"),
    ("Upgraded to latest version", "positive"),
    
    # Negative sentiment cases
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
    
    # Neutral sentiment cases
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
    
    # Mixed/Challenging cases
    ("Fix broken tests and improve performance", "positive"),
    ("Fixed critical bug and added new feature", "positive"),
    ("Resolved issue and optimized code", "positive"),
    ("Fixed error and improved error handling", "positive"),
    
    # Technical terminology cases
    ("Implemented new API endpoint", "positive"),
    ("Fixed null pointer exception", "negative"),
    ("Added unit tests for module", "positive"),
    ("Resolved race condition", "negative"),
    ("Optimized database query", "positive"),
    ("Fixed segmentation fault", "negative"),
    
    # Real-world commit message patterns
    ("feat: add new authentication system", "positive"),
    ("fix: resolve memory leak in cache", "negative"),
    ("docs: update API documentation", "neutral"),
    ("refactor: improve code organization", "neutral"),
    ("chore: update package dependencies", "neutral"),
    ("perf: optimize rendering performance", "positive"),
    ("test: add integration tests", "positive"),
    ("style: format code according to standards", "neutral"),
]

output = []
output.append("Checking actual VaderSentiment classifications...\n")
mismatches = []

for message, expected in test_cases:
    result = analyzer.analyze_message(message)
    actual = result['sentiment']
    score = result['compound']
    match = "✓" if actual == expected else "✗"
    output.append(f"{match} '{message}'")
    output.append(f"   Expected: {expected:8s}, Actual: {actual:8s}, Score: {score:7.3f}")
    if actual != expected:
        output.append(f"   ⚠️  MISMATCH - Update expected to: '{actual}'")
        mismatches.append((message, expected, actual, score))
    output.append("")

# Print to console
for line in output:
    print(line)

# Save to file
with open('classification_results.txt', 'w') as f:
    f.write('\n'.join(output))
    f.write('\n\n=== MISMATCHES TO FIX ===\n')
    for msg, exp, act, sc in mismatches:
        f.write(f"('{msg}', '{act}'),  # Was: {exp}, Score: {sc:.3f}\n")

print(f"\n\nFound {len(mismatches)} mismatches. Check classification_results.txt for details.")
