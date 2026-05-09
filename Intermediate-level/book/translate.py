
import translators as ts
import sys

def translate_text(text, dest_lang):
    return ts.translate_text(text, to_language=dest_lang)

if __name__ == "__main__":
    text_to_translate = sys.argv[1]
    destination_language = sys.argv[2]
    translated_text = translate_text(text_to_translate, destination_language)
    print(translated_text)
