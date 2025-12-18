import random
from .base_game import BaseGame

class ReverseGame(BaseGame):
    """لعبة عكس الكلمات"""
    
    def __init__(self):
        super().__init__("reverse")
        self.words = ["كمبيوتر", "هاتف", "سيارة", "شجرة", "كتاب", "قلم", "مدرسة", "حاسوب"]
        
    def start_game(self, chat_id: int, user_id: int):
        """بدء لعبة جديدة"""
        word = random.choice(self.words)
        reversed_word = word[::-1]
        
        game_id = f"reverse_{chat_id}_{user_id}_{datetime.now().timestamp()}"
        self.active_games[game_id] = {
            'chat_id': chat_id,
            'player': user_id,
            'word': word,
            'reversed': reversed_word,
            'start_time': datetime.now()
        }
        
        return {
            'game_id': game_id,
            'question': f"ما هي الكلمة الأصلية لكلمة: {reversed_word}؟",
            'answer': word,
            'hint': f"الحرف الأول: {word[0]} | عدد الأحرف: {len(word)}"
        }
    
    def handle_move(self, game_id: str, user_id: int, answer: str):
        """معالجة إجابة اللاعب"""
        if game_id not in self.active_games:
            return {'error': 'اللعبة غير موجودة'}
        
        game = self.active_games[game_id]
        if user_id != game['player']:
            return {'error': 'ليس دورك للعب'}
        
        if answer.strip().lower() == game['word'].lower():
            self.end_game(game_id, user_id)
            return {
                'result': True,
                'message': "🎉 أحسنت! إجابة صحيحة",
                'word': game['word']
            }
        else:
            return {
                'result': False,
                'message': "❌ إجابة خاطئة، حاول مرة أخرى",
                'hint': game['hint']
  }
      
