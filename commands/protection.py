from telegram import Update, ChatPermissions
from telegram.ext import CallbackContext
from core.database import db
from core.security import SecurityManager
import re
from typing import Optional

class AdvancedProtection:
    def __init__(self):
        self.security = SecurityManager()
        self.patterns = {
            'links': re.compile(r'https?://[^\s]+'),
            'mentions': re.compile(r'@(\w+)'),
            'bots': re.compile(r'@\w+bot', re.IGNORECASE),
            'phones': re.compile(r'\+?\d[\d\s-]{8,}\d')
        }
    
    async def handle_protection(self, update: Update, context: CallbackContext):
        """معالجة الحماية بشكل غير متزامن"""
        message = update.message
        if not message or not message.chat:
            return
        
        chat_id = message.chat.id
        user = message.from_user
        
        # تخطي الرسائل من المدراء
        if await self._is_user_admin(chat_id, user.id):
            return
        
        # فحص أنواع المحتوى المختلفة
        checks = [
            self._check_links(message, chat_id),
            self._check_mentions(message, chat_id),
            self._check_media(message, chat_id),
            self._check_spam(message, chat_id)
        ]
        
        for check in checks:
            result = await check
            if result:
                await self._apply_penalty(message, result['penalty'], result['reason'])
                break
    
    async def _check_links(self, message, chat_id) -> Optional[Dict]:
        """فحص الروابط"""
        if not message.text:
            return None
            
        protection = db.get_protection_status(chat_id, 'link_protection')
        if protection and protection['is_active']:
            if self.patterns['links'].search(message.text):
                return {
                    'penalty': protection['penalty_type'],
                    'reason': 'إرسال روابط'
                }
        return None
    
    async def _check_media(self, message, chat_id) -> Optional[Dict]:
        """فحص الوسائط"""
        media_types = {
            'photo': 'photo_protection',
            'video': 'video_protection',
            'sticker': 'sticker_protection',
            'document': 'file_protection'
        }
        
        for media_type, protection_key in media_types.items():
            if getattr(message, media_type, None):
                protection = db.get_protection_status(chat_id, protection_key)
                if protection and protection['is_active']:
                    return {
                        'penalty': protection['penalty_type'],
                        'reason': f'إرسال {media_type}'
                    }
        return None
    
    async def _apply_penalty(self, message, penalty: str, reason: str):
        """تطبيق العقوبة المناسبة"""
        try:
            await message.delete()
            
            penalty_actions = {
                'delete': lambda: None,
                'warn': lambda: message.reply_text(f"⚠️ تحذير: {reason}"),
                'mute': lambda: self._mute_user(message, 300), 5 دقائق
                'kick': lambda: message.chat.ban_member(message.from_user.id)
            }
            
            action = penalty_actions.get(penalty, penalty_actions['delete'])
            await action()
            
        except Exception as e:
            print(f"❌ خطأ في تطبيق العقوبة: {e}")

def setup_protection_commands(bot):
    """إعداد أوامر الحماية"""
    protection = AdvancedProtection()
    
    bot.register_handler('message', protection.handle_protection, 
                        Filters.all & ~Filters.command)
    
    # أوامر القفل والفتح
    bot.register_handler('command', 'قفل', lock_command)
    bot.register_handler('command', 'فتح', unlock_command)

async def lock_command(update: Update, context: CallbackContext):
    """أمر القفل المتطور"""
    # ... (كود متطور للقفل)
    pass

async def unlock_command(update: Update, context: CallbackContext):
    """أمر الفتح المتطور"""
    # ... (كود متطور للفتح)
    pass
  
