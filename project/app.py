from flask import Flask, render_template, request
import os
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# Ініціалізація Flask
app = Flask(__name__)

import matplotlib
matplotlib.use('Agg')  # Використовуємо бекенд без графічного інтерфейсу

app = Flask(__name__, static_folder='static2')  # Вказуємо правильну папку для статичних файлів

# Створюємо папку для статичних файлів, якщо вона не існує
if not os.path.exists("static2"):
    os.makedirs("static2")

# Головне меню Lab7
@app.route('/lab7')
def lab7_menu():
    return render_template('lab7.html')

# Lab7 Task1: Побудова графіка функції
@app.route('/lab7/task1')
def lab7_task1():
    x = np.linspace(1, 10, 500)
    y = x ** np.sin(10 * x)

    # Побудова графіка
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label=r"$Y(x) = x^{\sin(10x)}$", color="blue")
    plt.title("Графік функції $Y(x) = x^{\sin(10x)}$", fontsize=14)
    plt.xlabel("$x$", fontsize=12)
    plt.ylabel("$Y(x)$", fontsize=12)
    plt.legend(fontsize=12, loc="upper right")

    # Збереження графіка у файл
    graph_path = "static2/2d_graph_function.png"  # Файл збережений в статичній папці
    plt.savefig(graph_path, format="png", dpi=300)
    plt.close()

    # Повертаємо шаблон з правильним шляхом до зображення
    return render_template('lab7-Task1.html', graph_path='/static2/2d_graph_function.png')

# Lab7 Task2: Побудова гістограми частоти літер
@app.route('/lab7/task2', methods=['GET', 'POST'])
def lab7_task2():
    if request.method == 'POST':
        # Отримуємо текст з форми
        user_text = request.form['user_text']

        # Обробляємо текст
        letters_only = [char.lower() for char in user_text if char.isalpha()]
        letter_counts = Counter(letters_only)

        letters = list(letter_counts.keys())
        frequencies = list(letter_counts.values())

        # Побудова гістограми
        plt.figure(figsize=(10, 6))
        plt.bar(letters, frequencies, color="skyblue", edgecolor="black")

        plt.title("Частота появи літер у тексті", fontsize=14)
        plt.xlabel("Літери", fontsize=12)
        plt.ylabel("Кількість появ", fontsize=12)

        # Збереження графіка у файл
        graph_path = "static2/letter_frequency_histogram.png"
        plt.savefig(graph_path, format="png", dpi=300)
        plt.close()

        # Повертаємо шаблон з графіком
        return render_template('lab7-Task2.html', graph_path='/static2/letter_frequency_histogram.png')

    return render_template('lab7-Task2.html')

# Lab7 Task3: Побудова гістограми типів речень
@app.route('/lab7/task3', methods=['GET', 'POST'])
def lab7_task3():
    if request.method == 'POST':
        # Отримуємо текст з форми
        user_text = request.form['user_text']

        # Логіка для аналізу типів речень
        def count_sentence_types(text):
            normal = text.count(".") - text.count("...")  
            exclamatory = text.count("!")  
            interrogative = text.count("?")  
            ellipsis = text.count("...")  
            return {"Звичайні": normal, "Питальні": interrogative, "Окличні": exclamatory, "Трикрапка": ellipsis}

        sentence_counts = count_sentence_types(user_text)

        categories = list(sentence_counts.keys())
        counts = list(sentence_counts.values())

        # Побудова гістограми
        plt.figure(figsize=(10, 6))
        plt.bar(categories, counts, color=["blue", "green", "red", "purple"], edgecolor="black")

        plt.title("Частота появи різних типів речень", fontsize=14)
        plt.xlabel("Типи речень", fontsize=12)
        plt.ylabel("Кількість речень", fontsize=12)

        # Збереження графіка у файл
        graph_path = "static2/sentence_type_histogram.png"
        plt.savefig(graph_path, format="png", dpi=300)
        plt.close()

        # Повертаємо шаблон з графіком
        return render_template('lab7-Task3.html', graph_path='/static2/sentence_type_histogram.png')

    return render_template('lab7-Task3.html')

# Функція для аналізу сторінки новин
def analyze_news_page(url):
    try:
        # Кодування URL
        encoded_url = quote(url, safe=':/')

        # Надсилання запиту
        request = Request(encoded_url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(request)
        html_content = response.read().decode('utf-8')

        # Видалення HTML-тегів
        text = re.sub(r'<[^>]+>', ' ', html_content)
        words = re.findall(r'\b\w+\b', text.lower())
        word_frequency = Counter(words)

        # Частота тегів
        tags = re.findall(r'<(\w+)', html_content)
        tags_frequency = Counter(tags)

        # Кількість посилань
        links = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)', html_content)
        links_count = len(links)

        # Кількість зображень
        images = re.findall(r'<img\s+[^>]*src=["\']([^"\']+)', html_content)
        images_count = len(images)

        # Повернення результатів
        return {
            "word_frequency": word_frequency.most_common(10),
            "tags_frequency": tags_frequency.most_common(10),
            "links_count": links_count,
            "images_count": images_count
        }

    except Exception as e:
        return {"error": f"Помилка при завантаженні сторінки: {e}"}


# Маршрут для лабораторної 3
@app.route('/lab3', methods=['GET', 'POST'])
def lab3():
    result = None
    error = None

    if request.method == 'POST':
        # Додайте обробку даних для лаб3 тут, якщо потрібно
        pass

    return render_template('lab3.html', result=result, error=error)


# Маршрут для лабораторної 6
@app.route('/lab6', methods=['GET', 'POST'])
def lab6():
    result = None
    error = None

    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            error = "Будь ласка, введіть URL."
        else:
            analysis_result = analyze_news_page(url)
            if "error" in analysis_result:
                error = analysis_result["error"]
            else:
                result = analysis_result

    return render_template('lab6.html', result=result, error=error)

#лаба4
import re

# Функція для аналізу тексту
def analyze_sentences(text):
    sentences = re.split(r'[.!?…]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    total_sentences = len(sentences)
    exclamatory_sentences = len(re.findall(r'!', text))
    interrogative_sentences = len(re.findall(r'\?', text))
    ellipsis_sentences = len(re.findall(r'\.\.\.', text))

    return total_sentences, exclamatory_sentences, interrogative_sentences, ellipsis_sentences

# Лабораторна 4
@app.route('/lab4', methods=['GET', 'POST'])
def lab4():
    result = None
    error = None

    if request.method == 'POST':
        user_text = request.form.get('text', '').strip()
        if user_text:
            total, exclamatory, interrogative, ellipsis = analyze_sentences(user_text)
            result = {
                'total': total,
                'exclamatory': exclamatory,
                'interrogative': interrogative,
                'ellipsis': ellipsis
            }
        else:
            error = "Будь ласка, введіть текст для аналізу."

    return render_template('lab4.html', result=result, error=error)


#лаба 5

import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit  # Масть карти
        self.rank = rank  # Номер/ранг карти

    def __str__(self):
        return f"{self.rank} {self.suit}"

# Клас Deck
class Deck:
    # Масти карт українською
    suits = ['Черви', 'Бубни', 'Трефи', 'Піки']
    # Ранги карт українською
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Валет', 'Дама', 'Король', 'Туз']

    def __init__(self):
        # Створення колоди карт
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        self.shuffle()  # Перемішування колоди при створенні

    def shuffle(self):
        """Перемішує карти в колоді."""
        random.shuffle(self.cards)

    def get_card_by_position(self, position):
        """Отримати карту за номером розташування в колоді (починаючи з 1)."""
        if 1 <= position <= len(self.cards):
            return self.cards[position - 1]
        else:
            raise ValueError("Неправильна позиція!")

    def draw_one_card(self):
        """Видає одну карту з колоди."""
        if self.cards:
            return self.cards.pop(0)
        else:
            raise ValueError("Колода порожня!")

    def draw_six_cards(self):
        """Видає шість карт з колоди."""
        if len(self.cards) >= 6:
            return [self.draw_one_card() for _ in range(6)]
        else:
            raise ValueError("У колоді недостатньо карт!")

    def show_all_cards(self):
        """Виводить всі карти в колоді."""
        return [str(card) for card in self.cards]

# Створення колоди карт
deck = Deck()

# Обробник для лабораторної роботи 5
@app.route('/lab5', methods=['GET', 'POST'])
def lab5():
    result = None
    error = None
    position = None

    if request.method == 'POST':
        command = request.form.get('command')
        position = request.form.get('position')

        try:
            if command == 'show_all':
                result = deck.show_all_cards()
            elif command == 'get_card':
                position = int(position)
                result = deck.get_card_by_position(position)
            elif command == 'shuffle':
                deck.shuffle()
                result = "Колода перемішана!"
            elif command == 'draw_one':
                result = deck.draw_one_card()
            elif command == 'draw_six':
                result = deck.draw_six_cards()
            elif command == 'show_remaining':
                result = deck.show_all_cards()
            else:
                error = "Невідома команда."
        except ValueError as e:
            error = f"Помилка: {e}"
        except Exception as e:
            error = f"Щось пішло не так: {e}"

    return render_template('lab5.html', result=result, error=error, position=position)



# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')

# Сторінка "Про мене"
@app.route('/about')
def about_me():
    return render_template('aboutMe.html')

# Сторінка "Зворотній зв'язок"
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Головна сторінка лабораторної роботи
@app.route('/lab1')
def lab1():
    return render_template('lab1.html')

# лаба 1
@app.route('/lab1/task1', methods=['GET', 'POST'])
def task1():
    results = None
    error = None

    if request.method == 'POST':
        try:
            num1 = float(request.form.get('num1', 0))
            num2 = float(request.form.get('num2', 0))
            results = {
                'addition': num1 + num2,
                'subtraction': num1 - num2,
                'multiplication': num1 * num2,
                'division': num1 / num2 if num2 != 0 else 'Ділення на 0!'
            }
        except ValueError:
            error = 'Будь ласка, введіть коректні числа!'

    return render_template('task1.html', results=results, error=error)

# Завдання 2
@app.route('/lab1/task2', methods=['GET', 'POST'])
def task2():
    result = None
    error = None

    if request.method == 'POST':
        try:
            akvariomA = float(request.form.get('akvariomA', 0))
            akvariomB = float(request.form.get('akvariomB', 0))
            result = akvariomA * akvariomB
        except ValueError:
            error = 'Будь ласка, введіть коректні числа!'

    return render_template('task2.html', result=result, error=error)

# Завдання 3
@app.route('/lab1/task3', methods=['GET', 'POST'])
def task3():
    penalty = None
    error = None

    if request.method == 'POST':
        try:
            boxes = float(request.form.get('boxes', 0))
            bananas_per_box = float(request.form.get('bananasPerBox', 0))
            price_per_kg = float(request.form.get('pricePerKg', 0))
            overweight = float(request.form.get('overweight', 0)) / 100

            penalty = round((bananas_per_box * (1 + overweight) * price_per_kg) * 5, 2)
        except ValueError:
            error = 'Будь ласка, введіть коректні числа!'

    return render_template('task3.html', penalty=penalty, error=error)

@app.route('/lab2', methods=['GET', 'POST'])
def lab2():
    result = None
    error = None
    elements = ['телефон', 'бункер', 'табір', 'машина', 'стіл']

    if request.method == 'POST':
        search_element = request.form.get('searchElement', '').strip()
        if search_element:
            if search_element in elements:
                result = f"Значення знайдено: {search_element}"
            else:
                result = "Значення не знайдено"
        else:
            error = "Будь ласка, введіть текст для пошуку."

    return render_template('lab2.html', result=result, error=error)



if __name__ == '__main__':
    app.run(debug=True)

