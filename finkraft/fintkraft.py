# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import mysql.connector

from getpass import getpass
from mysql.connector import connect, Error

use_database = "USE testdb"

create_Transaction_table_query = """
CREATE TABLE Transaction(
    TransactionID VARCHAR(10) PRIMARY KEY,
    CustomerName VARCHAR(20),
    TransactionDate DATE,
    Amount double(5,2),
    Status VARCHAR(12),
    InvoiceURL VARCHAR(100)
)
"""
change_column_name = """
ALTER TABLE Transaction
    RENAME COLUMN TrasnsactionID to TransactionID"""

show_table_query = "DESCRIBE Transaction"

try:
    with connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
    ) as connection:
        with connection.cursor() as cursor:
            
            cursor.execute(use_database)
            connection.commit()
            
            #cursor.execute(create_Transaction_table_query)
            #connection.commit()
            cursor.execute(change_column_name)
            connection.commit()
            
            cursor.execute(show_table_query)
            # Fetch rows from last executed query
            result = cursor.fetchall()
            for row in result:
                print(row)
except Error as e:
    print(e)
    


