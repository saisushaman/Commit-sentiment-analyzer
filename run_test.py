import sys
import io
from test_validation import test_sentiment_analyzer

# Capture stdout
old_stdout = sys.stdout
sys.stdout = buffer = io.StringIO()

# Run the test
result = test_sentiment_analyzer()

# Get output
output = buffer.getvalue()
sys.stdout = old_stdout

# Extract accuracy from output
lines = output.split('\n')
for line in lines:
    if 'Overall Accuracy' in line:
        print(line)
        # Write to file
        with open('accuracy_output.txt', 'w') as f:
            f.write(line + '\n')
            f.write(f"Test passed: {result}\n")
        break
