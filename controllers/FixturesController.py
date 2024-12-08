import sqlite3

class FixturesController:

    @staticmethod
    def load_fixtures(conn):

        mock_items = [
        {
            "charName": "Grixus",
            "itemLocation": "Inventory",
            "itemName": "Abashi",
            "itemId": "100",
            "itemCount": "1",
            "itemSlots": "1",
            "fileDate": "date"
        },
        {
            "charName": "Grixus",
            "itemLocation": "Inventory",
            "itemName": "Eye of Cazic-Thule",
            "itemId": "100",
            "itemCount": "1",
            "itemSlots": "1",
            "fileDate": "date"
        },
        {
            "charName": "Grixus",
            "itemLocation": "Inventory",
            "itemName": "Silver Charm of Tranquility",
            "itemId": "100",
            "itemCount": "1",
            "itemSlots": "1",
            "fileDate": "date"
        },
        {
            "charName": "Grixus",
            "itemLocation": "Inventory",
            "itemName": "Barrier of Sound",
            "itemId": "100",
            "itemCount": "1",
            "itemSlots": "1",
            "fileDate": "date"
        },
        {
            "charName": "Grixus",
            "itemLocation": "Inventory",
            "itemName": "Zlandicar's Heart",
            "itemId": "100",
            "itemCount": "1",
            "itemSlots": "1",
            "fileDate": "date"
        }
    ]

        mock_missing_spells = [
        {
            "charName": "Stork",
            "spellName": "Sunstrike",
            "level": 60,
            "fileDate": "date"
        },
        {
            "charName": "Stork",
            "spellName": "Lure of Ice",
            "level": 60,
            "fileDate": "date"
        },
        {
            "charName": "Stork",
            "spellName": "Gate",
            "level": 60,
            "fileDate": "date"
        },
        {
            "charName": "Stork",
            "spellName": "Invisibility",
            "level": 60,
            "fileDate": "date"
        },
        {
            "charName": "Stork",
            "spellName": "Ice Comet",
            "level": 60,
            "fileDate": "date"
        }
    ]

        mock_yellow_text = [
        {
            "charName": "Grixus",
            "victim": "Sirban",
            "zone": "Western Wastes",
            "timeStamp": "date"
        },
        {
            "charName": "Grixus",
            "victim": "Tomb",
            "zone": "Plane of Mischief",
            "timeStamp": "date"
        },
        {
            "charName": "Grixus",
            "victim": "Suna",
            "zone": "Wakening Lands",
            "timeStamp": "date"
        },
        {
            "charName": "Grixus",
            "victim": "Pucca",
            "zone": "Cobalt Scar",
            "timeStamp": "date"
        },
        {
            "charName": "Grixus",
            "victim": "Xeek",
            "zone": "Western Wastes",
            "timeStamp": "date"
        }
    ]

        mock_camp_out = [
        {
            "charName": "Grixus",
            "zone": "Western Wastes",
            "timeStamp": "date"
        },
        {
            "charName": "Grixus",
            "zone": "Plane of Mischief",
            "timeStamp": "date"
        },
        {
            "charName": "Stork",
            "zone": "Wakening Lands",
            "timeStamp": "date"
        },
        {
            "charName": "Captainn",
            "zone": "Cobalt Scar",
            "timeStamp": "date"
        },
        {
            "charName": "Lifesaver",
            "zone": "Western Wastes",
            "timeStamp": "date"
        }
    ]
    
        items_query = """INSERT INTO items (
        charName, 
        itemLocation, 
        itemName, 
        itemId, 
        itemCount, 
        itemSlots, 
        fileDate
        ) VALUES (?, ?, ?, ?, ?, ?, ?);"""

        spells_query = """INSERT INTO missingSpells (
        charName,
        spellName,
        level,
        fileDate
        ) VALUES (?, ?, ?, ?);"""

        yellow_text_query = """INSERT INTO yellowtext (
        killer,
        victim,
        zone,
        timeStamp
        ) VALUES (?, ?, ?, ?);"""

        campout_query = """INSERT INTO campOut (
        charName,
        zone,
        timeStamp
        ) VALUES (?, ?, ?);"""

        try:
            cursor = conn.cursor()
            for item in mock_items:
                cursor.execute(items_query, tuple(item.values()))
            for spell in mock_missing_spells:
                cursor.execute(spells_query, tuple(spell.values()))
            for yt in mock_yellow_text:
                cursor.execute(yellow_text_query, tuple(yt.values()))
            for camp in mock_camp_out:
                cursor.execute(campout_query, tuple(camp.values()))
            conn.commit()
        except sqlite3.Error as e:
            print(f"load_fxitures error: {e}")

        