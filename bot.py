import json
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = '6511495388:AAFXF4_cEGCdX2zjNm8HhhfINWivojm2mMM'
USER_DATA_FILE = 'user_data.json'

# Функція для збереження даних користувача
def save_user_data(user_data):
    # Якщо файл існує, завантажуємо існуючі дані
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            data = json.load(file)
    else:
        data = {}  # Якщо файл не існує, створюємо новий словник

    # Оновлюємо або додаємо дані про користувача
    data[user_data['user_id']] = user_data

    # Записуємо оновлені дані назад у файл
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Функція старту
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)  # Отримуємо user_id з повідомлення користувача
    username = update.message.from_user.username or "No username"
    
    # Формуємо словник з даними користувача
    user_data = {
        "username": username,
        "user_id": user_id,
        "balance": "444",
        "level": "1",
        "bonus": "0"
    }

    # Зберігаємо дані користувача у файл
    save_user_data(user_data)

# Функція старту
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id  # Отримуємо user_id з повідомлення користувача
    app_url = f"http://127.0.0.1:5000/?user_id={user_id}"  # Генеруємо URL з user_id
    keyboard = [[InlineKeyboardButton("Відкрити Mini App", url=app_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Натисніть кнопку, щоб відкрити Mini App', reply_markup=reply_markup)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == '__main__':
    main()
