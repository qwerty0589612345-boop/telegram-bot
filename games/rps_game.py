import random
from .base_game import BaseGame

class RPSGame(BaseGame):
    """لعبة حجرة ورقة مقص"""
    
    def __init__(self):
        super().__init__("rps")
        self.choices = {
            "حجرة": "✊",
            "ورقة": "✋",
            "مقص": "✌️"
        }
        self.rules = {
            "حجرة": {"حجرة": 0, "ورقة": -1, "مقص": 1},
            "ورقة": {"حجرة": 1, "ورقة": 0, "مقص": -1},
            "مقص": {"حجرة": -1, "ورقة": 1, "مقص": 0}
        }
        
    def start_game(self, chat_id: int, user_id: int):
        """بدء لعبة جديدة"""
        game_id = f"rps_{chat_id}_{user_id}_{datetime.now().timestamp()}"
        self.active_games[game_id] = {
            'chat_id': chat_id,
            'player': user_id,
            'start_time': datetime.now(),
            'rounds': 0,
            'wins': 0,
            'losses': 0
        }
        
        return {
            'game_id': game_id,
            'message': "اختر أحد الخيارات: حجرة، ورقة، مقص",
            'choices': list(self.choices.keys())
        }
    
    def handle_move(self, game_id: str, user_id: int, choice: str):
        """معالجة اختيار اللاعب"""
        if game_id not in self.active_games:
            return {'error': 'اللعبة غير موجودة'}
        
        game = self.active_games[game_id]
        if user_id != game['player']:
            return {'error': 'ليس دورك للعب'}
        
        if choice.lower() not in self.choices:
            return {'error': 'اختيار غير صحيح'}
        
        # اختيار البوت عشوائياً
        bot_choice = random.choice(list(self.choices.keys()))
        
        # تحديد الفائز
        result = self.rules[choice.lower()][bot_choice]
        
        game['rounds'] += 1
        if result == 1:
            game['wins'] += 1
            message = f"🎉 فزت! {self.choices[choice]} يهزم {self.choices[bot_choice]}"
        elif result == -1:
            game['losses'] += 1
            message = f"❌ خسرت! {self.choices[bot_choice]} يهزم {self.choices[choice]}"
        else:
            message = f"⚖️ تعادل! كلانا اختار {self.choices[choice]}"
        
        # إذا كانت الجولة الخامسة، إنهاء اللعبة
        if game['rounds'] >= 5:
            if game['wins'] > game['losses']:
                final_message = f"🏆 فزت بالمباراة! {game['wins']}-{game['losses']}"
                self.end_game(game_id, user_id)
            elif game['losses'] > game['wins']:
                final_message = f"💣 خسرت المباراة! {game['wins']}-{game['losses']}"
                self.end_game(game_id)
            else:
                final_message = f"🤝 انتهت المباراة بالتعادل! {game['wins']}-{game['losses']}"
                self.end_game(game_id)
            
            return {
                'game_over': True,
                'message': f"{message}\n\n{final_message}",
                'player_choice': self.choices[choice],
                'bot_choice': self.choices[bot_choice],
                'score': f"{game['wins']}-{game['losses']}"
            }
        
        return {
            'message': message,
            'player_choice': self.choices[choice],
            'bot_choice': self.choices[bot_choice],
            'score': f"{game['wins']}-{game['losses']}",
            'rounds_left': 5 - game['rounds']
  }
                                                    
