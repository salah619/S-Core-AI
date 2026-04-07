"""
S-Core Pro AI Assistant - Main Entry Point
Developed by: Eng. Salah Al-Wafi
Version: v2.5.0-Stable
"""

import os
import sys
import logging
from dotenv import load_dotenv

# إضافة المسارات لضمان عمل الاستيراد بشكل سليم في بيئة Termux
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from src.utils.logger import setup_logger
    from src.database.db_manager import DatabaseManager
    from src.core.ai_engine import SCoreEngine
    from src.handlers import messages
    from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
    from telegram.request import HTTPXRequest
except ImportError as e:
    print(f"❌ خطأ في استيراد المكتبات: {e}")
    sys.exit(1)

# تحميل إعدادات البيئة من ملف .env
load_dotenv()

# تهيئة نظام التسجيل الاحترافي
logger = setup_logger()

class SCoreApp:
    def __init__(self):
        self.version = "v2.5.0-Stable"
        try:
            # تهيئة قاعدة البيانات ومحرك الذكاء
            self.db = DatabaseManager()
            self.engine = SCoreEngine(
                api_key=os.getenv("GROQ_API_KEY"),
                text_model="llama-3.3-70b-versatile",
                vision_model="llama-3.2-11b-vision-preview",
                system_prompt="أنت S-Core Pro، مساعد مهني محترف مطورك المهندس صلاح الوافي."
            )
            logger.info(f"--- S-Core {self.version} تم التشغيل بنجاح ---")
        except Exception as e:
            logger.error(f"❌ خطأ أثناء التهيئة: {e}")

    def format_ui(self, text):
        """تنسيق واجهة الردود (Header & Footer) الاحترافي"""
        header = "<code>─── S-CORE SYSTEM v2.5.0-Stable ───</code>"
        footer = "<code>──────────────────────────</code>"
        return f"{header}\n\n{text}\n\n{footer}"

    async def start(self, update, context):
        """رسالة الترحيب المخصصة بالتصميم الجديد"""
        user_name = update.effective_user.first_name
        
        # تصميم الرسالة الترحيبية كما طلبت بدقة
        welcome_msg = (
            f"مرحباً <b>{user_name}</b>! 👋\n\n"
            f"أنا 🚀<b>S-Core Pro</b> مساعدك الذكي المتكامل.\n"
            f"يمكنني الإجابة على الأسئلة، 📉وتحليل 🌃الصور، 🔊والصوت.\n\n"
            f"🛠️ تم التطوير بواسطة: <b>المهندس صلاح الوافي</b>"
        )
        
        await update.message.reply_text(
            self.format_ui(welcome_msg), 
            parse_mode="HTML"
        )

    def run(self):
        """تشغيل البوت واستقبال الرسائل"""
        try:
            token = os.getenv("TELEGRAM_TOKEN")
            if not token: 
                raise ValueError("لم يتم العثور على TELEGRAM_TOKEN في ملف .env")
            
            # ضبط مهلة الاتصال لضمان الاستقرار في الشبكات الضعيفة
            req = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
            app = ApplicationBuilder().token(token).request(req).build()
            
            # ربط الأوامر والرسائل بالمعالجات (Handlers)
            app.add_handler(CommandHandler("start", self.start))
            
            # معالجة النصوص
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, 
                lambda u, c: messages.handle_text(u, c, self.engine, self.db, self.format_ui)))
            
            # معالجة الصور
            app.add_handler(MessageHandler(filters.PHOTO, 
                lambda u, c: messages.handle_photo(u, c, self.engine, self.db, self.format_ui)))

            logger.info("✅ S-Core قيد التشغيل الآن ومراقبة الشبكة...")
            app.run_polling(drop_pending_updates=True)
            
        except Exception as e:
            logger.error(f"❌ خطأ في وقت التشغيل: {e}")

if __name__ == "__main__":
    app = SCoreApp()
    app.run()

