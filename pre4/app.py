from flask import Flask, render_template, request, redirect
import csv
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# プリントのデータをCSVファイルから読み込む関数
def load_handouts():
    handouts = []
    try:
        with open('data/handouts.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            handouts = list(reader)
    except FileNotFoundError:
        pass
    return handouts

# プリントを年と月ごとに分類する関数
def group_handouts_by_month(handouts):
    grouped = defaultdict(list)
    for name, date in handouts:
        year_month = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m')  # 年と月を抽出
        grouped[year_month].append((name, date))
    return grouped

# プリントのデータをCSVファイルに保存する関数
def save_handout(name, date):
    with open('data/handouts.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([name, date])

# プリントのデータをCSVファイルに更新する関数
def update_handout(name, new_date):
    handouts = load_handouts()
    with open('data/handouts.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for handout in handouts:
            if handout[0] == name:
                writer.writerow([handout[0], new_date])  # 更新された日付で書き込む
            else:
                writer.writerow(handout)

# メインページのルート
@app.route('/')
def index():
    handouts = load_handouts()
    grouped_handouts = group_handouts_by_month(handouts)
    return render_template('index.html', grouped_handouts=grouped_handouts)

# 新しいプリントを追加するルート
@app.route('/add', methods=['POST'])
def add_handout():
    name = request.form['name']
    date = datetime.now().strftime('%Y-%m-%d')  # 現在の日付を取得
    save_handout(name, date)
    return redirect('/')

# 日付を更新するルート
@app.route('/update/<name>', methods=['POST'])
def update_handout_date(name):
    new_date = request.form['date']
    update_handout(name, new_date)
    return redirect('/')
    
if __name__ == '__main__':
    app.run(debug=True)
