import os
import time
import logging
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import telebot

# Загрузка переменных из .env
load_dotenv()
TOKEN = os.getenv("AWS_CHECK_BOT_TOKEN")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

if not all([TOKEN, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER]):
    raise ValueError("Не все переменные окружения установлены")

# Настройка логгера
log_file = "bot.log"
logging.basicConfig(
    encoding="UTF-8",
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Запись времени запуска
start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
start_time1 = time.time()
logging.info(f"Bot started at {start_time}")

# Инициализация бота
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Напиши 'send', чтобы получить log-файл на email.")


@bot.message_handler(func=lambda message: message.text.lower() == "send")
def send_log_via_email(message):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Log file from Telegram Bot"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg.set_content("Во вложении находится лог-файл бота.")

        with open(log_file, "rb") as f:
            msg.add_attachment(f.read(), maintype="text", subtype="plain", filename=log_file)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)

        bot.reply_to(message, "Log-файл отправлен на email.")
        logging.info("Log-файл успешно отправлен.")
    except Exception as e:
        bot.reply_to(message, "Ошибка при отправке email. См. лог.")
        logging.error(f"Ошибка при отправке email: {e}")


@bot.message_handler(func=lambda message: message.text.lower() == "report")
def report_time(message):
    uptime_seconds = int(time.time() - start_time1)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_message = f"ужо працую {hours:02}:{minutes:02}:{seconds:02}."
    bot.reply_to(message, uptime_message)


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
