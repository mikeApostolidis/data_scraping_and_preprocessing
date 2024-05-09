# database.py

import mysql.connector
from ScrappingBot.src.db.config import DATABASE_CONFIG


def connect_to_db():
    return mysql.connector.connect(
        host=DATABASE_CONFIG['host'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password'],
        database=DATABASE_CONFIG['database'],
        port=DATABASE_CONFIG['port']
    )


# Create a connection pool
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="my_pool",
    pool_size=5,
    **DATABASE_CONFIG
)


def execute_query(query):

    # connection = connect_to_db()

    connection = connection_pool.get_connection()
    cursor = connection.cursor()

    cursor.execute(query)
    result = cursor.fetchall()

    #
    cursor.close()
    connection.close()

    return result


def get_max_date():
    # date = '2018-01-12'
    # connection = connect_to_db()
    connection = connection_pool.get_connection()
    cursor = connection.cursor()

    query = "SELECT MAX(Hmeromnia) FROM anaplirotes ;"

    cursor.execute(query)
    result = cursor.fetchall()

    # result = execute_query(query)
    max_date = result[0][0] if result and result[0] and result[0][0] else None

    cursor.close()
    connection.close()

    return max_date
