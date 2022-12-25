import sqlite3
import os
import naevpm.directories

SCHEMA = """
CREATE TABLE IF NOT EXISTS registry (
    clone_url            text,
    repo_path            text
);
"""

def init_database():
    # Don't reinitialize the database if it already exists.
    if os.path.exists(naevpm.directories.NaevPMDirectories.DATABASE):
        return
    db = sqlite3.connect(naevpm.directories.NaevPMDirectories.DATABASE)
    cur = db.cursor()
    cur.executescript(SCHEMA)
    db.commit()
    db.close()

def check_database():
    naevpm.directories.init_directories()
    init_database()
