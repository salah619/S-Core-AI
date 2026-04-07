import logging
import sys

def setup_logger():
    logger = logging.getLogger("S-Core-AI")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # العرض في التيرمكس
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # الحفظ في ملف للرجوع إليه عند حدوث أخطاء
    file_handler = logging.FileHandler("bot.log")
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger

