import os
from pathlib import Path
from dotenv import load_dotenv

# تحديد المسار الحالي للمجلد لضمان تحميل ملف .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # تحويل ADMIN_ID إلى رقم، مع قيمة افتراضية لتجنب تعطل الكود
    raw_admin_id = os.getenv("ADMIN_ID", "6850112777")
    ADMIN_ID = int(raw_admin_id) if raw_admin_id.isdigit() else 0
    
    TEXT_MODEL = "llama-3.3-70b-versatile"
    VISION_MODEL = "llama-3.2-11b-vision-preview"
    WHISPER_MODEL = "whisper-large-v3"
    
    SYSTEM_PROMPT = "أنت S-Core Pro، مساعد ذكي مطور بواسطة م.صلاح الوافي."

