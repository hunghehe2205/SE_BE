import mysql.connector
from mysql.connector import Error


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
                print_query = 'SELECT * FROM Printers'
                cursor.execute(print_query)
                printers = cursor.fetchall()
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
                    # Check printer status
                    if printer['printer_status'] != "Available":
                        continue

                    # Check color and duplex support
                    if not ((setting['color'] == printer['supports_color']) or (setting['color'] == 0 and printer['supports_color'] == 1)):
                        continue

                    if not ((setting['duplex'] == printer['supports_duplex']) or (setting['duplex'] == 0 and printer['supports_duplex'] == 1)):
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
