import subprocess
import sys
import os

# Run the test_all_cases script and capture output
result = subprocess.run(
    [sys.executable, 'test_all_cases.py'],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    capture_output=True,
    text=True,
    encoding='utf-8'
)

# Write output to file
with open('test_output_captured.txt', 'w', encoding='utf-8') as f:
    f.write("STDOUT:\n")
    f.write(result.stdout)
    f.write("\n\nSTDERR:\n")
    f.write(result.stderr)

# Extract accuracy from output
for line in result.stdout.split('\n'):
    if 'Accuracy:' in line:
        print(line)
        with open('ACCURACY_FOUND.txt', 'w') as f:
            f.write(line)
