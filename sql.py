import sqlite3 as sq


def create_database_connection(database_name):
    try:
        connection = sq.connect("ver_1_4/%s.db" % database_name)
        return connection
    except:
        print("Failed to create connection")


def execute_query(database_name, query):
    try:
        connection = sq.connect("ver_1_4/%s.db" % database_name)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except:
        print("Failed to exectute query")


def read_query(database_name, query):
    try:
        connection = sq.connect("ver_1_4/%s.db" % database_name)
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except:
        print("Failed to read database")
