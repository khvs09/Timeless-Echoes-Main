# -*- coding: utf-8 -*-
import sys
from deep_translator import GoogleTranslator

# Ensure console uses UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

def test_translation():
    text = "Hello, how are you?"
    target_lang = "hi"

    print(f"Original text: {text}")
    print(f"Target language: {target_lang}")

    translator = GoogleTranslator(source='auto', target=target_lang)
    translated = translator.translate(text)

    print(f"Translated text: {translated}")

    assert translated is not None
    assert translated != text


if __name__ == "__main__":
    test_translation()
