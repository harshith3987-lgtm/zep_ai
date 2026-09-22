import os
import re
import json
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_JSON = os.path.join(DATA_DIR, 'raw_scraped_books.json')
DB_PATH = os.path.join(DATA_DIR, 'books_catalog.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'schema.sql')

GBP_TO_INR_RATE = 105.0

RATING_MAP = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}

def clean_price(price_raw):
    """Strips currency symbols and converts to float."""
    match = re.search(r'[\d.]+', price_raw)
    return float(match.group(0)) if match else 0.0

def clean_rating(rating_str):
    """Maps star-rating word to integer (1-5)."""
    return RATING_MAP.get(rating_str.strip().capitalize(), 0)

def clean_stock(stock_str):
    """Converts availability text to binary indicator (1/0)."""
    return 1 if 'in stock' in stock_str.lower() else 0

def init_db(conn):
    """Executes schema.sql to initialize normalized tables."""
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)

def load_data():
    if not os.path.exists(RAW_JSON):
        raise FileNotFoundError(f"Raw data not found at {RAW_JSON}. Run scraper.py first.")

    with open(RAW_JSON, 'r', encoding='utf-8') as f:
        raw_books = json.load(f)

    # Remove existing DB if fresh reload
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    init_db(conn)

    # 1. Populate categories table uniquely
    categories = sorted(list(set(b['category'] for b in raw_books)))
    category_id_map = {}
    for cat in categories:
        cursor.execute("INSERT INTO categories (category_name) VALUES (?)", (cat,))
        category_id_map[cat] = cursor.lastrowid

    # 2. Clean and populate books table
    cleaned_rows = []
    for b in raw_books:
        title = b['title'].strip()
        price_gbp = clean_price(b['price_raw'])
        price_inr = round(price_gbp * GBP_TO_INR_RATE, 2)
        rating = clean_rating(b['star_rating_text'])
        in_stock = clean_stock(b['availability_text'])
        cat_id = category_id_map[b['category']]

        cleaned_rows.append((title, price_gbp, price_inr, rating, in_stock, cat_id))

    cursor.executemany(
        """
        INSERT INTO books (title, price_gbp, price_inr, rating, in_stock, category_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        cleaned_rows
    )
    conn.commit()
    print(f"[✓] Successfully inserted {len(cleaned_rows)} cleaned records into {DB_PATH}\n")

    return conn

def run_analytical_queries(conn):
    print("=" * 65)
    print("EXECUTING 5 ANALYTICAL SQL QUERIES")
    print("=" * 65)

    # Query 1: Book count and average price per category
    q1 = """
    SELECT c.category_name, COUNT(b.book_id) AS total_books, 
           ROUND(AVG(b.price_gbp), 2) AS avg_price_gbp,
           ROUND(AVG(b.price_inr), 2) AS avg_price_inr
    FROM categories c
    JOIN books b ON c.category_id = b.category_id
    GROUP BY c.category_name;
    """
    print("\n--- Query 1: Book Count & Average Price by Category ---")
    print(pd.read_sql_query(q1, conn).to_string(index=False))

    # Query 2: Top 5 most expensive books
    q2 = """
    SELECT b.title, c.category_name, b.price_gbp, b.price_inr, b.rating
    FROM books b
    JOIN categories c ON b.category_id = c.category_id
    ORDER BY b.price_gbp DESC
    LIMIT 5;
    """
    print("\n--- Query 2: Top 5 Most Expensive Books ---")
    print(pd.read_sql_query(q2, conn).to_string(index=False))

    # Query 3: Star rating distribution
    q3 = """
    SELECT rating, COUNT(*) AS count,
           ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM books), 2) AS percentage
    FROM books
    GROUP BY rating
    ORDER BY rating DESC;
    """
    print("\n--- Query 3: Star Rating Distribution ---")
    print(pd.read_sql_query(q3, conn).to_string(index=False))

    # Query 4: Total catalog inventory valuation
    q4 = """
    SELECT COUNT(*) AS total_inventory_units,
           ROUND(SUM(price_gbp), 2) AS total_valuation_gbp,
           ROUND(SUM(price_inr), 2) AS total_valuation_inr
    FROM books
    WHERE in_stock = 1;
    """
    print("\n--- Query 4: Total Catalog Valuation (In-Stock) ---")
    print(pd.read_sql_query(q4, conn).to_string(index=False))

    # Query 5: Categories ranked by average star rating
    q5 = """
    SELECT c.category_name, ROUND(AVG(b.rating), 2) AS avg_rating, COUNT(b.book_id) AS book_count
    FROM categories c
    JOIN books b ON c.category_id = b.category_id
    GROUP BY c.category_name
    ORDER BY avg_rating DESC;
    """
    print("\n--- Query 5: Categories Ranked by Average Star Rating ---")
    print(pd.read_sql_query(q5, conn).to_string(index=False))

def verify_with_pandas(conn):
    print("\n" + "=" * 65)
    print("PANDAS MERGE & FOREIGN KEY INTEGRITY VERIFICATION")
    print("=" * 65)
    df_books = pd.read_sql_query("SELECT * FROM books", conn)
    df_cats = pd.read_sql_query("SELECT * FROM categories", conn)

    merged = pd.merge(df_books, df_cats, on="category_id", how="inner")
    
    # Assertions for rubric verification
    assert len(merged) == len(df_books), "Foreign key mismatch detected!"
    assert merged['price_inr'].isna().sum() == 0, "Missing price calculations!"
    assert (merged['rating'].between(1, 5)).all(), "Invalid rating values found!"

    print(f"[✓] Integrity check passed: {len(merged)} records merged cleanly without orphan rows.")
    print(f"[✓] Sample validated record:\n    Title: '{merged.iloc[0]['title']}' | Category: '{merged.iloc[0]['category_name']}' | £{merged.iloc[0]['price_gbp']} (₹{merged.iloc[0]['price_inr']}) | Rating: {merged.iloc[0]['rating']}/5")

if __name__ == '__main__':
    connection = load_data()
    run_analytical_queries(connection)
    verify_with_pandas(connection)
    connection.close()