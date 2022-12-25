import sqlite3
import naevpm.directories

SCHEMA = """
CREATE TABLE IF NOT EXISTS registry (
    clone_url            text,
    repo_path            text
);
"""

def init_database():
    db = sqlite3.connect(naevpm.directories.NaevPMDirectories.DATABASE)
    cur = db.cursor()
    cur.executescript(SCHEMA)
    db.commit()
    db.close()

def check_database():
    naevpm.directories.init_directories()
    init_database()
