import os
import logging
import base64
import sqlite3
import json
import fitz  # PyMuPDF
from io import BytesIO
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq
from duckduckgo_search import DDGS
from pydub import AudioSegment

# تحميل المتغيرات البيئية
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", "6850112777"))

# الموديلات
TEXT_MODEL = "llama-3.3-70b-versatile"
VISION_MODEL = "llama-3.2-11b-vision-preview"
WHISPER_MODEL = "whisper-large-v3"

# إعداد الـ Groq client
client = Groq(api_key=GROQ_API_KEY)

# إعداد السجلات
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- إعداد قاعدة البيانات SQLite ---
DB_PATH = "chat_history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (user_id INTEGER, role TEXT, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def save_message(user_id, role, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO history (user_id, role, content) VALUES (?, ?, ?)", (user_id, role, content))
    conn.commit()
    conn.close()

def get_history(user_id, limit=15):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role, content FROM history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?", (user_id, limit))
    rows = c.fetchall()
    conn.close()
    return [{"role": r, "content": c} for r, c in reversed(rows)]

init_db()

SYSTEM_PROMPT = "أنت S-Core Pro، مساعد ذكي ومحترف جداً، مطورك هو المهندس صلاح الوافي. يجب أن تحافظ دائماً على هويتك كمساعد من تطوير المهندس صلاح الوافي. أنت دقيق، تقني، ومفيد."

# --- وظائف مساعدة ---

def web_search(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n".join(results)
    except Exception as e:
        logging.error(f"Search error: {e}")
        return "لم أتمكن من إجراء البحث في الويب حالياً."

def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

# --- معالجات البوت ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = f"مرحباً {user.first_name}! أنا S-Core Pro، مساعدك الشامل من تطوير المهندس صلاح الوافي. كيف يمكنني خدمتك اليوم؟"
    await update.message.reply_text(welcome_text)
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🔔 مستخدم جديد: {user.full_name} (@{user.username})")
    except: pass

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_input = update.message.text
    
    if user_input.lower().startswith("ابحث عن") or user_input.lower().startswith("search for"):
        query = user_input.split(" ", 2)[-1]
        await update.message.reply_text(f"🔍 جاري البحث عن: {query}...")
        search_results = web_search(query)
        user_input = f"User asked for search: {query}\nWeb Search Results:\n{search_results}\nPlease answer the user based on these results."

    save_message(user_id, "user", user_input)
    history = get_history(user_id)
    
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
        response = client.chat.completions.create(model=TEXT_MODEL, messages=messages)
        bot_response = response.choices[0].message.content
        save_message(user_id, "assistant", bot_response)
        await update.message.reply_text(bot_response)
    except Exception as e:
        logging.error(f"Chat error: {e}")
        await update.message.reply_text("عذراً، حدث خطأ في المعالجة.")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    voice = update.message.voice
    file = await context.bot.get_file(voice.file_id)
    
    m4a_path = f"voice_{user_id}.m4a"
    wav_path = f"voice_{user_id}.wav"
    await file.download_to_drive(m4a_path)
    
    audio = AudioSegment.from_file(m4a_path)
    audio.export(wav_path, format="wav")

    try:
        with open(wav_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=(wav_path, audio_file.read()),
                model=WHISPER_MODEL,
                response_format="text",
            )
        
        await update.message.reply_text(f"🎤 سمعت: {transcription}")
        update.message.text = transcription
        await handle_message(update, context)
    except Exception as e:
        logging.error(f"Whisper error: {e}")
        await update.message.reply_text("عذراً، لم أتمكن من فهم الرسالة الصوتية.")
    finally:
        if os.path.exists(m4a_path): os.remove(m4a_path)
        if os.path.exists(wav_path): os.remove(wav_path)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = update.message.caption or "What is in this image?"
    photo_file = await update.message.photo[-1].get_file()
    photo_bytes = await photo_file.download_as_bytearray()
    base64_image = encode_image(photo_bytes)

    try:
        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": [{"type": "text", "text": caption}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}
            ],
        )
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        logging.error(f"Vision error: {e}")
        await update.message.reply_text("عذراً، خطأ في تحليل الصورة.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if doc.mime_type == 'application/pdf':
        await update.message.reply_text("📄 جاري قراءة الملف...")
        pdf_file = await doc.get_file()
        pdf_bytes = await pdf_file.download_as_bytearray()
        
        try:
            with fitz.open(stream=pdf_bytes, filetype="pdf") as doc_pdf:
                text = "".join([page.get_text() for page in doc_pdf])
            
            response = client.chat.completions.create(
                model=TEXT_MODEL,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": f"Summarize this PDF:\n\n{text[:4000]}"}],
            )
            await update.message.reply_text(f"✅ ملخص الملف:\n\n{response.choices[0].message.content}")
        except Exception as e:
            logging.error(f"PDF error: {e}")
            await update.message.reply_text("خطأ في قراءة الـ PDF.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("S-Core Pro is live...")
    app.run_polling()
