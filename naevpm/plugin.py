import os
from naevpm import database, plugin_registry
import lxml.etree as etree

PLUGIN_DIR = "plugins"


def list_all_plugins():
    registries = plugin_registry.get_registries_from_database()

    plugins = []

    for registry in registries:
        plugins += all_plugins_in_registry(registry[1])

    return plugins


def update_plugin_list(plugins):
    for plugin in plugins:
        database.add_plugin_to_database(plugin)


def all_xml_files_in_directory(dir: str):
    xmls = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if (file.endswith('.xml')):
                xmls.append(file)
    return xmls


def parse_plugin_xml_file(file):
    plugin = etree.XML(open(file).read().encode())
    return {
        "name": plugin.get("name"),
        "author": plugin.findtext("author"),
        "git": plugin.findtext("git"),
        "license": plugin.findtext("license"),
        "website": plugin.findtext("website")
    }


def all_plugins_in_registry(registry_dir):
    return [parse_plugin_xml_file(os.path.join(registry_dir, PLUGIN_DIR, xml_file))
            for xml_file in all_xml_files_in_directory(
                os.path.join(registry_dir, PLUGIN_DIR))]


def install_plugin():
    pass
