import sqlite3
import os
import re

class YellowTextController:

    conn = None
    eq_dir = None
    parsed_yellow_text = []
    colors = {
        "RESET": "\033[0m",
        "RED": "\033[31m",
        "GREEN": "\033[32m",
        "YELLOW": "\033[33m",
        "BLUE": "\033[34m",
    }

    def __init__(self, conn, eq_dir):
        self.conn = conn
        self.eq_dir = eq_dir

    def query_yellow_text(self, params: dict):
        killer = "%" + params.get('charName', '') + "%"
        zone = "%" + params.get('zone', '') + "%"
        query = """SELECT * FROM yellowText
        WHERE killer LIKE ? AND zone LIKE ?;"""

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (killer, zone))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"query_yellow_text error: {e}")

    def parse_yellow_text(self):
        print(f"Parsing yellow texts...")
        file_regex = r'eqlog_(.*)_P1999PVP\.txt'
        first_line_regex = r'^\[\w{3} \w{3} \d{2} \d{2}:\d{2}:\d{2} \d{4}\] .*'
        yellow_text_regex = r'\[(.*)\] \[PvP\] (.*) <(.*)> has been defeated by (.*) <(.*)> in (.*)!'
        logs_dir = self.eq_dir + "/Logs/"
        file_names_list = []

        try:
            files = os.listdir(logs_dir) if os.path.isdir(logs_dir) else []
            for file in files:
                matches = re.match(file_regex, file)
                if matches:
                    file_names_list.append(file)

            for file in file_names_list:
                file_path = logs_dir + file

                with open(file_path, "r") as f:
                    first_line = f.readline().strip()
                    if not re.match(first_line_regex, first_line):
                        continue
                    
                    # include first line
                    matches = re.match(yellow_text_regex, first_line)
                    if matches:
                        yellow_text_time = matches[1]
                        victim = matches[2]
                        killer = matches[4]
                        zone = matches[6]
                        self.parsed_yellow_text.append([yellow_text_time, victim, killer, zone])
                    
                    for line in f:
                        line = line.strip()
                        if "has been defeated" in line:
                            matches = re.match(yellow_text_regex, line)
                            if matches:
                                yellow_text_time = matches[1]
                                victim = matches[2]
                                killer = matches[4]
                                zone = matches[6]
                                self.parsed_yellow_text.append([yellow_text_time, victim, killer, zone])

            try:
                print("Inserting yellow texts into database...")
                query = """INSERT INTO yellowText (timeStamp, victim, killer, zone) VALUES (?, ?, ?, ?);"""
                cursor = self.conn.cursor()
                cursor.executemany(query, self.parsed_yellow_text)
                self.conn.commit()
                print(f"Yellow texts inserted.")
            except Exception as e:
                print(f"parse_yellow_text mass insert error: {e}")

        except Exception as e:
            print(f"parse_yellow_text error: {e}")




