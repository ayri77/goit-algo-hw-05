import pytest
import sys
from pathlib import Path

# Додаємо src до шляху для імпорту
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from task1 import HashTable


class TestHashTable:
    """Тести для класу HashTable"""

    def test_init(self):
        """Тест ініціалізації хеш-таблиці"""
        ht = HashTable(10)
        assert ht.size == 10
        assert len(ht.table) == 10
        assert all(isinstance(bucket, list) for bucket in ht.table)

    def test_hash_function(self):
        """Тест хеш-функції"""
        ht = HashTable(5)
        key = "test"
        hash_value = ht.hash_function(key)
        assert 0 <= hash_value < 5

    def test_insert_new_key(self):
        """Тест вставки нового ключа"""
        ht = HashTable(5)
        result = ht.insert("apple", 10)
        assert result is True
        assert ht.get("apple") == 10

    def test_insert_multiple_keys(self):
        """Тест вставки кількох ключів"""
        ht = HashTable(5)
        ht.insert("apple", 10)
        ht.insert("orange", 20)
        ht.insert("banana", 30)
        
        assert ht.get("apple") == 10
        assert ht.get("orange") == 20
        assert ht.get("banana") == 30

    def test_insert_update_existing_key(self):
        """Тест оновлення існуючого ключа"""
        ht = HashTable(5)
        ht.insert("apple", 10)
        ht.insert("apple", 25)  # Оновлюємо значення
        
        assert ht.get("apple") == 25

    def test_get_existing_key(self):
        """Тест отримання існуючого ключа"""
        ht = HashTable(5)
        ht.insert("apple", 10)
        assert ht.get("apple") == 10

    def test_get_nonexistent_key(self):
        """Тест отримання неіснуючого ключа"""
        ht = HashTable(5)
        assert ht.get("nonexistent") is None

    def test_get_after_insert(self):
        """Тест отримання після вставки"""
        ht = HashTable(5)
        test_data = {
            "apple": 10,
            "orange": 20,
            "banana": 30,
            "grape": 40,
            "kiwi": 50
        }
        
        for key, value in test_data.items():
            ht.insert(key, value)
        
        for key, expected_value in test_data.items():
            assert ht.get(key) == expected_value

    def test_delete_existing_key(self):
        """Тест видалення існуючого ключа"""
        ht = HashTable(5)
        ht.insert("apple", 10)
        ht.insert("orange", 20)
        
        result = ht.delete("apple")
        assert result is True
        assert ht.get("apple") is None
        assert ht.get("orange") == 20  # Інший ключ має залишитись

    def test_delete_nonexistent_key_raises_error(self):
        """Тест видалення неіснуючого ключа викликає KeyError"""
        ht = HashTable(5)
        ht.insert("apple", 10)
        
        with pytest.raises(KeyError, match="not found in hash-table"):
            ht.delete("nonexistent")

    def test_delete_from_empty_table(self):
        """Тест видалення з порожньої таблиці"""
        ht = HashTable(5)
        
        with pytest.raises(KeyError):
            ht.delete("any_key")

    def test_delete_all_keys(self):
        """Тест видалення всіх ключів"""
        ht = HashTable(5)
        keys = ["apple", "orange", "banana"]
        
        for key in keys:
            ht.insert(key, 10)
        
        for key in keys:
            ht.delete(key)
            assert ht.get(key) is None

    def test_insert_after_delete(self):
        """Тест вставки після видалення"""
        ht = HashTable(5)
        ht.insert("apple", 10)
        ht.delete("apple")
        ht.insert("apple", 20)
        
        assert ht.get("apple") == 20

    def test_hash_collision(self):
        """Тест обробки колізій хешу (якщо два ключі мають однаковий хеш)"""
        ht = HashTable(1)  # Маленький розмір для гарантованих колізій
        
        ht.insert("key1", 10)
        ht.insert("key2", 20)
        ht.insert("key3", 30)
        
        assert ht.get("key1") == 10
        assert ht.get("key2") == 20
        assert ht.get("key3") == 30

    def test_delete_with_collision(self):
        """Тест видалення при наявності колізій"""
        ht = HashTable(2)  # Маленький розмір для колізій
        
        ht.insert("a", 1)
        ht.insert("b", 2)
        ht.insert("c", 3)
        
        ht.delete("b")
        
        assert ht.get("a") == 1
        assert ht.get("b") is None
        assert ht.get("c") == 3

    def test_different_types(self):
        """Тест роботи з різними типами ключів"""
        ht = HashTable(10)
        
        # Різні типи ключів
        ht.insert("string", 1)
        ht.insert(123, 2)
        ht.insert(3.14, 3)
        ht.insert((1, 2), 4)
        
        assert ht.get("string") == 1
        assert ht.get(123) == 2
        assert ht.get(3.14) == 3
        assert ht.get((1, 2)) == 4

    def test_update_and_delete_sequence(self):
        """Тест послідовності оновлень і видалень"""
        ht = HashTable(5)
        
        # Вставка
        ht.insert("key", 1)
        assert ht.get("key") == 1
        
        # Оновлення
        ht.insert("key", 2)
        assert ht.get("key") == 2
        
        # Видалення
        ht.delete("key")
        assert ht.get("key") is None
        
        # Повторна вставка
        ht.insert("key", 3)
        assert ht.get("key") == 3

    def test_large_table(self):
        """Тест великої таблиці"""
        ht = HashTable(100)
        
        # Вставляємо багато елементів
        for i in range(100):
            ht.insert(f"key_{i}", i)
        
        # Перевіряємо, що всі елементи на місці
        for i in range(100):
            assert ht.get(f"key_{i}") == i

    def test_string_with_special_characters(self):
        """Тест ключів зі спеціальними символами"""
        ht = HashTable(10)
        
        special_keys = [
            "key with spaces",
            "key-with-dashes",
            "key_with_underscores",
            "key@with#special$chars"
        ]
        
        for i, key in enumerate(special_keys):
            ht.insert(key, i)
            assert ht.get(key) == i

