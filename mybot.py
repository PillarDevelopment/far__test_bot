import logging
from datetime import datetime, timedelta
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from tabulate import tabulate

# Настройки бота
TOKEN = "____"
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I am a bot for analyzing crypto token diamond hands.\n"
        "Just send me the token name (eg: USDT or LINK) and I will show you the top holders with 'diamond hands''!"
    )

async def analyze_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = update.message.text.upper()
    await update.message.reply_text(f"🔍 analyzing {token}...")

    # generate test data
    holders = generate_mock_holders(100)
    calculate_diamond_score(holders)
    top_holders = sorted(holders, key=lambda x: x['score'], reverse=True)[:10]

    # Formatting results
    results = format_results(top_holders)

    # Submitting results
    await update.message.reply_text(
        f"🏆 top-10 holder {token} with 'diamond hands':\n"
        f"<pre>{results}</pre>",
        parse_mode='HTML'
    )

def generate_mock_holders(num):
    holders = []
    for _ in range(num):
        holders.append({
            'address': '0x' + ''.join(random.choices('0123456789abcdef', k=10)),
            'balance': random.uniform(1000, 1000000),
            'first_transaction': datetime.now() - timedelta(days=random.randint(30, 730))
        })
    return holders

def calculate_diamond_score(holders):
    balances = [h['balance'] for h in holders]
    durations = [(datetime.now() - h['first_transaction']).days for h in holders]

    max_balance = max(balances) if balances else 1
    min_balance = min(balances) if balances else 0
    max_duration = max(durations) if durations else 1
    min_duration = min(durations) if durations else 0

    for holder in holders:
        norm_balance = (holder['balance'] - min_balance) / (max_balance - min_balance) if (max_balance - min_balance) != 0 else 0
        norm_duration = ((datetime.now() - holder['first_transaction']).days - min_duration) / (max_duration - min_duration) if (max_duration - min_duration) != 0 else 0

        holder['score'] = round((norm_balance * 0.7 + norm_duration * 0.3) * 100, 2)
        holder['days_held'] = (datetime.now() - holder['first_transaction']).days

def format_results(data):
    table = []
    for i, holder in enumerate(data, 1):
        table.append([
            i,
            holder['address'],
            f"{holder['balance']:,.0f}",
            holder['days_held'],
            f"{holder['score']}%"
        ])
    return tabulate(table,
                  headers=["#", "Адрес", "Баланс", "Дней", "Рейтинг"],
                  tablefmt="simple_grid",
                  numalign="right")

def main():
    app = Application.builder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_token))

    # run
    logging.info("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
