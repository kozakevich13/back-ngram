from flask import Flask, jsonify, request
from flask_cors import CORS
import nltk
from nltk import bigrams
from nltk.probability import FreqDist

nltk.download('punkt')

app = Flask(__name__)
CORS(app)

# Змінні для зберігання тексту та слова


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
        # Зчитати слова з файлу saved_words.txt
        with open('saved_words.txt', 'r', encoding='utf-8') as file:
            words = file.read().split()
        
        # Зчитати текст з файлу saved_text.txt
        with open('saved_text.txt', 'r', encoding='utf-8') as text_file:
            saved_text = text_file.read()
            
        return jsonify(success=True, message={'words': words, 'saved_text': saved_text})
    except Exception as e:
        return jsonify(success=False, message=str(e))

# @app.route('/get_data', methods=['GET'])
# def get_data():
#     # Повернути збережені дані
#     return jsonify(stored_text=stored_text, stored_word=stored_word)

if __name__ == '__main__':
    app.run(debug=True)
