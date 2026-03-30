import os

from translate import lang_dir_walk, lang_dirs

def action(file_path, target_lang):
    file_name = file_path.split(os.sep)[-1]
    folder = os.sep.join(file_path.split(os.sep)[:-1])
    gsrc_name = "CoffeeBean.ColorGroups.csv"
    gdst_name = "CoffeeBean.SlotGroups.csv"
    if file_name == f"{gsrc_name[:-4]}_{target_lang}.csv":
        dst_name = f"{gdst_name[:-4]}_{target_lang}.csv"
        os.rename(file_path, f"{folder}{os.sep}{dst_name}")

def proc(root, target_lang):
    lang_dir_walk(root + target_lang, 'new-lang', lambda x: action(x, target_lang))

if __name__ == "__main__":
    [proc('../', x) for x in lang_dirs('../')]