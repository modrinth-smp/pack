import os

import tomli


def load_mod_set(filename: str) -> set[str]:
    with open(filename) as fp:
        return set(line.rstrip() for line in fp)


ignored_mods = load_mod_set('mods-list/ignored.txt')
library_mods = load_mod_set('mods-list/library.txt')
optimization_mods = load_mod_set('mods-list/optimization-client.txt')

content_mods_text = '## Content Mods\n\n'
library_mods_text = '## Library Mods\n\n'
optimization_mods_text = '## Optimization/Client Mods\n\n'

for filename in os.listdir('mods'):
    if not filename.endswith('.pw.toml'):
        continue
    mod_name = filename.removesuffix('.pw.toml')
    # print(f'Processing {mod_name}...', end=' ')
    if mod_name in ignored_mods:
        # print('Skipped')
        continue
    with open(f'mods/{filename}', 'rb') as fp:
        mod_data = tomli.load(fp)
    mod_text = '  + '
    try:
        update_origin: str = next(iter(mod_data['update']))
        mod_text += f'[{mod_data["name"]}]('
        match update_origin:
            case 'curseforge':
                mod_text += f'https://www.curseforge.com/minecraft/mc-mods/{mod_name}'
            case 'modrinth':
                mod_text += f'https://modrinth.com/mod/{mod_data["update"]["modrinth"]["mod-id"]}'
        mod_text += ')\n'
    except KeyError:
        mod_text += mod_data['name']
    if mod_name in library_mods:
        library_mods_text += mod_text
    elif mod_name in optimization_mods:
        optimization_mods_text += mod_text
    else:
        content_mods_text += mod_text
    # print('Added')

print(content_mods_text)
print(library_mods_text)
print(optimization_mods_text)
