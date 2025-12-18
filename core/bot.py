#!/usr/bin/env python3
"""
🤖 البوت الرئيسي - الإصدار المتكامل
يجمع جميع الأوامر: إعدادات المجموعة، الحماية، الألعاب، والأوامر الإضافية
"""

import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)
from activation_system import ActivationSystem
from group_settings_manager import GroupSettingsManager
from other_commands import OtherCommands
from protection_manager import ProtectionManager
from games.activation_system import GamesManager  # إذا كان لديك ملف ألعاب منفصل

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class BotManager:
    """مدير البوت الرئيسي"""
    
    def __init__(self, token: str):
        self.token = token
        self.application = ApplicationBuilder().token(self.token).build()
        
        # تهيئة الأنظمة الفرعية
        self.activation_system = ActivationSystem()
        self.group_settings = GroupSettingsManager()
        self.other_commands = OtherCommands()
        self.protection_manager = ProtectionManager()
        self.games_manager = GamesManager()  # إذا كان لديك نظام ألعاب منفصل
        self._setup_handlers()
    
    def _setup_handlers(self):
        """إعداد جميع المعالجات"""
        
        # أوامر التفعيل والتعطيل
        self.activation_system.setup_commands(self.application)
        
        # إعدادات المجموعة
        self.group_settings.setup_group_settings_commands(self.application)
        
        # الأوامر الإضافية
        self.other_commands.setup_commands(self.application)
        
        # نظام الحماية
        self.protection_manager.setup_protection_commands(self.application)
        
        # نظام الألعاب
        self.games_manager.setup_game_commands(self.application)
        
        # معالجة الرسائل العامة
        self.application.add_handler(MessageHandler(Filters.text, self.handle_message))
        self.application.add_handler(MessageHandler(Filters.status_update.new_chat_members, self.welcome_new_members))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
    
    async def handle_message(self, update: Update, context: CallbackContext):
        """معالجة الرسائل العامة"""
        # يمكنك إضافة منطق إضافي هنا
        pass
    
    async def welcome_new_members(self, update: Update, context: CallbackContext):
        """ترحيب بالأعضاء الجدد"""
        await self.group_settings.welcome_member(update, context)
    
    async def handle_callback(self, update: Update, context: CallbackContext):
        """معالجة استدعاءات الأزرار"""
        # يمكنك إضافة منطق إضافي هنا
        pass
    
    def start(self):
        """بدء تشغيل البوت"""
        logger.info("🤖 بدء تشغيل البوت...")
        self.application.run_polling()

# دالة التشغيل الرئيسية
if __name__ == "__main__":
    # توكن البوت - يُفضل قراءته من ملف بيئة بدلاً من الكود مباشرة
    BOT_TOKEN = "8257887627:AAEZ2I9Q97ma1C07Hp1bKNHLibIVsrQLCxc"
    
    # إنشاء وإدارة البوت
    bot = BotManager(BOT_TOKEN)
    bot.start()
