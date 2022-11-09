import mysql.connector
import sys
sys.stdout = open('out.txt', 'w')
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
)

def drop_db():
    cursor = mydb.cursor()
    cursor.execute('SHOW DATABASES')
    dbs = []
    for name in cursor.fetchall():
        cursor.execute('DROP DATABASE '+name[0])
        # if 'db' in name[0]: 
            # dbs.append(name[0])

def show_projects():
    cursor = mydb.cursor()
    cursor.execute('SHOW DATABASES')
    dbs = []
    for name in cursor.fetchall():
        if 'db' in name[0]: dbs.append(name[0])

    print(dbs)
    for db in dbs:
        print(db, end=' => ')
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = db
        )
        cur = conn.cursor()
        sql = 'SELECT PROJECTNAME FROM Project'
        cur.execute(sql)
        print(cur.fetchall())
        # break 

def show_tables_rows(db):
    conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = db
        )
    cur = conn.cursor()
    cur.execute('SHOW TABLES')
    tables = [table[0] for table in cur.fetchall()]
    # print(tables)
    for tab in tables:
        cur.execute('SELECT * FROM '+tab)
        res = cur.fetchall()
        if res:
            print('*'*50)
            print(tab)
            print('*'*50)
            print(res[0])
            # print(len(res))
            # for r in res:
            #     print(r)
            # break

# show_projects()
# show_tables_rows('db5001db')
