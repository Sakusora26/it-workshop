from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# データベースのパス設定
db_path = os.path.join(app.instance_path, 'app.db')

# データベースを初期化
def init_db():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

# ホームページ（ログイン画面）
@app.route('/')
def login():
    return render_template('login.html')

# ログイン処理
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
    
    if user and check_password_hash(user[2], password):
        session['user_id'] = user[0]
        flash('ログイン成功！')
        return redirect(url_for('dashboard'))
    else:
        flash('ユーザー名またはパスワードが間違っています')
        return redirect(url_for('login'))

# ダッシュボード（ログイン後のページ）
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('ログインしてください')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')

# ログアウト処理
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('ログアウトしました')
    return redirect(url_for('login'))

if __name__ == '__main__':
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
    init_db()  # 初回起動時にデータベースを初期化
    app.run(debug=True)
