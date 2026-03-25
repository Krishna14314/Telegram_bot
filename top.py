import requests
from bs4 import BeautifulSoup
import datetime

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "8680978500:AAGGna0fqxdxKiDrHo-VB6FWPgNk-Reba40"
CHAT_ID = "5634233006"   # un chat id

# 🔎 Job Scraper
def get_jobs():
    url = "https://www.tnpsc.gov.in/notifications"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    jobs = []
    for link in soup.find_all("a"):
        text = link.text.strip()
        href = link.get("href")

        if text and "Notification" in text:
            jobs.append(f"{text}\nhttps://www.tnpsc.gov.in{href}")

    return jobs[:5]

# 🤖 Auto Reply
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()

    if "job" in user_text:
        jobs = get_jobs()

        if jobs:
            msg = "🔥 Latest TNPSC Jobs:\n\n"
            for job in jobs:
                msg += f"👉 {job}\n\n"
        else:
            msg = "😔 No jobs found"

    else:
        msg = "Type 'job' nu anupu da 😄"

    await update.message.reply_text(msg)

# ⏰ Daily Auto Send
async def send_daily(context: ContextTypes.DEFAULT_TYPE):
    jobs = get_jobs()

    if jobs:
        msg = "🔥 Daily TNPSC Jobs:\n\n"
        for job in jobs:
            msg += f"👉 {job}\n\n"
    else:
        msg = "😔 No jobs today"

    await context.bot.send_message(chat_id=CHAT_ID, text=msg)

# 🚀 Main
app = ApplicationBuilder().token(TOKEN).build()

# Auto reply handler
app.add_handler(MessageHandler(filters.TEXT, reply))

# ⏰ Daily 9 AM
app.job_queue.run_daily(send_daily, time=datetime.time(hour=9, minute=0))

print("🤖 Bot running da...")

app.run_polling()