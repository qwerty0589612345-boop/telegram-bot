from telegram import Update
from telegram.ext import CallbackContext
from core.database import db

PROTECTION_TYPES = [
    "التاك", "القناة", "الصور", "الرابط", "الفشار", "الموقع",
    "التكرار", "الفيديو", "الدخول", "الاضافة", "الاغاني", "الصوت",
    "الملفات", "الرسائل", "الدردشة", "الجهات", "السيلفي", "التثبيت",
    "الشارحة", "الكلايش", "البوتات", "التوجيه", "التعديل", "الانلاين",
    "المعرفات", "الكيبورد", "الفارسية", "الانكليزية", "الاستفتاء",
    "الملصقات", "الاشعارات", "الماركداون", "المتحركات"
]

PENALTY_TYPES = ["بالتقيد", "بالطرد", "بالكتم", "بالتقييد"]

def lock_command(update: Update, context: CallbackContext):
    """أمر القفل"""
    chat_id = update.message.chat.id
    args = context.args
    
    if not args or args[0].lower() not in PROTECTION_TYPES:
        update.message.reply_text(
            "🔒 **أمر القفل:**\n\n"
            "◍ استخدم: `/قفل النوع [العقوبة]`\n"
            "◍ مثال: `/قفل الصور بالطرد`\n\n"
            "**الأنواع المتاحة:**\n" + "\n".join(PROTECTION_TYPES) + "\n\n"
            "**أنواع العقوبات:**\n" + "\n".join(PENALTY_TYPES)
        )
        return
    
    lock_type = args[0].lower()
    penalty = args[1].lower() if len(args) > 1 else "بالتقيد"
    
    if penalty not in PENALTY_TYPES:
        update.message.reply_text(f"❌ العقوبة {penalty} غير موجودة!")
        return
    
    db.set_protection(chat_id, lock_type, is_active=True, penalty=penalty)
    update.message.reply_text(f"✅ تم قفل {lock_type} بنجاح ({penalty})")

def unlock_command(update: Update, context: CallbackContext):
    """أمر الفتح"""
    chat_id = update.message.chat.id
    args = context.args
    
    if not args or args[0].lower() not in PROTECTION_TYPES:
        update.message.reply_text(
            "🔓 **أمر الفتح:**\n\n"
            "◍ استخدم: `/فتح النوع`\n"
            "◍ مثال: `/فتح الصور`\n\n"
            "**الأنواع المتاحة:**\n" + "\n".join(PROTECTION_TYPES)
        )
        return
    
    lock_type = args[0].lower()
    
    db.set_protection(chat_id, lock_type, is_active=False)
    update.message.reply_text(f"✅ تم فتح {lock_type} بنجاح")
