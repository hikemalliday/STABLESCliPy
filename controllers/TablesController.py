import sqlite3

class TablesController:

    @staticmethod
    def create_tables(conn):

        queries = [
    """CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        charName TEXT,
        itemLocation TEXT,
        itemName TEXT,
        itemId INTEGER,
        itemSlots INTEGER,
        itemCount INTEGER,
        fileDate TEXT
    );""",
    """CREATE TABLE IF NOT EXISTS eqDir (
        id INTEGER PRIMARY KEY,
        eqDir TEXT
    );""",
    """CREATE TABLE IF NOT EXISTS missingSpells (
        id INTEGER PRIMARY KEY,
        charName TEXT,
        spellName TEXT,
        level INTEGER
    );""",
    """CREATE TABLE IF NOT EXISTS yellowText (
        id INTEGER PRIMARY KEY,
        killer TEXT,
        victim TEXT,
        zone TEXT,
        timeStamp TEXT
    );""",
    """CREATE TABLE IF NOT EXISTS campOut (
        id INTEGER PRIMARY KEY,
        charName TEXT,
        zone TEXT,
        timeStamp TEXT
    );"""
]
        try:
            for query in queries:
                conn.execute(query)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM eqDir")
            rows = cursor.fetchall()

            if len(rows) == 0:
               eq_dir_value = "C:/r99/"
               insert_query = "INSERT INTO eqDir (eqDir) VALUES (?)"
               conn.execute(insert_query, (eq_dir_value,))
               print("Default eqDir inserted.")

            conn.commit()
        except sqlite3.Error as e:
            print(f"create_tables error: {e}")
            conn.rollback()

    
    @staticmethod
    def drop_tables(conn):
        query = "DROP TABLES";
        try:
            cursor = conn.cursor()
            cursor.execute(query)
        except sqlite3.Error as e:
            print(f"drop_tables error: {e}")

    
    @staticmethod
    def delete_rows(conn):
        queries = [
            "DELETE FROM items;",
            "DELETE FROM missingSpells;",
            "DELETE FROM yellowText;",
            "DELETE FROM campOut;",
        ]
        try:
            cursor = conn.cursor()
            for query in queries:
                cursor.execute(query)
            conn.commit()
        except sqlite3.Error as e:
            print(f"delete_rows error: {e}")

    @staticmethod
    def set_eq_dir(conn, eq_dir):
        try:
            query = """UPDATE eqDir (eqDir) VALUES (?)"""
            cursor = conn.cursor()
            cursor.execute(query, eq_dir)
            conn.commit()
            return eq_dir if eq_dir else None
        except Exception as e:
            print(f"'\033[31m'set_eq_dir error:'\033[0m' {e}")

    @staticmethod
    def get_eq_dir(conn):
        try:
            query = """SELECT (eqDir) FROM eqDir;"""
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"'\033[31m'get_eq_dir error:'\033[0m' {e}")

    


