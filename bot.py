from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import json, time, os

BOT_TOKEN = os.getenv("8756023029:AAFyJolQVNcz6X84rhh-ffyHj7CK-X4drkM")
ADMIN_ID = 5924662015

DB = "data.json"

def load():
    try:
        return json.load(open(DB))
    except:
        return {}

def save(data):
    json.dump(data, open(DB, "w"))

def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Points", callback_data="p")],
        [InlineKeyboardButton("🎁 Bonus", callback_data="b")],
        [InlineKeyboardButton("🏆 Top 20", callback_data="l")]
    ])

def back():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back", callback_data="back")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    d = load()
    uid = str(u.id)

    if uid not in d:
        d[uid] = {"name": u.first_name, "points": 10, "bonus": 0}
        save(d)

    await update.message.reply_text("Welcome 🎉", reply_markup=menu())

async def click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = load()
    uid = str(q.from_user.id)

    if q.data == "p":
        await q.edit_message_text(f"Points: {d[uid]['points']}", reply_markup=back())

    elif q.data == "b":
        now = int(time.time())
        if now - d[uid]["bonus"] > 86400:
            d[uid]["points"] += 20
            d[uid]["bonus"] = now
            save(d)
            msg = "20 points added 🎁"
        else:
            msg = "Already claimed ❌"
        await q.edit_message_text(msg, reply_markup=back())

    elif q.data == "l":
        s = sorted(d.items(), key=lambda x: x[1]["points"], reverse=True)
        text = "🏆 Top 20:\\n"
        for i, (uid, info) in enumerate(s[:20], 1):
            text += f"{i}. {info['name']} - {info['points']}\\n"
        await q.edit_message_text(text, reply_markup=back())

    elif q.data == "back":
        await q.edit_message_text("Menu 🔙", reply_markup=menu())

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        uid = context.args[0]
        amt = int(context.args[1])
        d = load()
        d[uid]["points"] += amt
        save(d)
        await update.message.reply_text("Added ✅")
    except:
        await update.message.reply_text("Error ❌")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CallbackQueryHandler(click))

print("Bot Running...")
app.run_polling()
