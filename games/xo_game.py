import random
from typing import Dict, List, Optional
from datetime import datetime
from core.database import db

class XOGame:
    def __init__(self):
        self.games: Dict[str, Dict] = {}
    
    def create_game(self, player1_id: int, player2_id: int = None) -> str:
        """إنشاء لعبة XO جديدة"""
        game_id = f"xo_{player1_id}_{datetime.now().timestamp()}"
        
        self.games[game_id] = {
            'board': [['' for _ in range(3)] for _ in range(3)],
            'players': {'X': player1_id, 'O': player2_id or self._create_bot()},
            'current_player': 'X',
            'created_at': datetime.now(),
            'moves': 0
        }
        
        return game_id
    
    def make_move(self, game_id: str, row: int, col: int, player_id: int) -> Dict:
        """تنفيذ حركة في اللعبة"""
        game = self.games.get(game_id)
        if not game:
            return {'error': 'اللعبة غير موجودة'}
        
        if game['players'][game['current_player']] != player_id:
            return {'error': 'ليس دورك للعب'}
        
        if game['board'][row][col] != '':
            return {'error': 'هذه الخلية محجوزة'}
        
        game['board'][row][col] = game['current_player']
        game['moves'] += 1
        
        result = self._check_winner(game['board'])
        if result:
            game['winner'] = result
            return {'winner': result, 'board': game['board']}
        
        if game['moves'] >= 9:
            game['winner'] = 'draw'
            return {'winner': 'draw', 'board': game['board']}
        
        # تبديل اللاعب
        game['current_player'] = 'O' if game['current_player'] == 'X' else 'X'
        
        # إذا كان اللاعب التالي بوت
        if isinstance(game['players'][game['current_player']], str):
            return self._make_bot_move(game_id)
        
        return {'board': game['board'], 'next_player': game['current_player']}
    
    def _make_bot_move(self, game_id: str) -> Dict:
        """تنفيذ حركة البوت"""
        game = self.games[game_id]
        empty_cells = [(i, j) for i in range(3) for j in range(3) 
                      if game['board'][i][j] == '']
        
        if empty_cells:
            row, col = random.choice(empty_cells)
            return self.make_move(game_id, row, col, game['players'][game['current_player']])
        
        return {'winner': 'draw', 'board': game['board']}
    
    def _check_winner(self, board: List[List[str]]) -> Optional[str]:
        """فحص الفائز"""
        # فحص الصفوف والأعمدة
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != '':
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != '':
                return board[0][i]
        
        # فحص القطرين
        if board[0][0] == board[1][1] == board[2][2] != '':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != '':
            return board[0][2]
        
        return None
    
    def _create_bot(self) -> str:
        """إنشاء بوت للعب"""
        return "xo_bot"
          
