import sqlite3
from controllers.TablesController import TablesController
from controllers.FixturesController import FixturesController
from controllers.ItemsController import ItemsController
from controllers.SpellsController import SpellsController
from controllers.CampoutController import CampoutController
from controllers.YellowTextController import YellowTextController
from controllers.InterfaceController import InterfaceController

if __name__ == "__main__":
    try:
        print("""\033[31m
⣿⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣀⠀⠰⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⠄⠀⠸⢿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⡄⠀⠀⠸⢿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣄⣠⣄⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣷⠀⠀⠀⠸⢿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡶⣷⣿⣿⣿⢻⣿⡿⣿⣿⡏⠹⣿⣷⡶⠶⢶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠁⢻⣷⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⣯⠁⣠⣾⣿⠋⠀⣿⣿⡅⢸⣿⣷⠀⠙⢿⣤⣀⠀⠙⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠹⡆⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣦⣤⣶⣿⣶⣾⣿⣿⣶⣾⣿⣿⣿⣿⣿⣿⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢻⣦⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⡟⠛⢻⣿⣿⠟⠁⠛⠁⠈⠛⠙⢻⣿⣿⡟⠛⢻⣿⣿⣿⢿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢸⡇⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡿⢟⣿⣿⣿⣷⣤⣄⠘⠁⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⣦⣤⣾⣿⣿⣿⡎⠻⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢸⣧⠀⢸⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⣋⣁⣾⣿⡈⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⢀⣿⣧⣀⡈⠛⢲⣦⣀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣿⣋⣀⣉⣹⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⣄⣶⣿⣿⡿⠉⠻⠷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠖⠋⠉⢿⣿⣿⣆⣼⣷⣟⣷⣄⠀⠀⠀⠀
⠀⠀⠀⣿⣿⣿⣿⣿⣿⡟⢶⣦⣄⣀⠀⢀⣀⣴⣶⠻⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠈⠻⣿⣯⣽⠿⠿⠿⠿⠿⠿⠿⠿⣿⣹⣿⡟⠁⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣷⠟⣷⡀⠀⠀
⠀⠀⠀⣿⣿⣿⣿⣿⣿⣇⣀⣠⣿⣿⣿⣿⡟⢿⣿⣶⣾⣿⣿⣿⣿⣯⣴⣧⡀⠀⠀⠀⠀⠈⢙⣿⣷⣶⣿⣿⣷⣿⣶⣿⣿⡟⠃⠀⠀⠀⠀⠀⣤⣄⣭⣹⠿⢿⣿⣿⣦⣾⣿⣆⡀
⠀⠀⠀⣿⣿⠟⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣯⡿⠟⠛⠋⠈⣿⣇⠀⠀⢀⣤⣶⣿⣿⣿⣿⣟⠉⠉⠻⣿⣿⣿⣿⣶⣄⠀⠀⠀⢀⣿⠉⠉⠙⠛⠮⣽⣿⣿⣿⣯⠈⠻
⠀⠀⠀⢿⣅⠀⣘⣶⠟⠀⠀⠈⠙⠛⠻⢿⣿⠿⠟⠛⠉⠁⠀⠀⠀⠀⠀⠛⣿⣇⣴⣿⣻⣿⣤⣤⣿⣿⠛⠛⠛⠻⣿⣿⣤⣤⣼⣿⣿⣦⣾⣿⠟⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿
⠀⠀⠀⠈⠙⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣩⣿⣷⣤⣶⣦⣿⣿⣦⠀⠀⣤⣿⣤⣶⣤⣤⣼⣿⣹⣿⡟⠀⠀⠀⠀⠀⠀⠀⣠⢾⡏⣼⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣯⣤⣤⣤⡤⠀⣴⣿⡀⢀⣿⣶⣴⣶⣶⣤⣬⣿⡾⠋⠀⠀⠀⠀⠀⠀⣠⠾⢉⣀⣤⠛⠈⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⡷⠶⣤⡀⠙⣛⠛⢛⣵⡆⠀⢸⣿⡿⠏⠀⠀⠀⠀⠀⠀⣤⠞⢉⣰⣿⣿⠇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⢠⡀⠉⠿⣿⣿⡿⠟⠉⠀⣀⣿⢻⣷⠀⠀⠀⠀⠀⠀⠀⣿⢴⣾⣿⣿⣷⡄⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣾⣷⣦⡀⠉⠁⠀⢀⣴⣾⣿⣷⣿⣿⡇⠀⠀⠀⠀⠀⠀⠈⠻⣽⣿⣯⠿⠋⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠛⢉⣿⣿⡏⠁⢹⣿⣿⣿⣿⠋⠀⢹⣿⣏⡉⠉⢳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⡟⠀⢠⣶⡿⣿⣿⣿⣦⣀⠀⢹⣿⣿⣿⣿⠻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡏⢻⣿⣿⡿⠋⣀⣶⠟⠉⠀⠈⠋⠁⠉⠛⢶⣄⠘⢻⣿⣿⠛⠹⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣯⣴⣿⣿⡏⣀⣶⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣄⢸⣿⣿⣦⣾⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣷⣶⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣟⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣾⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣽⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣷⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣿⣿⢀⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣼⣿⣿⡏⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠟⢩⣥⠀⠉⢡⣼⣿⣯⡷⠀⠀⠀⠀⠀⠀⠀⠰⢿⣽⣿⣯⡍⠉⠀⣬⠉⠛⠣⠀⠀⠀
\033[0m""")
        conn = sqlite3.connect("master.db")
        eq_dir = TablesController.get_eq_dir(conn)
        interface_controller = InterfaceController(conn, eq_dir)
        #TablesController.create_tables(conn)
        #TablesController.delete_rows(conn)
        # FixturesController.load_fixtures(conn)
        #items_controller = ItemsController(conn)
        #items_controller.parse_items()
        #spells_controller = SpellsController(conn)
        #spells_controller.parse_spells()
        #campout_controller = CampoutController(conn, "C:/r99")
        #campout_controller.parse_campout()
        #campout_controller.query_campout({'zone': 'Western'})
        #items_controller.query_items({'itemName': 'green'})
        #spells_controller.query_spells({'charName': 'Grixus'})
        #yellow_text_controller = YellowTextController(conn, "C:/r99")
        #yellow_text_controller.parse_yellow_text()
        # yellow_text_controller.query_yellow_text({})
        interface_controller.start()
    finally:
        conn.close()
