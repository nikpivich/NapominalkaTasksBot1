from datetime import datetime
import telebot
import json
from telebot.types import Message
from envparse import Env
from client import TelegramClient

env = Env()
TOKEN = env.str('TOKEN')
ADMIN_CHAT_ID = env.int('ADMIN_CHAT_ID')


class MyBot(telebot.TeleBot):
    def __init__(self, telegram_client: TelegramClient, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.telegram_client = telegram_client


telegram_client = TelegramClient(token=TOKEN, base_url="https://api.telegram.org")
bot = MyBot(token=TOKEN, telegram_client= telegram_client)


@bot.message_handler(commands=['start'])
def start(message: Message):
    with open('user.json', 'r') as f_o:
        data_from_json = json.load(f_o)

    user_id = message.from_user.id
    username = message.from_user.username

    if str(user_id) not in data_from_json:
        data_from_json[user_id] = {'username': username}

    with open('user.json', 'w') as f_o:
        json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    bot.reply_to(message=message, text=str(f"Регистрация прошла успешно"
                                           f"Добро пожаловать: {username}"))


def handle_standup_speech(message: Message):
    bot.reply_to(message, 'Спасибо большое, до завтра')


@bot.message_handler(commands=['say_standup_speech'])
def say_standup_speech(message: Message):
    bot.reply_to(message, text='ПРивет чем занимался вчера ?'
                               'Какие планы?')
    bot.register_next_step_handler(message, handle_standup_speech)


def create_err_message(err: Exception) -> str:
    return f"{datetime.now()} ::: {err.__class__} ::: {err}"


while True:
    try:
        bot.polling()
    except Exception as err:
        error_message = create_err_message(err)
        bot.telegram_client.post(method="sendMessage", params={"text": error_message, "chat_id": ADMIN_CHAT_ID})
