from telegram import constants

async def handle_text(update, context, engine, db, formatter):
    """معالجة الرسائل النصية بذكاء"""
    user_input = update.message.text
    user_id = update.effective_user.id
    
    # إظهار حالة الكتابة في التليجرام
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
    
    # 1. حفظ رسالة المستخدم في الذاكرة (الدور: user)
    db.log_interaction(user_id, "user", user_input)
    
    # 2. جلب الرد الذكي من المحرك (مع السياق والبحث)
    reply = engine.generate_smart_response(user_id, user_input, db)
    
    # 3. حفظ رد البوت في الذاكرة (الدور: assistant) ليتذكره لاحقاً
    db.log_interaction(user_id, "assistant", reply)
    
    # 4. إرسال الرد النهائي للمستخدم بتنسيق S-Core
    await update.message.reply_text(formatter(reply), parse_mode=constants.ParseMode.HTML)

async def handle_photo(update, context, engine, db, formatter):
    """معالجة الصور وتحليلها"""
    await update.message.reply_text("<code>📸 جاري تحليل البيانات البصرية...</code>", parse_mode=constants.ParseMode.HTML)
    
    photo_file = await update.message.photo[-1].get_file()
    img_bytes = await photo_file.download_as_bytearray()
    
    reply = engine.analyze_image(img_bytes)
    await update.message.reply_text(formatter(reply), parse_mode=constants.ParseMode.HTML)

