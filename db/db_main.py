# db_main.py
import sqlite3
import aiosqlite

def get_db_connection():
    conn = sqlite3.connect('db_3month/store.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

async def create_tables():
    async with aiosqlite.connect('db_3month/store.sqlite3') as conn:
        cursor = await conn.cursor()

        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS products_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                productid INTEGER,
                category TEXT,
                infoproduct TEXT,
                price TEXT,
                photo TEXT
            );
        ''')

        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS collection_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                productid INTEGER,
                collection TEXT
            );
        ''')

        await conn.commit()

async def insert_product_details(productid, category, infoproduct, price, photo):
    async with aiosqlite.connect('db_3month/store.sqlite3') as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
            INSERT INTO products_details (productid, category, infoproduct, price, photo)
            VALUES (?, ?, ?, ?, ?)
        ''', (productid, category, infoproduct, price, photo))
        await conn.commit()

async def insert_collection_product(productid, collection):
    async with aiosqlite.connect('db_3month/store.sqlite3') as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
            INSERT INTO collection_products (productid, collection)
            VALUES (?, ?)
        ''', (productid, collection))
        await conn.commit()

def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("""
        SELECT * FROM products_details pd
        INNER JOIN collection_products cp ON pd.productid = cp.productid
        """).fetchall()
    conn.close()
    return products

async def delete_product(product_id):
    try:
        async with aiosqlite.connect('db_3month/store.sqlite3') as conn:
            cursor = await conn.cursor()

            await cursor.execute('DELETE FROM collection_products WHERE productid = ?', (product_id,))
            await cursor.execute('DELETE FROM products_details WHERE productid = ?', (product_id,))

            await conn.commit()
    except Exception as e:
        print(f"При удалении продукта произошла ошибка: {e}")


def sql_create():
    return None