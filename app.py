from flask import Flask, jsonify, request
from flask_cors import CORS
import nltk
from nltk import bigrams
from nltk.probability import FreqDist

nltk.download('punkt')

app = Flask(__name__)
CORS(app)

# Змінні для зберігання тексту та слова
def load_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def load_word_from_file(word_file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text
file_path = 'saved_text.txt'

word_file_path = 'saved_words.txt'




def generate_message(seed_word, num_words=6):
    # Завантаження тексту із файлу
    text = load_text_from_file(file_path)

    word = load_word_from_file(word_file_path)


    # Токенізація тексту
    words = nltk.word_tokenize(text)

    # Визначення біграм
    bi_grams = list(bigrams(words))

    # Обчислення частот біграм
    freq_bi_grams = FreqDist(bi_grams)

    message = [seed_word]
    current_word = seed_word

    for _ in range(num_words - 1):
        # Вибір біграм, що починається поточним словом
        next_words = [word[1] for word in freq_bi_grams if word[0] == current_word]

        if next_words:
            next_word = next_words[0]
            message.append(next_word)

            # Перевірка, чи є крапка у згенерованому повідомленні
            if '.' in next_word:
                break

            current_word = next_word
        else:
            break

    return ' '.join(message)

@app.route('/', methods=['POST'])
def process_text():
    try:
        data = request.json  # Припустимо, що фронтенд відправляє дані у форматі JSON
        text = data.get('text', '')  # Отримати текст з об'єкту JSON
        
        # Додати текст в кінець файлу з пробілом
        with open('saved_text.txt', 'a', encoding='utf-8') as file:
            file.write(text + ' ')  # Додати новий текст з пробілом
            
        return jsonify(success=True, message='Text saved successfully.')
    except Exception as e:
        return jsonify(success=False, message=str(e))
    

@app.route('/word', methods=['POST'])
def process_word():
    try:
        data = request.json  # Припустимо, що фронтенд відправляє дані у форматі JSON
        text = data.get('text', '')  # Отримати текст з об'єкту JSON
        
        # Додати текст в кінець файлу з пробілом
        with open('saved_words.txt', 'w', encoding='utf-8') as file:
            file.write(text + ' ')  # Додати новий текст з пробілом
            
        return jsonify(success=True, message='Text saved successfully.')
    except Exception as e:
        return jsonify(success=False, message=str(e))

@app.route('/generation', methods=['GET'])
def process_generation():
    try:
        seed_word = request.args.get('seed_word', '')  # Отримати seed_word з параметрів запиту
        num_words = int(request.args.get('num_words', 6))  # Отримати num_words з параметрів запиту

        message = generate_message(seed_word, num_words)

        return jsonify(success=True, message=message)
    except Exception as e:
        return jsonify(success=False, message=str(e))

# @app.route('/get_data', methods=['GET'])
# def get_data():
#     # Повернути збережені дані
#     return jsonify(stored_text=stored_text, stored_word=stored_word)

if __name__ == '__main__':
    app.run(debug=True)
