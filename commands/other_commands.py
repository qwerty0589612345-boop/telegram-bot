"""
🎯 الأوامر الإضافية للبوت التليجرام
تشمل: الألعاب، الإحصائيات، الإدارة، والترفيه
"""

import sqlite3
import random
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters

class OtherCommands:
    """فئة الأوامر الإضافية المتكاملة"""
    
    def __init__(self, db_path: str = "bot_database.db"):
        self.db_path = db_path
        self._init_database()
        self.games_data = {}
    
    def _init_database(self):
        """تهيئة قاعدة البيانات"""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            
            # جدول النقاط والرسائل
            c.execute('''CREATE TABLE IF NOT EXISTS user_stats (
                         user_id INTEGER,
                         chat_id INTEGER,
                         points INTEGER DEFAULT 0,
                         messages INTEGER DEFAULT 0,
                         contacts INTEGER DEFAULT 0,
                         edits INTEGER DEFAULT 0,
                         last_active TIMESTAMP,
                         PRIMARY KEY (user_id, chat_id)
                         )''')
            
            # جدول الأوامر المخصصة
            c.execute('''CREATE TABLE IF NOT EXISTS custom_commands (
                         chat_id INTEGER,
                         command TEXT,
                         response TEXT,
                         added_by INTEGER,
                         added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                         PRIMARY KEY (chat_id, command)
                         )''')
            
            # جدول الردود المخصصة
            c.execute('''CREATE TABLE IF NOT EXISTS custom_replies (
                         chat_id INTEGER,
                         trigger TEXT,
                         response TEXT,
                         reply_type TEXT DEFAULT 'text',
                         added_by INTEGER,
                         added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                         PRIMARY KEY (chat_id, trigger)
                         )''')
            
            # جدول المحظورات
            c.execute('''CREATE TABLE IF NOT EXISTS banned_words (
                         chat_id INTEGER,
                         word TEXT,
                         banned_by INTEGER,
                         banned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                         PRIMARY KEY (chat_id, word)
                         )''')
            
            conn.commit()

    """🎮 الألعاب والإحصائيات"""
    
    async def pro_games(self, update: Update, context: CallbackContext):
        """قائمة الألعاب الاحترافية"""
        games_list = """
🎮 **الألعاب الاحترافية المتاحة:**

🕹️ **ألعاب الذكاء:**
• /xo - لعبة XO الكلاسيكية
• /math - تحديات رياضية
• /puzzle - ألغاز ذكاء
• /wordgame - لعبة الكلمات

🏆 **ألعاب التحدي:**
• /speed - اختبار السرعة
• /trivia - معلومات عامة
• /captcha - اختبار البوت
• /memory - اختبار الذاكرة

🎯 **ألعاب المسابقة:**
• /quiz - مسابقة الأسئلة
• /battle - معارك جماعية
• /race - سباق الزمن
• /challenge - التحديات
        """
        await update.message.reply_text(games_list, parse_mode='Markdown')
    
    async def group_info(self, update: Update, context: CallbackContext):
        """معلومات المجموعة"""
        chat = update.effective_chat
        members_count = chat.get_member_count() if hasattr(chat, 'get_member_count') else 'غير معروف'
        
        info_text = f"""
👥 **معلومات المجموعة:**

🏷️ **الاسم:** {chat.title}
🔢 **الأعضاء:** {members_count}
📝 **النوع:** {chat.type}
🆔 **المعرف:** `{chat.id}`
        """
        await update.message.reply_text(info_text, parse_mode='Markdown')
    
    async def group_link(self, update: Update, context: CallbackContext):
        """رابط المجموعة"""
        chat = update.effective_chat
        
        try:
            # محاولة الحصول على رابط الدعوة
            chat_invite = await chat.export_invite_link()
            await update.message.reply_text(f"🔗 رابط المجموعة:\n{chat_invite}")
        except Exception:
            await update.message.reply_text("❌ لا يمكن الحصول على رابط المجموعة")
    
    async def my_name(self, update: Update, context: CallbackContext):
        """عرض اسم المستخدم"""
        user = update.effective_user
        name = user.first_name + (f" {user.last_name}" if user.last_name else "")
        await update.message.reply_text(f"👤 اسمك: {name}")
    
    async def my_id(self, update: Update, context: CallbackContext):
        """عرض آيدي المستخدم"""
        user = update.effective_user
        await update.message.reply_text(f"🆔 آيديك: `{user.id}`", parse_mode='Markdown')
    
    async def my_points(self, update: Update, context: CallbackContext):
        """عرض نقاط المستخدم"""
        user = update.effective_user
        chat = update.effective_chat
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT points, messages FROM user_stats WHERE user_id=? AND chat_id=?', 
                     (user.id, chat.id))
            result = c.fetchone()
        
        points = result[0] if result else 0
        messages = result[1] if result else 0
        
        await update.message.reply_text(
            f"🎯 **إحصائياتك:**\n\n"
            f"• النقاط: {points}\n"
            f"• الرسائل: {messages}\n"
            f"• كل نقطة = 25 رسالة\n\n"
            f"استخدم /تحويل_نقاط لتحويل نقاطك", 
            parse_mode='Markdown'
        )
    
    async def clear_my_points(self, update: Update, context: CallbackContext):
        """مسح نقاط المستخدم"""
        user = update.effective_user
        chat = update.effective_chat
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('UPDATE user_stats SET points = 0 WHERE user_id=? AND chat_id=?', 
                     (user.id, chat.id))
            conn.commit()
        
        await update.message.reply_text("✅ تم مسح نقاطك بنجاح")
    
    async def my_messages(self, update: Update, context: CallbackContext):
        """عرض عدد رسائل المستخدم"""
        user = update.effective_user
        chat = update.effective_chat
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT messages FROM user_stats WHERE user_id=? AND chat_id=?', 
                     (user.id, chat.id))
            result = c.fetchone()
        
        messages = result[0] if result else 0
        await update.message.reply_text(f"📨 عدد رسائلك: {messages}")
    
    async def clear_my_messages(self, update: Update, context: CallbackContext):
        """مسح عدد رسائل المستخدم"""
        user = update.effective_user
        chat = update.effective_chat
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('UPDATE user_stats SET messages = 0 WHERE user_id=? AND chat_id=?', 
                     (user.id, chat.id))
            conn.commit()
        
        await update.message.reply_text("✅ تم مسح عدد رسائلك")

    """👥 الإحصائيات الشخصية"""
    
    async def my_contacts(self, update: Update, context: CallbackContext):
        """عرض عدد الجهات"""
        user = update.effective_user
        chat = update.effective_chat
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT contacts FROM user_stats WHERE user_id=? AND chat_id=?', 
                     (user.id, chat.id))
            result = c.fetchone()
        
        contacts = result[0] if result else 0
        await update.message.reply_text(f"📞 عدد جهاتك: {contacts}")
    
    async def clear_my_contacts(self, update: Update, context: CallbackContext):
        """مسح عدد الجهات"""
        user = update.effective_user
        chat = update.effective_chat
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('UPDATE user_stats SET contacts = 0 WHERE user_id=? AND chat_id=?', 
                     (user.id, chat.id))
            conn.commit()
        
        await update.message.reply_text("✅ تم مسح عدد جهاتك")
    
    async def my_engagement(self, update: Update, context: CallbackContext):
        """عرض تفاعل المستخدم"""
        user = update.effective_user
        chat = update.effective_chat
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT points, messages, contacts, edits FROM user_stats WHERE user_id=? AND chat_id=?', 
                     (user.id, chat.id))
            result = c.fetchone()
        
        if result:
            points, messages, contacts, edits = result
            total = points + messages + contacts + (edits or 0)
            
            # حساب مستوى التفاعل
            if total > 1000: level = "🏆 نجم"
            elif total > 500: level = "⭐ نشيط"
            elif total > 100: level = "🔥 متفاعل"
            else: level = "🌱 جديد"
            
            await update.message.reply_text(
                f"📊 **تفاعلك:** {level}\n\n"
                f"• النقاط: {points}\n"
                f"• الرسائل: {messages}\n"
                f"• الجهات: {contacts}\n"
                f"• التعديلات: {edits or 0}\n"
                f"• المجموع: {total}", 
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("📊 لم يتم تسجيل تفاعلك بعد")

    """🗑️ أوامر المسح"""
    
    async def delete_reply(self, update: Update, context: CallbackContext):
        """مسح الرسالة برد"""
        if update.message.reply_to_message:
            try:
                await update.message.reply_to_message.delete()
                await update.message.delete()
            except Exception as e:
                await update.message.reply_text("❌ لا يمكنني مسح الرسالة")
    
    async def clean_messages(self, update: Update, context: CallbackContext):
        """تنظيف عدد محدد من الرسائل"""
        if not context.args:
            await update.message.reply_text("استخدم: /تنظيف + العدد")
            return
        
        try:
            count = int(context.args[0])
            if count > 100 or count < 1:
                await update.message.reply_text("❌ العدد يجب أن يكون بين 1 و 100")
                return
            
            # مسح الرسائل
            chat_id = update.effective_chat.id
            message_id = update.message.message_id
            
            for i in range(count + 1):  # +1 ليشمل الرسالة الأصلية
                try:
                    await context.bot.delete_message(chat_id, message_id - i)
                except:
                    continue
                
                await asyncio.sleep(0.1)  # تجنب التحميل الزائد
                
        except ValueError:
            await update.message.reply_text("❌ الرقم غير صالح")

    """⚙️ أوامر الإدارة"""
    
    async def ban_word(self, update: Update, context: CallbackContext):
        """منع كلمة"""
        if not context.args and not update.message.reply_to_message:
            await update.message.reply_text("استخدم: /منع + الكلمة أو رد على رسالة")
            return
        
        word = " ".join(context.args) if context.args else update.message.reply_to_message.text
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('INSERT OR REPLACE INTO banned_words (chat_id, word, banned_by) VALUES (?, ?, ?)', 
                     (chat_id, word.lower(), user_id))
            conn.commit()
        
        await update.message.reply_text(f"✅ تم منع الكلمة: {word}")
    
    async def ban_list(self, update: Update, context: CallbackContext):
        """قائمة الكلمات الممنوعة"""
        chat_id = update.effective_chat.id
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT word FROM banned_words WHERE chat_id=?', (chat_id,))
            words = c.fetchall()
        
        if words:
            word_list = "\n".join([f"• {word[0]}" for word in words])
            await update.message.reply_text(f"📋 الكلمات الممنوعة:\n{word_list}")
        else:
            await update.message.reply_text("✅ لا توجد كلمات ممنوعة")

    """🛠️ الأوامر المخصصة"""
    
    async def add_command(self, update: Update, context: CallbackContext):
        """إضافة أمر مخصص"""
        if len(context.args) < 2:
            await update.message.reply_text("استخدم: /اضف_امر الأمر الرد")
            return
        
        command = context.args[0].lower()
        response = " ".join(context.args[1:])
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('INSERT OR REPLACE INTO custom_commands (chat_id, command, response, added_by) VALUES (?, ?, ?, ?)', 
                     (chat_id, command, response, user_id))
            conn.commit()
        
        await update.message.reply_text(f"✅ تم إضافة الأمر: /{command}")
    
    async def delete_command(self, update: Update, context: CallbackContext):
        """حذف أمر مخصص"""
        if not context.args:
            await update.message.reply_text("استخدم: /حذف_امر الأمر")
            return
        
        command = context.args[0].lower()
        chat_id = update.effective_chat.id
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM custom_commands WHERE chat_id=? AND command=?', 
                     (chat_id, command))
            conn.commit()
        
        await update.message.reply_text(f"✅ تم حذف الأمر: /{command}")

    """🎵 أوامر الترفيه"""
    
    async def sing_for_me(self, update: Update, context: CallbackContext):
        """أمر غنيلي"""
        songs = [
            "🎵 غنيلي غنيلي يا قلبي...",
            "🎶 على ضوء القمر...",
            "🎼 ياحبيبي وينك وينك...",
            "🎤 طالعة من دارها...",
            "🎹 ياعينيك سحرهم قوي..."
        ]
        await update.message.reply_text(random.choice(songs))
    
    async def send_video(self, update: Update, context: CallbackContext):
        """إرسال فيديو"""
        videos = [
            "🎥 فيديو مضحك 1",
            "🎬 فيديو رومانسي 2", 
            "📹 فيديو مغامرة 3"
        ]
        await update.message.reply_text(random.choice(videos))

    """🔧 إعداد الأوامر"""
    
    def setup_commands(self, application):
        """تسجيل جميع الأوامر"""
        
        # الألعاب والإحصائيات
        application.add_handler(CommandHandler("الالعاب_الاحترافية", self.pro_games))
        application.add_handler(CommandHandler("المجموعة", self.group_info))
        application.add_handler(CommandHandler("الرابط", self.group_link))
        application.add_handler(CommandHandler("اسمي", self.my_name))
        application.add_handler(CommandHandler("ايديي", self.my_id))
        application.add_handler(CommandHandler("نقاطي", self.my_points))
        application.add_handler(CommandHandler("مسح_نقاطي", self.clear_my_points))
        application.add_handler(CommandHandler("رسائلي", self.my_messages))
        application.add_handler(CommandHandler("مسح_رسائلي", self.clear_my_messages))
        application.add_handler(CommandHandler("جهاتي", self.my_contacts))
        application.add_handler(CommandHandler("مسح_جهاتي", self.clear_my_contacts))
        application.add_handler(CommandHandler("تفاعلي", self.my_engagement))
        
        # أوامر المسح
        application.add_handler(CommandHandler("مسح", self.delete_reply))
        application.add_handler(CommandHandler("تنظيف", self.clean_messages))
        
        # إدارة المحتوى
        application.add_handler(CommandHandler("منع", self.ban_word))
        application.add_handler(CommandHandler("قائمة_المنع", self.ban_list))
        
        # الأوامر المخصصة
        application.add_handler(CommandHandler("اضف_امر", self.add_command))
        application.add_handler(CommandHandler("حذف_امر", self.delete_command))
        
        # الترفيه
        application.add_handler(CommandHandler("غنيلي", self.sing_for_me))
        application.add_handler(CommandHandler("فلم", self.send_video))
        application.add_handler(CommandHandler("فيديو", self.send_video))

# استخدام الفئة
def setup_other_commands(application):
    """إعداد الأوامر الإضافية"""
    other_cmds = OtherCommands()
    other_cmds.setup_commands(application)
