import os
import pandas as pd
from deep_translator import GoogleTranslator

# --- Configuration ---
SOURCE_COL = 'en'  # The column to translate

def proc_file(file_path, target_lang, translator):
    df = pd.read_csv(file_path, dtype=str, keep_default_na=False)

    # 1. Ensure the target column exists
    if target_lang not in df.columns:
        print(f"missing column {target_lang}")
        return

    # 2. Identify rows that need translation (Source exists AND Target is null)
    mask = (df[SOURCE_COL] != "") & (df[target_lang] == "")

    rows_to_translate = df[mask]

    if rows_to_translate.empty:
        print(f"is complete, not updated")
        return

    print(f"Translating {len(rows_to_translate)} rows...", end="")

    # Convert only the filtered rows to a list
    texts = rows_to_translate[SOURCE_COL].astype(str).tolist()

    # Translate batch
    translated_texts = translator.translate_batch(texts)

    # 3. Use .loc to update ONLY the specific rows that were null
    df.loc[mask, target_lang] = translated_texts

    # Save the updated CSV
    df.to_csv(file_path, index=False)
    print(f"Updated successfully.")

def add_reviewed_column(file_path):
    df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
    if len(df.columns) == 3 and 'reviewed' not in df.columns:
        df['reviewed'] = False
        df.to_csv(file_path, index=False)

def lang_dir_walk(lang_root, desc_str, func):
    for root, _, files in os.walk(lang_root):
        for file in files:
            if not file.endswith('.csv'):
                continue
            file_path = os.path.join(root, file)
            print(f"{desc_str} {file} ", end="")
            try:
                func(file_path)
            except Exception as e:
                print(f"Error {desc_str} {file}: {e}")

def lang_dirs(root):
    dirs = set(os.listdir(root))
    langs = GoogleTranslator().get_supported_languages(as_dict=True).values()

    return dirs.intersection(langs).union({'zh-Hant'})

def proc(root):
    for dir in lang_dirs(root):
        # translator = GoogleTranslator(source=SOURCE_COL, target=target_code)
        lang_dir_walk(root + dir, 'add-rev-col', add_reviewed_column)

if __name__ == "__main__":
    proc('../')