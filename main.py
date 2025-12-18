#!/usr/bin/env python3
"""
🤖 بوت تيليجرام متكامل - الإصدار المتطور
أحدث التقنيات وأذكى الأكواد
"""

import asyncio
from core.bot import create_bot
from core.database import DatabaseManager
from commands.protection import setup_protection_commands
from commands.settings import setup_settings_commands
from commands.games import setup_games_commands
from interface.keyboards import SmartKeyboard
from config import BOT_TOKEN

async def main():
    """الدالة الرئيسية للتشغيل"""
    try:
        # إنشاء وإعداد البوت
        bot = create_bot(BOT_TOKEN)
        
        # إعداد القواعد الأساسية
        bot.setup_logging()
        bot.dispatcher.add_error_handler(bot.smart_error_handler)
        
        # إعداد الوحدات
        setup_protection_commands(bot)
        setup_settings_commands(bot)
        setup_games_commands(bot)
        
        # أمر البدء الذكي
        async def smart_start(update, context):
            user = update.effective_user
            welcome_text = f"""
🎉 **مرحباً {user.first_name}!**

🤖 أنا بوت حماية متكامل ذكي، مزود بأحدث التقنيات:

✨ **المميزات:**
- 🛡️ حماية ذكية للمجموعات
- 🎮 ألعاب تفاعلية متطورة  
- ⚙️ إعدادات متقدمة
- 📊 إحصائيات ذكية
- 🎯 ردود ذكية

استخدم الأزرار أدناه للتحكم ⬇️
            """
            
            await update.message.reply_text(
                welcome_text,
                reply_markup=SmartKeyboard.create_main_menu(),
                parse_mode='Markdown'
            )
        
        bot.register_handler('command', 'start', smart_start)
        
        # بدء التشغيل
        print("🚀 تشغيل البوت المتطور...")
        bot.start()
        
    except Exception as e:
        print(f"💥 خطأ فادح: {e}")
        # إعادة التشغيل التلقائي بعد 5 ثواني
        await asyncio.sleep(5)
        await main()

if __name__ == "__main__":
    # تشغيل البوت
    asyncio.run(main())
          
