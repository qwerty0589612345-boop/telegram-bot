from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime
from core.database import db

class BaseGame(ABC):
    """الفئة الأساسية لجميع الألعاب"""
    
    def __init__(self, game_type: str):
        self.game_type = game_type
        self.active_games: Dict[str, Dict] = {}
        
    @abstractmethod
    def start_game(self, chat_id: int, user_id: int) -> Dict[str, Any]:
        """بدء لعبة جديدة"""
        pass
    
    @abstractmethod
    def handle_move(self, game_id: str, user_id: int, move: Any) -> Dict[str, Any]:
        """معالجة حركة اللاعب"""
        pass
    
    def end_game(self, game_id: str, winner_id: int = None):
        """إنهاء اللعبة وتوزيع النقاط"""
        if game_id not in self.active_games:
            return
        
        game = self.active_games[game_id]
        players = game.get('players', [])
        
        # توزيع النقاط
        if winner_id:
            self._add_points(winner_id, game['chat_id'], 10)  # 10 نقاط للفائز
            for player in players:
                if player != winner_id:
                    self._add_points(player, game['chat_id'], 2)  # 2 نقاط للمشاركة
        
        # حذف اللعبة من القائمة النشطة
        del self.active_games[game_id]
    
    def _add_points(self, user_id: int, chat_id: int, points: int):
        """إضافة نقاط للاعب"""
        db.execute_query(
            '''INSERT OR REPLACE INTO user_points 
               (user_id, chat_id, points) 
               VALUES (?, ?, COALESCE((SELECT points FROM user_points WHERE user_id=? AND chat_id=?), 0) + ?)''',
            (user_id, chat_id, user_id, chat_id, points)
        )
    
    def convert_points_to_messages(self, user_id: int, chat_id: int):
        """تحويل النقاط إلى رسائل"""
        result = db.execute_query(
            '''SELECT points FROM user_points WHERE user_id=? AND chat_id=?''',
            (user_id, chat_id),
            fetch=True
        )
        
        if not result or result[0][0] < 1:
            return False
        
        points = result[0][0]
        messages = points * 25  # تحويل النقاط إلى رسائل
        
        # تحديث الرسائل
        db.execute_query(
            '''UPDATE user_stats 
               SET messages = messages + ? 
               WHERE user_id=? AND chat_id=?''',
            (messages, user_id, chat_id)
        )
        
        # إعادة تعيين النقاط
        db.execute_query(
            '''UPDATE user_points SET points = 0 WHERE user_id=? AND chat_id=?''',
            (user_id, chat_id)
        )
        
        return messages
          
