from deep_translator import GoogleTranslator

def test_translation():
    # Test text
    text = "Hello, how are you?"
    target_lang = "hi"

    print(f"Original text: {text}")
    print(f"Target language: {target_lang}")

    # Create translator instance
    translator = GoogleTranslator(source='auto', target=target_lang)

    # Translate
    translated = translator.translate(text)

    print(f"Translated text: {translated}")

    # Assertions (pytest will fail the test if these are false)
    assert translated is not None
    assert translated != text  # ensures translation actually changed text


if __name__ == "__main__":
    # For manual local runs (not needed by pytest, but useful if you just run the file)
    test_translation()
