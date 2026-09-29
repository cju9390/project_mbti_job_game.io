import sqlite3
import os
from model import MBTI_STAT_BONUS

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'guild.db')

MBTI_JOBS = {
    "INTJ": "대마법사(Archmage)", "INTP": "연금술사(Alchemist)",
    "ENTJ": "총사령관(Commander)", "ENTP": "환영술사(Illusionist)",
    "INFJ": "예언자(Oracle)", "INFP": "바드(Bard)",
    "ENFJ": "성기사(Paladin)", "ENFP": "유랑객(Wanderer)",
    "ISTJ": "수호 기사(Guardian)", "ISFJ": "성직자(Cleric)",
    "ESTJ": "길드 마스터(Guild Master)", "ESFJ": "치유사(Healer)",
    "ISTP": "어쌔신(Assassin)", "ISFP": "드루이드(Druid)",
    "ESTP": "격투가(Fighter)", "ESFP": "어릿광대(Jester)"
}

FANTASY_NAMES = {
    "INTJ": "알드릭", "INTP": "엘리온", "ENTJ": "발레리우스", "ENTP": "자크스",
    "INFJ": "셀레네", "INFP": "리안", "ENFJ": "테오도르", "ENFP": "피핀",
    "ISTJ": "바르가스", "ISFJ": "안나", "ESTJ": "케드릭", "ESFJ": "엘라",
    "ISTP": "카일", "ISFP": "미라", "ESTP": "렉스", "ESFP": "리오"
}

STAT_WEIGHTS = {
    'E': [0.5, 0,   0,   1.0, 1.5, 0  ],
    'I': [0,   1.0, 0.5, 0,   0,   1.5],
    'S': [1.5, 0,   1.0, 0.5, 0,   1.0],
    'N': [0,   1.5, 0,   1.0, 1.0, 0  ],
    'T': [1.5, 1.0, 0,   0,   1.0, 0.5],
    'F': [0,   0,   2.0, 0.5, 0.5, 1.0],
    'J': [0.5, 0,   1.0, 0,   2.0, 1.5],
    'P': [1.0, 1.0, 0,   2.0, 0,   0.5],
}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, mbti TEXT, job TEXT,
                  atk REAL, mag REAL, holy REAL,
                  dex REAL, lead REAL, sur REAL,
                  img_url TEXT)''')
    conn.commit()
    conn.close()

def save_user_result(name, mbti, job, stats):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    img_url = f"{mbti}.png"
    c.execute('''INSERT INTO users (name, mbti, job, atk, mag, holy, dex, lead, sur, img_url)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (name, mbti, job, *stats, img_url))
    conn.commit()
    conn.close()

def calculate_npc_stats(mbti):
    stats = [3.0] * 6
    for char in mbti:
        weights = STAT_WEIGHTS[char]
        for i in range(6):
            stats[i] += weights[i]
    stats = [min(10.0, round(s, 1)) for s in stats]
    bonus = MBTI_STAT_BONUS.get(mbti, [0] * 6)
    return [min(10.0, stats[i] + bonus[i]) for i in range(6)]

def seed_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM users")
    for mbti, job in MBTI_JOBS.items():
        name = FANTASY_NAMES[mbti]
        stats = calculate_npc_stats(mbti)
        img_url = f"{mbti}.png"
        c.execute('''INSERT INTO users (name, mbti, job, atk, mag, holy, dex, lead, sur, img_url)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (name, mbti, job, *stats, img_url))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    seed_data()
