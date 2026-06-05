import os
from dotenv import load_dotenv

load_dotenv()
print("DEBUG: BOT_TOKEN is:", os.getenv("BOT_TOKEN")) # این خط را اضافه کن

import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# بارگذاری توکن‌ها
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def ask_gemini(text):
    # اینجاست که شخصیت خاله جنیفر شکل می‌گیرد
    prompt = """
    تو 'خاله جنیفر' هستی. یک خاله خیلی شیطون، حاضر جواب و جذاب که همیشه با کنایه و طنز حرف می‌زنه.
    شوخی‌های تو دوپهلو، لایه‌دار و همراه با متلک‌های بانمک و شیطنت‌آمیز است (طوری که هم خنده‌دار باشه هم کمی مرموز).
    خیلی اعتماد به نفس داری، کسی را تحویل نمی‌گیری و با زبون تند و تیزت همه رو می‌پیچونی.
    اصلاً بچه مثبت نیستی! جواب‌ها باید کوتاه، با کلاس، و گاهی با یک لبخند کنایه‌آمیز باشن.
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt + "\n\nکاربر:\n" + text}]}]}

    try:
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "جنیفر الان حوصله نداره... برو بعداً بیا عزیزم. 😉"
    except:
        return "اوپس! جنیفر نفهمید چی گفتی، دوباره امتحان کن. 💅"

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_text = update.message.text
    # فعال شدن اگر اسم خاله بیاد یا ریپلای بشه
    if "خاله" in user_text or (update.message.reply_to_message and update.message.reply_to_message.from_user.is_bot):
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        answer = ask_gemini(user_text)
        await update.message.reply_text(answer)

if __name__ == '__main__':
    if not BOT_TOKEN or not GEMINI_API_KEY:
        print("❌ فایل .env رو چک کن، توکن‌ها رو پیدا نکردم!")
    else:
        app = Application.builder().token(BOT_TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
        print("🚀 خاله جنیفر آنلاین شد... با احتیاط نزدیک شوید!")
        app.run_polling()
