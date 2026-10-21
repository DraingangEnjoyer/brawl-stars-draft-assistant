import sqlite3
import brawlstats


API_KEY = ""


client = brawlstats.Client(API_KEY)


conn = sqlite3.connect("brawl_data.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS gracze (
    tag TEXT PRIMARY KEY,
    nazwa TEXT,
    pucharki INTEGER
)
""")
conn.commit()

try:
    
    player_tag = "#2PP"
    player = client.get_profile(player_tag)
    
    print(f"Pobrano gracza: {player.name} (Pucharki: {player.trophies})")
    
    
    cursor.execute("""
    INSERT OR REPLACE INTO gracze (tag, nazwa, pucharki)
    VALUES (?, ?, ?)
    """, (player.tag, player.name, player.trophies))
    
    conn.commit()
    print("Sukces! Dane zostały zapisane w lokalnej bazie danych (brawl_data.db).")

except Exception as e:
    print(f"Wystąpił błąd: {e}")

finally:
    
    conn.close()