import argparse as ap
from datetime import datetime
from sys import stderr
import pygit2 as git
import click
from naevpm.database import get_key
from naevpm.plugin import install_plugin, list_all_plugins

import naevpm.plugin_registry
from naevpm.update import update_registries


def reminders():
    registry_update_reminder()


def registry_update_reminder():
    # Remind the player to update their registries once in a while.
    last_update_timestamp = get_key("last_registry_update_time")
    if last_update_timestamp is None:
        return
    now = datetime.now()
    last_update_time = datetime.fromisoformat(last_update_timestamp)
    delta = now - last_update_time

    if delta.days >= 7:
        print("It has been more than 7 days since you last updated your local package registry.")
        print("To update, run naevpm registry update. Updating is recommended to keep")
        print("up to date on the latest plugins for Naev.")


@click.group()
def root():
    reminders()


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
@click.argument('clone_url')
def registry_add(clone_url):
    """"Add a new registry"""
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


@plugin.command(name='ls')
def plugin_ls():
    """List all plugins in all registries installed"""
    plugins = list_all_plugins()

    print(f"{'Plugin':<40}{'Author':<30}{'Git URL'}")
    print("-"*100)
    for plugin in plugins:
        print(f"{plugin.get('name'):<40}{plugin.get('author'):<30}{plugin.get('git')}")


@plugin.command(name='install')
@click.argument("plugin_name")
def plugin_install(plugin_name):
    """Install a plugin"""
    plugins = list_all_plugins()

    for plugin in plugins:
        if plugin_name.lower() in plugin.get("name").lower():
            print("Install "+plugin.get("name")+" by "+plugin.get("author")+"? (y/n) ",end='')
            if input()[0].lower().strip() == 'y':
                print("Installing...")
                install_plugin(plugin)
                exit(0)


if __name__ == '__main__':
    root()
