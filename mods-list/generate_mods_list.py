import os
from typing import Any

import tomli


def load_mod_set(filename: str) -> set[str]:
    with open(filename) as fp:
        return set(line.rstrip() for line in fp)


ignored_mods = load_mod_set('mods-list/ignored.txt')
library_mods = load_mod_set('mods-list/library.txt')
optimization_mods = load_mod_set('mods-list/optimization-client.txt')

with open('mods-list/extra_meta.toml', 'rb') as fp:
    extra_meta = tomli.load(fp)

content_mods_text = '## Content Mods\n\n'
library_mods_text = '## Library Mods\n\n'
optimization_mods_text = '## Optimization/Client Mods\n\n'

for filename in sorted(os.listdir('mods')):
    mod_name = filename.removesuffix('.pw.toml').removesuffix('.jar')
    # print(f'Processing {mod_name}...', end=' ')
    if mod_name in ignored_mods:
        # print('Skipped')
        continue
    url: str | None = None
    if filename.endswith('.pw.toml'):
        with open(f'mods/{filename}', 'rb') as fp:
            mod_data = tomli.load(fp)
        friendly_name: str = mod_data['name']
        try:
            update_origin: str = next(iter(mod_data['update']))
            match update_origin:
                case 'curseforge':
                    url = f'https://www.curseforge.com/minecraft/mc-mods/{mod_name}'
                case 'modrinth':
                    url = f'https://modrinth.com/mod/{mod_data["update"]["modrinth"]["mod-id"]}'
        except KeyError:
            pass
    else:
        friendly_name = mod_name
    if mod_name in extra_meta:
        mod_extra_meta: dict[str, str] = extra_meta[mod_name]
        friendly_name = mod_extra_meta['name']
        url = mod_extra_meta['url']
    mod_text = '  + '
    if url is None:
        mod_text += friendly_name
    else:
        mod_text += f'[{friendly_name}]({url})'
    mod_text += '\n'
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
