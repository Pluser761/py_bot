import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup
from flask import Flask, request, render_template, redirect
import retailcrm
import os
import time
import mysql.connector as connector

token = "TOKEN"
bot = telebot.TeleBot(token=token)
server = Flask(__name__, static_folder='')
database = connector.connect(host='host',
                             database='database_name',
                             user='user_name',
                             password='password')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_chat_action(chat_id=message.chat.id, action='typing')
    bot.send_message(message.chat.id, 'Отправьте свой телефон через меню в верхнем правом углу экрана')


@bot.message_handler()
def save_message(message):
    database.reconnect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO `messages` (`text`, `id`)  VALUES (%s, %s)", (message.text, message.from_user.id))
    cursor.close()
    database.commit()
    database.close()


@server.route("/" + token, methods=["POST"])
def getMessage():
    print("getMessage")
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/setter")
def setter():
    print("setter")
    bot.remove_webhook()
    bot.set_webhook(url="CURRENT_URL" + token)
    print(bot.get_webhook_info())
    return "!", 200



if __name__ == "__main__":
    print("__main__")
    database.close()
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8443)))
