import sqlite3
import os
import re

class CampoutController:

    conn = None
    eq_dir = None
    campout_locations = {}
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

    def query_campout(self, params: dict):

        charName = "%" + params.get('charName', '') + "%" 
        zone = "%" + params.get('zone', '') + "%"
        query = """SELECT charName, zone, timeStamp FROM campOut 
        WHERE charName LIKE ? AND zone LIKE ?;""" 

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (charName, zone))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"query_campout error: {e}")

    def parse_campout(self):
        print(f"Parsing campout locations...")
        file_regex = f'^eqlog_(.*)_P1999PVP\.txt$'
        first_line_regex = r'^\[\w{3} \w{3} \d{2} \d{2}:\d{2}:\d{2} \d{4}\] .*'
        campout_regex = r"\[(.+?)\] You have entered (.+?)\."
        logs_dir = self.eq_dir + "/Logs/"
        file_names_list = []
        
        try:
            files = os.listdir(logs_dir) if os.path.isdir(logs_dir) else []
            for file in files:
                matches = re.match(file_regex, file)
                if matches:
                    char_name = matches.group(1)
                    self.campout_locations[char_name] = []
                    file_names_list.append(file)

            for file in file_names_list:
                campout_time = ""
                campout_zone = ""
                char_name = re.match(file_regex, file).group(1)
                file_path = logs_dir + file

                with open(file_path, "r") as f:
                    first_line = f.readline().strip()
                    if not re.match(first_line_regex, first_line):
                        continue

                    file_size = os.path.getsize(file_path)
                    if file_size > 10 * 1024 * 1024:
                        file_size * 3 // 4
                        f.seek(file_size * 3 // 4)
                        f.readline()

                    for line in f:
                        line = line.strip()
                        if "You have entered" in line:
                            matches = re.match(campout_regex, line)
                            if matches:
                                campout_time = matches[1]
                                campout_zone = matches[2]
                    if not self.campout_locations[char_name]:
                        self.campout_locations[char_name] = []
                    self.campout_locations[char_name] = [campout_zone, campout_time]

            campout_list = []
            for char_name, campout_info in self.campout_locations.items():
                campout_zone = campout_info[0]
                campout_time = campout_info[1]
                campout_list.append([char_name, campout_zone, campout_time])

            try:
                print("Inserting campout locations into database...")
                query = """INSERT INTO campOut 
                (charName, zone, timeStamp) VALUES (?, ?, ?);"""
                cursor = self.conn.cursor()
                cursor.executemany(query, campout_list)
                self.conn.commit()
                print(f"Successfully inserted campout locations into database.")
            except Exception as e:
                print(f"parse_campout mass insert error: {e}")

        except Exception as e:
            print(f"parse_campout error: {e}")
            
