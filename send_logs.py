import telebot 
import datetime
import os

from config import TOKEN, ID_CHAT_REPORTS


bot = telebot.TeleBot(TOKEN)

def send_logs():
    PATH_LOG_INFO = "/root/.pm2/logs/main-out.log"
    PATH_LOG_ERR = "/root/.pm2/logs/main-error.log"
    try:
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        with open(PATH_LOG_INFO, 'rb') as f:
            bot.send_document(ID_CHAT_REPORTS, f, caption=f"Логи за {yesterday}")

        with open(PATH_LOG_ERR, 'rb') as f:
            bot.send_document(696906752, f, caption=f"Логи ошибок за {yesterday}")

        os.system("pm2 flush")
        return True
    except Exception as e:
        print(f"Ошибка при отправке логов: {str(e)}")
        return False
    
def send_logs_today():
    PATH_LOG_INFO = "/root/.pm2/logs/main-out.log"
    try:
        with open(PATH_LOG_INFO, 'rb') as f:
            bot.send_document(ID_CHAT_REPORTS, f, caption=f"Логи на сегодня")
        return True
    except Exception as e:
        print(f"Ошибка при отправке логов: {str(e)}")
        return False