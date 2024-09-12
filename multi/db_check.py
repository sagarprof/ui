import sqlite3

# Connect to the database file
conn = sqlite3.connect(r'D:\citi\ui\multi\.langchain_cache.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Execute a query to fetch table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables:", tables)

# full_llm_cache
# full_md5_llm_cache
# checking table schema

cursor.execute("PRAGMA table_info(full_md5_llm_cache);")
print('table info of full_md5_llm_cache :')
schema = cursor.fetchall()
for column in schema:
    print(column)

cursor.execute("PRAGMA table_info(full_llm_cache);")
print(f'\n table info of full_llm_cache :')
schema = cursor.fetchall()
for column in schema:
    print(column)

cursor.execute("SELECT COUNT(*) FROM full_llm_cache;")
count = cursor.fetchone()[0]
print(f"\n Number of rows in 'full_md5_llm_cache': {count}")



try:
    cursor.execute("SELECT * FROM full_llm_cache LIMIT 10;")
    rows = cursor.fetchall()
    if not rows:
        print("No data found in 'full_llm_cache'.")
    for row in rows:
        print(row)
except sqlite3.Error as e:
    print(f"An error occurred: {e}")


# # Close the connection
conn.close()
