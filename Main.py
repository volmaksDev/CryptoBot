import requests
import time
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv
import os

load_dotenv()

# Налаштування токена бота Telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Ініціалізація бота
bot = Bot(token=TELEGRAM_TOKEN)

# Функція для отримання поточної ціни з Binance
def get_binance_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return float(data['price'])
    else:
        print(f"Binance API error: {response.status_code}")
        return None

# Функція для отримання всіх торгових пар з Binance
def get_binance_symbols():
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            symbols = [item['symbol'] for item in data]
            return symbols
        except requests.exceptions.JSONDecodeError:
            print("Помилка декодування JSON з Binance")
            return []
    else:
        print(f"Binance API error: {response.status_code}")
        return []

# Функція для отримання поточної ціни з KuCoin
def get_kucoin_price(symbol):
    url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            return float(data['data']['price'])
        except requests.exceptions.JSONDecodeError:
            print(f"Помилка декодування JSON для {symbol} з KuCoin")
            return None
    else:
        print(f"KuCoin API error: {response.status_code}")
        return None

# Функція для отримання всіх торгових пар з KuCoin
def get_kucoin_symbols():
    url = "https://api.kucoin.com/api/v1/symbols"
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            data = response.json()
            symbols = [item['symbol'] for item in data['data']]
            return symbols
        except requests.exceptions.JSONDecodeError:
            print("Помилка декодування JSON з KuCoin")
            return []
    else:
        print(f"KuCoin API error: {response.status_code}")
        return []

# Функція для надсилання повідомлення в Telegram
def send_telegram_message(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

# Функція для моніторингу всіх популярних монет
def monitor_prices(interval=60):
    # Отримати список монет з Binance і KuCoin
    binance_symbols = get_binance_symbols()
    kucoin_symbols = get_kucoin_symbols()

    # Створимо словники для зберігання попередніх цін
    prev_binance_prices = {symbol: get_binance_price(symbol) for symbol in binance_symbols}
    prev_kucoin_prices = {symbol: get_kucoin_price(symbol) for symbol in kucoin_symbols}

    while True:
        time.sleep(interval)
        
        print(f"Моніторинг за інтервалом {interval} секунд:")

        # Моніторинг монет на Binance
        for symbol in binance_symbols:
            current_price = get_binance_price(symbol)
            if current_price is None:
                continue
            prev_price = prev_binance_prices[symbol]

            if current_price > prev_price:
                message = f"Binance: Ціна {symbol} виросла з {prev_price} до {current_price}"
                print(message)
                send_telegram_message(message)
            elif current_price < prev_price:
                message = f"Binance: Ціна {symbol} впала з {prev_price} до {current_price}"
                print(message)
                send_telegram_message(message)
            else:
                print(f"Binance: Ціна {symbol} не змінилась")

            # Оновити попередню ціну
            prev_binance_prices[symbol] = current_price

        # Моніторинг монет на KuCoin
        for symbol in kucoin_symbols:
            current_price = get_kucoin_price(symbol)
            if current_price is None:
                continue
            prev_price = prev_kucoin_prices[symbol]

            if current_price > prev_price:
                message = f"KuCoin: Ціна {symbol} виросла з {prev_price} до {current_price}"
                print(message)
                send_telegram_message(message)
            elif current_price < prev_price:
                message = f"KuCoin: Ціна {symbol} впала з {prev_price} до {current_price}"
                print(message)
                send_telegram_message(message)
            else:
                print(f"KuCoin: Ціна {symbol} не змінилась")

            # Оновити попередню ціну
            prev_kucoin_prices[symbol] = current_price

# Виклик функції для моніторингу популярних монет кожні 60 секунд
monitor_prices(interval=5)
