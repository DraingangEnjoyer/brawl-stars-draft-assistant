import brawlstats

API_KEY = ""

try:
    client = brawlstats.Client(API_KEY)
    
    player_tag = "#9JQV8RU8P"
    player = client.get_profile(player_tag)
    
    print("=" * 40)
    print(" SUKCES! Połączono z API Brawl Stars")
    print("=" * 40)
    print(f"Gracz: {player.name}")
    print(f"Pucharki: {player.trophies}")
    print(f"Wygrane 3v3: {player.x3v3_victories}")
    print("=" * 40)

except brawlstats.Unauthorized:
    print(" BŁĄD: Niepoprawny klucz API lub Twój adres IP uległ zmianie.")
except Exception as e:
    print(f" BŁĄD: {e}")