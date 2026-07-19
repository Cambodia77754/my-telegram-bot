import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import yt_dlp

# ការកំណត់ Logging
logging.basicConfig(level=logging.INFO)
TOKEN = "8830743228:AAE55qWmpkXYmmJ90OjD4hdaIquzlpuaHSI"

# កំណត់ដំណាក់កាល
LANG_SELECT = 1

# ល្បឿនទាញយកអតិបរមា
def get_ydl_opts(lang):
    return {
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
        'quiet': True,
        'concurrent_fragment_downloads': 20,
        'http_chunk_size': 10485760,
        'writesubtitles': True,
        'subtitleslangs': [lang], # ជ្រើសរើសភាសាដែលអ្នកចង់បាន
        'writeautomaticsub': True,
        'outtmpl': '%(title)s.%(ext)s',
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇰🇭 ខ្មែរ (Khmer)", callback_data='km')],
        [InlineKeyboardButton("🇬🇧 អង់គ្លេស (English)", callback_data='en')]
    ]
    await update.message.reply_text("សូមជ្រើសរើសភាសាសម្រាប់វីដេអូរបស់អ្នក៖", reply_markup=InlineKeyboardMarkup(keyboard))
    return LANG_SELECT

async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    lang = query.data
    context.user_data['lang'] = lang
    await query.answer()
    await query.edit_message_text(f"អ្នកបានជ្រើសរើសភាសា៖ {'🇰🇭 ខ្មែរ' if lang == 'km' else '🇬🇧 អង់គ្លេស'}\n\nសូមផ្ញើ Link វីដេអូមក៖")
    return 2 # ទៅកាន់ដំណាក់កាលរង់ចាំ Link

async def handle_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    lang = context.user_data.get('lang', 'en')
    status_msg = await update.message.reply_text("កំពុងទាញយកយ៉ាងលឿន... 🚀")
    
    try:
        with yt_dlp.YoutubeDL(get_ydl_opts(lang)) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        await update.message.reply_video(video=open(filename, 'rb'))
        if os.path.exists(filename): os.remove(filename)
        await status_msg.delete()
    except Exception as e:
        await update.message.reply_text(f"មានបញ្ហា៖ {e}")
    return 2

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANG_SELECT: [CallbackQueryHandler(set_lang)],
            2: [MessageHandler(filters.TEXT & (~filters.COMMAND), handle_download)]
        },
        fallbacks=[CommandHandler('start', start)]
    )
    
    application.add_handler(conv_handler)
    application.run_polling()
