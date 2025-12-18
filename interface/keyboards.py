from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from typing import List, Dict, Tuple

class SmartKeyboard:
    """نظام كيبورد ذكي ومتطور"""
    
    @staticmethod
    def create_main_menu(user_role: str = "member") -> InlineKeyboardMarkup:
        """إنشاء القائمة الرئيسية الذكية حسب دور المستخدم"""
        base_buttons = [
            [InlineKeyboardButton("🛡️ الحماية الذكية", callback_data="protection_menu")],
            [InlineKeyboardButton("⚙️ الإعدادات المتقدمة", callback_data="settings_menu")],
            [InlineKeyboardButton("🎮 مركز الألعاب", callback_data="games_center")],
        ]
        
        if user_role in ["admin", "owner"]:
            base_buttons.append([InlineKeyboardButton("👑 أدوات الإدارة", callback_data="admin_tools")])
        
        base_buttons.append([InlineKeyboardButton("ℹ️ المساعدة", callback_data="help")])
        
        return InlineKeyboardMarkup(base_buttons)
    
    @staticmethod
    def create_protection_menu(chat_id: int) -> InlineKeyboardMarkup:
        """كيبورد الحماية الديناميكي"""
        from core.database import db
        
        protection_features = [
            ("التاك", "mention_protection"),
            ("الصور", "photo_protection"),
            ("الروابط", "link_protection"),
            ("الفيديوهات", "video_protection"),
            ("الملصقات", "sticker_protection"),
            ("البوتات", "bot_protection")
        ]
        
        keyboard = []
        row = []
        
        for feature_name, feature_key in protection_features:
            status = db.get_protection_status(chat_id, feature_key)
            icon = "🔒" if status and status['is_active'] else "🔓"
            
            row.append(InlineKeyboardButton(
                f"{icon} {feature_name}", 
                callback_data=f"toggle_protection_{feature_key}"
            ))
            
            if len(row) == 2:
                keyboard.append(row)
                row = []
        
        if row:
            keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton("🔙 الرجوع", callback_data="main_menu")])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_xo_game_board(board: List[List[str]], game_id: str) -> InlineKeyboardMarkup:
        """إنشاء لوحة لعبة XO ذكية"""
        keyboard = []
        for i, row in enumerate(board):
            keyboard_row = []
            for j, cell in enumerate(row):
                emoji = "⭕" if cell == "X" else "❌" if cell == "O" else "⬜"
                keyboard_row.append(
                    InlineKeyboardButton(emoji, callback_data=f"xo_move_{game_id}_{i}_{j}")
                )
            keyboard.append(keyboard_row)
        
        keyboard.append([InlineKeyboardButton("🔄 إعادة اللعبة", callback_data=f"xo_restart_{game_id}")])
        keyboard.append([InlineKeyboardButton("🔚 إنهاء اللعبة", callback_data="games_center")])
        
        return InlineKeyboardMarkup(keyboard)

class DynamicReplyKeyboard:
    """كيبورد الرد الديناميكي"""
    
    @staticmethod
    def get_contextual_keyboard(chat_type: str, user_status: str) -> ReplyKeyboardMarkup:
        """كيبورد يتكيف مع السياق"""
        if chat_type == "private":
            keyboard = [
                ["🎮 الألعاب", "⚙️ الإعدادات"],
                ["🛡️ الحماية", "ℹ️ المساعدة"]
            ]
        else:
            if user_status in ["creator", "administrator"]:
                keyboard = [
                    ["🔒 قفل الصور", "🔓 فتح الروابط"],
                    ["👥 إدارة الأعضاء", "📊 الإحصائيات"],
                    ["🎯 الألعاب", "⚙️ الإعدادات"]
                ]
            else:
                keyboard = [
                    ["🎮 الألعاب", "📊 نقاطي"],
                    ["ℹ️ معلوماتي", "🆘 المساعدة"]
                ]
        
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
              
