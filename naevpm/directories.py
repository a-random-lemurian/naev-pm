import appdirs
import os

class NaevPMDirectories:
    ROOT = appdirs.user_data_dir("naev-package-manager")
    DATABASE = os.path.join(ROOT, "naevpm.db")
    REGISTRIES = os.path.join(ROOT, "registries")

def make_registry_directory(name: str):
    return os.path.join(NaevPMDirectories.REGISTRIES, name)

def init_directories():
    os.makedirs(NaevPMDirectories.REGISTRIES, exist_ok=True)
