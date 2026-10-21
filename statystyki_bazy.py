import sqlite3

def pokaz_statystyki_bazy():
    conn = sqlite3.connect("brawl_data.db")
    cursor = conn.cursor()

    print("=" * 45)
    print("📊 PODSUMOWANIE TWOJEJ BAZY DANYCH BRAWL STARS")
    print("=" * 45)

  
    cursor.execute("SELECT COUNT(*) FROM battle_logs")
    total_battles = cursor.fetchone()[0]

  
    cursor.execute("SELECT COUNT(DISTINCT map_name) FROM map_stats")
    total_maps = cursor.fetchone()[0]

    
    cursor.execute("SELECT COUNT(DISTINCT brawler_name) FROM map_stats")
    total_brawlers = cursor.fetchone()[0]

    print(f"🎮 Zapisane rekordy meczowe:  {total_battles}")
    print(f"🗺️  Liczba unikalnych map:       {total_maps}")
    print(f"🥊 Brawlerzy ze statystykami:   {total_brawlers}")
    print("-" * 45)

    
    print("🔥 TOP 5 MAP Z NAJWIĘKSZĄ LICZBĄ MECZÓW:")
    cursor.execute("""
        SELECT map_name, SUM(total_games) as mecze 
        FROM map_stats 
        GROUP BY map_name 
        ORDER BY mecze DESC 
        LIMIT 5
    """)
    top_mapy = cursor.fetchall()

    if top_mapy:
        for idx, (mapa, mecze) in enumerate(top_mapy, 1):
            print(f"  {idx}. {mapa}: {mecze} gier")
    else:
        print("  Brak danych o mapach w bazie.")

    print("=" * 45)
    conn.close()

if __name__ == "__main__":
    pokaz_statystyki_bazy()