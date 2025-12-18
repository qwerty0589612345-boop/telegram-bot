import sqlite3
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import threading

class SmartCache:
    """نظام كاش ذكي لتحسين الأداء"""
    def __init__(self, max_size=1000, ttl=300):
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl  # وقت انتهاء الصلاحية بالثواني
        
    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.ttl):
                return data
            else:
                del self.cache[key]
        return None
        
    def set(self, key: str, value: Any):
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        self.cache[key] = (value, datetime.now())
        
    def _evict_oldest(self):
        oldest_key = min(self.cache.keys(), 
                        key=lambda k: self.cache[k][1])
        del self.cache[oldest_key]

class DatabaseManager:
    def __init__(self, db_path="smart_bot.db"):
        self.db_path = db_path
        self.cache = SmartCache()
        self.lock = threading.Lock()
        self._init_database()
        
    def _init_database(self):
        """تهيئة قاعدة البيانات بجداول متقدمة"""
        tables = {
            'protection_settings': '''
                CREATE TABLE IF NOT EXISTS protection_settings (
                    chat_id INTEGER,
                    feature TEXT,
                    is_active BOOLEAN DEFAULT FALSE,
                    penalty_type TEXT DEFAULT 'delete',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (chat_id, feature)
                )
            ''',
            'custom_replies': '''
                CREATE TABLE IF NOT EXISTS custom_replies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER,
                    trigger_text TEXT,
                    reply_text TEXT,
                    reply_type TEXT DEFAULT 'text',
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'user_stats': '''
                CREATE TABLE IF NOT EXISTS user_stats (
                    user_id INTEGER,
                    chat_id INTEGER,
                    messages_sent INTEGER DEFAULT 0,
                    games_played INTEGER DEFAULT 0,
                    points INTEGER DEFAULT 0,
                    last_active TIMESTAMP,
                    PRIMARY KEY (user_id, chat_id)
                )
            ''',
            'game_sessions': '''
                CREATE TABLE IF NOT EXISTS game_sessions (
                    session_id TEXT PRIMARY KEY,
                    game_type TEXT,
                    players TEXT,  JSON
                    game_state TEXT,  JSON
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''
        }
        
        with self.lock, sqlite3.connect(self.db_path) as conn:
            for table_name, schema in tables.items():
                conn.execute(schema)
            conn.commit()
    
    def execute_query(self, query: str, params: tuple = (), fetch: bool = False):
        """تنفيذ استعلام مع معالجة الأخطاء"""
        cache_key = f"{query}{params}"
        
        if not fetch:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cached
        
        try:
            with self.lock, sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(query, params)
                
                if fetch:
                    result = [dict(row) for row in cursor.fetchall()]
                    if result:
                        self.cache.set(cache_key, result)
                    return result
                else:
                    conn.commit()
                    self.cache.set(cache_key, cursor.rowcount)
                    return cursor.rowcount
                    
        except sqlite3.Error as e:
            print(f"❌ خطأ في قاعدة البيانات: {e}")
            return None
    
    def get_protection_status(self, chat_id: int, feature: str) -> Dict:
        """الحصول على حالة الحماية مع الكاش"""
        query = "SELECT * FROM protection_settings WHERE chat_id = ? AND feature = ?"
        result = self.execute_query(query, (chat_id, feature), fetch=True)
        return result[0] if result else None
    
    def add_custom_reply(self, chat_id: int, trigger: str, reply: str, reply_type: str = "text"):
        """إضافة رد مخصص"""
        query = '''
            INSERT OR REPLACE INTO custom_replies 
            (chat_id, trigger_text, reply_text, reply_type) 
            VALUES (?, ?, ?, ?)
        '''
        return self.execute_query(query, (chat_id, trigger.lower(), reply, reply_type))
