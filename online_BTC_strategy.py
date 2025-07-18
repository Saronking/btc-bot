import asyncio
import yfinance as yf
from telegram import Bot
import os
from flask import Flask

# Dummy Flask app to keep Render happy
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running."

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = 6170049666

async def send_btc_signals():
    bot = Bot(token=BOT_TOKEN)
    prev_price = None
    running_pct = 0.0

    while True:
        btc = yf.Ticker("BTC-USD")
        price = btc.info.get("regularMarketPrice")

        if price:
            if prev_price is None:
                msg = f"BTC: ${price:.2f} — First reading.\nRunning total: {running_pct:.2f}%"
            else:
                pct_change = ((price - prev_price) / prev_price) * 100
                running_pct += pct_change

                gain_loss_line = f"Previous trade: {pct_change:+.2f}%"
                if price > prev_price:
                    signal_line = f"📈 Buy Signal (Price ↑ from ${prev_price:.2f})"
                elif price < prev_price:
                    signal_line = f"📉 Sell Signal (Price ↓ from ${prev_price:.2f})"
                else:
                    signal_line = f"➖ Hold (No change)"

                msg = (
                    f"BTC: ${price:.2f}\n"
                    f"{gain_loss_line}\n"
                    f"{signal_line}\n"
                    f"Running total: {running_pct:.2f}%"
                )
            prev_price = price
        else:
            msg = "Failed to fetch BTC price."

        await bot.send_message(chat_id=USER_ID, text=msg)
        await asyncio.sleep(300)

# Start the bot loop in the background
def start_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(send_btc_signals())

start_bot()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
