import pandas as pd
import os

from translate import lang_dir_walk, lang_dirs

def proc_collage_file(file_path, langs):
    file_name = file_path.split(os.sep)[-1]
    directory = os.sep.join(file_path.split(os.sep)[:-1]) + os.sep
    right_key = 'Key'

    if file_name in ['Main Menu String Table.csv']:
        left_key = 'Key'
    elif file_name.split('.')[0] in ['CoffeeBean']:
        left_key = 'DisplayName'
    else:
        raise Exception(f'{__file__}: unrecognized file name pattern')

    df = pd.read_csv(file_path)
    df = df.loc[:, :'en']  # keep all columns left of and including 'en'

    for lang in langs:
        lang_fname = file_name[:-4] + f'_{lang}.csv'
        lang_dir = directory.replace(f'{os.sep}_collage{os.sep}', f'{os.sep}{lang}{os.sep}')
        df_lang = pd.read_csv(f'{lang_dir}{os.sep}{lang_fname}').loc[:, [right_key, lang]]

        if left_key != right_key:
            df = pd.merge(df, df_lang, left_on=left_key, right_on=right_key, how='left').drop(columns=[right_key])
        else:
            df = pd.merge(df, df_lang, on=left_key, how='left')


    df.to_csv(file_path, index=False)

def proc(root):
    langs = lang_dirs(root)
    lang_dir_walk(root + '_collage', __file__, lambda x: proc_collage_file(x, langs))

if __name__ == "__main__":
    proc(f'..{os.sep}')

# summary
# above threshold pct, add column - no manual so nothing gets removed
# collage folder next to languages - has same format as final - need zh-Hans as a language folder
