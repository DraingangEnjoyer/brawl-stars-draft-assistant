import sqlite3
import brawlstats

API_KEY = ""

client = brawlstats.Client(API_KEY)

def analizuj_mecze_gracza(player_tag):
    clean_tag = player_tag.strip().upper()
    if not clean_tag.startswith("#"):
        clean_tag = "#" + clean_tag

    conn = sqlite3.connect("brawl_data.db")
    cursor = conn.cursor()
    
    try:
        print(f"🔍 Pobieram historię dla gracza: {clean_tag}...")
        battles = client.get_battle_logs(clean_tag)
        
        if not battles:
            print(f"⚠️ API zwróciło 0 meczów dla {clean_tag}.")
            return

        nowe_mecze = 0
        pominiete = 0
        
        for item in battles:
            
            b_data = getattr(item, 'battle', item)
            
            
            mapa = getattr(b_data, 'map', None)
            if not mapa and hasattr(item, 'event'):
                mapa = getattr(item.event, 'map', None)

            
            result = getattr(b_data, 'result', None)
            battle_time = getattr(item, 'battle_time', '')

            
            if not mapa or result not in ['victory', 'defeat']:
                pominiete += 1
                continue

            
            teams = getattr(b_data, 'teams', None)
            
            if teams:
                for team in teams:
                    for player in team:
                        brawler_info = getattr(player, 'brawler', None)
                        if brawler_info:
                            brawler = getattr(brawler_info, 'name', '').upper()
                            if not brawler:
                                continue
                                
                            try:
                                cursor.execute("""
                                INSERT INTO battle_logs (battle_time, map_name, brawler_name, result)
                                VALUES (?, ?, ?, ?)
                                """, (battle_time, mapa, brawler, result))
                                
                                wygrana = 1 if result == 'victory' else 0
                                cursor.execute("""
                                INSERT INTO map_stats (map_name, brawler_name, wins, total_games)
                                VALUES (?, ?, ?, 1)
                                ON CONFLICT(map_name, brawler_name) DO UPDATE SET
                                    wins = wins + ?,
                                    total_games = total_games + 1
                                """, (mapa, brawler, wygrana, wygrana))
                                
                                nowe_mecze += 1
                            except sqlite3.IntegrityError:
                                
                                pass

        conn.commit()
        print(f"✅ Dodano {nowe_mecze} zapisów brawlerów z meczów! (Pominięte/Inne tryby: {pominiete})")
        
    except Exception as e:
        print(f"❌ Błąd dla {clean_tag}: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    
    TAGI = [
         "#8LQCUYPYL", 
         "#9JQV8RU8P", 
         "#29C8PULJ9",
         "#QVLRCJQ00",
         "#2V0LYPV9L8",
         "#LJQVURL2G",
         "#UUJY28UJ",
         "#8Y9UCCPC2",
         "#8V92UYCJ",
         "#P8U999R9P",
       ]
       
    
    for tag in TAGI:
        analizuj_mecze_gracza(tag)
        print("-" * 40)