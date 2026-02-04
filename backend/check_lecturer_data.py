#!/usr/bin/env python
"""Check lecturer and syllabus data"""
from app.core.database import SessionLocal
from app.models.syllabus import Syllabus
from app.models.user import User

db = SessionLocal()

print("\n=== LECTURERS ===")
lecturers = db.query(User).filter(User.role == 'lecturer').all()
for l in lecturers:
    print(f"ID: {l.id}, Email: {l.email}, Name: {l.full_name}")

print("\n=== SYLLABUSES ===")
syllabuses = db.query(Syllabus).all()
for s in syllabuses[:15]:
    creator = db.query(User).filter(User.id == s.created_by).first()
    creator_email = creator.email if creator else "NOT FOUND"
    print(f"ID: {s.id}, Code: {s.subject_code}, Status: {s.status}, Created By: {s.created_by} ({creator_email})")

print("\n=== SYLLABUSES FOR EACH LECTURER ===")
for l in lecturers:
    count = db.query(Syllabus).filter(Syllabus.created_by == l.id).count()
    print(f"{l.full_name} ({l.email}): {count} syllabuses")
    syllabuses_for_lecturer = db.query(Syllabus).filter(Syllabus.created_by == l.id).all()
    for s in syllabuses_for_lecturer[:3]:
        print(f"  - {s.subject_code}: {s.subject_name}")

db.close()
