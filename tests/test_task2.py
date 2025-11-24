import pytest
import sys
from pathlib import Path

# Додаємо src до шляху для імпорту
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from task2 import binary_search


class TestBinarySearch:
    """Тести для функції binary_search"""

    def test_exact_match_found(self):
        """Тест знаходження точного значення"""
        arr = [-7.8, 1.5, 2.7, 3.3, 14.9, 15.6, 122.0]
        iterations, upper_bound = binary_search(arr, 3.3)
        assert upper_bound == 3.3
        assert iterations > 0

    def test_exact_match_first_element(self):
        """Тест знаходження першого елемента"""
        arr = [-7.8, 1.5, 2.7, 3.3, 14.9, 15.6, 122.0]
        iterations, upper_bound = binary_search(arr, -7.8)
        assert upper_bound == -7.8

    def test_exact_match_last_element(self):
        """Тест знаходження останнього елемента"""
        arr = [-7.8, 1.5, 2.7, 3.3, 14.9, 15.6, 122.0]
        iterations, upper_bound = binary_search(arr, 122.0)
        assert upper_bound == 122.0

    def test_value_between_elements(self):
        """Тест значення між елементами"""
        arr = [-7.8, 1.5, 2.7, 3.3, 14.9, 15.6, 122.0]
        iterations, upper_bound = binary_search(arr, 0)
        assert upper_bound == 1.5  # Найменший елемент >= 0

    def test_value_smaller_than_all(self):
        """Тест значення меншого за всі елементи"""
        arr = [-7.8, 1.5, 2.7, 3.3, 14.9, 15.6, 122.0]
        iterations, upper_bound = binary_search(arr, -10)
        assert upper_bound == -7.8  # Перший елемент

    def test_value_larger_than_all(self):
        """Тест значення більшого за всі елементи"""
        arr = [-7.8, 1.5, 2.7, 3.3, 14.9, 15.6, 122.0]
        iterations, upper_bound = binary_search(arr, 200)
        assert upper_bound is None  # Немає верхньої межі

    def test_single_element_found(self):
        """Тест одного елемента - знайдено"""
        arr = [1.5]
        iterations, upper_bound = binary_search(arr, 1.5)
        assert upper_bound == 1.5
        assert iterations == 1

    def test_single_element_not_found_smaller(self):
        """Тест одного елемента - значення менше"""
        arr = [1.5]
        iterations, upper_bound = binary_search(arr, 0)
        assert upper_bound == 1.5  # Єдина верхня межа

    def test_single_element_not_found_larger(self):
        """Тест одного елемента - значення більше"""
        arr = [1.5]
        iterations, upper_bound = binary_search(arr, 2)
        assert upper_bound is None  # Немає верхньої межі

    def test_empty_array(self):
        """Тест порожнього масиву"""
        arr = []
        iterations, upper_bound = binary_search(arr, 5)
        assert upper_bound is None
        assert iterations == 0

    def test_two_elements_found_first(self):
        """Тест двох елементів - знайдено перший"""
        arr = [1.5, 3.3]
        iterations, upper_bound = binary_search(arr, 1.5)
        assert upper_bound == 1.5

    def test_two_elements_found_second(self):
        """Тест двох елементів - знайдено другий"""
        arr = [1.5, 3.3]
        iterations, upper_bound = binary_search(arr, 3.3)
        assert upper_bound == 3.3

    def test_two_elements_between(self):
        """Тест двох елементів - значення між ними"""
        arr = [1.5, 3.3]
        iterations, upper_bound = binary_search(arr, 2.0)
        assert upper_bound == 3.3  # Найменший >= 2.0

    def test_duplicate_elements(self):
        """Тест масиву з дублікатами"""
        arr = [1.5, 1.5, 1.5, 2.7, 3.3, 3.3, 14.9]
        iterations, upper_bound = binary_search(arr, 1.5)
        assert upper_bound == 1.5  # Знаходить один з дублікатів

    def test_duplicate_upper_bound(self):
        """Тест верхньої межі з дублікатами"""
        arr = [1.5, 1.5, 1.5, 2.7, 3.3, 3.3, 14.9]
        iterations, upper_bound = binary_search(arr, 2.0)
        assert upper_bound == 2.7

    def test_negative_values(self):
        """Тест від'ємних значень"""
        arr = [-100.5, -50.2, -25.1, -10.0, -5.5, 0.0, 5.5, 10.0]
        iterations, upper_bound = binary_search(arr, -7.5)
        assert upper_bound == -5.5  # Найменший >= -7.5

    def test_negative_values_found(self):
        """Тест знаходження від'ємного значення"""
        arr = [-100.5, -50.2, -25.1, -10.0, -5.5, 0.0, 5.5, 10.0]
        iterations, upper_bound = binary_search(arr, -10.0)
        assert upper_bound == -10.0

    def test_large_array(self):
        """Тест великого масиву"""
        arr = sorted([float(i) for i in range(1000)])
        iterations, upper_bound = binary_search(arr, 500.0)
        assert upper_bound == 500.0
        assert iterations <= 10  # Бінарний пошук має бути ефективним

    def test_large_array_not_found(self):
        """Тест великого масиву - значення не знайдено"""
        arr = sorted([float(i) for i in range(1000)])
        iterations, upper_bound = binary_search(arr, 500.5)
        assert upper_bound == 501.0  # Найменший >= 500.5

    def test_fractional_values(self):
        """Тест дробових значень"""
        arr = [0.1, 0.5, 1.23, 3.456, 7.89, 10.234, 15.678]
        iterations, upper_bound = binary_search(arr, 2.0)
        assert upper_bound == 3.456  # Найменший >= 2.0

    def test_return_tuple_format(self):
        """Тест формату повернення"""
        arr = [1.5, 2.7, 3.3]
        result = binary_search(arr, 2.0)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], int)  # Кількість ітерацій
        assert isinstance(result[1], (float, type(None)))  # Верхня межа або None

    def test_iterations_count(self):
        """Тест підрахунку ітерацій"""
        arr = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
        iterations, _ = binary_search(arr, 4.0)
        assert iterations > 0
        assert iterations <= 4  # Для 8 елементів має бути максимум log2(8) = 3 ітерації + 1

    def test_sorted_requirement(self):
        """Перевірка, що функція працює з відсортованим масивом"""
        arr = sorted([5.5, 1.2, 9.8, 3.3, 7.1, 2.4, 8.6, 4.7])
        iterations, upper_bound = binary_search(arr, 6.0)
        assert upper_bound == 7.1

    def test_zero_value(self):
        """Тест значення нуль"""
        arr = [-5.0, -2.0, 0.0, 2.0, 5.0]
        iterations, upper_bound = binary_search(arr, 0.0)
        assert upper_bound == 0.0

    def test_very_close_values(self):
        """Тест дуже близьких значень"""
        arr = [1.0001, 1.0002, 1.0003, 1.0004, 1.0005]
        iterations, upper_bound = binary_search(arr, 1.00025)
        assert upper_bound == 1.0003  # Найменший >= 1.00025

