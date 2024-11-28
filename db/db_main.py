# db_main.py
import sqlite3
import aiosqlite
from db import queries

def get_db_connection():
    conn = sqlite3.connect('db_3month/store.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("""
        SELECT * FROM products_details pd
        INNER JOIN collection_products cp ON pd.productid = cp.productid
        """).fetchall()
    conn.close()
    return products


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

async def delete_product(product_id):
    try:
        async with aiosqlite.connect('db_3month/store.sqlite3') as conn:
            cursor = await conn.cursor()

            await cursor.execute('DELETE FROM collection_products WHERE productid = ?', (product_id,))
            await cursor.execute('DELETE FROM products_details WHERE productid = ?', (product_id,))

            await conn.commit()
    except Exception as e:
        print(f"Ошибка при удалении продукта: {e}")

def update_product_field(product_id, field_name, new_value):
    store_table = ["infoproduct", "price", "photo"]
    store_detail_table = ["category"]

    conn = get_db_connection()

    try:
        if field_name in store_table:
            query = f'UPDATE products_details SET {field_name} = ? WHERE productid = ?'
        elif field_name in store_detail_table:
            query = f'UPDATE collection_products SET {field_name} = ? WHERE productid = ?'
        else:
            raise ValueError(f'Нет такого поля {field_name}')

        conn.execute(query, (new_value, product_id))
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f'Ошибка - {e}')
    finally:
        conn.close()

async def sql_insert_store(name_product, product_id, size, price, photo):
    async with aiosqlite.connect('db_3month/store.sqlite3') as conn:
        cursor = await conn.cursor()
        await cursor.execute(queries.INSERT_STORE, (
            name_product, product_id, size, price, photo
        ))
        await conn.commit()

async def sql_insert_store_detail(info_product, product_id, category):
    async with aiosqlite.connect('db_3month/store.sqlite3') as conn:
        cursor = await conn.cursor()
        await cursor.execute(queries.INSERT_STORE_DETAIL, (
            info_product, product_id, category
        ))
        await conn.commit()

async def sql_create(db=None):
    if db:
        print('База данных подключена!')
    await create_tables()