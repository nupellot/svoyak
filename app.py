from flask import Flask, render_template, url_for, request, redirect
import json
from datetime import datetime

app = Flask(__name__)

# Загрузка данных из JSON
with open("questions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

CATEGORIES = data["categories"]

# Состояние отвеченных вопросов
answered_questions = [
    [False for _ in category["questions"]] for category in CATEGORIES
]


@app.route('/')
def home():
    return render_template('home.html', categories=CATEGORIES, answered=answered_questions, enumerate=enumerate)


@app.route('/question/<int:row>/<int:col>')
def question(row, col):
    question_data = CATEGORIES[row]["questions"][col]
    start_time = datetime.now()
    return render_template('question.html', question=question_data["question"], start_time=start_time.isoformat(), row=row, col=col)


@app.route('/answer/<int:row>/<int:col>')
def answer(row, col):
    global answered_questions
    answer_data = CATEGORIES[row]["questions"][col]["answer"]
    start_time = request.args.get('start_time')
    elapsed_time = None
    if start_time:
        start_time = datetime.fromisoformat(start_time)
        elapsed_time = (datetime.now() - start_time).total_seconds()
    answered_questions[row][col] = True
    return render_template('answer.html', answer=answer_data, elapsed_time=elapsed_time, row=row, col=col)


@app.route('/reset')
def reset():
    global answered_questions
    answered_questions = [
        [False for _ in category["questions"]] for category in CATEGORIES
    ]
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
