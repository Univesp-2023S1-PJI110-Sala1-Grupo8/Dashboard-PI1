import mysql.connector
from mysql.connector import errorcode


class Database:

    config = {
      'host': '127.0.0.1',
      'user': 'dashboard_user',
      'password': 'dashpass',
      'database': 'dashboard_db',
      'raise_on_warnings': True
    }

    conn: 0

    def __init__(self):
      self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
              print("ERROR: Something is wrong with dashboard username or password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
              print("ERROR: Dashboard Database does not exist.")
            else:
              print("ERROR: {}", err)

    def test(self):
        cursor = self.conn.cursor()
        query = ("SELECT * FROM usuario")
        cursor.execute(query)
        for (name) in cursor:
            print("{}".format(name))

    def disconnect(self):
        self.conn.close()