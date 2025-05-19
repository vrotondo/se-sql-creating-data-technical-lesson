import sqlite3
import pandas as pd
import os

# Check if database file exists and remove it if restarting from scratch
# (This is for practice purposes - normally you wouldn't do this in production!)
if os.path.exists('my_db.sqlite'):
    os.remove('my_db.sqlite')
    print("Removed existing database to start fresh.")

# Connect to the database
conn = sqlite3.connect('my_db.sqlite')
cur = conn.cursor()
print("Connected to database successfully.")

# STEP 1: Plan your data structure
# (This is conceptual - no code required)
print("\n--- STEP 1: Planning Data Structure ---")
print("We'll create a users table with id, name, email, and signup_date fields.")

# STEP 2: Create the table
print("\n--- STEP 2: Creating Table ---")
cur.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        signup_date DATE DEFAULT CURRENT_DATE
    );  
""")
print("Users table created successfully.")

# View the table structure
cur.execute("PRAGMA table_info(users);")
table_info = cur.fetchall()
print("\nTable structure:")
for column in table_info:
    print(f"Column: {column[1]}, Type: {column[2]}, Nullable: {not column[3]}, Default: {column[4]}")

# STEP 3: Add data (INSERT)
print("\n--- STEP 3: Adding Data ---")
cur.execute("""
    INSERT INTO users (name, email)
    VALUES 
        ('Sofia Ramirez', 'sofia.ramirez@example.com'),
        ('Devon Blake', 'devon.blake@example.com');
""")
conn.commit()
print("Added initial user data.")

# View the data
cur.execute("SELECT * FROM users;")
users = cur.fetchall()
print("\nCurrent users:")
for user in users:
    print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Signup Date: {user[3]}")

# STEP 4: Modify data (UPDATE)
print("\n--- STEP 4: Modifying Data ---")
cur.execute("""
    UPDATE users
    SET email = 'devon.blake@newdomain.com'
    WHERE email = 'devon.blake@example.com';
""")
conn.commit()
print("Updated Devon's email address.")

# View the updated data
cur.execute("SELECT * FROM users;")
users = cur.fetchall()
print("\nUsers after update:")
for user in users:
    print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Signup Date: {user[3]}")

# STEP 5: Add and then Remove test data (DELETE)
print("\n--- STEP 5: Removing Data ---")

# Add test data
cur.execute("""
    INSERT INTO users (name, email)
    VALUES 
        ('Test User', 'test@test.com');
""")
conn.commit()
print("Added test user.")

# View data with test user
cur.execute("SELECT * FROM users;")
users = cur.fetchall()
print("\nUsers including test user:")
for user in users:
    print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Signup Date: {user[3]}")

# Preview what will be deleted
cur.execute("SELECT * FROM users WHERE name = 'Test User';")
test_users = cur.fetchall()
print("\nUsers that will be deleted:")
for user in test_users:
    print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Signup Date: {user[3]}")

# Delete test user
cur.execute("""
    DELETE FROM users
    WHERE name = 'Test User';
""")
conn.commit()
print("Deleted test user.")

# Verify deletion
cur.execute("SELECT * FROM users;")
users = cur.fetchall()
print("\nFinal users list:")
for user in users:
    print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Signup Date: {user[3]}")

# BONUS: Display data as a pandas DataFrame
print("\n--- BONUS: Displaying Data as DataFrame ---")
df = pd.read_sql_query("SELECT * FROM users", conn)
print(df)

# ALTER TABLE example (commented out by default)
"""
print("\n--- BONUS: Altering Table Structure ---")
cur.execute("ALTER TABLE users ADD COLUMN phone_number TEXT;")
print("Added phone_number column.")

# View updated table structure
cur.execute("PRAGMA table_info(users);")
table_info = cur.fetchall()
print("\nUpdated table structure:")
for column in table_info:
    print(f"Column: {column[1]}, Type: {column[2]}, Nullable: {not column[3]}, Default: {column[4]}")

# Add phone numbers for existing users
cur.execute("UPDATE users SET phone_number = '555-123-4567' WHERE name = 'Sofia Ramirez';")
cur.execute("UPDATE users SET phone_number = '555-987-6543' WHERE name = 'Devon Blake';")
conn.commit()
print("Added phone numbers to existing users.")

# View the updated data
df = pd.read_sql_query("SELECT * FROM users", conn)
print(df)
"""

# DROP TABLE example (commented out by default)
"""
print("\n--- BONUS: Dropping Table ---")
cur.execute("DROP TABLE users;")
print("Users table dropped.")

# Verify table is gone
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
print("Remaining tables:", tables)
"""

# Close connection
conn.close()
print("\nDatabase connection closed.")