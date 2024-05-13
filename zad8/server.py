from flask import Flask, render_template, request, jsonify
import hashlib
import datetime
import secrets

app = Flask(__name__)

# Простая база данных для хранения пользователей
users = {}

# Функция для хеширования пароля с использованием соли
def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

# Главная страница с формой регистрации
@app.route('/')
def registration_form():
    return render_template('registration_form.html')

# Регистрация нового пользователя
@app.route('/register', methods=['POST'])
def register_user():
    login = request.form.get('login')
    password = request.form.get('password')
    
    if login in users:
        return jsonify({'error': 'User already exists'}), 400
    
    salt = secrets.token_hex(16)  # Генерируем случайную соль
    hashed_password = hash_password(password, salt)
    registration_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    users[login] = {
        'hashed_password': hashed_password,
        'salt': salt,
        'registration_date': registration_date
    }
    
    return jsonify({'message': 'User registered successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
