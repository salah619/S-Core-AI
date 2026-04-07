import logging
import sys

def setup_logger():
    logger = logging.getLogger("S-Core")
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # التسجيل في ملف
    file_handler = logging.FileHandler("bot.log")
    file_handler.setFormatter(formatter)

    # العرض في التيرمكس أيضاً
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

