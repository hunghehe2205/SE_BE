import mysql.connector
from mysql.connector import Error


class UserModel():
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

    def get_full_user_id_info(self, user_id: str):
        connection = self.get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                user_query = """
                            SELECT 
                                user_id, fullname, username, password
                            FROM Users
                            WHERE user_id = %s;
                            """
                cursor.execute(user_query, (user_id,))
                user_info = cursor.fetchone()  # Fetch one record
                if user_info is None:
                    return {"error": "User not found"}
                documents_query = """
                                    SELECT 
                                    D.document_id, 
                                    D.file_name, 
                                    D.upload_date, 
                                    D.file_path,
                                    PS.setting_id,
                                    PS.color,
                                    PS.copies,
                                    PS.duplex,
                                    PS.paper_size,
                                    PS.time_updated
                                FROM Documents D
                                LEFT JOIN PrintSettings PS ON D.document_id = PS.document_id
                                WHERE D.user_id = %s;
                            """
                cursor.execute(documents_query, (user_id,))
                documents = cursor.fetchall()  # Fetch all related documents
                if documents is None:
                    return {"error": "User has not uploaded any files"}
                result = {
                    "user": user_info,
                    "list_document_uploaded": documents
                }
                return result

            except Error as e:
                result = {'error': f'[{e.msg}]'}
                connection.rollback()
                return result
            finally:
                cursor.close()
                connection.close()
        return {'error': 'Failed to connect to the database'}

    def register_user(self, user_id: str, fullname: str, user_name: str,  password: str):
        connection = self.get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                check_query = """
                            SELECT user_id, username 
                            FROM Users 
                            WHERE user_id = %s OR username = %s;
                            """
                cursor.execute(check_query, (user_id, user_name))
                existing_user = cursor.fetchone()

                if existing_user:
                    return {"error": "User ID or Username already exists"}

                # Insert the new user
                insert_query = """
                    INSERT INTO Users (user_id, fullname, username, password)
                    VALUES (%s, %s, %s, %s);
                """
                cursor.execute(
                    insert_query, (user_id, fullname, user_name, password))
                connection.commit()

                return {"success": "User registered successfully"}
            except Error as e:
                result = {'error': f'[{e.msg}]'}
                connection.rollback()
                return result
            finally:
                cursor.close()
                connection.close()
        return {'error': 'Failed to connect to the database'}

    def log_in(self, user_name: str, password: str):
        connection = self.get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = """
                SELECT user_id, username, password
                FROM Users
                WHERE username = %s AND password = %s;
                """
                cursor.execute(query, (user_name, password))
                user = cursor.fetchone()

                if user is None:
                    return {'error': 'Wrong login info'}

                return {
                    "message": "Login successful",
                    "user_id": user["user_id"],
                    "username": user["username"]
                }
            except Error as e:
                result = {'error': f'[{e.msg}]'}
                connection.rollback()
                return result
            finally:
                cursor.close()
                connection.close()
        return {'error': 'Failed to connect to the database'}
