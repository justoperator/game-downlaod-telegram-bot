#CODE FOR WHAT CREATE database.db !!DATABASE ALREADY CREATE AND WORK, USE IT ONLY IF YOU DELETE DATABASE AND WANT GET BACK IT!!

import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS apps (
    images TEXT,
    appname TEXT,
    description TEXT,
    description_ru TEXT,
    download_link TEXT,
    tags TEXT,
    andpc TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user TEXT,
    areact TEXT,
    language TEXT,
    system TEXT
)
''')

conn.commit()
conn.close()