import json

class ParseModlist:
    def __init__(self, modlist):
        with open(modlist, 'r') as file:
            self.modlist = json.load(file)

    def get_links(self):
        links = []
        for mod in self.modlist["mods"]:
            links.append(mod["download_link"])
        return links

    def get_names(self):
        names = []
        for mod in self.modlist["mods"]:
            names.append(mod["name"])
        return names

    def get_list(self):
        return self.modlist

    def gen_modlist_file(self):
        lines = ["# This file was automatically generated by Mod Organizer."]
        for mod in self.modlist["mods"]:
            if mod["enabled"]:
                lines.append(f"+{mod['name']}")
            else:
                lines.append(f"-{mod['name']}")
        return "\n".join(lines)