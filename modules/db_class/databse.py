import sqlite3 

class database:
    def __init__(self,database=None,table=None,data=None, column=None, key=None):
        """
        database - name of the database
        table - name of the table
        data - tuple of the data to be inserted
        column - for search and delete
        key - value to search or delete
        """
        self.database = database
        self.table = table
        self.data = data
        self.column = column
        self.key = key

    def connect(self):
        if (self.database == None):
            print("Database not specified")
            return
        try:
            connection = sqlite3.connect(self.database)
            return connection
        except:
            print("Could not connect to database")


    def insert(self):
        if (self.data == None):
            print("No data to insert")
            return

        if (self.table == None):
            print("Table Name not specified")
            return

        try:
            connection = self.connect()
            cursor = connection.cursor()
            query = f"insert into {self.table} values {self.data}"
            cursor.execute(query)
            connection.commit()
        except:
            print("Could not insert the values to table")


    def delete(self):
        if (self.table == None):
            print("Table name not specified")

        try:
            connection = self.connect()
            cursor = connection.cursor()
            query = f"delete from {self.table} where {self.column}='{self.key}'"
            cursor.execute(query)
            connection.commit()
        except:
            print("Could not delete the value")


    def read(self):
        if (self.table == None):
            print("Table name not specified")

        try:
            connection = self.connect()
            cursor = connection.cursor()
            query = f"select * from {self.table}"
            cursor.execute(query)
            connection.commit()
            rows = cursor.fetchall()
            search_results = []
            for row in rows:
                search_results.append(row)
            return search_results
        except:
            print("Could not search the table")


    def find(self):
        if (self.table == None):
            print("Table name not specified")

        try:
            connection = self.connect()
            cursor = connection.cursor()
            query = f"select * from {self.table} where {self.column}='{self.key}'"
            cursor.execute(query)
            connection.commit()
            rows = cursor.fetchall()
            search_results = []
            for row in rows:
                search_results.append(row)
            return search_results
        except:
            print("Could not find the value")


