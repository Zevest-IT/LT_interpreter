import os
import telebot
from dotenv import load_dotenv
from googletrans import Translator


load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# BOT_TOKEN = os.getenv("BOT_TOKEN")
# BOT_TOKEN = os.environ["BOT_TOKEN"]

# print("🔍 Переменные окружения в контейнере Railway:")
# subprocess.run(["env"], shell=True)

if not BOT_TOKEN:
    raise ValueError("Ошибка: переменная BOT_TOKEN не загружена!")

bot = telebot.TeleBot(token=BOT_TOKEN)
translator = Translator()


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    text_to_translate = message.text
    try:
        detected = translator.detect(text_to_translate)
        lang_map = {"lt": "be", "be": "lt"}
        if detected.lang in lang_map and detected.confidence >= 0.80:
            translated_text = translator.translate(text_to_translate, dest=lang_map[detected.lang]).text
            bot.reply_to(message, translated_text)
    except Exception as e:
        bot.reply_to(message, f"Error occurred: {str(e)}")

if __name__ == "__main__":
    bot.polling(none_stop=True)
