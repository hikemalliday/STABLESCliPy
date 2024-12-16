import sqlite3
import os
import re
import json


class SpellsController:

    conn = None
    eq_dir = None
    parsed_spells = {}
    char_classes = {}
    missing_spells = {}
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

    def query_spells(self, params: dict):
        charName = "%" + params.get('charName', '') + "%"
        try:
            query = """SELECT * FROM missingSpells
            WHERE charName LIKE ?;
            """
            cursor = self.conn.cursor()
            cursor.execute(query, (charName,))
            return cursor.fetchall()
        except Exception as e:
            print(f"query_spells error: {e}")

    def _determine_char_class(self, char_name):
        class_tally = {}
        with open("spellsMaster.json", "r") as f:
            spells_master = json.load(f)
            for spell in self.parsed_spells[char_name]:
                spell_level = spell[0]
                spell_name = spell[1].strip()
                for class_name, class_spells in spells_master.items():
                    if spell_name in class_spells and int(spell_level) == int(class_spells[spell_name]):
                        class_tally.setdefault(class_name, 0)
                        class_tally[class_name] += 1
                        if class_tally[class_name] >= 14:
                            self.char_classes[char_name] = class_name
                            break
            
    def _determine_missing_spells(self, char_name):
        with open("spellsMaster.json", "r") as f:
            spells_master = json.load(f)
            class_spells_copy = spells_master[self.char_classes[char_name]].copy()
            for spell in self.parsed_spells[char_name]:
                spell_name = spell[1]
                if spell_name.strip() in class_spells_copy:
                    del class_spells_copy[spell_name.strip()]
            self.missing_spells[char_name] = class_spells_copy

            
    def parse_spells(self):
        print(f"{self.colors['YELLOW']}Parsing missing spells...{self.colors['RESET']}")
        regex = f'^(.*)-Spellbook\.txt$'
        first_line_len = 2
        file_names_list = []

        try:
            files = os.listdir(self.eq_dir) if os.path.isdir(self.eq_dir) else []
            for file in files:
                matches = re.match(regex, file)
                if matches:
                    char_name = matches.group(1)
                    self.parsed_spells[char_name] = []
                    file_names_list.append(file)
            for file in file_names_list:
                char_name = re.match(regex, file).group(1)
                file_path = self.eq_dir + file

                with open(file_path, "r") as f:
                    first_line = f.readline().replace("\n", "").split("\t")
                    if len(first_line) != first_line_len:
                        continue
                    
                    # Include first line if match
                    spell_level = first_line[0]
                    spell_name = first_line[1]
                    self.parsed_spells[char_name].append([spell_level, spell_name])

                    for line in f:
                        line = line.replace("\n", "").split("\t")

                        if line and len(line) == 2:
                            spell_level = line[0]
                            spell_name = line[1]
                            
                            self.parsed_spells[char_name].append([
                                spell_level,
                                spell_name,
                            ])

                self._determine_char_class(char_name)
                self._determine_missing_spells(char_name)
            # convert dict to master_list
            missing_spells_list = []
            for char_name, missing_spells in self.missing_spells.items():
                for spell_name, spell_level in missing_spells.items():
                    missing_spells_list.append([char_name, spell_name, spell_level])

            # perform bulk insert
            try:
                print("Inserting missing spells into database...")
                query = """INSERT INTO missingSpells (
                charName,
                spellName,
                level
                ) VALUES (?, ?, ?);"""
                cursor = self.conn.cursor()
                cursor.executemany(query, missing_spells_list)
                self.conn.commit()
                print(f"{self.colors['GREEN']}Successfully inserted missing spells into database.{self.colors['RESET']}")
            except Exception as e:
                print(f"{self.colors['RED']}_parse_spells mass insert error: {e}{self.colors['RESET']}")

        except Exception as e:
            print(f"{self.colors['RED']}_parse_spells error: {e}{self.colors['RED']}")


    