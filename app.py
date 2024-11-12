import os
from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__, static_folder='templates')


# Завантажуємо всі дані з user_data.json
def load_user_data():
    file_path = os.path.join(os.path.dirname(__file__), 'user_data.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Повертаємо порожній список, якщо файл не існує
    except json.JSONDecodeError:
        return []  # Повертаємо порожній список, якщо файл має неправильний формат JSON

# Зберігаємо оновлені дані в файл user_data.json
def save_user_data(user_data):
    file_path = os.path.join(os.path.dirname(__file__), 'user_data.json')
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(user_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving user data: {e}")
        return False
    return True

# Отримуємо дані конкретного користувача по user_id
def get_user_profile(user_id):
    user_data = load_user_data()
    for user in user_data:
        if isinstance(user, dict) and user.get('user_id') == str(user_id):  # Перевіряємо, чи це словник і чи є в ньому 'user_id'
            return user
    return None  # Якщо користувача з таким ID немає

@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для отримання профілю за user_id
@app.route('/get_profile/<user_id>')
def get_profile_by_id(user_id):
    user_data = get_user_profile(user_id)
    if user_data:
        return jsonify(user_data)
    else:
        return jsonify({'error': 'User not found'}), 404

# Маршрут для додавання нового користувача (POST)
@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        new_user = request.get_json()  # Отримуємо нові дані користувача у форматі JSON
        if not new_user or not new_user.get('user_id'):
            return jsonify({'error': 'Invalid data'}), 400

        # Завантажуємо існуючі дані користувачів
        user_data = load_user_data()

        # Перевіряємо, чи є користувач з таким же ID
        if get_user_profile(new_user['user_id']):
            return jsonify({'error': 'User already exists'}), 400

        # Додаємо нового користувача до списку
        user_data.append(new_user)

        # Зберігаємо оновлений список в файл
        if not save_user_data(user_data):
            return jsonify({'error': 'Failed to save user data'}), 500

        return jsonify({'message': 'User added successfully'}), 201
    except Exception as e:
        print(f"Error in /add_user endpoint: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
