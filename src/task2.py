'''
Реалізуйте двійковий пошук для відсортованого масиву з дробовими числами.
Написана функція для двійкового пошуку повинна повертати кортеж, де першим 
елементом є кількість ітерацій, потрібних для знаходження елемента. Другим 
елементом має бути "верхня межа" — це найменший елемент, який є більшим або 
рівним заданому значенню.
'''

import random

def binary_search(sorted_float_list: list[float], value: float) -> (int, float):
    counter = 0
    min_idx = 0
    max_idx = len(sorted_float_list) - 1
    min_max = None

    while min_idx <= max_idx:
        counter += 1
        idx = (max_idx + min_idx) // 2
        current_value = sorted_float_list[idx]
        if current_value < value:
            min_idx = idx + 1
        else:
            min_max = current_value
            max_idx = idx - 1
    return (counter, min_max)


if __name__ == "__main__":
    sorted_float = sorted([random.uniform(-100.0, 100.0) for _ in range(1000)])

    print(binary_search(sorted_float, 0))
    print(binary_search(sorted_float, 3))
    print(binary_search(sorted_float, 66))