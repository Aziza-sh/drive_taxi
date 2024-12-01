import telebot
import sqlite3
import random
import string

# Токен бота
TOKEN = '7633740407:AAH1fyCMHxluJrAj40qODI73ds86h9HhNP4'
bot = telebot.TeleBot(TOKEN)

# Функция генерации уникального номера заказа
def generate_order_id(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Подключение к базе данных
def get_route_duration(start_station, end_station):
    conn = sqlite3.connect('river_routes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT duration FROM routes WHERE start_station=? AND end_station=?", (start_station, end_station))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Введите начальную и конечную станции в формате: 'Станция1 Станция2'.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        start_station, end_station = message.text.split()
        duration = get_route_duration(start_station, end_station)
        
        if duration is not None:
            order_id = generate_order_id()
            driver_chat_id = 'DRIVER_CHAT_ID'  # Замените на реальный chat_id водителя
            
            # Отправка информации водителю
            bot.send_message(driver_chat_id, f"Новый заказ:\nID заказа: {order_id}\nМаршрут: {start_station} - {end_station}\nВремя в пути: {duration} минут.")
            
            # Отправка информации заказчику
            bot.send_message(message.chat.id, f"Ваш заказ создан!\nID заказа: {order_id}\nОжидаемое время прибытия: {duration} минут.")
        else:
            bot.reply_to(message, "Маршрут не найден. Пожалуйста, проверьте введенные станции.")
    
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка. Убедитесь, что вы ввели данные правильно.")

# Запуск бота
bot.polling()
