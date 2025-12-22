import pandas as pd
import pypyodbc as odbc

class DB_Configuration:
    #Creates SQL Server connection string
    def connection_string (self, driver, server_name, database_name):
            conn_string = f"""
                DRIVER={{{driver}}};
                SERVER={server_name};
                DATABASE={database_name};
                Trust_Connection=yes;
            """
            return conn_string
    
    #Establishes server connection based on user input for required information and obtains data
    def getUserConfig(self):
        print("To Access Your Data . . . ")
        #Enter these as you would in the server connection string
        driver = input("Enter DRIVER: ")
        server = input("Enter SERVER: ")
        database = input("Enter DATABASE: ")
        
        try:
            conn = odbc.connect(self.connection_string(driver, server, database))
            print("Connected to Database!\n")
            dataset = input("Which Dataset do you want to access?: ")
            query = "SELECT * FROM [dbo].[%s]" % dataset #Enter 'Dataset1' or 'Dataset2'
            cursor = conn.cursor()
            cursor.execute(query)
            cursor.fetchall()
            df_init = pd.read_sql(query, conn)
            self.df = df_init[['x', 'y']] #Columns MUST be labeled as such in the DB Table
        except odbc.DatabaseError as e:
            print('Database Error: ' + str(e.value[1]))
        except odbc.Error as e:
            print('Connection Error: ' + str(e.value[1]))

    def getData(self):
         return self.df