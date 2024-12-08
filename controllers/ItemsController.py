import sqlite3
import os
import re
from datetime import datetime


class ItemsController:

    conn = None
    eq_dir = None
    parsed_items = {}
    colors = {
        "RESET": "\033[0m",
        "RED": "\033[31m",
        "GREEN": "\033[32m",
        "YELLOW": "\033[33m",
        "BLUE": "\033[34m",
    }

    def __init__(self, conn, eq_dir = "C:/r99/"):
        self.conn = conn
        self.eq_dir = eq_dir


    def query_items(self, params: dict):
        itemName = "%" + params.get('itemName', '') + "%"
        charName = "%" + params.get('charName', '') + "%"
        query = """SELECT * FROM items 
        WHERE itemName LIKE ? AND charName LIKE ?;"""

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (itemName, charName))
            print(cursor.fetchall())
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"query_items error: {e}")
    
    def parse_items(self):
        regex = r'^(.*)-Inventory\.txt$'
        first_line_schema = ['Location', 'Name', 'ID', 'Count', 'Slots']
        file_names_list = []

        try:
            files = os.listdir(self.eq_dir) if os.path.isdir(self.eq_dir) else []
            for file in files:
                matches = re.match(regex, file)
                if matches:
                    char_name = matches.group(1)
                    self.parsed_items[char_name] = []
                    file_names_list.append(file)

            for file in file_names_list:
                char_name = re.match(regex, file).group(1)
                file_path = self.eq_dir + file
                
                with open(file_path, "r") as f:
                    file_mod_date = os.path.getmtime(file_path) 
                    file_mod_date_str = datetime.fromtimestamp(file_mod_date).strftime('%m-%d-%Y')
                    first_line = f.readline().replace("\n", "").split("\t")
                    if first_line != first_line_schema:
                        continue
                        
                    for line in f:
                        line = line.replace("\n", "").split("\t")
                        if line and len(line) == 5:
                             self.parsed_items[char_name].append([
                                char_name,
                                line[0],
                                line[1],
                                line[2],
                                line[3],
                                file_mod_date_str,
                            ])
                             
            try:
                print("Inserting items into database...")
                query = """INSERT INTO items (
                charName, 
                itemLocation, 
                itemName, 
                itemId, 
                itemCount, 
                fileDate
                ) VALUES (?, ?, ?, ?, ?, ?);"""
                cursor = self.conn.cursor()
                for _, items in  self.parsed_items.items():
                    if items:
                        cursor.executemany(query, items)
                self.conn.commit()
                print(f"{self.colors['GREEN']}Successfully inserted items into database.{self.colors['RESET']}")
            except Exception as e:
                print(f"{self.colors['RED']}_parse_items_error, query block: {e}{self.colors['RESET']}")
        
        except Exception as e:
            print(f"{self.colors['RED']}parse_items error: {e}{self.colors['RESET']}")
