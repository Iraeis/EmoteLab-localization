import pandas as pd

from translate import lang_dir_walk, lang_dirs

dct_rev = {}
dct_all = {}

def summarize(file_path, lang_code):
    df = pd.read_csv(file_path, keep_default_na=False)
    dct_rev[lang_code] += df.loc[:, 'reviewed'].sum()
    dct_all[lang_code] += len(df)


def proc(root, target_lang):
    print(f"{target_lang:10}: ", end="")
    dct_rev[target_lang] = 0
    dct_all[target_lang] = 0
    lang_dir_walk(root + target_lang, 'new-lang', lambda x: summarize(x, target_lang))
    print(f"{dct_rev[target_lang]/dct_all[target_lang]*100:4.1f}%")

if __name__ == "__main__":
    [proc('../', x) for x in lang_dirs('../')]
    print('')
