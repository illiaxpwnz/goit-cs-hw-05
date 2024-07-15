import requests
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import re

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the text: {e}")
        return None

def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

def map_reduce(text):
    words = re.findall(r'\b\w+\b', text.lower())  # Розбиваємо текст на слова

    # Паралельний Маппінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

def visualize_top_words(word_freq, top_n=10):
    # Сортуємо слова за частотою
    sorted_word_freq = sorted(word_freq.items(), key=lambda item: item[1], reverse=True)
    top_words = sorted_word_freq[:top_n]

    words, frequencies = zip(*top_words)

    plt.figure(figsize=(10, 5))
    plt.barh(words, frequencies, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title(f'Top {top_n} Words by Frequency')
    plt.gca().invert_yaxis()  # Інвертуємо вісь Y для правильного порядку слів
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Вхідний текст для обробки
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"  # URL до тексту "Гордість і упередження"
    text = get_text(url)
    if text:
        # Виконання MapReduce на вхідному тексті
        result = map_reduce(text)
        print("Результат підрахунку слів:", result)

        # Візуалізація топ-10 слів
        visualize_top_words(result, top_n=10)
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")
