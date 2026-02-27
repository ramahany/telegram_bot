import telebot 
from telebot.types import Message
from helpers.config import get_settings
from llm import GroqClient
from collections import defaultdict
import logging

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
logger = logging.getLogger("telegram_bot_log")

bot_settings = get_settings()
client = GroqClient(api_key=bot_settings.GROQ_API_KEY)
bot = telebot.TeleBot(token=bot_settings.BOT_TOKEN)
all_hist = defaultdict(list)

@bot.message_handler(commands=['hello']) # / + command
def send_welcome(message:Message): 
    bot.reply_to(
        message=message,
        text=f"hello, I am a BOT created by the most spactcaular, amazing woman on planet earth.\n her name is r4m4 you would love to know her, but she doesn't like talking to human beings so NO."
    )

@bot.message_handler(func= lambda message: True)
def groq_response(message:Message): 
    all_hist[message.chat.id].append({
        "role": "user",
        "content":message.text
    })

    groq_response = client.response(hist=all_hist[message.chat.id])

    all_hist[message.chat.id].append({
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
    bot.infinity_polling()
    