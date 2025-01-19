from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/module/<string:module_name>')
def module(module_name):
    return render_template('module.html', module_name=module_name)

@app.route('/quiz/<string:module_name>', methods=['GET', 'POST'])
def quiz(module_name):
    if request.method == 'POST':
        answers = request.json
        # Handle quiz submission logic here
        return jsonify({"result": "success"})

    # Load quiz questions from JSON file
    with open('data/quizzes.json', 'r') as f:
        quizzes = json.load(f)
        quiz_questions = quizzes.get(module_name, [])
    return render_template('quiz.html', module_name=module_name, questions=quiz_questions)

if __name__ == '__main__':
    app.run(debug=True)
