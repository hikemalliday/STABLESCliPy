from .CampoutController import CampoutController
from .ItemsController import ItemsController
from .SpellsController import SpellsController
from .TablesController import TablesController
from .YellowTextController import YellowTextController
import re
import os
import msvcrt 


class InterfaceController:

    conn = None
    eq_dir = None
    items_controller = None
    spells_controller = None
    campout_controller = None
    yellow_text_controller = None
    page_size = 50
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
            "-page_size": self.set_page_size,
            "-eq_dir": self.set_eq_dir,
        }
        TablesController.create_tables(conn)

    def parse_all(self):
        if not os.path.isdir(self.eq_dir):
            print(f"""{self.colors['RED']}ERROR:{self.colors['RESET']}'{self.eq_dir}'{self.colors['RED']} is not a valid directory.{self.colors['RESET']}""")
            return
        TablesController.delete_rows(self.conn)
        self.items_controller.parse_items()
        self.spells_controller.parse_spells()
        self.campout_controller.parse_campout()
        self.yellow_text_controller.parse_yellow_text()

    def get_items(self, params: dict):
        results = self.items_controller.query_items(params)
        self.show_paginated_results(results, "Items")

    def get_spells(self, params: dict):
        results = self.spells_controller.query_spells(params)
        self.show_paginated_results(results, "Missing Spells")

    def get_campout(self, params: dict):
        results = self.campout_controller.query_campout(params)
        self.show_paginated_results(results, "Campout")

    def get_yellow_text(self, params: dict):
        results = self.yellow_text_controller.query_yellow_text(params)
        self.show_paginated_results(results, "Yellow Text")

    def set_page_size(self, params: dict):
        self.page_size = int(params["page_size"])
        print(f"Page size has been set to {params['page_size']}")

    def set_eq_dir(self, params: dict):
        eq_dir = params["eq_dir"]
        self.eq_dir =eq_dir
        self.items_controller = ItemsController(self.conn, eq_dir)
        self.spells_controller = SpellsController(self.conn, eq_dir)
        self.campout_controller = CampoutController(self.conn, eq_dir)
        self.yellow_text_controller = YellowTextController(self.conn, eq_dir)
        TablesController.set_eq_dir(self.conn, eq_dir)
        print(f"Eq dir has been set to {eq_dir}")

    def get_params(self, command: str):
        command_type_regex = r"^(-i|-s|-yt|-camp|-page_size|-eq_dir)"
        items_regex = r"^-i(?:\s+(?!-char|-zone)(\S+))?"
        char_name_regex = r"-char\s+([^-].*?)(?=\s-|\s*$)"
        zone_regex = r"-zone\s+([^-].*?)(?=\s-|\s*$)"
        page_size_regex = r"-page_size\s+(\d+)"
        eq_dir_regex = r"-eq_dir\s+(.+)"

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
        
        elif command_type == "-page_size":
            match = re.match(page_size_regex, command)
            params["page_size"] = match.group(1) if match else 50

        elif command_type == "-eq_dir":
            match = re.match(eq_dir_regex, command)
            params["eq_dir"] = match.group(1) if match else "C:/r99/"

        # Handle common keyword arguments: -char and -zone
        char_name_match = re.search(char_name_regex, command)
        params["charName"] = char_name_match.group(1) if char_name_match else ""

        zone_match = re.search(zone_regex, command)
        params["zone"] = zone_match.group(1) if zone_match else ""

        return params
    
    def show_help(self, _ = None):
        print(f"""Available commands:
              
                  help                - Show this help message
                  exit                - Exit the application
                  -parse              - Parse all data
                  -i <item name>      - Query items (optional params: -char)
                  -s                  - Query missing spells (optional params: -char)
                  -yt                 - Query yellow texts (optional params: -char, -zone)
                  -camp               - Query camp out locations (optional params: -char, -zone)
                  -page_size <int>    - Set the results page size, example: -page_size 50
                  -eq_dir <str>       - Set the eq dir, example: -eq_dir C:/r99/

                  Current eq dir is: {self.eq_dir}

""")

    def show_paginated_results(self, results, query_type):
        """
        Display paginated results in the terminal, navigating with Left/Right arrow keys.
        :param results: List of items to display
        """
        current_page = 0
        total_pages = (len(results) + self.page_size - 1) // self.page_size

        while True:
            # Clear the screen
            self.clear_screen()

            # Render the current page
            self.render_page(results, current_page, total_pages, query_type)

            # Wait for user input
            key = self.get_key()

            if key == "RIGHT":  # Next page
                if current_page < total_pages - 1:
                    current_page += 1
            elif key == "LEFT":  # Previous page
                if current_page > 0:
                    current_page -= 1
            elif key == "ESC":  # Exit
                self.clear_screen()
                self.show_help()
                break

    def render_page(self, results, current_page, total_pages, query_type):
        """
        Render a single page of results.
        :param results: List of items to display
        :param current_page: Current page index (0-based)
        :param total_pages: Total number of pages
        """
        # Calculate start and end indices for the current page
        start_idx = current_page * self.page_size
        end_idx = min(start_idx + self.page_size, len(results))

        # Print header
        print(f"{query_type} (Page {current_page + 1}/{total_pages})")
        print("-" * 50)

        # Print items for the current page
        for row in results[start_idx:end_idx]:
            print(row)

        # Print footer
        print("\n" + "-" * 50)
        print("← Previous | → Next | ESC Exit")

    def clear_screen(self):
        """
        Clear the terminal screen in a cross-platform way.
        """
        os.system("cls" if os.name == "nt" else "clear")

    def get_key(self):
        """
        Wait for and return a key press. Handles Left/Right arrow keys and ESC.
        :return: One of 'LEFT', 'RIGHT', or 'ESC'
        """
        while True:
                key = msvcrt.getch()
                if key == b'\xe0':  # Arrow keys are prefixed with b'\xe0'
                    arrow_key = msvcrt.getch()
                    if arrow_key == b'K':  # Left arrow
                        return "LEFT"
                    elif arrow_key == b'M':  # Right arrow
                        return "RIGHT"
                elif key == b'\x1b':  # ESC key
                    return "ESC"
    

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
                    command_type = params["command_type"]
                    self.commands[command_type](params)
            



    

    







    