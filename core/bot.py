from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import Update
from typing import Dict, List, Callable
import logging
import asyncio

class AdvancedBot:
    def __init__(self, token: str):
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.handlers: Dict[str, List[Callable]] = {}
        self.setup_logging()
        
    def setup_logging(self):
        """إعداد نظام التسجيل المتقدم"""
        logging.basicConfig(
            format='🎯 %(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO,
            handlers=[
                logging.FileHandler('bot_analytics.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def register_handler(self, handler_type: str, handler: Callable, *args, **kwargs):
        """تسجيل المعالجات بطريقة ذكية"""
        if handler_type == 'command':
            self.dispatcher.add_handler(CommandHandler(*args, **kwargs))
        elif handler_type == 'message':
            self.dispatcher.add_handler(MessageHandler(*args, **kwargs))
        elif handler_type == 'callback':
            self.dispatcher.add_handler(CallbackQueryHandler(*args, **kwargs))
            
    def smart_error_handler(self, update: Update, context):
        """معالجة الأخطاء الذكية"""
        error_msg = str(context.error)
        self.logger.error(f"🚨 خطأ: {error_msg}")
        
        # إرسال رسالة خطأ مناسبة للمستخدم
        if "Not enough rights" in error_msg:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⚠️ ليس لدي الصلاحيات الكافية لهذا الإجراء!"
            )
        elif "Message to delete not found" in error_msg:
            pass  # تجاهل الخطأ الشائع
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ حدث خطأ غير متوقع، جاري إصلاحه..."
            )
    
    def start(self):
        """بدء تشغيل البوت بشكل آمن"""
        try:
            self.logger.info("🚀 بدء تشغيل البوت المتقدم...")
            self.updater.start_polling(
                drop_pending_updates=True,
                allowed_updates=['message', 'callback_query']
            )
            self.updater.idle()
        except Exception as e:
            self.logger.critical(f"💥 فشل تشغيل البوت: {e}")
            raise

# إنشاء كائن البوت العالمي
from core.database import DatabaseManager
db = DatabaseManager()
bot_instance = None

def create_bot(token: str):
    global bot_instance
    bot_instance = AdvancedBot(token)
    return bot_instance
