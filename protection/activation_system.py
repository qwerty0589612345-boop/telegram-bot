from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
import sqlite3
from typing import Literal

class ActivationSystem:
    """نظام التفعيل والتعطيل الذكي مع الصلاحيات"""
    
    def __init__(self, db_path="bot_data.db"):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        """تهيئة قاعدة البيانات"""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            
            # جدول الصلاحيات
            c.execute('''CREATE TABLE IF NOT EXISTS permissions (
                         chat_id INTEGER,
                         feature TEXT,
                         level TEXT,
                         status INTEGER DEFAULT 0,
                         PRIMARY KEY (chat_id, feature, level)
                         )''')
            
            # جدول إعدادات المجموعات
            c.execute('''CREATE TABLE IF NOT EXISTS group_settings (
                         chat_id INTEGER PRIMARY KEY,
                         owner_id INTEGER,
                         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                         )''')
            
            conn.commit()

    def _check_permission(self, update: Update, required_level: str) -> bool:
        """التحقق من صلاحية المستخدم"""
        user = update.effective_user
        chat = update.effective_chat
        
        if user.id == chat.id:  # خاص
            return True
            
        # جلب صلاحية المستخدم من قاعدة البيانات
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT status FROM permissions WHERE chat_id=? AND level=?', 
                     (chat.id, required_level))
            result = c.fetchone()
            
            return bool(result[0]) if result else False

    """🔐 صلاحيات المالك"""
    
    async def toggle_super(self, update: Update, context: CallbackContext):
        """تفعيل/تعطيل وضع السوبر"""
        if not self._check_permission(update, "owner"):
            await update.message.reply_text("❌ تحتاج إلى صلاحية المالك")
            return
            
        chat_id = update.effective_chat.id
        action = "تفعيل" if context.args and context.args[0] == "تفعيل" else "تعطيل"
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''INSERT OR REPLACE INTO permissions 
                         (chat_id, feature, level, status) 
                         VALUES (?, ?, ?, ?)''',
                         (chat_id, "السوبر", "owner", 1 if action == "تفعيل" else 0))
            conn.commit()
            
        await update.message.reply_text(f"✅ تم {action} وضع السوبر بنجاح")

    async def toggle_all(self, update: Update, context: CallbackContext):
        """تفعيل/تعطيل أمر all"""
        if not self._check_permission(update, "owner"):
            await update.message.reply_text("❌ تحتاج إلى صلاحية المالك")
            return
            
        chat_id = update.effective_chat.id
        action = "تفعيل" if context.args and context.args[0] == "تفعيل" else "تعطيل"
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''INSERT OR REPLACE INTO permissions 
                         (chat_id, feature, level, status) 
                         VALUES (?, ?, ?, ?)''',
                         (chat_id, "all", "owner", 1 if action == "تفعيل" else 0))
            conn.commit()
            
        await update.message.reply_text(f"✅ تم {action} أمر all بنجاح")

    """🛠️ صلاحيات المنشئ الأساسي"""
    
    async def toggle_auto_promote(self, update: Update, context: CallbackContext):
        """تفعيل/تعطيل رفع مميز تلقائي"""
        if not self._check_permission(update, "creator"):
            await update.message.reply_text("❌ تحتاج إلى صلاحية المنشئ الأساسي")
            return
            
        chat_id = update.effective_chat.id
        action = "تفعيل" if context.args and context.args[0] == "تفعيل" else "تعطيل"
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''INSERT OR REPLACE INTO permissions 
                         (chat_id, feature, level, status) 
                         VALUES (?, ?, ?, ?)''',
                         (chat_id, "رفع_مميز", "creator", 1 if action == "تفعيل" else 0))
            conn.commit()
            
        await update.message.reply_text(f"✅ تم {action} الرفع التلقائي بنجاح")

    """👔 صلاحيات المدير"""
    
    async def toggle_welcome(self, update: Update, context: CallbackContext):
        """تفعيل/تعطيل الترحيب"""
        if not self._check_permission(update, "admin"):
            await update.message.reply_text("❌ تحتاج إلى صلاحية المدير")
            return
            
        chat_id = update.effective_chat.id
        action = "تفعيل" if context.args and context.args[0] == "تفعيل" else "تعطيل"
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''INSERT OR REPLACE INTO permissions 
                         (chat_id, feature, level, status) 
                         VALUES (?, ?, ?, ?)''',
                         (chat_id, "الترحيب", "admin", 1 if action == "تفعيل" else 0))
            conn.commit()
            
        await update.message.reply_text(f"✅ تم {action} الترحيب بنجاح")

    """🎮 أوامر التسلية"""
    
    async def toggle_games(self, update: Update, context: CallbackContext):
        """تفعيل/تعطيل الألعاب"""
        if not self._check_permission(update, "admin"):
            await update.message.reply_text("❌ تحتاج إلى صلاحية المدير")
            return
            
        chat_id = update.effective_chat.id
        action = "تفعيل" if context.args and context.args[0] == "تفعيل" else "تعطيل"
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''INSERT OR REPLACE INTO permissions 
                         (chat_id, feature, level, status) 
                         VALUES (?, ?, ?, ?)''',
                         (chat_id, "الألعاب", "admin", 1 if action == "تفعيل" else 0))
            conn.commit()
            
        await update.message.reply_text(f"✅ تم {action} الألعاب بنجاح")

    """🎵 أوامر التسلية الإضافية"""
    
    async def toggle_sing(self, update: Update, context: CallbackContext):
        """تفعيل/تعطيل غنيلي"""
        if not self._check_permission(update, "admin"):
            await update.message.reply_text("❌ تحتاج إلى صلاحية المدير")
            return
            
        chat_id = update.effective_chat.id
        action = "تفعيل" if context.args and context.args[0] == "تفعيل" else "تعطيل"
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''INSERT OR REPLACE INTO permissions 
                         (chat_id, feature, level, status) 
                         VALUES (?, ?, ?, ?)''',
                         (chat_id, "غنيلي", "admin", 1 if action == "تفعيل" else 0))
            conn.commit()
            
        await update.message.reply_text(f"✅ تم {action} أمر غنيلي بنجاح")

    def setup_commands(self, application):
        """تسجيل جميع الأوامر"""
        # صلاحيات المالك
        application.add_handler(CommandHandler("تفعيل_السوبر", self.toggle_super))
        application.add_handler(CommandHandler("تعطيل_السوبر", self.toggle_super))
        application.add_handler(CommandHandler("تفعيل_all", self.toggle_all))
        application.add_handler(CommandHandler("تعطيل_all", self.toggle_all))
        
        # صلاحيات المنشئ الأساسي
        application.add_handler(CommandHandler("تفعيل_الرفع_التلقائي", self.toggle_auto_promote))
        application.add_handler(CommandHandler("تعطيل_الرفع_التلقائي", self.toggle_auto_promote))
        
        # صلاحيات المدير
        application.add_handler(CommandHandler("تفعيل_الترحيب", self.toggle_welcome))
        application.add_handler(CommandHandler("تعطيل_الترحيب", self.toggle_welcome))
        
        # أوامر التسلية
        application.add_handler(CommandHandler("تفعيل_الألعاب", self.toggle_games))
        application.add_handler(CommandHandler("تعطيل_الألعاب", self.toggle_games))
        application.add_handler(CommandHandler("تفعيل_غنيلي", self.toggle_sing))
        application.add_handler(CommandHandler("تعطيل_غنيلي", self.toggle_sing))
