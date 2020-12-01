import sqlite3

class DbHelper:

    def __init__(self):
        self.db_name = 'my_data.db'
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.setup()
        # self.intial_product()
        # self.intial_data()

    def setup(self):
        self.conn.execute(""" CREATE TABLE IF NOT EXISTS tg_user(
          id INTEGER PRIMARY KEY UNIQUE,
          username TEXT DEFAULT NULL,
          first_name TEXT NOT NULL,
          birth_year INTEGER,
          full_name TEXT
        )""")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS category(
            id INTEGER PRIMARY KEY UNIQUE,
            name TEXT NOT NULL,
            parent_id INTEGER
        )""")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS product(
                id INTEGER NOT NULL PRIMARY KEY UNIQUE,
                name TEXT,
                amount INTEGER,
                file_path TEXT,
                category_id INTEGER
        )""")

        self.conn.commit()

    def getCategories(self):
        return self.conn.execute('SELECT * FROM category where parent_id is null limit 20').fetchall();

    def getCategorychilds(self, parent_id):
        return self.conn.execute('SELECT * FROM category where parent_id =? limit 20', [parent_id]).fetchall();


    def getproductByCategory_id(self, id):
        return self.conn.execute('SELECT * FROM product where category_id=?', [id]).fetchone();

    def getproductById(self, id):
        return self.conn.execute('SELECT * FROM product where id=?', [id]).fetchone();

    def getUserById(self, id):
        return self.conn.execute('SELECT * FROM tg_user where id=?', [id]).fetchone();

    def createUser(self, id, username, first_name):
        self.conn.execute("""
        INSERT INTO tg_user(id, username, first_name)
        VALUES(?, ?, ?)
        """, (id, username, first_name))
        self.conn.commit()


    def intial_data(self):
        categories = [
            (1, '🌯 Лаваш', None),
            (2, '🌮 Шаурма', None),
            (3, '🍲 Донар', None),
            (4, '🍔 Бургер', None),
            (5, '🌭 Хот-дог', None),
            (6, '🍰 Десерты', None),
            (7, '☕️ Напитки', None),
            (8, '🍟 Гарнир', None),
            (9, 'Говяжиний лаваш', 1),
            (10, 'Говяжиний лаваш с сыром', 1),
            (11, 'Мини', 9),
            (12, 'Классичиский', 9),
            (13, 'Мини', 10),
            (14, 'Классичиский', 10),
        ]
        self.conn.executemany("""
            INSERT INTO category(id, name, parent_id) VALUES(?, ?, ?)""",
            categories
        )
        self.conn.commit()


    def intial_product(self):
        products = [
            (1, 'Говяжиний Мини Лаваш', 17000, 'lavash_1.jpg', 11),
            (2, 'Говяжиний Классичиский Лаваш', 17000, 'lavash_2.jpg', 12)
        ]
        self.conn.executemany("""
            INSERT INTO product(id, name, amount, file_path, category_id) VALUES(?, ?, ?, ?, ?)""",
            products
        )
        self.conn.commit()
