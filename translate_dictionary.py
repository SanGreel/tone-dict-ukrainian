import httpcore
import pandas
from googletrans import Translator

DICT_PATH = "emo_dict.csv"
WORDS_COL_NAME = "term"
DICT_COL_SEPARATOR = ","
TRANSLATE_FROM = "ru"
TRANSLATE_TO = "uk"

dict_df = pandas.read_csv(DICT_PATH, sep=";")
translator = Translator()

def translate_word(word, translate_from=TRANSLATE_FROM,
                            translate_to=TRANSLATE_TO):

    translated_word = translator.translate(word, scr=translate_from, dest=translate_to)

    return translated_word.text


last_exec_ind = 0


# TODO: Stops working when computer sleeps
# TODO: Sometimes doesn't translate words (skips them) even though manual translation works

def translate_dictionary(dict_df, start_ind=0):

    try:
        for row_ind, row in dict_df.iloc[start_ind:].iterrows():

            # Write translated dataframe to a file every 100 translated words
            if row_ind % 100 == 0:

                last_exec_ind = row_ind
                print(row_ind)
                dict_df.to_csv(f"tranlated_dict.csv", index=False)

            # Translate the word and replace original
            translated_word = translate_word(dict_df.loc[row_ind, WORDS_COL_NAME])
            dict_df.loc[row_ind, WORDS_COL_NAME] = translated_word

    except httpcore._exceptions.ReadTimeout:
        translate_dictionary(dict_df, last_exec_ind)

translate_dictionary(dict_df, last_exec_ind)





