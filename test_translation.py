from deep_translator import GoogleTranslator

def test_translation():
    try:
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
        return True
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    test_translation() 