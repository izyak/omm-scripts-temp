import pymysql.cursors
from dotenv import dotenv_values

config = dotenv_values(".env")
HOST = config.get("host")
USER = config.get("user")
PASSWORD = config.get("password")
DATABASE = config.get("database")

connection = pymysql.connect(host=HOST,
                             user=USER,
                             password=PASSWORD,
                             database=DATABASE,
                             cursorclass=pymysql.cursors.DictCursor)

# mydb = mysql.connector.connect(
#     host=HOST, user=USER, password=PASSWORD, database=DATABASE
# )


def get_prev_timestamp(key) -> int:
    with connection.cursor() as cursor:
        cursor.execute("select `timestamp` from timestamp_history where _key=%s", (key,))
        value = cursor.fetchone()
        return value['timestamp'];
