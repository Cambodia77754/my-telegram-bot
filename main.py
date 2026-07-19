import os
import yt_dlp
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '8981729970:AAEQtZLqHKr40v_Xj3ZHQo_dq-Vp1W-i7dQ'
# មុខងារសម្រាប់ប៊ូតុងស្អាតៗ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📥 ទាញយកវីដេអូ", "📢 ចូលរួមឆានែល"],
        ["💡 របៀបប្រើប្រាស់", "💬 ទំនាក់ទំនង"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "✨ សួស្តី! សូមជ្រើសរើសមុខងារដែលអ្នកចង់ប្រើ៖",
        reply_markup=reply_markup
    )

# មុខងារគ្រប់គ្រងប៊ូតុង
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "📢 ចូលរួមឆានែល":
        await update.message.reply_text("👉 ចុចទីនេះដើម្បីចូលរួម៖ https://t.me/LYMOCAMBO_PC")
    
    elif text == "💡 របៀបប្រើប្រាស់":
        await update.message.reply_text("គ្រាន់តែផ្ញើលីង TikTok ឬ Facebook មកខ្ញុំ ខ្ញុំនឹងទាញយកជូនភ្លាមៗ!")
        
    elif text == "💬 ទំនាក់ទំនង":
        await update.message.reply_text("មានបញ្ហា? សូមទំនាក់ទំនងមកកាន់៖ @LYMOCAMBO_PC")
        
    else:
        # បើវាមិនមែនជាប៊ូតុងទេ គឺសន្មត់ថាជាលីងវីដេអូ
        await download_media(update, context)

# មុខងារទាញយកវីដេអូ
async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    status_msg = await update.message.reply_text("⏳ កំពុងទាញយក... សូមរង់ចាំបន្តិច!")
    
    ydl_opts = {'outtmpl': 'video.mp4', 'format': 'best'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)
        await update.message.reply_video(video=open('video.mp4', 'rb'))
        await status_msg.delete()
        os.remove('video.mp4')
    except Exception as e:
        await status_msg.edit_text(f"❌ មានបញ្ហា៖ {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot កំពុងដំណើរការហើយ...")
    app.run_polling()
