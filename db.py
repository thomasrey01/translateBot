import psycopg2

def initialise():
    conn = psycopg2.connect(
        host="ec2-34-240-75-196.eu-west-1.compute.amazonaws.com",
        database="d897ishrgcmr7u",
        user="isxhajtrtdvrcp",
        password="c24be5116e2e4981b769224b49c99b3719b9d18cacee01ea16aed1fc11741584",
    )
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS languages(
                    guildID BIGINT PRIMARY KEY UNIQUE,
                    language VARCHAR(5) DEFAULT 'en');''')
    conn.commit()
    print("created table")
    return conn

def update_language(guildID, lang, conn):
    check_table(guildID, conn)
    cur = conn.cursor()
    cur.execute('''UPDATE languages
                    SET language = %s
                    WHERE guildID = %s''', [lang, guildID])
    conn.commit()

def check_table(guildID, conn):
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO languages (guildID)
                    VALUES (%s) ON CONFLICT (guildID)
                    DO NOTHING;''', [guildID])
    conn.commit()

def get_language(guildID, conn):
    cursor = conn.cursor()
    check_table(guildID, conn)
    cursor.execute("SELECT language FROM languages WHERE guildID = %s;", [guildID])
    lang = cursor.fetchall()
    return lang[0]