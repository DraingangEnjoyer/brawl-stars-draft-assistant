import sqlite3
import brawlstats


API_KEY = ""
client = brawlstats.Client(API_KEY)


conn = sqlite3.connect("brawl_data.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS brawlers (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")
conn.commit()

try:
    print("Pobieram listę Zadymiarzy z API...")
    brawlers = client.get_brawlers()
    
    
    for b in brawlers:
        cursor.execute("""
        INSERT OR REPLACE INTO brawlers (id, name)
        VALUES (?, ?)
        """, (b.id, b.name))
        
    conn.commit()
    print(f"Sukces! Zapisano {len(brawlers)} Zadymiarzy w bazie danych.")

except Exception as e:
    print(f"Wystąpił błąd: {e}")

finally:
    conn.close()