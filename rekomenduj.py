import sqlite3

def rekomenduj_picki(mapa, wrogowie):
    conn = sqlite3.connect("brawl_data.db")
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT name FROM brawlers")
    brawlerzy = [row[0].upper() for row in cursor.fetchall()]
    
    punkty_postaci = {b: 0.0 for b in brawlerzy}
    
    
    for wrog in wrogowie:
        wrog = wrog.upper()
        cursor.execute("SELECT countered_by, score FROM counters WHERE brawler = ?", (wrog,))
        kontry = cursor.fetchall()
        for kontra, silka in kontry:
            if kontra in punkty_postaci:
                punkty_postaci[kontra] += silka * 15 # +15/30 pkt za kontrę
                
    
    cursor.execute("""
    SELECT brawler_name, wins, total_games 
    FROM map_stats 
    WHERE map_name = ? AND total_games >= 1
    """, (mapa,))
    
    staty_mapy = cursor.fetchall()
    for brawler, wins, total in staty_mapy:
        if brawler in punkty_postaci:
            win_rate = (wins / total) * 100
            # Dodajemy punkty proporcjonalnie do % wygranych na tej mapie
            punkty_postaci[brawler] += (win_rate * 0.5)

    posortowane = sorted(punkty_postaci.items(), key=lambda x: x[1], reverse=True)
    conn.close()
    return posortowane


if __name__ == "__main__":
    Wybrana_Mapa = "Shooting Star" # Przykładowa mapa
    Wrogowie = ["FRANK"]
    
    print(f"=== DRAFT: MAPA '{Wybrana_Mapa}' | WRÓG: {Wrogowie} ===")
    wyniki = rekomenduj_picki(Wybrana_Mapa, Wrogowie)
    
    print("\n Najlepsze Picki wg Algorytmu:")
    for brawler, score in wyniki[:5]:
        print(f"-> {brawler}: {score:.1f} pkt")