import mysql.connector
from mysql.connector import Error


class LogModel():
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

    def insert_log(self, doc_id: str, printer_id: str):
        connection = self.get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                # Insert the new user
                insert_query = """
                    INSERT INTO PrintingLog (document_id, printer_id)
                    VALUES (%s, %s);
                """
                cursor.execute(
                    insert_query, (doc_id, printer_id))
                connection.commit()

                return {"success": "Success"}
            except Error as e:
                result = {'error': f'[{e.msg}]'}
                connection.rollback()
                return result
            finally:
                cursor.close()
                connection.close()
        return {'error': 'Failed to connect to the database'}

    def get_printing_log(self):
        connection = self.get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = """
                            SELECT 
                                P.printer_id,
                                P.printer_name,
                                P.location,
                                P.printer_status,
                                PL.document_id,
                                PL.time_updated
                            FROM 
                                PrintingLog PL
                            JOIN 
                                Printers P
                            ON 
                                PL.printer_id = P.printer_id;
                            """
                cursor.execute(query)
                result = cursor.fetchall()
                connection.commit()
                return result

            except Error as e:
                result = {'error': f'[{e.msg}]'}
                connection.rollback()
                return result
            finally:
                cursor.close()
                connection.close()
        return {'error': 'Failed to connect to the database'}
