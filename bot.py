# Gerekli kütüphaneleri yüklüyoruz
!pip install python-telegram-bot google-generativeai nest_asyncio -q

import os
import asyncio
import nest_asyncio
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# nest_asyncio'yu aktif hale getiriyoruz (Jupyter/Colab için zorunludur)
nest_asyncio.apply()

# Şifreleriniz
TELEGRAM_BOT_TOKEN = "9095217892:AAFJ5RoTiqD03w9CktFq4KVxfkilres532M"
GEMINI_API_KEY = "AQ.Ab8RN6IfIVswKyuSS6J-bHbPZ5yX_JFu8hpgExQfBTJa3pHoRw"

# Google Gemini modelini ayarlıyoruz
genai.configure(api_key=GEMINI_API_KEY)

system_instruction = (
    "Sen öğrenciler için uzman bir özel ders öğretmenisin ve aynı zamanda güvenilir "
    "akademik kaynak/kitap bulucusun. Öğrencilerin ders sorularını adım adım, anlaşılır "
    "şekilde çöz. Onların istediği ders kitapları, kaynak önerileri veya konu özetleri "
    "hakkında rehberlik et. Eğitici, teşvik edici ve net bir dil kullan."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.effective_user.first_name

    wait_message = await update.message.reply_text(f"📚 Merhaba {user_name}, sorunuzu inceliyorum, lütfen bekleyin...")

    try:
        response = model.generate_content(user_message)
        bot_reply = response.text

        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_message.message_id)
        await update.message.reply_text(bot_reply)

    except Exception as e:
        await update.message.reply_text(f"Üzgünüm, bir hata oluştu: {str(e)}")

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(echo_handler)

    print("🤖 Bot çalışmaya hazır ve aktif!")
    # Jupyter ortamında hata vermemesi için close_loop=False yapıyoruz
    application.run_polling(close_loop=False)

if name == "__main__":
    main()