import MySQLdb

conn = MySQLdb.connect("localhost", "root", "", "test")


def readdata():
    users = []
    sql = conn.cursor()
    sql.execute("SELECT * FROM emp_records ")
    for row in sql.fetchall():
        list = (row[0], row[1], row[3], row[4], row[5])
        users.append(list)
    return users


def login(user, password):
    sql = conn.cursor()
    sql.execute("SELECT * FROM emp_records where username='{}'and password='{}'".format(user, password))  
    for row in sql.fetchall():
        if row[6] and row[7]:
            return True
    return False


def insert_data(employee_record):
    sql = conn.cursor()
    for r in employee_record:
        first_name = r[0]
        last_name = r[1]
        date_of_birth = r[2]
        aadahr_id = r[3]
        gender = r[4]
        email = r[5]
        user_name = r[6]
        password = r[7]
        try:
            sql.execute("insert into emp_records values('%s','%s','%s','%s','%s','%s','%s','%s')"
                %(first_name,last_name,date_of_birth,aadahr_id,gender,email,user_name,password))      
        except MySQLdb.Error as e:
            print(e)
        conn.commit()
