import sqlite3

conn = sqlite3.connect("brawl_data.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS brawler_roles (
    brawler_name TEXT PRIMARY KEY,
    role TEXT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS counters (
    brawler TEXT,
    countered_by TEXT,
    score INTEGER
)
""")


role_data = [
    ('FRANK', 'Tank'),
    ('EL PRIMO', 'Tank'),
    ('COLETTE', 'Anti-Tank'),
    ('GALE', 'Anti-Tank'),
    ('CLANCY', 'Anti-Tank'),
    ('PIPER', 'Sniper'),
    ('ANGELO', 'Sniper'),
    ('NANI', 'Sniper'),
    ('EMZ', 'Controller'),
    ('GENE', 'Support')
]

cursor.executemany("INSERT OR REPLACE INTO brawler_roles VALUES (?, ?)", role_data)


counter_data = [
    ('FRANK', 'COLETTE', 3),
    ('FRANK', 'GALE', 3),
    ('FRANK', 'CLANCY', 3),
    ('EL PRIMO', 'GALE', 3),
    ('PIPER', 'NANI', 2),
    ('EMZ', 'PIPER', 2)
]

cursor.executemany("INSERT OR REPLACE INTO counters VALUES (?, ?, ?)", counter_data)

conn.commit()
conn.close()

print("Baza danych została pomyślnie zaktualizowana o role i system kontr!")