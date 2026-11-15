import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# --- SIFRELERINIZI BURAYA YAZIN ---
TELEGRAM_BOT_TOKEN = "9095217892:AAFJ5RoTiqD03w9CktFq4KVxfkilres532M"
GEMINI_API_KEY = "AQ.Ab8RN6IfIVswKyuSS6J-bHbPZ5yX_JFu8hpgExQfBTJa3pHoRw"
# ----------------------------------

# Google Gemini modelini ayarl?yoruz
genai.configure(api_key=GEMINI_API_KEY)

system_instruction = (
    "Sen ogrenciler icin uzman bir ozel ders ogretmenisin ve ayn? zamanda guvenilir "
    "akademik kaynak/kitap bulucusun. Ogrencilerin ders sorular?n? ad?m ad?m, anlas?l?r "
    "sekilde coz. Onlar?n istedigi ders kitaplar?, kaynak onerileri veya konu ozetleri "
    "hakk?nda rehberlik et. Egitici, tesvik edici ve net bir dil kullan."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.effective_user.first_name
    
    wait_message = await update.message.reply_text(f"?? Merhaba {user_name}, sorunuzu inceliyorum, lutfen bekleyin...")

    try:
        response = model.generate_content(user_message)
        bot_reply = response.text
        
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_message.message_id)
        await update.message.reply_text(bot_reply)

    except Exception as e:
        await update.message.reply_text(f"Uzgunum, bir hata olustu: {str(e)}")

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(echo_handler)
    
    print("?? Bot cal?smaya haz?r!")
    application.run_polling()

if name == "__main__":
    main()