import base64
from groq import Groq
from googlesearch import search

class SCoreEngine:
    def __init__(self, api_key, text_model, vision_model, system_prompt):
        self.client = Groq(api_key=api_key)
        self.text_model = text_model
        self.vision_model = vision_model
        self.system_prompt = system_prompt

    def _quick_search(self, query):
        try:
            results = list(search(query, num_results=3, lang="ar"))
            return "\n".join(results) if results else "لا توجد نتائج حية."
        except: return ""

    def generate_smart_response(self, user_id, user_input, db):
        history = db.get_chat_history(user_id)
        
        # تفعيل البحث إذا وجد كلمات دليلة
        extra_context = ""
        if any(word in user_input for word in ["سعر", "أخبار", "اليوم", "تحديث"]):
            extra_context = f"\n[بحث حي]: {self._quick_search(user_input)}"

        messages = [{"role": "system", "content": self.system_prompt + extra_context}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_input})

        try:
            completion = self.client.chat.completions.create(
                model=self.text_model,
                messages=messages,
                temperature=0.7
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"⚠️ خطأ تقني في المحرك: {str(e)}"

