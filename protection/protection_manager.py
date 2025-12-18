from typing import Dict, Optional
from telegram import Update
from telegram.ext import CallbackContext
from .penalty_system import PenaltySystem
from .content_analysis import ContentAnalyzer
from core.database import db

class ProtectionManager:
    """مدير نظام الحماية الرئيسي"""
    
    def __init__(self):
        self.penalty = PenaltySystem()
        self.analyzer = ContentAnalyzer()
        
    def apply_protection(self, update: Update, context: CallbackContext):
        """تطبيق قواعد الحماية على الرسائل"""
        if not update.message or not update.message.chat:
            return
        
        chat_id = update.message.chat.id
        user = update.message.from_user
        
        # تخطي الرسائل من المدراء
        if self._is_admin(chat_id, user.id):
            return
        
        # التحقق من جميع أنواع الحماية
        violations = self._check_violations(update.message, chat_id)
        
        # تطبيق العقوبات المحددة
        for violation in violations:
            self.penalty.apply_penalty(
                chat_id=chat_id,
                user_id=user.id,
                violation_type=violation['type'],
                penalty=violation['penalty']
            )
    
    def _check_violations(self, message, chat_id: int) -> list:
        """فحص انتهاكات الحماية"""
        violations = []
        
        # فحص أنواع المحتوى المختلفة
        content_type = self.analyzer.detect_content_type(message)
        if content_type:
            protection = db.get_protection(chat_id, content_type['type'])
            if protection and protection['is_active']:
                violations.append({
                    'type': content_type['type'],
                    'penalty': protection['penalty']
                })
        
        # فحص التكرار (Spam)
        if self.analyzer.is_spam(message, chat_id):
            protection = db.get_protection(chat_id, 'التكرار')
            if protection and protection['is_active']:
                violations.append({
                    'type': 'التكرار',
                    'penalty': protection['penalty']
                })
        
        return violations
    
    def _is_admin(self, chat_id: int, user_id: int) -> bool:
        """التحقق إذا كان المستخدم مديرًا"""
        # هنا يمكن استبدالها بوظيفة تستعلم عن صلاحيات المستخدم
        return False
      
