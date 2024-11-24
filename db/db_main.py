import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            productid INTEGER,
            category TEXT,
            infoproduct TEXT,
            price TEXT,
            photo TEXT
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS collection_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            productid INTEGER,
            collection TEXT
        );
    ''')

    conn.commit()
    conn.close()

def insert_product_details(productid, category, infoproduct, price, photo):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO products_details (productid, category, infoproduct, price, photo)
        VALUES (?, ?, ?, ?, ?)
    ''', (productid, category, infoproduct, price, photo))

    conn.commit()
    conn.close()

def insert_collection_product(productid, collection):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO collection_products (productid, collection)
        VALUES (?, ?)
    ''', (productid, collection))

    conn.commit()
    conn.close()