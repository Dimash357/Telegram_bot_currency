import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Список криптовалютных символов
    cryptocurrencies = ['bitcoin', 'ethereum', 'litecoin']

    # Отправляем запрос к API CoinGecko для получения данных о курсах криптовалют
    response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={",".join(cryptocurrencies)}&vs_currencies=usd')
    if response.status_code == 200:
        data = response.json()
        message = "Current prices:\n"
        for cryptocurrency in cryptocurrencies:
            if cryptocurrency in data:
                price = data[cryptocurrency]['usd']
                message += f"{cryptocurrency.capitalize()}: ${price}\n"
            else:
                message += f"{cryptocurrency.capitalize()}: N/A\n"
    else:
        message = "Failed to fetch cryptocurrency prices"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


if __name__ == '__main__':
    application = ApplicationBuilder().token('6092154327:AAE94d0G6eJ-fQTIDX4P9qwrBXPL-tEEtyw').build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()
