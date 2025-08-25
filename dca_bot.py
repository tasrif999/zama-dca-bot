import ccxt
import schedule
import time
import os
from dotenv import load_dotenv
import random

# Load API keys safely
load_dotenv()
api_key = os.getenv('BYBIT_API_KEY')
api_secret = os.getenv('BYBIT_API_SECRET')

# Connect to Bybit testnet
exchange = ccxt.bybit({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'testnet': True
})

# Simple fake encryption (mimics Zama's FHE for learning)
def fake_encrypt(amount):
    key = 12345  # Pretend secret key (not real encryption)
    return amount * key  # "Encrypt" by multiplying

def fake_decrypt(encrypted_amount):
    key = 12345
    return encrypted_amount / key  # "Decrypt" by dividing

# Batch orders with fake users
def batch_orders(my_amount):
    # Your order
    my_encrypted = fake_encrypt(my_amount)
    print(f"Your encrypted amount: {my_encrypted}")

    # Fake users' orders (random amounts for demo)
    fake_user1 = fake_encrypt(random.uniform(5, 15))  # $5-$15
    fake_user2 = fake_encrypt(random.uniform(5, 15))
    batch_encrypted = my_encrypted + fake_user1 + fake_user2
    print(f"Batched encrypted total: {batch_encrypted}")

    # Decrypt total for trading
    batch_total = fake_decrypt(batch_encrypted)
    print(f"Decrypted batch total: ${batch_total:.2f}")
    return batch_total

# Buy Bitcoin function
def buy_bitcoin():
    try:
        symbol = 'BTC/USDT'
        my_amount = 10  # Your $10 buy
        batch_amount = batch_orders(my_amount)  # Batch with fake users
        ticker = exchange.fetch_ticker(symbol)
        price = ticker['last']
        amount_btc = batch_amount / price  # Buy for the whole batch
        order = exchange.create_market_buy_order(symbol, amount_btc)
        print(f"Bought {amount_btc:.6f} BTC at ${price:.2f} on {time.ctime()}")
    except Exception as e:
        print(f"Error: {e}")

# Run every day at 9 AM
schedule.every().day.at("09:00").do(buy_bitcoin)

# Start the bot
print("Zama-inspired DCA Bot started. Waiting for buys...")
while True:
    schedule.run_pending()
    time.sleep(60)
    