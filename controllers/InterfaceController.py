from .CampoutController import CampoutController
from .ItemsController import ItemsController
from .SpellsController import SpellsController
from .TablesController import TablesController
from .YellowTextController import YellowTextController
import re

class InterfaceController:

    conn = None
    eq_dir = None
    items_controller = None
    spells_controller = None
    campout_controller = None
    yellow_text_controller = None
    page_size = 75
    colors = {
        "RESET": "\033[0m",
        "RED": "\033[31m",
        "GREEN": "\033[32m",
        "YELLOW": "\033[33m",
        "BLUE": "\033[34m",
    }
    commands = {}

    def __init__(self, conn, eq_dir):
        self.conn = conn
        self.eq_dir = eq_dir
        self.items_controller = ItemsController(conn, eq_dir)
        self.spells_controller = SpellsController(conn, eq_dir)
        self.campout_controller = CampoutController(conn, eq_dir)
        self.yellow_text_controller = YellowTextController(conn, eq_dir)
        self.commands = {
            "-i": self.get_items,
            "-s": self.get_spells,
            "-yt": self.get_yellow_text,
            "-camp": self.get_campout,
        }
        TablesController.create_tables(conn)

    def parse_all(self):
        TablesController.delete_rows(self.conn)
        self.items_controller.parse_items()
        self.spells_controller.parse_spells()
        self.campout_controller.parse_campout()
        self.yellow_text_controller.parse_yellow_text()

    def get_items(self, params: dict):
        charName = params.get("charName", "")
        itemName = params.get("itemName", "")
        results = self.items_controller.query_items(params)

    def get_spells(self, params: dict):
        charName = params.get("charName", "")
        results = self.spells_controller.query_spells(params)

    def get_campout(self, params: dict):
        charName = params.get("charName", "")
        zone = params.get("zone", "")
        results = self.campout_controller.query_campout(params)

    def get_yellow_text(self, params: dict):
        results = self.yellow_text_controller.query_yellow_text(params)

    def get_params(self, command: str):
        command_type_regex = r"^(-i|-s|-yt|-camp)"
        items_regex = r"^-i(?:\s+(?!-char|-zone)(\S+))?"
        char_name_regex = r"-char\s+([^-].*?)(?=\s-|\s*$)"
        zone_regex = r"-zone\s+([^-].*?)(?=\s-|\s*$)"

        # Strip the command of extra whitespace
        command = command.strip()

        # Match the command type
        matches = re.match(command_type_regex, command)
        if not matches:
            print(f"Invalid command: {command}")
            return None

        # Extract the command type
        command_type = matches.group(1)
        params = {"command_type": command_type}

        # Handle -i specifically for itemName positional argument
        if command_type == "-i":
            match = re.match(items_regex, command)
            if match.group(1) == None:
                params["itemName"] = ""
            else:
                params["itemName"] = match.group(1) if match else ""

        # Handle common keyword arguments: -char and -zone
        char_name_match = re.search(char_name_regex, command)
        params["charName"] = char_name_match.group(1) if char_name_match else ""

        zone_match = re.search(zone_regex, command)
        params["zone"] = zone_match.group(1) if zone_match else ""

        return params



    def show_help(self, _ = None):
        print("""Available commands:
              
                  help              - Show this help message
                  exit              - Exit the application
                  -parse            - Parse all data
                  -i <item name>    - Query items (optional params: -char)
                  -s                - Query missing spells (optional params: -char)
                  -yt               - Query yellow texts (optional params: -char, -zone)
                  -camp             - Query camp out locations (optional params: -char, -zone)
""")
    

    def start(self):
        print("Welcome to STABLESCliPy! Type 'exit' to quit.")
        self.show_help()

        while True:
            command = input("> ")

            if command.lower() == 'exit':
                print("Goodbye.")
                break

            elif command.lower() == '-parse':
                self.parse_all()

            elif command.lower() == 'help':
                self.show_help()
            
            else:
                params = self.get_params(command)
                if params:
                    print(f"params: {params}")
                    command_type = params["command_type"]
                    self.commands[command_type](params)
            



    

    







    