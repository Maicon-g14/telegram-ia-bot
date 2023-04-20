import os
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes
import openai
import logger

default_agent = "Your name is White Pixel. You are a helpful and concise assistant."
system_agent = default_agent

openai.api_key = os.getenv("OPEN_AI_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def log_response(prompt, response, user):
    logger.log(prompt, response, user)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome to White Pixel chatbot. I'm a ChatGPT 3.5 based who can:"
             "- Remember things with /remember [prhase to remember]"
             "- Forget your things with /forgetAll"
             "Tip: The most things you remember the lesser space for queues you will have."
    )


async def remember(update: Update, context: ContextTypes.DEFAULT_TYPE):
    system_agent += str(update.message.text)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=system_agent
    )


async def forgetAll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    system_agent = default_agent
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=system_agent
    )


async def chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_agent},
            {"role": "user", "content": update.message.text}
        ]
    )

    if response['choices'][0]['finish_reason'] != 'stop':
        print(response)
        return

    log_response(update.message.text, response['choices'][0]['message']['content'], update.effective_chat.id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response['choices'][0]['message']['content']
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ['TELEGRAM_TOKEN']).build()

    chatgpt_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chatgpt)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(chatgpt_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
