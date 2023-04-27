import mysql.connector
import sys

def connection_pool():
    try:
        db_connection = mysql.connector.connect(user='root', password='secret123', host='127.0.0.1', database='user_db')
        return db_connection
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('Error in connection_pool function at %s:%s' % (exc_traceback.tb_lineno, e))       

def drop_tables():
    try:
        connection = connection_pool()
        cursor = connection.cursor()
        cursor.execute('drop table user;')
        cursor.execute('drop table deals;')
        connection.commit()
        connection.close()
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('Error in create table function at %s:%s' % (exc_traceback.tb_lineno, e))       

def create_user_table():
    try:
        connection = connection_pool()
        usertable_query = '''CREATE TABLE user (
                id INT NOT NULL AUTO_INCREMENT,
                name VARCHAR(30) NOT NULL,
                mobile VARCHAR(15),
                email VARCHAR(30),
                datamode ENUM('active', 'inactive', 'delete'),
                created_on DATETIME,
                updated_on DATETIME,
                PRIMARY KEY (id)
                );'''
        cursor = connection.cursor()
        cursor.execute(usertable_query)
        connection.commit()
        connection.close()
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('Error in create table function at %s:%s' % (exc_traceback.tb_lineno, e))       

def create_deals_table():
    try:
        connection = connection_pool()
        usertable_query = '''CREATE TABLE deals (
                id INT NOT NULL AUTO_INCREMENT,
                deal_date DATETIME,
                security_code VARCHAR(50),
                security_name VARCHAR(50),
                client_name VARCHAR(50),
                deal_type VARCHAR(50),
                quantity VARCHAR(50),
                price VARCHAR(50),
                datamode ENUM('active', 'inactive', 'delete'),
                created_on DATETIME,
                updated_on DATETIME,
                PRIMARY KEY (id)
                );'''
        cursor = connection.cursor()
        cursor.execute(usertable_query)
        connection.close()
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('Error in create table function at %s:%s' % (exc_traceback.tb_lineno, e))  

if __name__ == '__main__':
    drop_tables()
    create_user_table()
    create_deals_table()
