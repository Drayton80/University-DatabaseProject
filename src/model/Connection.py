import psycopg2

class Connection:
    _connection = None
    _cursor = None

    def start_database_connection(self):
        if not self._connection:
            self._connection = psycopg2.connect(database="postage", user="postgres", password="postgres", port=5433)
            self._cursor = self._connection.cursor()
        
        return self._cursor

    def close_database_connection(self):
        if self._cursor:
            self._cursor.close()
            self._cursor = None

        if self._connection:
            self._connection.commit()
            self._connection.close()
            self._connection = None
