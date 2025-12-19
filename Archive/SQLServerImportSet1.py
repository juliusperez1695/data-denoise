import pypyodbc as odbc #pip install pypyodbc
import pyodbc
import pandas as pd #pip install pandas
from sqlalchemy import create_engine
import urllib

class SQLServerImportSet1:
    
    def import_csv_tosql():
   
        ##1. Importing Dataset from csv
        df = pd.read_csv('Dataset1.csv', header = None)
        ## df = pd.read_csv('Dataset1.csv', header = None, usecols = [0, 1])

        #2. Select columns we want to import
        columns = [0, 1]

        df_data = df[columns]
        records = df_data.values.tolist()
        print(records)


        #Step 3. Create SQL Server Connection string
        DRIVER = 'SQL Server'
        SERVER_NAME = 'JC-ZENBOOK'
        DATABASE_NAME = 'testdb'

        def connection_string (driver, server_name, database_name):
            conn_string = f"""
                DRIVER={{{driver}}};
                SERVER={server_name};
                DATABASE={database_name};
                Trust_Connection=yes;
            """
            return conn_string
        """
        #Step 3.2 Create database connection instance
        """
        try:
            conn = odbc.connect(connection_string(DRIVER, SERVER_NAME, DATABASE_NAME))
        except odbc.DatabaseError as e:
            print('Database Error: ')
            print(str(e.value[1]))
        except odbc.Error as e:
            print('Connection Error:')
            print(str(e.value[1]))

        #Step 3.3 Create  cursor connection
        sql_insert = '''
            INSERT INTO [dbo].[Dataset1]
            VALUES (?,?)
        '''
        
        # write the DataFrame to a table in the sql database
        try:
            cursor = conn.cursor()
            cursor.executemany(sql_insert, records)
            cursor.commit()

        except Exception as e:
            cursor.rollback()
            print(str(e[1]))

        finally:
            print('Data Imported to Database.\n\n')
            cursor.close()
            conn.close()

        
