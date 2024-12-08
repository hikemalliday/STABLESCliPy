import pytest
import sqlite3
import os
from datetime import datetime
from unittest.mock import MagicMock
import shutil

from controllers.ItemsController import ItemsController
import tempfile
from controllers.TablesController import TablesController
from controllers.FixturesController import FixturesController


@pytest.fixture
def conn():
    conn = sqlite3.connect(":memory:")
    TablesController.create_tables(conn)
    FixturesController.load_fixtures(conn)
    yield conn
    conn.close()

@pytest.fixture
def mock_conn_and_cursor():
    """Fixture to provide fresh mock connection and cursor for each test"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor

class TestQueries:
    
    def test_item_query_all(self, conn):
        cursor = conn.cursor()
        query = """SELECT * FROM items;"""
        cursor.execute(query)
        results = cursor.fetchall()
        item_names = [item[3] for item in results] 
        assert "Abashi" in item_names

    def test_missing_spells_query_all(self, conn):
        cursor = conn.cursor()
        query = """SELECT * FROM missingSpells;"""
        cursor.execute(query)
        results = cursor.fetchall()
        spell_names = [spell[2] for spell in results]
        assert "Sunstrike" in spell_names

    def test_yellow_text_query_all(self, conn):
        cursor = conn.cursor()
        query = """SELECT * FROM yellowtext;"""
        cursor.execute(query)
        results = cursor.fetchall()
        killer_names = [yt[1] for yt in results]
        assert "Grixus" in killer_names

    def test_campout_query_all(self, conn):
        cursor = conn.cursor()
        query = """SELECT * FROM campOut;"""
        cursor.execute(query)
        results = cursor.fetchall()
        char_names = [row[1] for row in results]
        assert "Grixus" in char_names



# class TestParse:
#     def test_tmp_path(self, tmp_path, mock_conn_and_cursor):
#         conn, cursor = mock_conn_and_cursor
#         cursor.reset_mock()
#         conn.reset_mock()
#         conn.cursor.reset_value = cursor
#         mock_eq_dir = tmp_path
#         file_path = tmp_path / "Mock1-Inventory.txt"
#         file_content = """Location\tName\tID\tCount\tSlots\n
# Ear\tEarring of Essence\t1\t1\t\n
# Face\tEyepatch of Plunder\t2\t1\t\n
# Neck\tNecklace of Superiority\t3\t1\t\n
# """
#         file_path.write_text(file_content)
#         mock_mod_time = 1234567890
#         os.utime(file_path, (mock_mod_time, mock_mod_time))

#         items_controller = ItemsController(conn)
#         items_controller.eq_dir = mock_eq_dir
#         items_controller._parse_items()

#         cursor.executemany.assert_called()
#         args = cursor.executemany.call_args[0]
#         assert len(args[1]) == 3
#         assert args[1][0][1] == "Ear"
#         assert args[1][0][-1] == datetime.fromtimestamp(mock_mod_time).strftime('%m-%d-%Y')

#     def test_parse_items_valid_file(self, mock_conn_and_cursor):
#         with tempfile.TemporaryDirectory() as temp_dir:
#             conn, cursor = mock_conn_and_cursor
#             cursor.reset_mock()
#             conn.reset_mock()
#             conn.cursor.return_value = cursor
#             mock_eq_dir = temp_dir + "/"
#             file_name = "Mock1-Inventory.txt"
#             file_path = os.path.join(mock_eq_dir, file_name)
#             file_content = """Location\tName\tID\tCount\tSlots\n
# Ear\tEarring of Essence\t1\t1\t\n
# Face\tEyepatch of Plunder\t2\t1\t\n
# Neck\tNecklace of Superiority\t3\t1\t\n
# """
#             with open(file_path, "w") as mock_file:
#                 mock_file.write(file_content)

#             mock_mod_time = 1234567890
#             os.utime(file_path, (mock_mod_time, mock_mod_time))

#             items_controller = ItemsController(conn)
#             items_controller.eq_dir = mock_eq_dir
#             items_controller._parse_items()

#             cursor.executemany.assert_called()
#             args = cursor.executemany.call_args[0]
#             assert len(args[1]) == 3
#             assert args[1][0][1] == "Ear"
#             assert args[1][0][-1] == datetime.fromtimestamp(mock_mod_time).strftime('%m-%d-%Y')
    

#     def test_parse_items_invalid_file_name(self, mock_conn_and_cursor):
#         with tempfile.TemporaryDirectory() as temp_dir:
#             conn, cursor = mock_conn_and_cursor
#             cursor.reset_mock()
#             conn.reset_mock()
#             conn.cursor.return_value = cursor
#             mock_eq_dir = temp_dir + "/"
#             file_name = "Invalid-file-name.txt" # Will fail conditional (wont get parsed)
#             file_path = os.path.join(mock_eq_dir, file_name)
#             file_content = """test
# """
#             with open(file_path, "w") as mock_file:
#                 mock_file.write(file_content)

#             mock_mod_time = 1234567890
#             os.utime(file_path, (mock_mod_time, mock_mod_time))

#             items_controller = ItemsController(conn)
#             items_controller.eq_dir = mock_eq_dir
#             items_controller._parse_items()

#             cursor.executemany.assert_not_called()

