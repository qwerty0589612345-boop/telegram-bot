import random
from .base_game import BaseGame

class MathGame(BaseGame):
    """لعبة الرياضيات الذكية"""
    
    def __init__(self):
        super().__init__("math")
        self.operations = ['+', '-', '*', '/']
        
    def start_game(self, chat_id: int, user_id: int, difficulty: str = 'easy'):
        """بدء لعبة رياضيات جديدة"""
        if difficulty == 'easy':
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            operation = random.choice(['+', '-'])
        elif difficulty == 'medium':
            num1 = random.randint(5, 20)
            num2 = random.randint(5, 20)
            operation = random.choice(['+', '-', '*'])
        else:  # hard
            num1 = random.randint(10, 30)
            num2 = random.randint(1, 10)
            operation = random.choice(self.operations)
        
        # حساب النتيجة الصحيحة
        if operation == '+':
            answer = num1 + num2
        elif operation == '-':
            answer = num1 - num2
        elif operation == '*':
            answer = num1 * num2
        else:  # division
            num1 = num2 * random.randint(1, 5)  # للتأكد من وجود نتيجة صحيحة
            answer = num1 // num2
        
        question = f"{num1} {operation} {num2} = ؟"
        
        game_id = f"math_{chat_id}_{user_id}_{datetime.now().timestamp()}"
        self.active_games[game_id] = {
            'chat_id': chat_id,
            'player': user_id,
            'question': question,
            'answer': answer,
            'difficulty': difficulty,
            'start_time': datetime.now()
        }
        
        return {
            'game_id': game_id,
            'question': question,
            'difficulty': difficulty,
            'time_limit': 30  # ثانية للإجابة
        }
    
    def handle_move(self, game_id: str, user_id: int, answer: str):
        """معالجة إجابة اللاعب"""
        if game_id not in self.active_games:
            return {'error': 'اللعبة غير موجودة'}
        
        game = self.active_games[game_id]
        if user_id != game['player']:
            return {'error': 'ليس دورك للعب'}
        
        try:
            user_answer = int(answer)
        except ValueError:
            return {'error': 'الإجابة يجب أن تكون رقماً'}
        
        if user_answer == game['answer']:
            points = {'easy': 5, 'medium': 10, 'hard': 15}[game['difficulty']]
            self._add_points(user_id, game['chat_id'], points)
            self.end_game(game_id, user_id)
            return {
                'result': True,
                'message': f"🎉 إجابة صحيحة! لقد كسبت {points} نقاط",
                'correct_answer': game['answer']
            }
        else:
            return {
                'result': False,
                'message': "❌ إجابة خاطئة، حاول مرة أخرى",
                'hint': f"الإجابة بين {game['answer']-3} و {game['answer']+3}"
          }
          
