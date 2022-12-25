import os
from naevpm import plugin_registry
import xml.etree.cElementTree as ET

PLUGIN_DIR = "plugins"


def list_all_plugins():
    registries = plugin_registry.get_registries_from_database()

    plugins = []

    for registry in registries:
        plugins += all_plugins_in_registry(registry[1])

    for plugin in plugins:
        print(plugin)


def all_xml_files_in_directory(dir: str):
    xmls = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if (file.endswith('.xml')):
                xmls.append(file)
    return xmls


def parse_plugin_xml_file(file):
    tree = ET.parse(file)
    plugin = tree.getroot()
    return {
        "name": plugin.attrib.get("name"),
        "author": plugin.findtext("author"),
        "git": plugin.findtext("git")
    }


def all_plugins_in_registry(registry_dir):
    return [parse_plugin_xml_file(os.path.join(registry_dir, PLUGIN_DIR, xml_file))
            for xml_file in all_xml_files_in_directory(
                os.path.join(registry_dir, PLUGIN_DIR))]
