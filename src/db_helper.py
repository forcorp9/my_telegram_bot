import sqlite3

class DbHelper:
    def __init__(self):
        self.db_name = 'category.db'
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.setup()
        self.intial_product()
        #self.insert_data()


    def setup(self):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS category(
                             id INTEGER PRIMARY KEY UNIQUE,
                             name TEXT NOT NULL,
                             parent_id INTEGER
                        )""")
        self.conn.execute("""CREATE TABLE IF NOT EXISTS product(
                             id INTEGER PRIMARY KEY UNIQUE,
                             name TEXT,
                             amount INTEGER,
                             file_path TEXT,
                             category_id INTEGER
                                )""")
        self.conn.commit()
    def getproductByCategory_id(self, id):
        return self.conn.execute('SELECT * FROM product where category_id=?', [id]).fetchone()
    def getCategories(self):
        return self.conn.execute('SELECT * FROM category where parent_id is null limit 20').fetchall()

    def getParentId(self, parent_id):
        return self.conn.execute('SELECT * FROM category where parent_id=?', [parent_id]).fetchall()
    def insert_data(self):
        categories = [
            (1, 'Lavash', None),
            (2, 'Shaurma', None),
            (3, 'Donar', None),
            (4, 'Burger', None),
            (5, 'Hod-dog', None),
            (6, 'Ichimliklar', None),
            (7, 'Desertlar', None),
            (8, 'Говяжий лаваш', 1),
            (9, 'Говяжий лаваш с сыром', 1),
            (10, 'Мини', 8),
            (11, 'Классический', 8),
            (12, 'Мини', 9),
            (13, 'Классический', 9)
            ]

        self.conn.executemany("""
             INSERT INTO category(id, name, parent_id) VALUES(?, ?, ?)""",
             categories
        )
        self.conn.commit()



    def intial_product(self):
        products = [
            (1, 'Говяжиний Мини Лаваш', 15000, 'lavash_little.jpg', 10),
            (2, 'Говяжиний Классичиский Лаваш', 17000, 'lavash_big.jpg', 11),
            (3, 'Говяжий лаваш с сыром Классичиский Лаваш', 'lavash_big.jpg', 13),
            (4, 'Говяжий лаваш с сыром Мини Лаваш', 'lavash_little.jpg', 12)
        ]
        self.conn.executemany("""
            INSERT INTO product(id, name, amount, file_path, category_id) VALUES(?, ?, ?, ?, ?)""",
            products
        )
        self.conn.commit()
