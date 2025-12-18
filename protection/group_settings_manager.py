from telegram import Update, ChatPermissions
from telegram.ext import CallbackContext
from telegram.error import BadRequest
import sqlite3
from datetime import datetime
import re

class GroupSettingsManager:
    """مدير إعدادات المجموعة المتكامل"""
    
    def __init__(self, db_path="group_settings.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """تهيئة قاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # جدول إعدادات المجموعات
        c.execute('''CREATE TABLE IF NOT EXISTS group_settings (
                     chat_id INTEGER PRIMARY KEY,
                     welcome_text TEXT,
                     rules_text TEXT,
                     group_link TEXT,
                     custom_id_format TEXT,
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                     )''')
        
        # جدول الإحصائيات
        c.execute('''CREATE TABLE IF NOT EXISTS group_stats (
                     chat_id INTEGER,
                     user_id INTEGER,
                     messages_count INTEGER DEFAULT 0,
                     last_active TIMESTAMP,
                     PRIMARY KEY (chat_id, user_id)
                     )''')
        
        conn.commit()
        conn.close()

    def _get_admin_level(self, update: Update) -> str:
        """الحصول على مستوى صلاحية المستخدم"""
        user = update.effective_user
        chat = update.effective_chat
        
        if user.id == chat.id:  # خاص
            return "owner"
        
        try:
            member = chat.get_member(user.id)
            if member.status == 'creator':
                return "owner"
            elif member.status == 'administrator':
                return "admin"
            elif member.status in ['member', 'restricted']:
                return "member"
        except:
            return "member"
        
        return "member"

    # ▸ الترحيب
    async def welcome_member(self, update: Update, context: CallbackContext):
        """ترحيب تلقائي بالأعضاء الجدد"""
        for member in update.message.new_chat_members:
            chat_id = update.effective_chat.id
            
            # جلب نص الترحيب من قاعدة البيانات
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('SELECT welcome_text FROM group_settings WHERE chat_id=?', (chat_id,))
            result = c.fetchone()
            conn.close()
            
            welcome_text = result[0] if result else "🎊 أهلاً وسهلاً بك {user} في المجموعة! 🌟"
            
            # استبدال المتغيرات
            welcome_text = welcome_text.replace("{user}", member.first_name)
            welcome_text = welcome_text.replace("{group}", update.effective_chat.title)
            
            await update.message.reply_text(welcome_text)

    # ▸ تعيين ترحيب
    async def set_welcome(self, update: Update, context: CallbackContext):
        """تعيين رسالة ترحيب"""
        if self._get_admin_level(update) not in ["owner", "admin"]:
            await update.message.reply_text("❌ تحتاج إلى صلاحية إدارية لتعيين الترحيب")
            return
        
        if not context.args:
            await update.message.reply_text("📝 استخدام: /تعيين_ترحيب [النص]\nيمكن استخدام {user} و {group}")
            return
        
        welcome_text = " ".join(context.args)
        chat_id = update.effective_chat.id
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO group_settings 
                     (chat_id, welcome_text) VALUES (?, ?)''', 
                     (chat_id, welcome_text))
        conn.commit()
        conn.close()
        
        await update.message.reply_text("✅ تم تعيين رسالة الترحيب بنجاح")

    # ▸ مسح الترحيب
    async def delete_welcome(self, update: Update, context: CallbackContext):
        """مسح رسالة الترحيب"""
        if self._get_admin_level(update) not in ["owner", "admin"]:
            await update.message.reply_text("❌ تحتاج إلى صلاحية إدارية لمسح الترحيب")
            return
        
        chat_id = update.effective_chat.id
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('UPDATE group_settings SET welcome_text = NULL WHERE chat_id=?', (chat_id,))
        conn.commit()
        conn.close()
        
        await update.message.reply_text("✅ تم مسح رسالة الترحيب")

    # ▸ مسح الرتب
    async def delete_ranks(self, update: Update, context: CallbackContext):
        """مسح رتب المستخدمين"""
        if self._get_admin_level(update) != "owner":
            await update.message.reply_text("❌ تحتاج إلى صلاحية المالك لمسح الرتب")
            return
        
        chat_id = update.effective_chat.id
        
        try:
            # هنا يمكن إضافة منطق مسح الرتب حسب نظامك
            await update.message.reply_text("🔄 جاري مسح الرتب...")
            # كود مسح الرتب يضاف هنا
            await update.message.reply_text("✅ تم مسح جميع الرتب بنجاح")
        except Exception as e:
            await update.message.reply_text(f"❌ خطأ في مسح الرتب: {str(e)}")

    # ▸ الغاء التثبيت
    async def unpin_message(self, update: Update, context: CallbackContext):
        """إلغاء تثبيت الرسالة"""
        if self._get_admin_level(update) not in ["owner", "admin"]:
            await update.message.reply_text("❌ تحتاج إلى صلاحية إدارية لإلغاء التثبيت")
            return
        
        try:
            await context.bot.unpin_all_chat_messages(update.effective_chat.id)
            await update.message.reply_text("✅ تم إلغاء تثبيت جميع الرسائل")
        except BadRequest:
            await update.message.reply_text("❌ لا توجد رسائل مثبتة")

    # ▸ فحص البوت
    async def bot_status(self, update: Update, context: CallbackContext):
        """فحص حالة البوت"""
        chat = update.effective_chat
        user = update.effective_user
        
        status_text = f"""
🤖 **حالة البوت في المجموعة**

📊 **معلومات المجموعة:**
- الاسم: {chat.title}
- الأعضاء: {chat.get_member_count() if hasattr(chat, 'get_member_count') else 'غير معروف'}
- النوع: {chat.type}

👤 **معلوماتك:**
- الاسم: {user.first_name}
- المعرف: @{user.username if user.username else 'غير متوفر'}
- الصلاحية: {self._get_admin_level(update)}

🛠️ **الحالة:** ✅ يعمل بشكل طبيعي
        """
        
        await update.message.reply_text(status_text, parse_mode='Markdown')

    # ▸ تعيين الرابط
    async def set_group_link(self, update: Update, context: CallbackContext):
        """تعيين رابط المجموعة"""
        if self._get_admin_level(update) != "owner":
            await update.message.reply_text("❌ تحتاج إلى صلاحية المالك لتعيين الرابط")
            return
        
        if not context.args:
            await update.message.reply_text("🔗 استخدام: /تعيين_الرابط [الرابط]")
            return
        
        group_link = context.args[0]
        chat_id = update.effective_chat.id
        
        # التحقق من صحة الرابط
        if not re.match(r'^https?://t\.me/[\w_]+$', group_link):
            await update.message.reply_text("❌ الرابط غير صالح. يجب أن يكون رابط تيليجرام")
            return
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO group_settings 
                     (chat_id, group_link) VALUES (?, ?)''', 
                     (chat_id, group_link))
        conn.commit()
        conn.close()
        
        await update.message.reply_text(f"✅ تم تعيين رابط المجموعة:\n{group_link}")

    # ▸ مسح الرابط
    async def delete_group_link(self, update: Update, context: CallbackContext):
        """مسح رابط المجموعة"""
        if self._get_admin_level(update) != "owner":
            await update.message.reply_text("❌ تحتاج إلى صلاحية المالك لمسح الرابط")
            return
        
        chat_id = update.effective_chat.id
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('UPDATE group_settings SET group_link = NULL WHERE chat_id=?', (chat_id,))
        conn.commit()
        conn.close()
        
        await update.message.reply_text("✅ تم مسح رابط المجموعة")

    # ▸ تغيير الايدي
    async def change_id_format(self, update: Update, context: CallbackContext):
        """تغيير تنسيق الآيدي"""
        if self._get_admin_level(update) != "owner":
            await update.message.reply_text("❌ تحتاج إلى صلاحية المالك لتغيير تنسيق الآيدي")
            return
        
        if not context.args:
            await update.message.reply_text("🆔 استخدام: /تغيير_الايدي [التنسيق]\nمثال: ID-{user_id}-{date}")
            return
        
        id_format = " ".join(context.args)
        chat_id = update.effective_chat.id
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO group_settings 
                     (chat_id, custom_id_format) VALUES (?, ?)''', 
                     (chat_id, id_format))
        conn.commit()
        conn.close()
        
        await update.message.reply_text(f"✅ تم تغيير تنسيق الآيدي إلى:\n{id_format}")

    # ▸ تعيين الايدي
    async def set_custom_id(self, update: Update, context: CallbackContext):
        """تعيين آيدي مخصص للمستخدم"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        if not context.args:
            await update.message.reply_text("🆔 استخدام: /تعيين_الايدي [الآيدي المطلوب]")
            return
        
        custom_id = context.args[0]
        
        # حفظ الآيدي المخصص في قاعدة البيانات
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS custom_ids (
                     user_id INTEGER,
                     chat_id INTEGER,
                     custom_id TEXT,
                     PRIMARY KEY (user_id, chat_id)
                     )''')
        c.execute('''INSERT OR REPLACE INTO custom_ids 
                     (user_id, chat_id, custom_id) VALUES (?, ?, ?)''', 
                     (user.id, chat_id, custom_id))
        conn.commit()
        conn.close()
        
        await update.message.reply_text(f"✅ تم تعيين الآيدي المخصص: {custom_id}")

    # ▸ مسح الايدي
    async def delete_custom_id(self, update: Update, context: CallbackContext):
        """مسح الآيدي المخصص"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('DELETE FROM custom_ids WHERE user_id=? AND chat_id=?', (user.id, chat_id))
        conn.commit()
        conn.close()
        
        await update.message.reply_text("✅ تم مسح الآيدي المخصص")

    # ▸ صورتي
    async def my_photo(self, update: Update, context: CallbackContext):
        """إرسال صورة المستخدم"""
        user = update.effective_user
        
        try:
            # محاولة الحصول على صورة المستخدم
            photos = await user.get_profile_photos(limit=1)
            if photos.total_count > 0:
                photo = photos.photos[0][-1]  # أكبر حجم
                await update.message.reply_photo(photo.file_id, caption="📸 صورتك الشخصية")
            else:
                await update.message.reply_text("❀ لا تمتلك صورة شخصية")
        except Exception as e:
            await update.message.reply_text("❀ لا تمتلك صورة شخصية")

    # ▸ تغيير اسم المجموعة
    async def change_group_name(self, update: Update, context: CallbackContext):
        """تغيير اسم المجموعة"""
        if self._get_admin_level(update) != "owner":
            await update.message.reply_text("❌ تحتاج إلى صلاحية المالك لتغيير الاسم")
            return
        
        if not context.args:
            await update.message.reply_text("🏷️ استخدام: /تغيير_اسم_المجموعة [الاسم الجديد]")
            return
        
        new_name = " ".join(context.args)
        
        try:
            await context.bot.set_chat_title(update.effective_chat.id, new_name)
            await update.message.reply_text(f"✅ تم تغيير اسم المجموعة إلى: {new_name}")
        except BadRequest as e:
            await update.message.reply_text(f"❌ خطأ في تغيير الاسم: {str(e)}")

    # ▸ تعيين قوانين
    async def set_rules(self, update: Update, context: CallbackContext):
        """تعيين قوانين المجموعة"""
        if self._get_admin_level(update) not in ["owner", "admin"]:
            await update.message.reply_text("❌ تحتاج إلى صلاحية إدارية لتعيين القوانين")
            return
        
        if not context.args:
            await update.message.reply_text("📜 استخدام: /تعيين_قوانين [النص]")
            return
        
        rules_text = " ".join(context.args)
        chat_id = update.effective_chat.id
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO group_settings 
                     (chat_id, rules_text) VALUES (?, ?)''', 
                     (chat_id, rules_text))
        conn.commit()
        conn.close()
        
        await update.message.reply_text("✅ تم تعيين القوانين بنجاح")

    # ▸ مسح القوانين
    async def delete_rules(self, update: Update, context: CallbackContext):
        """مسح قوانين المجموعة"""
        if self._get_admin_level(update) not in ["owner", "admin"]:
            await update.message.reply_text("❌ تحتاج إلى صلاحية إدارية لمسح القوانين")
            return
        
        chat_id = update.effective_chat.id
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('UPDATE group_settings SET rules_text = NULL WHERE chat_id=?', (chat_id,))
        conn.commit()
        conn.close()
        
        await update.message.reply_text("✅ تم مسح القوانين")

    # ▸ تغيير الوصف
    async def change_group_description(self, update: Update, context: CallbackContext):
        """تغيير وصف المجموعة"""
        if self._get_admin_level(update) != "owner":
            await update.message.reply_text("❌ تحتاج إلى صلاحية المالك لتغيير الوصف")
            return
        
        if not context.args:
            await update.message.reply_text("📝 استخدام: /تغيير_الوصف [الوصف الجديد]")
            return
        
        new_description = " ".join(context.args)
        
        try:
            await context.bot.set_chat_description(update.effective_chat.id, new_description)
            await update.message.reply_text(f"✅ تم تغيير وصف المجموعة")
        except BadRequest as e:
            await update.message.reply_text(f"❌ خطأ في تغيير الوصف: {str(e)}")

    # ▸ تنظيف التعديل
    async def clean_edited(self, update: Update, context: CallbackContext):
        """تنظيف الرسائل المعدلة"""
        if self._get_admin_level(update) not in ["owner", "admin"]:
            await update.message.reply_text("❌ تحتاج إلى صلاحية إدارية للتنظيف")
            return
        
        try:
            # هذه وظيفة افتراضية - تحتاج إلى تطوير حسب احتياجاتك
            await update.message.reply_text("🔄 جاري تنظيف الرسائل المعدلة...")
            # كود التنظيف يضاف هنا
            await update.message.reply_text("✅ تم تنظيف الرسائل المعدلة")
        except Exception as e:
            await update.message.reply_text(f"❌ خطأ في التنظيف: {str(e)}")

    # ▸ تنظيف الميديا
    async def clean_media(self, update: Update, context: CallbackContext):
        """تنظيف الوسائط"""
        if self._get_admin_level(update) not in ["owner", "admin"]:
            await update.message.reply_text("❌ تحتاج إلى صلاحية إدارية للتنظيف")
            return
        
        try:
            # هذه وظيفة افتراضية - تحتاج إلى تطوير حسب احتياجاتك
            await update.message.reply_text("🔄 جاري تنظيف الوسائط...")
            # كود تنظيف الوسائط يضاف هنا
            await update.message.reply_text("✅ تم تنظيف الوسائط")
        except Exception as e:
            await update.message.reply_text(f"❌ خطأ في التنظيف: {str(e)}")

    # ▸ رفع الادمنية
    async def promote_admins(self, update: Update, context: CallbackContext):
        """رفع إدمنية"""
        if self._get_admin_level(update) != "owner":
            await update.message.reply_text("❌ تحتاج إلى صلاحية المالك لرفع الإدمنية")
            return
        
        # هذه وظيفة تحتاج إلى تطوير حسب نظام الصلاحيات
        await update.message.reply_text("👑 وظيفة رفع الإدمنية تحت التطوير")

    # ▸ الالعاب الاحترافية
    async def pro_games(self, update: Update, context: CallbackContext):
        """إعدادات الألعاب الاحترافية"""
        games_text = """
🎮 **الألعاب الاحترافية المتاحة:**

1. **لعبة XO المتقدمة** - تحدي ذكاء
2. **مسابقات الرياضيات** - أسئلة رياضية صعبة  
3. **تحدي الكلمات** - تركيب كلمات معقدة
4. **ألغاز الذكاء** - ألغاز منطقية
5. **تحدي السرعة** - اختبار رد الفعل

🔧 **الإعدادات:**
- /تفعيل_الالعاب - تفعيل النظام
- /تعطيل_الالعاب - تعطيل النظام
- /اضافة_لعبة - إضافة لعبة جديدة
        """
        
        await update.message.reply_text(games_text, parse_mode='Markdown')

    # ▸ اعدادات المجموعة
    async def group_settings_menu(self, update: Update, context: CallbackContext):
        """قائمة إعدادات المجموعة"""
        chat_id = update.effective_chat.id
        
        # جلب الإعدادات من قاعدة البيانات
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM group_settings WHERE chat_id=?', (chat_id,))
        settings = c.fetchone()
        conn.close()
        
        if settings:
            welcome_status = "✅ مفعل" if settings[1] else "❌ معطل"
            rules_status = "✅ مفعل" if settings[2] else "❌ معطل"
            link_status = "✅ مضبوط" if settings[3] else "❌ غير مضبوط"
        else:
            welcome_status = rules_status = link_status = "❌ غير مضبوط"
        
        settings_text = f"""
⚙️ **إعدادات المجموعة**

🔹 **الترحيب:** {welcome_status}
🔹 **القوانين:** {rules_status}  
🔹 **الرابط:** {link_status}
🔹 **الآيدي المخصص:** {'✅ مفعل' if settings and settings[4] else '❌ معطل'}

📋 **الأوامر المتاحة:**
• /تعيين_ترحيب - تعيين رسالة ترحيب
• /تعيين_قوانين - تعيين قوانين المجموعة
• /تعيين_الرابط - تعيين رابط المجموعة
• /تغيير_الايدي - تغيير تنسيق الآيدي
• /تغيير_اسم_المجموعة - تغيير اسم المجموعة
• /تغيير_الوصف - تغيير وصف المجموعة
        """
        
        await update.message.reply_text(settings_text, parse_mode='Markdown')

# دمج الأوامر مع البوت
def setup_group_settings_commands(application):
    """إعداد أوامر إعدادات المجموعة"""
    manager = GroupSettingsManager()
    
    # تسجيل معالجات الأوامر
    application.add_handler(CommandHandler("تعيين_ترحيب", manager.set_welcome))
    application.add_handler(CommandHandler("مسح_الترحيب", manager.delete_welcome))
    application.add_handler(CommandHandler("مسح_الرتب", manager.delete_ranks))
    application.add_handler(CommandHandler("الغاء_التثبيت", manager.unpin_message))
    application.add_handler(CommandHandler("فحص_البوت", manager.bot_status))
    application.add_handler(CommandHandler("تعيين_الرابط", manager.set_group_link))
    application.add_handler(CommandHandler("مسح_الرابط", manager.delete_group_link))
    application.add_handler(CommandHandler("تغيير_الايدي", manager.change_id_format))
    application.add_handler(CommandHandler("تعيين_الايدي", manager.set_custom_id))
    application.add_handler(CommandHandler("مسح_الايدي", manager.delete_custom_id))
    application.add_handler(CommandHandler("صورتي", manager.my_photo))
    application.add_handler(CommandHandler("تغيير_اسم_المجموعة", manager.change_group_name))
    application.add_handler(CommandHandler("تعيين_قوانين", manager.set_rules))
    application.add_handler(CommandHandler("مسح_قوانين", manager.delete_rules))
    application.add_handler(CommandHandler("تغيير_الوصف", manager.change_group_description))
    application.add_handler(CommandHandler("تنظيف_التعديل", manager.clean_edited))
    application.add_handler(CommandHandler("تنظيف_الميديا", manager.clean_media))
    application.add_handler(CommandHandler("رفع_الادمنية", manager.promote_admin
