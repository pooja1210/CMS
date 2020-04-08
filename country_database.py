import mysql.connector

def connects():
    global conn
    global cur

    try:
        conn=mysql.connector.connect(host="localhost", user="root", passwd="", database="template_adduser")
        
        cur= conn.cursor(dictionary=True)
    except mysql.connector.Error as err:
        print(err)
        #conn.rollback()

connects();

