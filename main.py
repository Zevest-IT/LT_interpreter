import os
import telebot
import time
from dotenv import load_dotenv
from googletrans import Translator


load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_TELEGRAM_ID = os.environ.get("ADMIN_TELEGRAM_ID")


if not BOT_TOKEN:
    raise ValueError("Ошибка: переменная BOT_TOKEN не загружена!")

bot = telebot.TeleBot(token=BOT_TOKEN)
translator = Translator()
start_time = time.time()


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    text_to_translate = message.text
    if message.text.lower() == "report":
        uptime_seconds = int(time.time() - start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_message = f"ужо працую {hours:02}:{minutes:02}:{seconds:02}."
        bot.reply_to(message, uptime_message)
    else:
        try:
            detected = translator.detect(text_to_translate)
            lang_map = {"lt": "be", "be": "lt"}
            if detected.lang in lang_map and detected.confidence >= 0.80:
                translated_text = translator.translate(text_to_translate, dest=lang_map[detected.lang]).text
                # bot.reply_to(message, translated_text)
                bot.send_message(ADMIN_TELEGRAM_ID, f'{message.from_user.username}: {translated_text}')
        except Exception as e:
            bot.reply_to(message, f"Error occurred: {str(e)}")


if __name__ == "__main__":
    bot.polling(none_stop=True)
