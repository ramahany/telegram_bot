import telebot 
from telebot.types import Message
from helpers.config import get_settings
from llm import GroqClient

bot_settings = get_settings()
client = GroqClient(api_key=bot_settings.GROQ_API_KEY)
bot = telebot.TeleBot(token=bot_settings.BOT_TOKEN)

@bot.message_handler(commands=['hello', 'r4m4']) # / + command
def send_welcome(message:Message): 
    print(message)
    bot.reply_to(
        message=message,
        text=f"hello, {message.text}"
    )

@bot.message_handler(func= lambda message: True)
def groq_response(message:Message): 
    bot.reply_to(
        message=message, 
        text=client.response(message.text[:4000])
    )
    # bot.send_message(
    #     chat_id=message.chat.id,
    #     text="done"
    # )

if __name__ == '__main__':
    print("bot is running ...")
    bot.infinity_polling()
    