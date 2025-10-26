import mysql.connector

def test_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database_name'
        )
        
        if connection.is_connected():
            print("Successfully connected to the database!")
            db_info = connection.get_server_info()
            print(f"MySQL Server version: {db_info}")
            
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"Connected to database: {db_name}")
            
            # Test if the resume table exists
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = %s
                AND table_name = 'resume'
            """, (db_name,))
            
            if cursor.fetchone()[0] == 1:
                print("Resume table exists!")
            else:
                print("Resume table does not exist!")
                
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    test_db_connection()