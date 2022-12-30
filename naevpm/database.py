import sqlite3
import os
import naevpm.directories

SCHEMA = """
CREATE TABLE IF NOT EXISTS registry (
    registry_id          integer primary key
    clone_url            text,
    repo_path            text
);
CREATE TABLE IF NOT EXISTS keyval (
    key                  text,
    value                any
);
CREATE TABLE IF NOT EXISTS plugin (
    plugin_id            integer primary key,
    name                 text,
    author               text,
    license              text,
    website              text,
    git                  text,
    directory            text,
    installed            text
);
"""

db = sqlite3.connect(naevpm.directories.NaevPMDirectories.DATABASE)

def init_database():
    # Don't reinitialize the database if it already exists.
    if os.path.exists(naevpm.directories.NaevPMDirectories.DATABASE):
        return
    cur = db.cursor()
    cur.executescript(SCHEMA)
    db.commit()
    db.close()


def check_database():
    naevpm.directories.init_directories()
    init_database()


def add_plugin_to_database(plugin, commit=True):
    cur = db.cursor()
    cur.execute("""SELECT * FROM plugin WHERE name = ?""", [plugin.get("name")])
    if cur.fetchone() is not None:
        return
    cur.execute("""
        INSERT INTO plugin (name, author, license, website,
                            git, directory, installed)
        VALUES             (?,?,?,?,?,?,?);
        """,
        [
            plugin.get("name"),
            plugin.get("author"),
            plugin.get("git"),
            plugin.get("license"),
            plugin.get("website"),
            None,
            False
        ]
    )

    if commit:
        db.commit()
    pass


def set_plugin_install_status(plugin, status):
    cur = db.cursor()
    cur.execute("""UPDATE plugin SET installed = ? WHERE name = ?""", [
        status,
        plugin.get("name")
    ])


def get_plugin_install_status(plugin):
    cur = db.cursor()
    cur.execute("""SELECT installed FROM plugin WHERE name = ?""", [
        plugin.get("name")
    ])
    return cur.fetchone()[0]


def plugin_set_install_directory(plugin, directory):
    cur = db.cursor()
    cur.execute("""SELECT installed FROM plugin WHERE name = ?""", [
        plugin.get("name")
    ])
    db.commit()


def set_key(key: str, val):
    cur = db.cursor()
    if get_key(key) is None:
        cur.execute("INSERT INTO keyval VALUES (?,?)", [key, val])
    else:
        cur.execute("UPDATE keyval SET value = ? WHERE key = ?", [val, key])
    db.commit()


def get_key(key: str):
    cur = db.cursor()
    cur.execute("SELECT * FROM keyval WHERE key = ?", [key,])
    results = cur.fetchone()
    if results is None:
        return None
    return results[1]
