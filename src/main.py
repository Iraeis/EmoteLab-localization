import os
import pandas as pd

"""
input:
collated csv files (row reference)
ordered dict langlist
dct = {
    lang: translation src,
    ...
}

1. create missing langs based on langlist
2. update rows (strings) based on _collage
3. machine translate missing items based on dct
4. collate, summarize

"""

dct_langs = {
    'zh-Hans': None,  # src lang None indicates manual translation only
    'zh-Hant': 'zh-Hans',
    'de': 'en',
    'es': 'en',
    'fr': 'en',
    'hu': 'en',
    'ja': 'zh-Hans',
    'ko': 'zh-Hans',
    'ru': 'en',
}

class LangDir:
    def __init__(self):
        # load and store a language directory
        raise NotImplementedError

class CSVFile:
    def __init__(self, filepath):
        self.key = 'Key'  # join key
        self.filepath = filepath
        self.df = pd.read_csv(filepath)

    def __repr__(self):
        return f'"{self.filepath.split(os.sep)[-1]}" on key "{self.key}"'

    def write(self):
        self.df.to_csv(self.filepath)

class LanguageCSVFile(CSVFile):
    def update(self):
        # put all rows from reference into csv
        raise NotImplementedError

    def translate(self):
        # machine translate empty
        raise NotImplementedError

class Collator:
    def __init__(self, dct_langs, collage_path):
        # load references (key, en) from collage files
        self.dct_langs = dct_langs
        csvs = self.recursive_csvs(collage_path)
        """
        current patterns: 
        Key, en                         (Main Menu String Table)
        *(wildcard), DisplayName, en    (other; DisplayName is join key)
        """
        self.dct_refs = {filepath.split(os.sep)[-1]: CSVFile(filepath) for filepath in csvs}
        for k, v in self.dct_refs.items():
            col_idx = v.df.columns.get_loc('en')
            self.dct_refs[k].df = v.df.iloc[:, :col_idx]
            if k == "Main Menu String Table.csv":
                self.dct_refs[k].key = "Key"
            else:
                self.dct_refs[k].key = "DisplayName"
        """
        self.dct_langs:     langs: machine translation src
        self.dct_refs:      filename: CSVFile
        """
        # load language files

    def recursive_csvs(self, root):
        lst = []
        for fileroot, _, files in os.walk(root):
            lst += [f"{fileroot}{os.sep}{file}" for file in files if file.endswith('.csv')]
        return lst

    def create_lang_dir(self):
        # create a language directory - copy from another dir
        # rename lang, clear translations, set reviewd col to False
        raise NotImplementedError

    def collate(self):
        # build collage from langauge dirs
        raise NotImplementedError

Collator(dct_langs, f"..{os.sep}_collage")
