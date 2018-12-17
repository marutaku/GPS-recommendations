import pandas as pd
import pymysql.cursors
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from lib import config
connection = pymysql.connect(
    host='localhost',
    user=config.MYSQL_USER,
    password=config.MYSQL_PASSWORD,
    db=config.MYSQL_DB_NAME,
    cursorclass=pymysql.cursors.DictCursor
)

def insert_db(user_id, active_hour):
    with connection.cursor() as cursor:
        sql = 'UPDATE user SET active_hour = %s WHERE id = %s'
        cursor.execute(sql, (active_hour, user_id))
    connection.commit()


def main():
    data = pd.read_sql('''
    SELECT
        user_id,
        DATE_FORMAT(create_at, '%H') as create_at,
        COUNT(*) as visited_count
    FROM
        visited_place
    GROUP BY
        user_id,
        DATE_FORMAT(create_at, '%H');
    ''', connection)

    mode_dict = {}
    target_hour = list(range(10, 18))
    for index, row in data.iterrows():
        if row.user_id in mode_dict.keys():
            current = mode_dict[row.user_id]
            if list(current.values())[0] < row.visited_count and int(row.create_at) in target_hour:
                mode_dict[row.user_id] = {
                    int(row.create_at): row.visited_count
                }
        else:
            if int(row.create_at) in target_hour:
                mode_dict[row.user_id] = {
                        int(row.create_at): row.visited_count
                }

    for key, val in mode_dict.items():
        insert_db(key, list(val.keys())[0])

if __name__ == '__main__':
    main()
