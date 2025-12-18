#!/usr/bin/env python3
"""
Script migrate data từ SQLite sang MySQL
Chạy sau khi setup MySQL database
"""

import sqlite3
import pymysql
from contextlib import contextmanager

# SQLite connection
SQLITE_DB = "database.db"  # Thay đổi path nếu cần

# MySQL connection
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'syllabus_db',
    'port': 3306,
    'charset': 'utf8mb4'
}

@contextmanager
def sqlite_connection():
    """Context manager cho SQLite connection"""
    conn = sqlite3.connect(SQLITE_DB)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def mysql_connection():
    """Context manager cho MySQL connection"""
    conn = pymysql.connect(**MYSQL_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

def get_sqlite_tables():
    """Lấy danh sách tables từ SQLite"""
    with sqlite_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        return [row[0] for row in cursor.fetchall()]

def migrate_table(table_name):
    """Migrate một table từ SQLite sang MySQL"""
    print(f"📋 Migrating table: {table_name}")

    try:
        # Lấy data từ SQLite
        with sqlite_connection() as sqlite_conn:
            cursor = sqlite_conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

        if not rows:
            print(f"   ⚠️  Table {table_name} is empty, skipping...")
            return True

        # Insert vào MySQL
        with mysql_connection() as mysql_conn:
            with mysql_conn.cursor() as cursor:
                # Tạo placeholders cho INSERT
                placeholders = ', '.join(['%s'] * len(columns))
                columns_str = ', '.join(columns)
                insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

                # Insert từng row
                for row in rows:
                    values = tuple(row)
                    cursor.execute(insert_sql, values)

            mysql_conn.commit()

        print(f"   ✅ Migrated {len(rows)} rows")
        return True

    except Exception as e:
        print(f"   ❌ Error migrating {table_name}: {e}")
        return False

def main():
    print("🚀 Starting data migration from SQLite to MySQL...")

    # Kiểm tra SQLite database
    try:
        with sqlite_connection() as conn:
            pass
    except sqlite3.Error as e:
        print(f"❌ Cannot connect to SQLite database: {e}")
        return

    # Kiểm tra MySQL database
    try:
        with mysql_connection() as conn:
            pass
    except pymysql.Error as e:
        print(f"❌ Cannot connect to MySQL database: {e}")
        return

    # Lấy danh sách tables
    tables = get_sqlite_tables()
    if not tables:
        print("⚠️  No tables found in SQLite database")
        return

    print(f"📋 Found {len(tables)} tables: {', '.join(tables)}")

    # Migrate từng table
    success_count = 0
    for table in tables:
        if migrate_table(table):
            success_count += 1

    print(f"\n🎉 Migration completed! {success_count}/{len(tables)} tables migrated successfully")

    if success_count == len(tables):
        print("💡 You can now delete the SQLite database file if migration was successful")
    else:
        print("⚠️  Some tables failed to migrate. Please check the errors above.")

if __name__ == "__main__":
    main()