from yaml import load, dump, SafeLoader
from os.path import exists
from os import makedirs

if not exists('build'): makedirs('build')

with open('rime-middle-chinese.yaml') as f:
    CONFIG = load(f, Loader=SafeLoader)

ALGEBRA = CONFIG['algebra']
PREEDIT_FORMAT = CONFIG['preedit_format']
TONE = CONFIG['tone']

with open('build/sampheng.custom.yaml', 'w') as f:
    f.write('patch:\n')
    f.write('  speller/alphabet: ;zyxwvutsrqponmlkjihgfedcba\n')

    f.write('  speller/algebra:\n')
    algebra = ''
    for s1, s2 in ALGEBRA['special_syllable'] + ALGEBRA['preprocessing'] + ALGEBRA[1] + ALGEBRA[3] + ALGEBRA[2]+ ALGEBRA['postprocessing']:
        algebra += f'    - xform/{s1}/{s2}/\n'
    algebra += '    - xlit/ABCDEFGHIJKLMNOPQRSTUVWXYZ/abcdefghijklmnopqrstuvwxyz/\n'
    f.write(algebra)
    f.write('    - abbrev/^([a-z;]).+$/$1/\n')

    f.write('  translator/preedit_format:\n')
    preedit = ''
    for s1, s2 in PREEDIT_FORMAT[3] + PREEDIT_FORMAT[1] + PREEDIT_FORMAT[2]:
        preedit += f'    - xform/{s1}/{s2}/\n'
    preedit += '    - xform/平//\n'
    preedit += '    - xform/([祭泰夬废])去/$1/\n'
    for key, value in TONE.items():
        preedit += f'    - xform/{key}上/{value[0]}/\n'
        preedit += f'    - xform/{key}去/{value[1]}/\n'
        if len(value) == 3:
            preedit += f'    - xform/{key}入/{value[2]}/\n'
    f.write(preedit)

    f.write('  reverse_lookup/comment_format:\n')
    f.write(algebra)
    f.write(preedit)
