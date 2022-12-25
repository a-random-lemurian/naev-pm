import argparse as ap
from sys import stderr
import pygit2 as git
import click
from naevpm.plugin import list_all_plugins

import naevpm.plugin_registry
from naevpm.update import update_registries


@click.group()
def root():
    pass


@root.group()
def registry():
    pass


@registry.command("update")
def registry_update():
    update_registries()


# https://github.com/naev/naev-plugins is the only trusted
# plugin registry. Players are free to add other registries
# but will receive a warning.
TRUSTED = ["https://github.com/naev/naev-plugins"]
UNTRUSTED_WARNING = """\
Warning: Naev does not sandbox any plugin code run on the system. Be careful when installing
unknown plugins, as they may contain malware that could seriously harm your system.

https://github.com/naev/naev-plugins is a curated list, and all plugins submitted there
are subject to manual human review to prevent malicious or offensive plugins.\
"""


@registry.command("add")
@click.argument('clone_url', help="Add a new registry")
def registry_add(clone_url):
    if clone_url not in TRUSTED:
        print(UNTRUSTED_WARNING, file=stderr)

    try:
        naevpm.plugin_registry.add_repository(clone_url)
    except git.GitError as err:
        print(err.with_traceback())
        print(f"Error: Cloning repository \"{clone_url}\" failed.")


@root.group()
def plugin():
    pass


@plugin.command(name='ls', help="List all plugins in all registries installed")
def plugin_ls():
    plugins = list_all_plugins()

    print(f"{'Plugin':<40}{'Author':<30}{'Git URL'}")
    print("-"*100)
    for plugin in plugins:
        print(f"{plugin.get('name'):<40}{plugin.get('author'):<30}{plugin.get('git')}")


if __name__ == '__main__':
    root()
