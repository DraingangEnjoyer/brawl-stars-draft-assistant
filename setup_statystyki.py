import sqlite3

conn = sqlite3.connect("brawl_data.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS battle_logs (
    battle_time TEXT,
    map_name TEXT,
    brawler_name TEXT,
    result TEXT,
    PRIMARY KEY (battle_time, brawler_name)
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS map_stats (
    map_name TEXT,
    brawler_name TEXT,
    wins INTEGER DEFAULT 0,
    total_games INTEGER DEFAULT 0,
    PRIMARY KEY (map_name, brawler_name)
)
""")

conn.commit()
conn.close()

print(" Tabela meczów i statystyk map zostały pomyślnie utworzone!")