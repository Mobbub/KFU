def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_language(text, en_words, rus_words):
    en_count = sum(word in text for word in en_words)
    rus_count = sum(word in text for word in rus_words)
    return 'EN' if en_count > rus_count else 'RUS'

train_en_text = load_text('trainEN.txt')
train_rus_text = load_text('trainRUS.txt')
input_text = load_text('input.txt')

en_words = set(train_en_text.split())
rus_words = set(train_rus_text.split())

language = get_language(input_text, en_words, rus_words)
print(language)
