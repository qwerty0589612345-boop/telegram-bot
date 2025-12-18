import os
from typing import List

# إعدادات البوت
BOT_TOKEN = os.getenv("BOT_TOKEN", "8257887627:AAEZ2I9Q97ma1C07Hp1bKNHLibIVsrQLCxc")

# إعدادات قاعدة البيانات
DATABASE_CONFIG = {
    "path": "smart_bot.db",
    "backup_interval": 3600,  # نسخ احتياطي كل ساعة
    "auto_cleanup": True
}

# إعدادات الأمان
SECURITY_CONFIG = {
    "max_message_length": 4096,
    "max_media_size": 50 * 1024 * 1024,  # 50MB
    "rate_limit_per_user": 10,  # 10 رسائل في الدقيقة
    "allowed_chat_types": ["group", "supergroup", "private"]
}

# قائمة المطورين
DEVELOPER_IDS = [7127207234]  # أضف معرفات المطورين

# إعدادات الألعاب
GAME_CONFIG = {
    "xo_timeout": 300,  # 5 دقائق
    "max_games_per_user": 3,
    "points_per_win": 10,
    "points_per_draw": 5
}
