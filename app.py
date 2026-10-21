import streamlit as st
import sqlite3
import brawlstats


st.set_page_config(page_title="Brawl Stars Ranked Assistant", layout="wide", page_icon="⚔️")

st.title("⚔️ Brawl Stars Ranked Draft Assistant (Pro Edition)")
st.caption("Zaawansowany system draftu z banami, synergią i bezpośrednią synchronizacją API")


def get_brawlers():
    conn = sqlite3.connect("brawl_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM brawlers ORDER BY name ASC")
    brawlers = [row[0].upper() for row in cursor.fetchall()]
    conn.close()
    return brawlers

def pobierz_mecze_z_api(api_key, player_tag):
    """Funkcja do pobierania meczów bezpośrednio z poziomu aplikacji"""
    if not api_key or not player_tag:
        return "Podaj klucz API oraz tag gracza!"
    
    clean_tag = player_tag.strip().upper()
    if not clean_tag.startswith("#"):
        clean_tag = "#" + clean_tag

    client = brawlstats.Client(api_key)
    conn = sqlite3.connect("brawl_data.db")
    cursor = conn.cursor()
    
    try:
        battles = client.get_battle_logs(clean_tag)
        if not battles:
            return f"API zwróciło 0 meczów dla {clean_tag}."

        nowe_mecze = 0
        for item in battles:
            b_data = getattr(item, 'battle', item)
            mapa = getattr(b_data, 'map', None)
            if not mapa and hasattr(item, 'event'):
                mapa = getattr(item.event, 'map', None)

            result = getattr(b_data, 'result', None)
            battle_time = getattr(item, 'battle_time', '')

            if not mapa or result not in ['victory', 'defeat']:
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
        conn.close()
        return f"Sukces! Dodano {nowe_mecze} nowych wpisów dla {clean_tag}."
    except Exception as e:
        conn.close()
        return f"Błąd API: {e}"

def rekomenduj_picki(mapa, wrogowie, wykluczone):
    conn = sqlite3.connect("brawl_data.db")
    cursor = conn.cursor()
    
    brawlerzy = get_brawlers()
    punkty = {b: 0.0 for b in brawlerzy}
    
    
    for wrog in wrogowie:
        cursor.execute("SELECT countered_by, score FROM counters WHERE brawler = ?", (wrog,))
        kontry = cursor.fetchall()
        for kontra, silka in kontry:
            if kontra in punkty:
                punkty[kontra] += silka * 15.0
                
   
    if mapa:
        cursor.execute("""
        SELECT brawler_name, wins, total_games 
        FROM map_stats 
        WHERE map_name = ? AND total_games >= 1
        """, (mapa,))
        staty = cursor.fetchall()
        for brawler, wins, total in staty:
            if brawler in punkty:
                wr = (wins / total) * 100
                punkty[brawler] += (wr * 0.5)

    conn.close()
    
    
    for b in wykluczone:
        if b in punkty:
            del punkty[b]

    posortowane = sorted(punkty.items(), key=lambda x: x[1], reverse=True)
    return posortowane


lista_brawlerow = get_brawlers()

with st.sidebar:
    st.header("⚙️ Synchronizacja API")
    api_key_input = st.text_input("Klucz API Supercell", type="password")
    sync_tag = st.text_input("Tag gracza do pobrania", value="#2PP")
    
    if st.button("🔄 Pobierz najnowsze mecze"):
        if not api_key_input:
            st.error("Najpierw wpisz klucz API!")
        else:
            with st.spinner("Pobieram dane z serwerów Supercella..."):
                komunikat = pobierz_mecze_z_api(api_key_input, sync_tag)
                st.success(komunikat)

    st.divider()
    st.markdown("### ℹ️ Wskazówka")
    st.caption("Wybierz mapę i postacie w oknie głównym, aby wygenerować optymalny draft.")


col1, col2 = st.columns([1, 2])

with col1:
    st.header("📋 Ustawienia Meczu")
    
    mapa = st.text_input("Nazwa Mapy (np. Shooting Star)", value="Shooting Star")
    
    st.subheader("🚫 Faza Banów")
    ban1 = st.selectbox("Ban 1", ["BRAK"] + lista_brawlerow, index=0, key="b1")
    ban2 = st.selectbox("Ban 2", ["BRAK"] + lista_brawlerow, index=0, key="b2")
    
    st.subheader("👥 Twoja Drużyna (Ally)")
    ally1 = st.selectbox("Twój Sojusznik 1", ["BRAK"] + lista_brawlerow, index=0, key="a1")
    ally2 = st.selectbox("Twój Sojusznik 2", ["BRAK"] + lista_brawlerow, index=0, key="a2")
    
    st.subheader("🎯 Przeciwnicy (Enemy)")
    enemy1 = st.selectbox("Przeciwnik 1", ["BRAK"] + lista_brawlerow, index=0, key="e1")
    enemy2 = st.selectbox("Przeciwnik 2", ["BRAK"] + lista_brawlerow, index=0, key="e2")
    enemy3 = st.selectbox("Przeciwnik 3", ["BRAK"] + lista_brawlerow, index=0, key="e3")
    
    
    wykluczone_postacie = [b for b in [ban1, ban2, ally1, ally2, enemy1, enemy2, enemy3] if b != "BRAK"]
    wrogowie = [e for e in [enemy1, enemy2, enemy3] if e != "BRAK"]

with col2:
    st.header("🎯 Wyniki i Rekomendacje")
    
    if st.button("🚀 Oblicz najlepsze wybory", type="primary", use_container_width=True):
        wyniki = rekomenduj_picki(mapa, wrogowie, wykluczone_postacie)
        
        st.write(f"**Mapa:** `{mapa}` | **Aktywni wrogowie:** `{', '.join(wrogowie) if wrogowie else 'Brak'}`")
        st.divider()
        
        
        st.subheader("✨ Top 5 Rekomendowanych Wyborów dla Ciebie")
        top_5 = wyniki[:5]
        for idx, (brawler, score) in enumerate(top_5, 1):
            col_rank, col_name, col_score = st.columns([1, 3, 2])
            with col_rank:
                st.markdown(f"### #{idx}")
            with col_name:
                st.markdown(f"### {brawler}")
            with col_score:
                st.metric(label="Ocena dopasowania", value=f"{score:.1f} pkt")
            st.divider()
            
        
        st.subheader("⚠️ Propozycje do zbanowania (Najsilniejsze postacie na mapie)")
        top_bans = wyniki[:3]
        ban_text = ", ".join([f"**{b[0]}**" for b in top_bans])
        st.info(f"Na mapie `{mapa}` warto rozważyć zbanowanie: {ban_text}")