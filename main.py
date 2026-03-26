import telebot 
from telebot.types import Message
from helpers.config import get_settings
from llm import GroqClient
from collections import defaultdict
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("telegram_bot_log")
# hist functions
def create_inner_dict():
    return {"hist":[], "last_active": datetime.today()}

def is_session_expired(last_sesion, curr,threshold): # threshold in hours
    return (curr-last_sesion).total_seconds() // 3600 >= threshold


bot_settings = get_settings()
client = GroqClient()
bot = telebot.TeleBot(token=bot_settings.BOT_TOKEN)
all_hist = defaultdict(create_inner_dict)

@bot.message_handler(commands=['hello']) # / + command
def send_welcome(message:Message): 
    bot.reply_to(
        message=message,
        text=f"hello, I am a CHAT BOT created by the most spactacular, amazing woman on planet earth.\nher name is r4m4 you would love to know her, but she doesn't like talking to human beings."
    )

@bot.message_handler(func= lambda message: True)
def groq_response(message:Message): 

    curr_time = datetime.today()

    if  is_session_expired(all_hist[message.chat.id]["last_active"], curr=curr_time, threshold=6): 
        all_hist[message.chat.id]["hist"] = []

    all_hist[message.chat.id]["last_active"] = curr_time    

    all_hist[message.chat.id]["hist"].append({
        "role": "user",
        "content":message.text
    })

    groq_response = client.response(hist=all_hist[message.chat.id]["hist"])

    all_hist[message.chat.id]["hist"].append({
        "role": "assistant",
        "content":groq_response
    })

    bot.reply_to(
        message=message, 
        text=groq_response[:4000]
    )
    
    # bot.send_message(
    #     chat_id=message.chat.id,
    #     text="done"
    # )

if __name__ == '__main__':
    logger.info("bot is running ...")
    print("bot is running ...")
    bot.infinity_polling()

