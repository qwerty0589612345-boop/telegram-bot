from .reverse_game import ReverseGame
from .emoji_quiz import EmojiQuiz
from .xo_game import XOGame
from .math_game import MathGame
from .guess_game import GuessGame
from .speed_game import SpeedGame
from .proverbs_game import ProverbsGame
from .difference_game import DifferenceGame
from .emoji_sender import EmojiSender
from .roulette import Roulette
from .number_guess import NumberGuess
from .capitals import Capitals
from .word_scramble import WordScramble
from .would_you import WouldYou
from .word_game import WordGame
from .flags_game import FlagsGame
from .truth_game import TruthGame
from .pat_game import PatGame
from .cars_game import CarsGame
from .trivia_game import TriviaGame
from .rps_game import RPSGame
from .challenge import Challenge

class GameManager:
    """مدير الألعاب المركزي"""
    
    def __init__(self):
        self.games = {
            'reverse': ReverseGame(),
            'emoji_quiz': EmojiQuiz(),
            'xo': XOGame(),
            'math': MathGame(),
            'guess': GuessGame(),
            'speed': SpeedGame(),
            'proverbs': ProverbsGame(),
            'difference': DifferenceGame(),
            'emoji_sender': EmojiSender(),
            'roulette': Roulette(),
            'number_guess': NumberGuess(),
            'capitals': Capitals(),
            'word_scramble': WordScramble(),
            'would_you': WouldYou(),
            'word_game': WordGame(),
            'flags': FlagsGame(),
            'truth': TruthGame(),
            'pat': PatGame(),
            'cars': CarsGame(),
            'trivia': TriviaGame(),
            'rps': RPSGame(),
            'challenge': Challenge()
        }
    
    def get_game(self, game_type: str):
        """الحصول على لعبة محددة"""
        return self.games.get(game_type.lower())
    
    def list_games(self):
        """قائمة جميع الألعاب المتاحة"""
        return [
            {"id": "reverse", "name": "العكس", "desc": "لعبة عكس الكلمات"},
            {"id": "emoji_quiz", "name": "معاني", "desc": "لعبة معاني الاموجي"},
            {"id": "xo", "name": "اكس او", "desc": "لعبة XO الكلاسيكية"},
            {"id": "math", "name": "رياضيات", "desc": "لعبة مسائل رياضية"},
            {"id": "guess", "name": "حزورة", "desc": "لعبة حزر الاشياء"},
            {"id": "speed", "name": "الاسرع", "desc": "لعبة السرعة في الكتابة"},
            {"id": "proverbs", "name": "امثلة", "desc": "لعبة تكملة الامثال"},
            {"id": "difference", "name": "المختلف", "desc": "لعبة كشف الاختلافات"},
            {"id": "emoji_sender", "name": "سمايلات", "desc": "لعبة ارسال السمايلات"},
            {"id": "roulette", "name": "روليت", "desc": "لعبة الحظ"},
            {"id": "number_guess", "name": "تخمين", "desc": "لعبة تخمين رقم عشوائي"},
            {"id": "capitals", "name": "عواصم", "desc": "لعبة عواصم الدول"},
            {"id": "word_scramble", "name": "تفكيك", "desc": "لعبة تفكيك الكلمات"},
            {"id": "would_you", "name": "لو خيروك", "desc": "لعبة الاختيارات الصعبة"},
            {"id": "word_game", "name": "كلمات", "desc": "لعبة كلمات متقاطعة"},
            {"id": "flags", "name": "اعلام", "desc": "لعبة اعلام الدول"},
            {"id": "truth", "name": "صراحة", "desc": "لعبة أسئلة صريحة"},
            {"id": "pat", "name": "بات", "desc": "لعبة بات محيبس"},
            {"id": "cars", "name": "سيارات", "desc": "لعبة معلومات السيارات"},
            {"id": "trivia", "name": "نشط عقلك", "desc": "لعبة اسئلة عامة"},
            {"id": "rps", "name": "حجرة", "desc": "لعبة حجرة ورقة مقص"},
            {"id": "challenge", "name": "تحدي", "desc": "لعبة تحدي الأصدقاء"}
        ]

# إنشاء مدير الألعاب الرئيسي
game_manager = GameManager()
              
