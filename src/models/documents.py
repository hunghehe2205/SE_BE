import mysql.connector
from mysql.connector import Error


class DocumentsModel():
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

    def generate_doc_id(self):
        connection = self.get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(document_id) FROM Documents;")
        result = cursor.fetchone()
        max_user_id = result[0]  # Fetch the current max UserID

        # Generate the next UserID
        if max_user_id is None:
            # If no UserID exists, start with 'U-001'
            next_user_id = "D-001"
        else:
            # Extract the numeric part, increment it, and format with leading zeros
            numeric_part = int(max_user_id.split('-')[1])
            next_user_id = f"D-{numeric_part + 1:03d}"

        cursor.close()
        connection.close()
        return next_user_id

    def insert_document(self, file_name: str, file_path: str, user_id: str):
        connection = self.get_db_connection()
        if connection:
            try:
                doc_id = self.generate_doc_id()
                cursor = connection.cursor(dictionary=True)
                query = 'INSERT INTO Documents (document_id, file_name, file_path, user_id) VALUES (%s,%s,%s,%s)'
                cursor.execute(
                    query, (doc_id, file_name, file_path, user_id))
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

    def get_doc_list(self):
        connection = self.get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = 'SELECT * FROM Documents'
                cursor.execute(query)
                result = cursor.fetchall()
                connection.commit()
                if result:
                    return result
                else:
                    return {'error': 'List is empty'}
            except Error as e:
                result = {'error': f'[{e.msg}]'}
                connection.rollback()
                return result
            finally:
                cursor.close()
                connection.close()
        return {'error': 'Failed to connect to the database'}

    def update_doc(self, doc_id: str, file_name: str):
        connection = self.get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = 'UPDATE Documents SET file_name = %s WHERE document_id = %s'
                cursor.execute(
                    query, (file_name, doc_id))
                query = 'SELECT * FROM Documents WHERE document_id = %s'
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

    def update_file_path_by_doc(self, doc_id: str, file_path: str):
        connection = self.get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = 'UPDATE Documents SET file_path = %s WHERE document_id = %s'
                cursor.execute(
                    query, (file_path, doc_id))
                connection.commit()
            except Error as e:
                result = {'error': f'[{e.msg}]'}
                connection.rollback()
                return result
            finally:
                cursor.close()
                connection.close()
        return {'error': 'Failed to connect to the database'}

    def get_file_path_by_doc_id(self, doc_id: str):
        connection = self.get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = 'SELECT file_path FROM Documents WHERE document_id = %s'
                cursor.execute(
                    query, (doc_id,))
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

    def get_name_by_doc_id(self, doc_id: str):
        connection = self.get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = 'SELECT file_name FROM Documents WHERE document_id = %s'
                cursor.execute(
                    query, (doc_id,))
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
