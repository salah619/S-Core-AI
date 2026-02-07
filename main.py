import os
import logging
import base64
import fitz  # PyMuPDF
from io import BytesIO
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# تحميل المتغيرات البيئية
load_dotenv()
def get_env(name: str, required=True, cast=None):
    value = os.getenv(name)
    if required and not value:
        raise RuntimeError(f"Environment variable {name} is missing")
    if cast and value:
        return cast(value)
    return value


# =========================
# المتغيرات
# =========================
TELEGRAM_TOKEN = get_env("TELEGRAM_TOKEN")
GROQ_API_KEY = get_env("GROQ_API_KEY")
ADMIN_ID = get_env("ADMIN_ID", cast=int)
TAVILY_API_KEY = get_env("TAVILY_API_KEY", required=False)

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
# الموديلات المطلوبة
TEXT_MODEL = "llama-3.3-70b-versatile"
VISION_MODEL = "llama-3.2-11b-vision-preview"

# إعداد الـ Groq client
client = Groq(api_key=GROQ_API_KEY)

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# نظام الذاكرة (Memory) - تخزين آخر 15 رسالة لكل مستخدم
user_memory = {}
MEMORY_LIMIT = 15

SYSTEM_PROMPT = "You are S-Core, a professional AI assistant developed by Engineer Salah Al-Wafi. You are helpful, technical, and precise."

def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    if user_id not in user_memory:
        user_memory[user_id] = []
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"🔔 مستخدم جديد بدأ البوت!\n\nالاسم: {user.full_name}\nاليوزر: @{user.username}\nالأيدي: {user_id}"
            )
        except Exception as e:
            logging.error(f"Error sending admin alert: {e}")

    welcome_text = f"مرحباً {user.first_name}! أنا S-Core، مساعدك الذكي المتطور. يمكنني الآن فهم الصور وقراءة ملفات PDF. كيف أساعدك؟"
    await update.message.reply_text(welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_input = update.message.text
    
    if user_id not in user_memory:
        user_memory[user_id] = []

    # إضافة رسالة المستخدم للذاكرة
    user_memory[user_id].append({"role": "user", "content": user_input})
    if len(user_memory[user_id]) > MEMORY_LIMIT:
        user_memory[user_id] = user_memory[user_id][-MEMORY_LIMIT:]

    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + user_memory[user_id]
        response = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=messages,
        )
        bot_response = response.choices[0].message.content
        user_memory[user_id].append({"role": "assistant", "content": bot_response})
        await update.message.reply_text(bot_response)
    except Exception as e:
        logging.error(f"Error in text chat: {e}")
        await update.message.reply_text("عذراً، حدث خطأ أثناء معالجة طلبك.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    caption = update.message.caption or "What is in this image?"
    
    photo_file = await update.message.photo[-1].get_file()
    photo_bytes = await photo_file.download_as_bytearray()
    base64_image = encode_image(photo_bytes)

    try:
        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": caption},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                }
            ],
        )
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        logging.error(f"Error in vision: {e}")
        await update.message.reply_text("عذراً، لم أتمكن من تحليل هذه الصورة.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if doc.mime_type == 'application/pdf':
        await update.message.reply_text("جاري قراءة ملف PDF وتلخيصه، انتظر لحظة...")
        
        pdf_file = await doc.get_file()
        pdf_bytes = await pdf_file.download_as_bytearray()
        
        try:
            # قراءة الـ PDF باستخدام PyMuPDF
            with fitz.open(stream=pdf_bytes, filetype="pdf") as doc_pdf:
                text = ""
                for page in doc_pdf:
                    text += page.get_text()
            
            # تلخيص النص (نأخذ أول 4000 حرف لتجنب تجاوز حدود الموديل)
            summary_prompt = f"Please summarize the following PDF content precisely:\n\n{text[:4000]}"
            
            response = client.chat.completions.create(
                model=TEXT_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": summary_prompt}
                ],
            )
            await update.message.reply_text(f"📄 تلخيص الملف:\n\n{response.choices[0].message.content}")
        except Exception as e:
            logging.error(f"Error in PDF processing: {e}")
            await update.message.reply_text("عذراً، حدث خطأ أثناء قراءة ملف PDF.")
    else:
        await update.message.reply_text("حالياً، يمكنني معالجة ملفات PDF فقط.")

if __name__ == '__main__':
    logging.info("Starting S-Core Pro AI Assistant 🚀")
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("S-Core Pro is running...")
    application.run_polling()
