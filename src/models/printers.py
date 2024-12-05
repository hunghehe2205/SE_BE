import mysql.connector
from mysql.connector import Error

printers = [
    {
        "printer_id": "PRN001",
        "printer_name": "HP LaserJet 500",
        "location": "1st Floor, Room 101",
        "supports_color": 1,
        "supports_duplex": 1,
        "max_paper_size": "A4",
        "printer_status": "Available"
    },
    {
        "printer_id": "PRN002",
        "printer_name": "Canon ColorPrint 3000",
        "location": "2nd Floor, Room 205",
        "supports_color": 1,
        "supports_duplex": 0,
        "max_paper_size": "A3",
        "printer_status": "Busy"
    },
    {
        "printer_id": "PRN003",
        "printer_name": "Epson EcoTank L3150",
        "location": "Ground Floor, Reception",
        "supports_color": 0,
        "supports_duplex": 1,
        "max_paper_size": "A4",
        "printer_status": "Available"
    },
    {
        "printer_id": "PRN004",
        "printer_name": "Brother HL-L2350DW",
        "location": "3rd Floor, Room 308",
        "supports_color": 0,
        "supports_duplex": 1,
        "max_paper_size": "A0",
        "printer_status": "Out of Paper"
    },
    {
        "printer_id": "PRN005",
        "printer_name": "Ricoh SP C261",
        "location": "4th Floor, Room 410",
        "supports_color": 1,
        "supports_duplex": 0,
        "max_paper_size": "A4",
        "printer_status": "Offline"
    },
    {
        "printer_id": "PRN006",
        "printer_name": "Samsung ProXpress M4020ND",
        "location": "1st Floor, Room 102",
        "supports_color": 0,
        "supports_duplex": 1,
        "max_paper_size": "A1",
        "printer_status": "Available"
    },
    {
        "printer_id": "PRN007",
        "printer_name": "Xerox WorkCentre 6515",
        "location": "5th Floor, Room 520",
        "supports_color": 1,
        "supports_duplex": 1,
        "max_paper_size": "A3",
        "printer_status": "Under Maintenance"
    },
    {
        "printer_id": "PRN008",
        "printer_name": "Dell E525w",
        "location": "2nd Floor, Lab",
        "supports_color": 1,
        "supports_duplex": 0,
        "max_paper_size": "A4",
        "printer_status": "Available"
    },
    {
        "printer_id": "PRN009",
        "printer_name": "Lexmark MB2236adw",
        "location": "Basement, Storage",
        "supports_color": 0,
        "supports_duplex": 1,
        "max_paper_size": "A4",
        "printer_status": "Available"
    },
    {
        "printer_id": "PRN010",
        "printer_name": "Kyocera TASKalfa 2552ci",
        "location": "3rd Floor, Admin Office",
        "supports_color": 1,
        "supports_duplex": 1,
        "max_paper_size": "A3",
        "printer_status": "Busy"
    }
]


def smaller_paper_sizes(size1: str, size2: str) -> bool:
    # Define the A-series paper sizes in a list, from largest to smallest
    paper_sizes = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"]

    # Get the index of each paper size from the list
    index1 = paper_sizes.index(size1)
    index2 = paper_sizes.index(size2)

    # Compare the indices to determine which paper size is smaller
    if index1 < index2:
        return True
    elif index1 > index2:
        return False
    else:
        return True


class PrinterModel():
    def __init__(self, db_config):
        self.db_config = db_config

    def get_db_connection(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error connecting to database: {e}")
        return None

    def get_printer_list(self):
        connection = self.get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = 'SELECT * FROM Printers'
                cursor.execute(query)
                result = cursor.fetchall()
                return result
            except Error as e:
                result = {'error': f'[{e.msg}]'}
                connection.rollback()
                return result
            finally:
                cursor.close()
                connection.close()
        return {'error': 'Failed to connect to the database'}

    def get_suitable_print_list(self, doc_id: str):
        connection = self.get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = ''' SELECT *
                            FROM PrintSettings
                            WHERE document_id = %s
                            ORDER BY time_updated DESC
                            LIMIT 1;'''
                cursor.execute(query, (doc_id,))
                setting = cursor.fetchone()
                connection.commit()
                res = []
                for printer in printers:
                    # Debugging output to see each printer's attributes
                    print(f"Checking printer: {printer}")

                    # Check printer status
                    if printer['printer_status'] != "Available":
                        continue

                    # Check color and duplex support
                    if setting['color'] != printer['supports_color']:
                        continue

                    if setting['duplex'] != printer['supports_duplex']:
                        continue

                    # Check if the printer supports the required paper size
                    if not smaller_paper_sizes(printer['max_paper_size'], setting['paper_size']):
                        continue

                    # If all conditions match, add the printer to the result list
                    res.append(printer)

                return res
            except Error as e:
                result = {'error': f'[{e.msg}]'}
                connection.rollback()
                return result
            finally:
                cursor.close()
                connection.close()
        return {'error': 'Failed to connect to the database'}
