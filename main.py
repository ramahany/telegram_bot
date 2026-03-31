import asyncio
from telebot.async_telebot import AsyncTeleBot
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
# bot = telebot.TeleBot(token=bot_settings.BOT_TOKEN)
bot = AsyncTeleBot(token= bot_settings.BOT_TOKEN)
all_hist = defaultdict(create_inner_dict)

@bot.message_handler(commands=['hello']) # / + command
async def send_welcome(message:Message): 
    await bot.reply_to(
        message=message,
        text=f"hello, I am a CHAT BOT created by the most spactacular, amazing woman on planet earth.\nher name is r4m4 you would love to know her, but she doesn't like talking to human beings."
    )
@bot.message_handler(commands=['start']) # / + command
async def send_welcome(message:Message): 
    await bot.reply_to(
        message=message,
        text=f"Hello, I am IdeaPop, I am an AI chatbot created by r4m4"
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text="I'm here to assist you with your late-night ideas and help you structure a plan and ask you clarifying questions. If you want to start, state your idea anytime."
    )
@bot.message_handler(func= lambda message: True)
async def groq_response(message:Message): 

    curr_time = datetime.today()

    if  is_session_expired(all_hist[message.chat.id]["last_active"], curr=curr_time, threshold=6): 
        all_hist[message.chat.id]["hist"] = []

    all_hist[message.chat.id]["last_active"] = curr_time    

    all_hist[message.chat.id]["hist"].append({
        "role": "user",
        "content":message.text
    })

    all_hist[message.chat.id]["hist"] = await client.responce_with_local_tools(hist=all_hist[message.chat.id]["hist"])
    groq_response = all_hist[message.chat.id]["hist"][-1].content
    await bot.reply_to(
        message=message, 
        text=groq_response[:4000]
    )


if __name__ == '__main__':
    logger.info("bot is running ......")
    print("bot is running ...")
    asyncio.run(bot.infinity_polling())

