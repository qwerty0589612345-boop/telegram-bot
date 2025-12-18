import re
from typing import Dict, Optional

class ContentAnalyzer:
    """محرك تحليل المحتوى الذكي"""
    
    def __init__(self):
        self.patterns = {
            'تاك': re.compile(r'@(\w+)'),
            'رابط': re.compile(r'https?://[^\s]+'),
            'بوتات': re.compile(r'@\w+bot', re.IGNORECASE),
            'فارسية': re.compile(r'[\u0600-\u06FF]'),
            'انكليزية': re.compile(r'[a-zA-Z]'),
            'توجيه': lambda msg: bool(msg.forward_from),
            'تعديل': lambda msg: bool(msg.edit_date),
            'انلاين': lambda msg: bool(msg.via_bot)
        }
        
    def detect_content_type(self, message) -> Optional[Dict]:
        """تحديد نوع المحتوى"""
        checks = [
            ('صور', lambda msg: bool(msg.photo)),
            ('فيديو', lambda msg: bool(msg.video)),
            ('ملصقات', lambda msg: bool(msg.sticker)),
            ('ملفات', lambda msg: bool(msg.document)),
            ('صوت', lambda msg: bool(msg.audio)),
            ('اغاني', lambda msg: bool(msg.audio and msg.audio.title)),
            ('سيلفي', lambda msg: bool(msg.photo and "selfie" in msg.caption.lower())),
            ('فشار', lambda msg: bool(message.text and "فشار" in message.text.lower())),
            ('شارحة', lambda msg: bool(message.text and len(message.text.split()) > 100)),
            ('كلايش', lambda msg: bool(message.text and len(message.text) > 500)),
            ('اشعارات', lambda msg: bool(msg.text and "اشعار" in msg.text.lower())),
            ('استفتاء', lambda msg: bool(msg.poll)),
            ('متحركات', lambda msg: bool(msg.animation)),
            ('ماركداون', lambda msg: bool(msg.text and any(mark in msg.text for mark in ["**", "__", "`", "```"]))),
            ('رسائل', lambda msg: bool(msg.text or msg.caption)),
            ('دردشة', lambda msg: bool(msg.text and msg.chat.type == "private")),
            ('جهات', lambda msg: bool(msg.contact)),
            ('دخول', lambda msg: bool(msg.new_chat_members)),
            ('اضافة', lambda msg: bool(msg.new_chat_members)),
            ('تثبيت', lambda msg: bool(msg.pinned_message))
        ]
        
        for content_type, check in checks:
            if check(message):
                return {'type': content_type, 'content': getattr(message, content_type)}
        
        for pattern_name, pattern in self.patterns.items():
            if message.text and pattern.search(message.text):
                return {'type': pattern_name, 'content': message.text}
        
        return None
    
    def is_spam(self, message, chat_id: int) -> bool:
        """الكشف عن التكرار (Spam)"""
        # يمكن تطوير هذه الوظيفة لفحص تكرار الرسائل
        return False
      
