"""
updates language folder files with any new string entries based on _collage files
for each reference file:
    for each lang:
        add new entries
        get machine translations
for each reference file:
    for each lang:
        stitch back to _collage/
"""

import pandas as pd
import os

from translate import lang_dir_walk, lang_dirs

def proc_collage_file(file_path, langs):
    file_name = os.path.basename(file_path)
    directory = os.sep.join(file_path.split(os.sep)[:-1]) + os.sep

    lang_key = 'Key'
    if file_name in ['Main Menu String Table.csv']:
        src_key = 'Key'
    elif file_name.split('.')[0] in ['CoffeeBean']:
        src_key = 'DisplayName'
    else:
        raise Exception(f'{__file__}: unrecognized file name pattern')

    df_source = pd.read_csv(file_path)[[src_key, 'en']]

    for lang in langs:
        lang_fname = file_name[:-4] + f'_{lang}.csv'
        lang_dir = directory.replace(f'{os.sep}_collage{os.sep}', f'{os.sep}{lang}{os.sep}')
        lang_file = f'{lang_dir}{os.sep}{lang_fname}'
        df_lang = pd.read_csv(lang_file)

        df_new = df_source[~df_source[src_key].isin(df_lang[lang_key])]
        df_new = df_new.rename(columns={src_key: lang_key})
        df_lang = pd.concat([df_lang, df_new], ignore_index=True)
        df_lang['reviewed'] = df_lang['reviewed'].fillna(False)
        df_lang.to_csv(lang_file, index=False)

def proc(root):
    langs = lang_dirs(root)
    lang_dir_walk(root + '_collage', __file__, lambda x: proc_collage_file(x, langs))

if __name__ == "__main__":
    proc(f'..{os.sep}')

