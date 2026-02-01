import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# تحميل المتغيرات البيئية
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
GROQ_MODEL = os.getenv("GROQ_MODEL")

# إعداد الـ Groq client
client = Groq(api_key=GROQ_API_KEY)

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# نظام الذاكرة (Memory) - بسيط في الذاكرة حالياً (In-memory)
# في الإنتاج يفضل استخدام قاعدة بيانات مثل Redis أو SQLite
user_memory = {}

SYSTEM_PROMPT = "مساعد تقني وتنفيذي ذكي جداً من تطوير المهندس صلاح الوافي."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # تنبيه الأدمن عند دخول مستخدم جديد
    if user_id not in user_memory:
        user_memory[user_id] = []
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"🔔 مستخدم جديد بدأ البوت!\n\nالاسم: {user.full_name}\nاليوزر: @{user.username}\nالأيدي: {user_id}"
            )
        except Exception as e:
            logging.error(f"Error sending admin alert: {e}")

    welcome_text = f"مرحباً {user.first_name}! أنا S-Core، مساعدك الذكي. كيف يمكنني مساعدتك اليوم؟"
    await update.message.reply_text(welcome_text)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_input = update.message.text

    if user_id not in user_memory:
        user_memory[user_id] = []

    # إضافة رسالة المستخدم للذاكرة
    user_memory[user_id].append({"role": "user", "content": user_input})
    
    # الحفاظ على آخر 10 رسائل فقط لتوفير التوكنز
    if len(user_memory[user_id]) > 10:
        user_memory[user_id] = user_memory[user_id][-10:]

    try:
        # إرسال الطلب لـ Groq
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + user_memory[user_id]
        
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
        )
        
        bot_response = response.choices[0].message.content
        
        # إضافة رد البوت للذاكرة
        user_memory[user_id].append({"role": "assistant", "content": bot_response})
        
        await update.message.reply_text(bot_response)
        
    except Exception as e:
        logging.error(f"Error calling Groq API: {e}")
        await update.message.reply_text("عذراً، حدث خطأ أثناء معالجة طلبك.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    chat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chat)
    
    application.add_handler(start_handler)
    application.add_handler(chat_handler)
    
    print("S-Core Bot is running...")
    application.run_polling()
