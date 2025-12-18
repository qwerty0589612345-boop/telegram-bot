from telegram import ChatPermissions
from datetime import datetime, timedelta
import time
from typing import Literal

class PenaltySystem:
    """نظام العقوبات الذكي"""
    
    def apply_penalty(self, chat_id: int, user_id: int, 
                     violation_type: str, 
                     penalty: Literal['بالتقيد', 'بالطرد', 'بالكتم', 'بالتقييد']):
        """تطبيق العقوبة المناسبة"""
        try:
            # حذف الرسالة المخالفة
            if update.message:
                update.message.delete()
            
            # تطبيق العقوبة حسب النوع
            if penalty == 'بالكتم':
                until = int(time.time()) + 3600  # كتم لمدة ساعة
                context.bot.restrict_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=until
                )
                context.bot.send_message(
                    chat_id=chat_id,
                    text=f"🔇 تم كتم @{user.username} لمدة ساعة بسبب: {violation_type}"
                )
                
            elif penalty == 'بالطرد':
                context.bot.ban_chat_member(chat_id, user_id)
                context.bot.send_message(
                    chat_id=chat_id,
                    text=f"🚫 تم طرد @{user.username} بسبب: {violation_type}"
                )
                
            elif penalty == 'بالتقييد':
                until = int(time.time()) + 3600  # تقييد لمدة ساعة
                context.bot.restrict_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    permissions=ChatPermissions(
                        can_send_messages=False,
                        can_send_media_messages=False,
                        can_send_polls=False,
                        can_send_other_messages=False,
                        can_add_web_page_previews=False
                    ),
                    until_date=until
                )
                context.bot.send_message(
                    chat_id=chat_id,
                    text=f"⛔ تم تقييد @{user.username} لمدة ساعة بسبب: {violation_type}"
                )
            
            elif penalty == 'بالتقيد':
                # تحذير فقط
                context.bot.send_message(
                    chat_id=chat_id,
                    text=f"⚠️ تحذير: @{user.username} - {violation_type}"
                )
                
        except Exception as e:
            print(f"❌ خطأ في تطبيق العقوبة: {e}")
          
