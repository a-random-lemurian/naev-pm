from dataclasses import dataclass
import sqlite3
import pygit2 as git
from naevpm.database import check_database
from naevpm.directories import NaevPMDirectories, make_registry_directory


class NaevPMRemoteCallbacks(git.RemoteCallbacks):
    def transfer_progress(self, stats):
        print(
            f'Cloning... {stats.indexed_objects} of {stats.total_objects} objects so far')


def add_repository(clone_url: str):
    registry_directory = make_registry_directory(clone_url.split('/')[-1])
    repo = git.clone_repository(
        clone_url, registry_directory)
    add_registry_to_database(clone_url, registry_directory)


def add_registry_to_database(clone_url, directory: str):
    check_database()
    db = sqlite3.connect(NaevPMDirectories.DATABASE)
    cur = db.cursor()
    cur.execute("""INSERT INTO registry (clone_url, repo_path) VALUES (?,?)""", [
        clone_url, directory
    ])
    db.commit()
    db.close()


def get_registries_from_database():
    check_database()
    db = sqlite3.connect(NaevPMDirectories.DATABASE)
    cur = db.cursor()
    cur.execute("SELECT * FROM registry")
    return cur.fetchall()
