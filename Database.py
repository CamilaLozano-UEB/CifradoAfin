import mysql.connector


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            # Configura la conexión a la base de datos aquí
            cls._instance.db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Escorpion25151.',
                database='seguridaddb'
            )
        return cls._instance

    def insert_rate_limit(self, ip_address, requests, limit_time):
        cursor = self.db.cursor()
        insert_query = "INSERT INTO rate_limit (ip_address, requests, limit_time) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (ip_address, requests, limit_time))
        self.db.commit()
        cursor.close()

    def get_rate_limit(self, ip_address):
        cursor = self.db.cursor()
        select_query = "SELECT requests, limit_time FROM rate_limit WHERE ip_address = %s"
        cursor.execute(select_query, (ip_address,))
        rate_limit_data = cursor.fetchone()
        cursor.close()
        return rate_limit_data

    def update_rate_limit(self, ip_address, requests, limit_time):
        cursor = self.db.cursor()
        update_query = "UPDATE rate_limit SET requests = %s, limit_time = %s WHERE ip_address = %s"
        cursor.execute(update_query, (requests, limit_time, ip_address))
        self.db.commit()
        cursor.close()

    def delete_rate_limit(self, ip_address):
        cursor = self.db.cursor()
        delete_query = "DELETE FROM rate_limit WHERE ip_address = %s"
        cursor.execute(delete_query, (ip_address,))
        self.db.commit()
        cursor.close()
