import random
from .base_game import BaseGame

class EmojiQuiz(BaseGame):
    """لعبة معاني الإيموجي"""
    
    def __init__(self):
        super().__init__("emoji_quiz")
        self.emoji_questions = {
            "😂": ["ضحك", "فرح", "سعادة"],
            "😢": ["حزن", "بكاء", "دموع"],
            "❤️": ["حب", "قلب", "عاطفة"],
            "🔥": ["نار", "حماس", "حرارة"],
            "🌟": ["نجمة", "تألق", "لمعان"]
        }
        
    def start_game(self, chat_id: int, user_id: int):
        """بدء لعبة جديدة"""
        emoji, meanings = random.choice(list(self.emoji_questions.items()))
        correct = random.choice(meanings)
        options = random.sample(meanings, min(3, len(meanings))) + ["خيار آخر"]
        random.shuffle(options)
        
        game_id = f"emoji_{chat_id}_{user_id}_{datetime.now().timestamp()}"
        self.active_games[game_id] = {
            'chat_id': chat_id,
            'player': user_id,
            'emoji': emoji,
            'correct': correct,
            'options': options
        }
        
        return {
            'game_id': game_id,
            'question': f"ما معنى هذا الإيموجي: {emoji}؟",
            'options': options,
            'correct': correct
        }
    
    def handle_move(self, game_id: str, user_id: int, answer: str):
        """معالجة إجابة اللاعب"""
        if game_id not in self.active_games:
            return {'error': 'اللعبة غير موجودة'}
        
        game = self.active_games[game_id]
        if user_id != game['player']:
            return {'error': 'ليس دورك للعب'}
        
        if answer.strip().lower() == game['correct'].lower():
            self.end_game(game_id, user_id)
            return {
                'result': True,
                'message': f"🎉 صحيح! معنى {game['emoji']} هو {game['correct']}",
                'emoji': game['emoji']
            }
        else:
            return {
                'result': False,
                'message': f"❌ خطأ، حاول مرة أخرى",
                'hint': f"المعنى يبدأ بحرف: {game['correct'][0]}"
          }
          
