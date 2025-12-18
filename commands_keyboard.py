"""
🎮 كيبورد الأوامر الشفاف - واجهة مستخدم تفاعلية
يعرض جميع الأوامر في كيبورد منظم مع أقسام واضحة
"""

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
import sqlite3

class CommandsKeyboard:
    """نظام كيبورد الأوامر الشفاف والمتطور"""
    
    def __init__(self, db_path="bot_database.db"):
        self.db_path = db_path
        self._init_database()
        self.setup_keyboards()
    
    def _init_database(self):
        """تهيئة قاعدة بيانات تفضيلات المستخدم"""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS user_preferences (
                         user_id INTEGER PRIMARY KEY,
                         keyboard_style TEXT DEFAULT 'شفاف',
                         last_menu TEXT DEFAULT 'الرئيسية',
                         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                         )''')
            conn.commit()
    
    def setup_keyboards(self):
        """إعداد جميع الكيبوردات"""
        
        # 🏠 الكيبورد الرئيسي الشفاف
        self.main_keyboard = ReplyKeyboardMarkup(
            [
                ["🎮 الألعاب", "⚙️ الإعدادات"],
                ["🛡️ الحماية", "🎵 الترفيه"],
                ["📊 الإحصائيات", "🔧 الأدوات"],
                ["❌ إخفاء الكيبورد"]
            ],
            resize_keyboard=True,
            input_field_placeholder="اختر من القائمة...",
            selective=True
        )
        
        # 🎮 كيبورد الألعاب
        self.games_keyboard = ReplyKeyboardMarkup(
            [
                ["🎯 الألعاب الاحترافية", "🎲 الألعاب العادية"],
                ["🏆 المسابقات", "🎪 التحديات"],
                ["🔙 القائمة الرئيسية"]
            ],
            resize_keyboard=True,
            input_field_placeholder="اختر نوع اللعبة..."
        )
        
        # ⚙️ كيبورد الإعدادات
        self.settings_keyboard = ReplyKeyboardMarkup(
            [
                ["🔒 إعدادات الحماية", "👥 إدارة المجموعة"],
                ["🎭 إعدادات الترفيه", "📝 إعدادات الآيدي"],
                ["🔙 القائمة الرئيسية"]
            ],
            resize_keyboard=True
        )
        
        # 🛡️ كيبورد الحماية
        self.protection_keyboard = ReplyKeyboardMarkup(
            [
                ["🔐 قفل/فتح", "🚫 إدارة المحظورات"],
                ["👮‍♂️ الصلاحيات", "📋 قائمة المنع"],
                ["🔙 القائمة الرئيسية"]
            ],
            resize_keyboard=True
        )
        
        # 📊 كيبورد الإحصائيات
        self.stats_keyboard = ReplyKeyboardMarkup(
            [
                ["👤 إحصائياتي", "📈 تفاعلي"],
                ["🏆 نقاطي", "📨 رسائلي"],
                ["🔙 القائمة الرئيسية"]
            ],
            resize_keyboard=True
        )
        
        # 🎵 كيبورد الترفيه
        self.entertainment_keyboard = ReplyKeyboardMarkup(
            [
                ["🎵 غنيلي", "🎬 أفلام"],
                ["📹 فيديوهات", "🖼️ متحركات"],
                ["🔙 القائمة الرئيسية"]
            ],
            resize_keyboard=True
        )
        
        # 🔧 كيبورد الأدوات
        self.tools_keyboard = ReplyKeyboardMarkup(
            [
                ["🗑️ مسح رسائل", "📋 الأوامر المخصصة"],
                ["🔍 بحث", "⚡ أدوات سريعة"],
                ["🔙 القائمة الرئيسية"]
            ],
            resize_keyboard=True
        )

    async def show_main_menu(self, update: Update, context: CallbackContext):
        """عرض القائمة الرئيسية"""
        await update.message.reply_text(
            "🏠 **القائمة الرئيسية**\n\n"
            "اختر من الأقسام التالية:",
            reply_markup=self.main_keyboard,
            parse_mode='Markdown'
        )
    
    async def handle_keyboard_selection(self, update: Update, context: CallbackContext):
        """معالجة اختيارات الكيبورد"""
        text = update.message.text
        
        if text == "🎮 الألعاب":
            await self.show_games_menu(update, context)
        
        elif text == "⚙️ الإعدادات":
            await self.show_settings_menu(update, context)
        
        elif text == "🛡️ الحماية":
            await self.show_protection_menu(update, context)
        
        elif text == "📊 الإحصائيات":
            await self.show_stats_menu(update, context)
        
        elif text == "🎵 الترفيه":
            await self.show_entertainment_menu(update, context)
        
        elif text == "🔧 الأدوات":
            await self.show_tools_menu(update, context)
        
        elif text == "🔙 القائمة الرئيسية":
            await self.show_main_menu(update, context)
        
        elif text == "❌ إخفاء الكيبورد":
            await self.hide_keyboard(update, context)
        
        else:
            await self.execute_command(update, context, text)

    async def show_games_menu(self, update: Update, context: CallbackContext):
        """عرض قائمة الألعاب"""
        await update.message.reply_text(
            "🎮 **قائمة الألعاب**\n\n"
            "• 🎯 الألعاب الاحترافية - تحديات ذكاء متقدمة\n"
            "• 🎲 الألعاب العادية - ألعاب مسلية بسيطة\n"
            "• 🏆 المسابقات - منافسات جماعية\n"
            "• 🎪 التحديات - اختبارات شخصية",
            reply_markup=self.games_keyboard,
            parse_mode='Markdown'
        )
    
    async def show_settings_menu(self, update: Update, context: CallbackContext):
        """عرض قائمة الإعدادات"""
        await update.message.reply_text(
            "⚙️ **قائمة الإعدادات**\n\n"
            "• 🔒 إعدادات الحماية - تحكم كامل في الأمان\n"
            "• 👥 إدارة المجموعة - إعدادات الأعضاء والمحتوى\n"
            "• 🎭 إعدادات الترفيه - تخصيص الترفيه\n"
            "• 📝 إعدادات الآيدي - تخصيص الهوية",
            reply_markup=self.settings_keyboard,
            parse_mode='Markdown'
        )
    
    async def show_protection_menu(self, update: Update, context: CallbackContext):
        """عرض قائمة الحماية"""
        await update.message.reply_text(
            "🛡️ **قائمة الحماية**\n\n"
            "• 🔐 قفل/فتح - إدارة المحتوى الممنوع\n"
            "• 🚫 إدارة المحظورات - الكلمات والأعضاء\n"
            "• 👮‍♂️ الصلاحيات - إدارة الصلاحيات\n"
            "• 📋 قائمة المنع - عرض المحظورات",
            reply_markup=self.protection_keyboard,
            parse_mode='Markdown'
        )
    
    async def show_stats_menu(self, update: Update, context: CallbackContext):
        """عرض قائمة الإحصائيات"""
        await update.message.reply_text(
            "📊 **قائمة الإحصائيات**\n\n"
            "• 👤 إحصائياتي - معلوماتك الشخصية\n"
            "• 📈 تفاعلي - مستوى نشاطك\n"
            "• 🏆 نقاطي - النقاط المكتسبة\n"
            "• 📨 رسائلي - عدد الرسائل المرسلة",
            reply_markup=self.stats_keyboard,
            parse_mode='Markdown'
        )
    
    async def show_entertainment_menu(self, update: Update, context: CallbackContext):
        """عرض قائمة الترفيه"""
        await update.message.reply_text(
            "🎵 **قائمة الترفيه**\n\n"
            "• 🎵 غنيلي - استمع إلى أغاني\n"
            "• 🎬 أفلام - مشاهدة مقاطع أفلام\n"
            "• 📹 فيديوهات - مقاطع فيديو مسلية\n"
            "• 🖼️ متحركات - صور متحركة مضحكة",
            reply_markup=self.entertainment_keyboard,
            parse_mode='Markdown'
        )
    
    async def show_tools_menu(self, update: Update, context: CallbackContext):
        """عرض قائمة الأدوات"""
        await update.message.reply_text(
            "🔧 **قائمة الأدوات**\n\n"
            "• 🗑️ مسح رسائل - تنظيف الدردشة\n"
            "• 📋 الأوامر المخصصة - إدارة الأوامر\n"
            "• 🔍 بحث - البحث في المحتوى\n"
            "• ⚡ أدوات سريعة - وظائف مفيدة",
            reply_markup=self.tools_keyboard,
            parse_mode='Markdown'
        )
    
    async def hide_keyboard(self, update: Update, context: CallbackContext):
        """إخفاء الكيبورد"""
        await update.message.reply_text(
            "✅ تم إخفاء الكيبورد\n"
            "لإظهاره مرة أخرى، اكتب /كيبورد",
            reply_markup=ReplyKeyboardRemove()
        )
    
    async def execute_command(self, update: Update, context: CallbackContext, command_text: str):
        """تنفيذ الأوامر بناءً على النص"""
        
        command_map = {
            "🎯 الألعاب الاحترافية": "/الالعاب_الاحترافية",
            "🎲 الألعاب العادية": "/الالعاب",
            "🏆 المسابقات": "/مسابقات",
            "🎪 التحديات": "/تحديات",
            "🔒 إعدادات الحماية": "/اعدادات_الحماية",
            "👥 إدارة المجموعة": "/اعدادات_المجموعة",
            "🎭 إعدادات الترفيه": "/اعدادات_الترفيه",
            "📝 إعدادات الآيدي": "/اعدادات_الايدي",
            "🔐 قفل/فتح": "/قفل_قائمة",
            "🚫 إدارة المحظورات": "/ادارة_المحظورات",
            "👮‍♂️ الصلاحيات": "/الصلاحيات",
            "📋 قائمة المنع": "/قائمة_المنع",
            "👤 إحصائياتي": "/احصائياتي",
            "📈 تفاعلي": "/تفاعلي",
            "🏆 نقاطي": "/نقاطي",
            "📨 رسائلي": "/رسائلي",
            "🎵 غنيلي": "/غنيلي",
            "🎬 أفلام": "/افلام",
            "📹 فيديوهات": "/فيديوهات",
            "🖼️ متحركات": "/متحركات",
            "🗑️ مسح رسائل": "/تنظيف",
            "📋 الأوامر المخصصة": "/الاوامر_المضافة",
            "🔍 بحث": "/بحث",
            "⚡ أدوات سريعة": "/ادوات"
        }
        
        if command_text in command_map:
            # محاكاة الأمر عن طريق إرسال النص المناسب
            context.args = []
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=command_map[command_text]
            )
        else:
            await update.message.reply_text(
                "⚠️ الأمر غير معروف\n"
                "اختر من القوائم المتاحة"
            )

    async def toggle_keyboard(self, update: Update, context: CallbackContext):
        """تبديل إظهار/إخفاء الكيبورد"""
        user_id = update.effective_user.id
        
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT keyboard_style FROM user_preferences WHERE user_id=?', (user_id,))
            result = c.fetchone()
            
            if result and result[0] == 'مخفي':
                # إظهار الكيبورد
                c.execute('UPDATE user_preferences SET keyboard_style=? WHERE user_id=?', ('شفاف', user_id))
                await self.show_main_menu(update, context)
            else:
                # إخفاء الكيبورد
                c.execute('INSERT OR REPLACE INTO user_preferences (user_id, keyboard_style) VALUES (?, ?)', 
                         (user_id, 'مخفي'))
                await self.hide_keyboard(update, context)
            
            conn.commit()

    def setup_commands(self, application):
        """تسجيل معالجات الكيبورد"""
        
        # أمر إظهار الكيبورد
        application.add_handler(CommandHandler("كيبورد", self.show_main_menu))
        application.add_handler(CommandHandler("menu", self.show_main_menu))
        application.add_handler(CommandHandler("start", self.show_main_menu))
        
        # معالجة اختيارات الكيبورد
        application.add_handler(MessageHandler(Filters.text & (~Filters.command), self.handle_keyboard_selection))
        
        # أمر تبديل الكيبورد
        application.add_handler(CommandHandler("تبديل_الكيبورد", self.toggle_keyboard))

# استخدام الفئة
def setup_interactive_keyboard(application):
    """إعداد الكيبورد التفاعلي"""
    keyboard_system = CommandsKeyboard()
    keyboard_system.setup_commands(application)

# 📱 إضافة هذا الكود إلى ملف bot.py الرئيسي
def enhance_bot_with_keyboard(bot_manager):
    """تحسين البوت بإضافة الكيبورد التفاعلي"""
    setup_interactive_keyboard(bot_manager.application)
