import psycopg2


class Database():
    
    def createTable(self):
        connection = psycopg2.connect(
            dbname="testdb",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE items (
            id serial NOT NULL PRIMARY KEY,
            title VARCHAR (100) NOT NULL UNIQUE,
            image_path VARCHAR (200) NOT NULL 
        );''')
        cursor.execute("INSERT INTO items (id, title, image_path) VALUES (1,'item 1','image.png');")
        cursor.execute("INSERT INTO items (id, title, image_path) VALUES (2, 'item 2','image.png');")
        cursor.execute("INSERT INTO items (id, title, image_path) VALUES (3, 'item 3','image.png');")
        cursor.execute("INSERT INTO items (id, title, image_path) VALUES (4, 'item 4','image.png');")
        cursor.execute("INSERT INTO items (id, title, image_path) VALUES (5, 'item 5','image.png');")
        connection.commit()
        
        cursor.close()
        connection.close()
        

    def dropTable(self):
        with psycopg2.connect(
            dbname="testdb",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("DROP TABLE IF EXISTS items;")
                connection.commit()
                
    def getData(self):
        with psycopg2.connect(
            dbname="testdb",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM items;")
                rows = cur.fetchall()
                print(rows)
                return rows
        

    def connect(self,  db_name: str):
        # connection это инкапсуляция сессии
        connection = psycopg2.connect(
            dbname=db_name,
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )
        
        return connection

    def connect_and_get_cursor(self, db_name:str):
        connection = psycopg2.connect(
            dbname=db_name,
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )
        # cursor позволяет взаимодействовать с базой данных
        return connection.cursor()       
    
    
    
    

# conn = psycopg2.connect(
#     dbname="testdb",
#     user="postgres",
#     password="password",
#     host="localhost",
#     port="5432"
# )

# cur = conn.cursor()

# # Создание новой базы данных
# cur.execute("CREATE DATABASE selecteldb;")
# conn.commit()

# # Закрытие курсора и соединения
# cur.close()
# conn.close()