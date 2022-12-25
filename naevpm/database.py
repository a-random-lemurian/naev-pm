import sqlite3
import os
import naevpm.directories

SCHEMA = """
CREATE TABLE IF NOT EXISTS registry (
    clone_url            text,
    repo_path            text
);
CREATE TABLE IF NOT EXISTS keyval (
    key                  text,
    value                any
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


def set_key(key: str, val):
    db = sqlite3.connect(naevpm.directories.NaevPMDirectories.DATABASE)
    cur = db.cursor()
    if get_key(key) is None:
        cur.execute("UPDATE keyval SET value = ? WHERE key = ?", [val, key])
    else:
        cur.execute("INSERT INTO keyval VALUES (?,?)", [key, val])
    db.commit()
    db.close()


def get_key(key: str):
    db = sqlite3.connect(naevpm.directories.NaevPMDirectories.DATABASE)
    cur = db.cursor()
    cur.execute("SELECT * FROM keyval WHERE key = ?", [key,])
    results = cur.fetchone()
    db.close()
    if results is None:
        return None
    return results[1]
