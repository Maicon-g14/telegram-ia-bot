import asyncio
import telegram
import os


async def main():
    bot = telegram.Bot(os.environ['TELEGRAM_TOKEN'])
    async with bot:
        #print((await bot.get_updates())[0])
        await bot.send_message(text='Hayoo! Koma-chan R3b0rns', chat_id=os.environ['TELEGRAM_USER_ID'])


if __name__ == '__main__':
    asyncio.run(main())