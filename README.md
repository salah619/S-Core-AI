# S-Core Telegram Bot

بوت تلجرام احترافي يعمل بالذكاء الاصطناعي باستخدام موديل `llama-3.3-70b-specdec` عبر Groq.

## الميزات
- نظام ذاكرة للمحادثة.
- تنبيهات فورية للأدمن عند انضمام مستخدمين جدد.
- مساعد تقني وتنفيذي ذكي.

## النشر على Render
1. اربط حساب GitHub الخاص بك بـ Render.
2. أنشئ "New Web Service" أو "Background Worker".
3. اختر هذا المستودع.
4. أضف المتغيرات البيئية (Environment Variables) التالية:
   - `TELEGRAM_TOKEN`
   - `GROQ_API_KEY`
   - `ADMIN_ID`
   - `GROQ_MODEL`
5. أمر التشغيل: `python bot.py`

تطوير: المهندس صلاح الوافي.
