import mysql.connector
from mysql.connector import Error
from datetime import datetime
from typing import Optional


class PrintSettingsModel():
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

    def generate_setting_id(self):
        connection = self.get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(setting_id) FROM PrintSettings;")
        result = cursor.fetchone()
        max_user_id = result[0]  # Fetch the current max UserID

        # Generate the next UserID
        if max_user_id is None:
            # If no UserID exists, start with 'U-001'
            next_user_id = "S-001"
        else:
            # Extract the numeric part, increment it, and format with leading zeros
            numeric_part = int(max_user_id.split('-')[1])
            next_user_id = f"S-{numeric_part + 1:03d}"

        cursor.close()
        connection.close()
        return next_user_id

    def create_setting(self, doc_id: str, color: bool, copies: int, duplex: bool, paper_size: str):
        connection = self.get_db_connection()
        if connection:
            try:
                setting_id = self.generate_setting_id()
                cursor = connection.cursor(dictionary=True)
                cursor.callproc('InsertSettings', [
                                setting_id, doc_id, color, copies, duplex, paper_size])
                connection.commit()
                return {'message': 'Adding successfully'}
            except Error as e:
                result = {'error': f'[{e.msg}]'}
                connection.rollback()
                return result
            finally:
                cursor.close()
                connection.close()
        return {'error': 'Failed to connect to the database'}

    def get_settings(self, doc_id: str):
        connection = self.get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.callproc('GetSettings', [doc_id])
                setting = None
                for result in cursor.stored_results():
                    setting = result.fetchone()

            # Check if user data was found
                if setting:
                    return setting
                else:
                    return {'error': 'Setting not found'}

            except Error as e:
                result = {'error': f'[{e.msg}]'}
                connection.rollback()
                return result
            finally:
                cursor.close()
                connection.close()
        return {'error': 'Failed to connect to the database'}

    def update_setting(self, doc_id: str, color: Optional[bool] = None, copies: Optional[int] = None, duplex: Optional[bool] = None, paper_size: Optional[str] = None):
        connection = self.get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.callproc('UpdateSettings', [
                                doc_id, color, copies, duplex, paper_size])
                query = '''SELECT *
                            FROM PrintSettings
                            WHERE document_id = %s
                            ORDER BY time_updated DESC
                            LIMIT 1;
                            '''
                cursor.execute(query, (doc_id,))
                result = cursor.fetchone()
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
