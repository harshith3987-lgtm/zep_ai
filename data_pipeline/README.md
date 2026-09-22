# Module 1: Data Pipeline & Relational Storage

## 1. Overview & Architecture

This module implements an automated data ingestion, cleaning, and relational storage pipeline simulating Zepto's product catalog extraction. 

The pipeline performs three main operations:
1. Scrapes raw book catalog data across three distinct categories (*Mystery*, *Fantasy*, *Fiction*) from `books.toscrape.com`.
2. Cleans prices, standardizes ratings, converts currencies, and checks data types.
3. Loads the structured data into a normalized SQLite database enforcing third normal form (3NF) relational constraints.

### End-to-End Pipeline Flow

```text
+-------------------------------------------------------------+
|                    STEP 1: WEB SCRAPING                     |
|                                                             |
|  books.toscrape.com (Categories: Mystery, Fantasy, Fiction) |
|                              |                              |
|                              v                              |
|                   data_pipeline/scraper.py                  |
|                              |                              |
|                              v                              |
|               data/raw_scraped_books.json                   |
|                   (145 Raw JSON Records)                    |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|              STEP 2: TRANSFORMATION & LOADING               |
|                                                             |
|                data_pipeline/clean_and_load.py              |
|                                                             |
|  * Clean £ symbols -> Cast price to Float                   |
|  * Multiply by 105.00 -> Generate INR Price                 |
|  * Map words ('One'..'Five') -> Integer Ratings (1..5)      |
|  * Map stock strings -> Binary Flags (1 / 0)                |
|                              |                              |
|                              v                              |
|                     data_pipeline/schema.sql                |
|               (Applies 3NF Relational Structure)            |
|                              |                              |
|                              v                              |
|                   data/books_catalog.db                     |
|        [categories Table] <---> [books Table]               |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|             STEP 3: ANALYTICS & INTEGRITY AUDIT             |
|                                                             |
|  1. Execute 5 Analytical SQL Business Queries               |
|  2. Execute Pandas Inner Join Verification                   |
|  3. Run Assertions (0 Missing Values, 0 Orphan Foreign Keys)|
+-------------------------------------------------------------+
```

---

## 2. Relational Schema Design (3NF)

The schema is defined in `schema.sql` and separates repeating categorical text into a dedicated entity to eliminate redundancy:

### Table: `categories`
- `category_id` (INTEGER, Primary Key, Autoincrement) — Unique identifier for each category.
- `category_name` (TEXT, Unique, Not Null) — Standardized category name.

### Table: `books`
- `book_id` (INTEGER, Primary Key, Autoincrement) — Unique identifier for each book record.
- `title` (TEXT, Not Null) — Title of the book.
- `price_gbp` (REAL, Not Null) — Cleaned price in British Pounds (£).
- `price_inr` (REAL, Not Null) — Calculated price in Indian Rupees (₹) using a baseline conversion rate (1 GBP = 105.00 INR).
- `rating` (INTEGER, 1 to 5) — Star rating converted to a numerical value.
- `in_stock` (INTEGER, 0 or 1) — Availability indicator (1 = In Stock, 0 = Out of Stock).
- `category_id` (INTEGER, Foreign Key) — References `categories(category_id)`.

---

## 3. Data Cleaning & Transformations

During the `clean_and_load.py` execution, the following data cleaning operations are performed:

1. **Currency Normalization:** Stripped currency characters (`£`) and parsed numeric floating-point values from raw price strings.
2. **Rating Conversion:** Mapped text ratings (`One`, `Two`, `Three`, `Four`, `Five`) into numeric integers from 1 to 5.
3. **Availability Parsing:** Checked stock strings to assign a binary `1` (in stock) or `0` (out of stock).
4. **Currency Exchange Calculation:** Calculated `price_inr` using a constant exchange rate of 105.00 INR per GBP, rounded to two decimal places.
5. **Relational Ingestion:** Populated the `categories` lookup table first, mapped foreign keys dynamically, and inserted book records without orphan rows.

---

## 4. Analytical SQL Queries & Findings

Five analytical SQL queries were executed against `books_catalog.db` to inspect the catalog:

### Query 1: Book Count and Average Price per Category
- **Fantasy:** 48 books | Average Price: £39.59 (₹4,157.37)
- **Fiction:** 65 books | Average Price: £36.07 (₹3,786.99)
- **Mystery:** 32 books | Average Price: £31.72 (₹3,330.50)

### Query 2: Top 5 Most Expensive Books
1. *Last One Home (New Beginnings #1)* — Fiction | £59.98 (₹6,297.90) | Rating: 3/5
2. *Boar Island (Anna Pigeon #19)* — Mystery | £59.48 (₹6,245.40) | Rating: 3/5
3. *The Improbability of Love* — Fiction | £59.45 (₹6,242.25) | Rating: 1/5
4. *Myriad (Prentor #1)* — Fantasy | £58.75 (₹6,168.75) | Rating: 4/5
5. *The Rose & the Dagger (The Wrath and the Dawn #2)* — Fantasy | £58.64 (₹6,157.20) | Rating: 4/5

### Query 3: Star Rating Distribution
- **5 Stars:** 32 books (22.07%)
- **4 Stars:** 28 books (19.31%)
- **3 Stars:** 36 books (24.83%)
- **2 Stars:** 20 books (13.79%)
- **1 Star:** 29 books (20.00%)

### Query 4: Total In-Stock Catalog Valuation
- **Total Units in Stock:** 145 books
- **Total Valuation (GBP):** £5,259.85
- **Total Valuation (INR):** ₹552,284.25

### Query 5: Category Ranking by Average Star Rating
1. **Fiction:** 3.18 / 5.0 (65 books)
2. **Fantasy:** 3.08 / 5.0 (48 books)
3. **Mystery:** 2.94 / 5.0 (32 books)

---

## 5. Verification & Data Integrity

The pipeline includes automated verification steps using `pandas`:
- **Foreign Key Check:** An inner join on `category_id` confirms all 145 books map directly to a valid category with zero null entries.
- **Value Constraints:** Assertions verify that all ratings are between 1 and 5, and that no calculated prices are missing or negative.

---

## 6. How to Run

To run this pipeline from the repository root:

```bash
# Step 1: Scrape raw catalog data
python data_pipeline/scraper.py

# Step 2: Clean, populate database, run SQL queries, and verify
python data_pipeline/clean_and_load.py
```