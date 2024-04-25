import pandas as pd
import pypyodbc as odbc

class DB_Configuration:
    def connection_string (self, driver, server_name, database_name):
            conn_string = f"""
                DRIVER={{{driver}}};
                SERVER={server_name};
                DATABASE={database_name};
                Trust_Connection=yes;
            """
            return conn_string
    
    def getUserConfig(self):
        print("To Access Your Data . . . ")
        driver = input("Enter DRIVER: ")
        server = input("Enter SERVER: ")
        database = input("Enter DATABASE: ")
        
        try:
            conn = odbc.connect(self.connection_string(driver, server, database))
            print("Connected to Database!")
        except odbc.DatabaseError as e:
            print('Database Error: ')
            print(str(e.value[1]))
        except odbc.Error as e:
            print('Connection Error:')
            print(str(e.value[1]))

        dataset = input("Which Dataset do you want to access?: ")
        query = "SELECT * FROM [dbo].[%s]" % dataset
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.fetchall()
        df_init = pd.read_sql(query, conn)
        self.df = df_init[['x', 'y']]

    def getData(self):
         return self.df