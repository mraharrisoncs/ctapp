import json, subprocess, time, tempfile, os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from examples_loader import load_examples

app = Flask(__name__)
CORS(app)

# Dictionary to store the best scores for each example
best_scores = {}

# Load examples from the examples directory
examples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "examples")
examples = load_examples(examples_dir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sandbox', methods=['GET', 'POST'])
def sandbox():
    try:
        if request.method == 'POST':
            code = request.json.get('code')
            example_index = request.json.get('example_index', None)
            expected_output = request.json.get('expected_output', None)

            try:
                # Measure the start time
                start_time = time.time()

                # Execute the user's code and capture the output
                result = subprocess.run(['python', '-c', code], capture_output=True, text=True, timeout=10)
                
                # Measure the end time
                end_time = time.time()

                # Calculate the run duration in milliseconds
                run_duration = (end_time - start_time) * 1000

                output = result.stdout.strip()
                error = result.stderr

                # Check the code quality using flake8
                readability_score, flake8_output = run_flake8(code)

                # Compare the output with the expected output
                if output == expected_output:
                    success = True
                    # Check and update the best score for the example
                    if example_index is not None:
                        example_index = int(example_index)
                        best_score = best_scores.get(example_index, float('inf'))
                        if readability_score < best_score:
                            best_scores[example_index] = readability_score
                            improved = True
                        else:
                            improved = False
                else:
                    success = False
                    improved = False

                # Convert Infinity to a string
                best_score_str = str(best_scores.get(example_index, float('inf')))
                if best_score_str == 'inf':
                    best_score_str = 'Infinity'

                # Debugging info
                print(f"Run duration: {run_duration} ms")
                print(f"Readability score: {readability_score}")
                print(f"flake8 output: {flake8_output}")
                print(f"Best score for example {example_index}: {best_score_str}")
                print(f"Improved: {improved}")

                if success and improved:
                    message = "Success! Your code matches the expected output and has a better flake8 score!"
                elif success:
                    message = "Success! Your code matches the expected output but did not improve the flake8 score."
                else:
                    message = "Keep trying! Your code does not match the expected output."

                return jsonify({
                    'output': output,
                    'error': error,
                    'success': success,
                    'run_duration': run_duration,
                    'readability_score': readability_score,
                    'best_score': best_score_str,
                    'improved': improved,
                    'message': message,
                    'flake8_output': flake8_output
                })
            except subprocess.TimeoutExpired:
                return jsonify({'output': '', 'error': 'Code execution timed out.', 'success': False, 'run_duration': None, 'readability_score': None, 'best_score': None, 'improved': False, 'message': 'Code execution timed out.'})
        
        return render_template('sandbox.html', examples=examples)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'output': '', 'error': f'An error occurred: {str(e)}', 'success': False, 'run_duration': None, 'readability_score': None, 'best_score': None, 'improved': False, 'message': 'An error occurred.'})

@app.route('/get_refactored_code', methods=['POST'])
def get_refactored_code():
    try:
        example_index = request.json.get('example_index')
        refactored_code = examples["examples"][int(example_index)]["refactored_code"]
        expected_output = subprocess.run(['python', '-c', refactored_code], capture_output=True, text=True).stdout.strip()
        return jsonify({'refactored_code': refactored_code, 'expected_output': expected_output})
    except Exception as e:
        print(f"An error occurred while fetching refactored code: {e}")
        return jsonify({'refactored_code': '', 'error': f'An error occurred: {str(e)}'})

def run_flake8(code):
    flake8_path = r'C:\Users\alan\AppData\Roaming\Python\Python312\Scripts\flake8.exe'  # Use flake8 from the PATH
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        temp_file.write(code.encode('utf-8'))
        temp_file.flush()
        result = subprocess.run([flake8_path, '--exit-zero', temp_file.name], capture_output=True, text=True)
        flake8_output = result.stdout
        if result.returncode == 0:
            return 0, flake8_output  # No issues found
        else:
            return len(result.stdout.splitlines()), flake8_output  # Number of flake8 issues

if __name__ == '__main__':
    app.run(debug=True)
