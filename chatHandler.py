import os
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes
import openai

openai.api_key = os.getenv("OPEN_AI_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    length = 4097 - len(update.message.text)

    if length <= 0:
        print("Request too big! Please consider breaking it into multiple parts.")
        return

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=update.message.text,
        max_tokens=length,
        temperature=0.6,
    )
    print("Prompt: " + update.message.text)
    print("Response: " + response.choices[0].text)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response.choices[0].text
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
