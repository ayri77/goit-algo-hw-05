'''
Додайте метод delete для видалення пар ключ-значення таблиці HashTable , яка реалізована в конспекті.
'''

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        key_hash = self.hash_function(key)
        key_value = [key, value]

        if self.table[key_hash] is None:
            self.table[key_hash] = list([key_value])
            return True
        else:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        key_hash = self.hash_function(key)
        if self.table[key_hash] is not None:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    # ---------------------------
    # додано 
    # ---------------------------
    def delete(self, key):
        key_hash = self.hash_function(key)
        bucket = self.table[key_hash]
        
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                bucket.pop(i)
                return True
        
        raise KeyError(f"Key '{key}' not found in hash-table")


if __name__ == "__main__":
    # Тестуємо нашу хеш-таблицю:
    H = HashTable(5)
    H.insert("apple", 10)
    H.insert("orange", 20)
    H.insert("banana", 30)

    print(H.get("apple"))   # Виведе: 10
    print(H.get("orange"))  # Виведе: 20
    print(H.get("banana"))  # Виведе: 30

    H.delete("apple")
    print(H.get("apple"))   # Виведе: None
    
    # Перевірка видалення неіснуючого ключа
    try:
        H.delete("pineapple")
    except KeyError as e:
        print(f"Помилка: {e}")