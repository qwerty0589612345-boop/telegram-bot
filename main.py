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
          
from games import game_manager

def setup_games_commands(bot):
    """إعداد أوامر الألعاب"""
    
    @bot.command('الالعاب')
    async def games_list(update: Update, context: CallbackContext):
        """عرض قائمة الألعاب"""
        games = game_manager.list_games()
        response = "🎮 قائمة الألعاب المتاحة:\n\n"
        response += "\n".join(
            f"{i+1}. {game['name']} - {game['desc']} (/{game['id']})"
            for i, game in enumerate(games)
        )
        await update.message.reply_text(response)
    
    @bot.command('xo')
    async def start_xo_game(update: Update, context: CallbackContext):
        """بدء لعبة XO"""
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        
        # إذا تم ذكر لاعب آخر
        opponent_id = None
        if context.args and context.args[0].startswith('@'):
            opponent_username = context.args[0][1:]
            # هنا يجب البحث عن معرف اللاعب الثاني حسب اليوزرنيم
            
        game = game_manager.get_game('xo')
        result = game.start_game(chat_id, user_id, opponent_id)
        
        if 'error' in result:
            await update.message.reply_text(f"❌ {result['error']}")
            return
        
        # عرض لوحة اللعبة
        board = "\n".join(" | ".join(cell if cell else "⬜" for cell in row) for row in result['board'])
        await update.message.reply_text(
            f"🎮 بدأت لعبة XO!\n\n{board}\n\n{result['message']}",
            reply_markup=XOGameKeyboard(result['game_id'])
        )
    
    # إضافة أوامر للألعاب الأخرى بنفس الطريقة
    # ...
    
