from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import nltk
from nltk import bigrams
from nltk.probability import FreqDist
import io

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

dictionary_file_path = 'dictionary.txt'


def generate_message(seed_word, num_words=6, n_gram_type='bigram'):
    # Завантаження тексту із файлу
    text = load_text_from_file(file_path)

    word = load_word_from_file(word_file_path)

    # Токенізація тексту
    words = nltk.word_tokenize(text)

    # Визначення n-грам
    if n_gram_type == 'bigram':
        n_grams = list(bigrams(words))
    elif n_gram_type == 'trigram':
        n_grams = list(nltk.trigrams(words))
    else:
        raise ValueError('Invalid n-gram type. Use "bigram" or "trigram".', n_gram_type)

    # Обчислення частот n-грам
    freq_n_grams = FreqDist(n_grams)

    used_bigrams = set()  # Використані біграми зберігаються у множині

    message = [seed_word]
    current_word = seed_word

    for _ in range(num_words - 1):
        # Вибір доступних n-грам для поточного слова (без вже використаних біграм)
        next_words = [word[1] for word in freq_n_grams if word[0] == current_word and word not in used_bigrams]

        if next_words:
            next_word = next_words[0]

            # Додавання використаної біграми до множини
            used_bigrams.add((current_word, next_word))

            message.append(next_word)
            current_word = next_word
        else:
            break

    message_with_bigrams = ' '.join(message)
    return message_with_bigrams

@app.route('/', methods=['POST'])
def process_text():
    try:
        data = request.json  # Припустимо, що фронтенд відправляє дані у форматі JSON
        text = data.get('text', '')  # Отримати текст з об'єкту JSON
        
        # Додати текст в кінець файлу з пробілом
        with open('saved_text.txt', 'a', encoding='utf-8') as file:
            file.write(text + ' ')  # Додати новий текст з пробілом
            
        return jsonify(success=True, message='Збережено текст для навчання')
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
            
        return jsonify(success=True, message='Збережено текст для навчання')
    except Exception as e:
        return jsonify(success=False, message=str(e))

@app.route('/generation', methods=['GET'])
def process_generation():
    try:
        seed_word = request.args.get('seed_word', '')  # Отримати seed_word з параметрів запиту
        num_words = int(request.args.get('num_words', 6))  # Отримати num_words з параметрів запиту
        n_gram_type = request.args.get('n_gram_type', '')  # Отримати seed_word з параметрів запиту


        message = generate_message(seed_word, num_words, n_gram_type )

        return jsonify(success=True, message=message)
    except Exception as e:
        return jsonify(success=False, message=str(e))
    
@app.route('/delete_text', methods=['DELETE'])
def delete_text():
    try:
        # Очистити вміст файлу saved_text.txt
        with open('saved_text.txt', 'w', encoding='utf-8') as file:
            file.write('')
            
        return jsonify(success=True, message='Text deleted successfully.')
    except Exception as e:
        return jsonify(success=False, message=str(e))

@app.route('/bigram_dict', methods=['GET'])
def get_bigram_dict():
    try:
        # Завантаження тексту із файлу
        text = load_text_from_file(file_path)

        # Токенізація тексту
        words = nltk.word_tokenize(text)

        # Визначення біграм
        bi_grams = list(bigrams(words))

        # Обчислення частот біграм
        freq_bi_grams = FreqDist(bi_grams)

        # Перетворення в словник для відправки на клієнт
        bigram_dict = {f"{bigram[0]} {bigram[1]}": freq for bigram, freq in freq_bi_grams.items()}

        return jsonify(success=True, bigram_dict=bigram_dict)
    except Exception as e:
        return jsonify(success=False, message=str(e))
    
@app.route('/n-grams', methods=['GET'])
def get_n_grams():
    try:
        n_gram_type = request.args.get('type', 'bigram')  # Зчитування параметра типу н-грами (за замовчуванням - біграма)

        # Завантаження тексту із файлу
        text = load_text_from_file(file_path)

        # Токенізація тексту
        words = nltk.word_tokenize(text)

        # Визначення н-грами відповідно до вибраного типу
        if n_gram_type == 'bigram':
            n_grams = list(bigrams(words))
        elif n_gram_type == 'trigram':
            n_grams = list(nltk.trigrams(words))
        else:
            return jsonify(success=False, message='Invalid n-gram type. Use "bigram" or "trigram".')

        # Обчислення частот н-грами
        freq_n_grams = FreqDist(n_grams)

        # Сортування по частоті
        freq_n_grams = sorted(freq_n_grams.items(), key=lambda x: x[1], reverse=True)

        # Перетворення в словник для відправки на клієнт
        n_gram_dict = {' '.join(n_gram): freq for n_gram, freq in freq_n_grams}

        # Save the dictionary to 'dictionary.txt'
        with open(dictionary_file_path, 'w', encoding='utf-8') as file:
            for key, value in n_gram_dict.items():
                file.write(f"{key}: {value}\n")

        return jsonify(success=True, n_gram_dict=n_gram_dict, message='Dictionary saved to dictionary.txt')
    except Exception as e:
        return jsonify(success=False, message=str(e))
    
@app.route('/upload-fiel', methods=['POST'])
def process_text_file():
    try:
        # Check if the request has a file attached
        if 'file' not in request.files:
            return jsonify(success=False, message='No file part')

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return jsonify(success=False, message='No selected file')

        # Save the file to 'saved_text.txt'
        file.save(file_path)

        return jsonify(success=True, message='Text file saved successfully.')
    except Exception as e:
        return jsonify(success=False, message=str(e))
    
@app.route('/download-dictionary', methods=['GET'])
def download_dictionary():
    try:
        # Load the dictionary from 'dictionary.txt'
        with open(dictionary_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Set up response headers to force download
        response = send_file(
            io.BytesIO(content.encode('utf-8')),
            as_attachment=True,
            download_name='dictionary.txt',
            mimetype='text/plain'
        )

        return response
    except Exception as e:
        return jsonify(success=False, message=str(e))


# @app.route('/get_data', methods=['GET'])
# def get_data():
#     # Повернути збережені дані
#     return jsonify(stored_text=stored_text, stored_word=stored_word)

if __name__ == '__main__':
    app.run(debug=True)
