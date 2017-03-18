#!/usr/env/python3
from __future__ import print_function

import pymysql
import sys

db_host = "localhost"
db_port = 3306
db_user = "root"
db_pass = "password"
db_name = "somedb"

app_user = "test1"
app_pass = "1test"

read_only_user = "test2"
read_only_pass = "2test"

flush_privilege = "FLUSH PRIVILEGES"


##############################################################################
def get_connection():
    conn = ""
    try:
        conn = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            passwd=db_pass,
            db=db_name
        )
    except Exception as e:
        print("Cannot create connection" + str(e))
        sys.exit(1)

    return conn


##############################################################################
def run_sql_commands(create_user, create_pass, privilege, cursor):
    create_user_sql = "CREATE OR REPLACE USER '" + create_user + "'@'%' IDENTIFIED BY '" + create_pass + "'"
    grant_sql = "GRANT " + privilege + " ON `" + db_name + "`.* to '" + create_user + "'@'%';"
    cursor.execute(create_user_sql)
    cursor.execute(grant_sql)
    cursor.execute(flush_privilege)


##############################################################################
def main():

    conn = get_connection()

    run_sql_commands(app_user, app_pass, "ALL PRIVILEGES", conn.cursor())
    run_sql_commands(read_only_user, read_only_pass, "SELECT", conn.cursor())

    conn.cursor().close()
    conn.close()


##############################################################################
if __name__ == '__main__':
    main()
