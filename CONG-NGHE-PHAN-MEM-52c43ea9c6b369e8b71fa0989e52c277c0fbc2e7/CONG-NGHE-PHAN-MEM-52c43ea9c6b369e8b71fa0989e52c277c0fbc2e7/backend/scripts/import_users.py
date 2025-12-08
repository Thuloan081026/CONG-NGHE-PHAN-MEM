"""
Simple CSV importer to create users in the local database.

CSV columns: email,full_name,password,role

Usage:
    python import_users.py path/to/users.csv
"""
import sys
import csv
from pathlib import Path

from app.core.database import SessionLocal, engine, Base
from app.services.user_service import import_users_from_list


def main(csv_path: str):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    rows = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    created = import_users_from_list(db, rows)
    print(f"Created {len(created)} users")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python import_users.py users.csv")
        sys.exit(1)
    path = sys.argv[1]
    if not Path(path).exists():
        print("CSV file not found:", path)
        sys.exit(1)
    main(path)
