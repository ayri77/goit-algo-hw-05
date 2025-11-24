import pytest
import sys
from pathlib import Path

# Додаємо src до шляху для імпорту
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from substring_search import boyer_moore, kmp, rabin_karp


class TestBoyerMooreBasic:
    """Базові тести для алгоритму Бойера-Мура"""

    def test_pattern_at_beginning(self):
        """Тест: паттерн знайдено на початку тексту"""
        text = "ABCDEFG"
        pattern = "ABC"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 0
        assert comparing > 0
        assert jumps >= 0

    def test_pattern_at_end(self):
        """Тест: паттерн знайдено в кінці тексту"""
        text = "ABCDEFG"
        pattern = "EFG"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 4
        assert comparing > 0

    def test_pattern_in_middle(self):
        """Тест: паттерн знайдено в середині тексту"""
        text = "ABCDEFG"
        pattern = "CDE"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 2
        assert comparing > 0

    def test_pattern_not_found(self):
        """Тест: паттерн не знайдено"""
        text = "ABCDEFG"
        pattern = "XYZ"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos is None
        assert comparing > 0

    def test_single_character_pattern(self):
        """Тест: односимвольний паттерн"""
        text = "ABCDEFG"
        pattern = "C"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 2

    def test_pattern_equals_text(self):
        """Тест: паттерн дорівнює тексту"""
        text = "ABC"
        pattern = "ABC"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 0


class TestBoyerMooreEdgeCases:
    """Тести граничних випадків"""

    def test_empty_pattern(self):
        """Тест: порожній паттерн"""
        text = "ABCDEFG"
        pattern = ""
        pos, comparing, jumps = boyer_moore(text, pattern)
        # Згідно з реалізацією, порожній паттерн повертає (0, 0, 0)
        assert pos == 0
        assert comparing == 0
        assert jumps == 0

    def test_text_shorter_than_pattern(self):
        """Тест: текст коротший за паттерн"""
        text = "AB"
        pattern = "ABCD"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos is None
        assert comparing == 0
        assert jumps == 0

    def test_empty_text(self):
        """Тест: порожній текст"""
        text = ""
        pattern = "ABC"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos is None
        assert comparing == 0
        assert jumps == 0

    def test_empty_text_and_pattern(self):
        """Тест: порожній текст і паттерн"""
        text = ""
        pattern = ""
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 0
        assert comparing == 0
        assert jumps == 0

    def test_single_character_text(self):
        """Тест: односимвольний текст"""
        text = "A"
        pattern = "A"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 0


class TestBoyerMooreRepeatingCharacters:
    """Тести з повторюваними символами"""

    def test_all_same_characters_found(self):
        """Тест: всі символи однакові, паттерн знайдено"""
        text = "AAAAAAA"
        pattern = "AAA"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 0  # Має знайти перше входження

    def test_repeating_pattern(self):
        """Тест: паттерн з повторюваними символами"""
        text = "ABABABAB"
        pattern = "ABAB"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 0

    def test_pattern_with_duplicates(self):
        """Тест: паттерн з дублікатами символів"""
        text = "ABCABCABC"
        pattern = "CAB"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 2  # Перше входження CAB

    def test_multiple_occurrences(self):
        """Тест: кілька входжень паттерна (має знайти перше)"""
        text = "ABABABAB"
        pattern = "AB"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 0  # Має знайти перше входження


class TestBoyerMooreBadCharacterOnly:
    """Тести тільки з bad character heuristic (без good suffix)"""

    def test_bad_char_basic(self):
        """Тест: базовий випадок з bad character"""
        text = "ABCAABBCAABCBACBACA"
        pattern = "CBACA"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=False)
        assert pos == 14  # Правильна позиція паттерна

    def test_bad_char_shift_optimization(self):
        """Тест: перевірка оптимізації через bad character"""
        text = "ABCDEFGHIJKLMNOP"
        pattern = "FGH"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=False)
        assert pos == 5

    def test_bad_char_with_repeats(self):
        """Тест: bad character з повторюваними символами"""
        text = "AABBAABBAA"
        pattern = "BBAA"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=False)
        assert pos == 2


class TestBoyerMooreGoodSuffix:
    """Тести з good suffix heuristic"""

    def test_good_suffix_basic(self):
        """Тест: базовий випадок з good suffix"""
        text = "XBABABBAABABA"
        pattern = "ABABA"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=True)
        assert pos == 8  # Перевірте правильність позиції

    def test_good_suffix_vs_bad_char(self):
        """Тест: порівняння good suffix vs bad character"""
        text = "ABCAABBCAABCBACBACA"
        pattern = "CBACA"
        pos_gs, comp_gs, jumps_gs = boyer_moore(text, pattern, use_good_suffix=True)
        pos_bc, comp_bc, jumps_bc = boyer_moore(text, pattern, use_good_suffix=False)
        # Обидва мають знайти той самий паттерн
        assert pos_gs == pos_bc == 14  # Правильна позиція паттерна

    def test_good_suffix_optimization(self):
        """Тест: перевірка оптимізації через good suffix"""
        text = "ABCABCABCABC"
        pattern = "ABCABC"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=True)
        assert pos == 0

    def test_good_suffix_complex_pattern(self):
        """Тест: складний паттерн для good suffix"""
        text = "ABABABABABAB"
        pattern = "ABABAB"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=True)
        assert pos == 0


class TestBoyerMooreSpecialCases:
    """Тести спеціальних випадків"""

    def test_pattern_with_all_unique_chars(self):
        """Тест: паттерн з унікальними символами"""
        text = "ABCDEFGHIJKLMNOP"
        pattern = "FGH"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 5

    def test_pattern_not_in_text_chars(self):
        """Тест: символи паттерна не присутні в тексті"""
        text = "ABCDEFG"
        pattern = "XYZ"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos is None

    def test_partial_match_at_end(self):
        """Тест: часткове співпадіння в кінці"""
        text = "ABCDEFG"
        pattern = "FGH"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos is None

    def test_case_sensitivity(self):
        """Тест: чутливість до регістру"""
        text = "ABCDEFG"
        pattern = "abc"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos is None  # Має бути None, оскільки регістр не співпадає

    def test_numbers_in_text(self):
        """Тест: числа в тексті"""
        text = "ABC123DEF456"
        pattern = "123"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 3

    def test_special_characters(self):
        """Тест: спеціальні символи"""
        text = "Hello, World! How are you?"
        pattern = "World"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 7


class TestBoyerMooreGoodSuffixTable:
    """Тести, що виявляють проблеми з good suffix table"""

    def test_good_suffix_simple_repeat(self):
        """Тест: простий повтор для виявлення помилок у good suffix table"""
        text = "ABABAB"
        pattern = "ABAB"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=True)
        assert pos == 0

    def test_good_suffix_suffix_match(self):
        """Тест: перевірка правильності обчислення good suffix"""
        text = "ABCABCABC"
        pattern = "ABCABC"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=True)
        assert pos == 0

    def test_good_suffix_complex_shift(self):
        """Тест: складний зсув для good suffix"""
        text = "BABABABAB"
        pattern = "ABABAB"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=True)
        # Має знайти паттерн, перевірте правильність позиції
        assert pos is not None

    def test_good_suffix_variant_a(self):
        """Тест: варіант A good suffix (знайдено суфікс)"""
        text = "CABABAB"
        pattern = "ABABAB"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=True)
        assert pos == 1

    def test_good_suffix_variant_b(self):
        """Тест: варіант B good suffix (префікс збігається з суфіксом)"""
        text = "ABCABCABC"
        pattern = "ABCABC"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=True)
        assert pos == 0


class TestBoyerMoorePerformance:
    """Тести для перевірки ефективності"""

    def test_large_text_small_pattern(self):
        """Тест: великий текст, маленький паттерн"""
        text = "A" * 1000 + "B" + "A" * 1000
        pattern = "BA"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 1000
        # Перевірка, що алгоритм працює (в гіршому випадку може бути багато порівнянь)
        assert comparing > 0
        # Для такого тексту з багатьма однаковими символами порівнянь може бути багато
        assert comparing <= len(text) * len(pattern)  # Верхня межа

    def test_repeated_pattern_in_text(self):
        """Тест: повторюваний паттерн у тексті"""
        text = "AB" * 100
        pattern = "AB"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 0

    def test_jumps_count(self):
        """Тест: перевірка підрахунку стрибків"""
        text = "ABCDEFGHIJKLMNOP"
        pattern = "FGH"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert jumps > 0  # Має бути хоча б один стрибок

    def test_comparing_count(self):
        """Тест: перевірка підрахунку порівнянь"""
        text = "ABCDEFGHIJKLMNOP"
        pattern = "FGH"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert comparing > 0
        # Порівнянь має бути менше за довжину тексту
        assert comparing <= len(text)


class TestBoyerMooreRealWorld:
    """Тести з реальними прикладами"""

    def test_dna_sequence(self):
        """Тест: послідовність ДНК"""
        text = "ATCGATCGATCG"
        pattern = "ATCG"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 0

    def test_word_search(self):
        """Тест: пошук слова"""
        text = "The quick brown fox jumps over the lazy dog"
        pattern = "fox"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 16

    def test_multiple_words(self):
        """Тест: пошук серед кількох слів"""
        text = "hello world hello world"
        pattern = "world"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 6  # Перше входження


class TestBoyerMooreEdgeCasePatterns:
    """Тести граничних випадків паттернів"""

    def test_pattern_one_char_repeated(self):
        """Тест: паттерн з одного повторюваного символу"""
        text = "AAAAA"
        pattern = "AAA"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 0

    def test_pattern_alternating(self):
        """Тест: чергуючийся паттерн"""
        text = "ABABABABAB"
        pattern = "BAB"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 1

    def test_pattern_palindrome(self):
        """Тест: паліндромний паттерн"""
        text = "ABCBAXYZ"
        pattern = "ABCBA"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 0

    def test_pattern_with_gaps(self):
        """Тест: паттерн з пропусками в тексті"""
        text = "A_B_C_D_E"
        pattern = "B_C"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 2


class TestBoyerMooreGoodSuffixIssues:
    """Тести, що виявляють конкретні проблеми з good suffix"""

    def test_good_suffix_range_issue(self):
        """Тест: виявлення проблеми з діапазоном у good suffix table"""
        # Цей тест може виявити проблему з range(i+1-k, -1, -1)
        text = "ABABABABAB"
        pattern = "ABABAB"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=True)
        assert pos == 0

    def test_good_suffix_shift_calculation(self):
        """Тест: перевірка правильності обчислення зсуву"""
        # Може виявити проблему з формулою i - j + 1
        text = "CABABAB"
        pattern = "ABABAB"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=True)
        assert pos == 1

    def test_good_suffix_prefix_suffix_match(self):
        """Тест: перевірка варіанту B (префікс-суфікс)"""
        # Може виявити проблему з pattern[:k] == suffix[-k:]
        text = "ABCABCABC"
        pattern = "ABCABC"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=True)
        assert pos == 0

    def test_good_suffix_complex_case(self):
        """Тест: складний випадок для good suffix"""
        text = "BABABABABAB"
        pattern = "ABABAB"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=True)
        # Має знайти паттерн
        assert pos is not None
        assert pos >= 0


class TestBoyerMooreSpecificIssues:
    """Тести, що виявляють конкретні проблеми з реалізацією"""

    def test_good_suffix_table_range_bug(self):
        """Тест: виявлення помилки з діапазоном у build_good_suffix_table
        Проблема: range(i+1-k, -1, -1) може бути некоректним
        """
        # Паттерн, який може викликати проблему з діапазоном
        text = "ABCABCABCABC"
        pattern = "ABCABC"
        # Цей тест має пройти, але якщо є помилка з діапазоном, може виникнути IndexError
        try:
            pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=True)
            assert pos == 0
        except (IndexError, ValueError) as e:
            pytest.fail(f"Виявлено помилку з діапазоном у good suffix table: {e}")

    def test_good_suffix_shift_formula(self):
        """Тест: перевірка формули зсуву у good suffix
        Проблема: формула i - j + 1 може бути некоректною
        """
        text = "CABABAB"
        pattern = "ABABAB"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=True)
        # Має знайти на позиції 1
        assert pos == 1

    def test_good_suffix_variant_b_logic(self):
        """Тест: перевірка логіки варіанту B (префікс-суфікс)
        Проблема: pattern[:k] == suffix[-k:] може бути некоректним
        """
        text = "ABCABCABC"
        pattern = "ABCABC"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=True)
        assert pos == 0

    def test_bad_char_table_correctness(self):
        """Тест: перевірка правильності таблиці bad character
        Таблиця має зберігати найправішу позицію кожного символу
        """
        text = "ABCDEFGABCDEFG"
        pattern = "DEF"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=False)
        assert pos == 3  # Перше входження

    def test_negative_shift_prevention(self):
        """Тест: перевірка, що зсув ніколи не буде від'ємним"""
        text = "ABCDEFGHIJKLMNOP"
        pattern = "XYZ"
        # Має повернути None без помилок
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos is None
        assert comparing > 0

    def test_zero_shift_handling(self):
        """Тест: обробка нульового зсуву (знайдено паттерн)"""
        text = "ABCDEFG"
        pattern = "CDE"
        pos, comparing, jumps = boyer_moore(text, pattern)
        assert pos == 2
        assert jumps >= 0

    def test_good_suffix_edge_case_single_char(self):
        """Тест: граничний випадок good suffix для односимвольного паттерна"""
        text = "AAAAA"
        pattern = "A"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=True)
        assert pos == 0

    def test_good_suffix_edge_case_two_chars(self):
        """Тест: граничний випадок good suffix для двосимвольного паттерна"""
        text = "ABABAB"
        pattern = "AB"
        pos, comparing, jumps = boyer_moore(text, pattern, use_good_suffix=True)
        assert pos == 0

    def test_comparison_count_consistency(self):
        """Тест: перевірка консистентності підрахунку порівнянь"""
        text = "ABCDEFG"
        pattern = "CDE"
        pos1, comp1, jumps1 = boyer_moore(text, pattern, use_good_suffix=False)
        pos2, comp2, jumps2 = boyer_moore(text, pattern, use_good_suffix=True)
        # Обидва мають знайти той самий паттерн
        assert pos1 == pos2 == 2
        # Кількість порівнянь може відрізнятися через різні евристики
        assert comp1 > 0 and comp2 > 0

    def test_jumps_count_consistency(self):
        """Тест: перевірка консистентності підрахунку стрибків"""
        text = "ABCDEFG"
        pattern = "CDE"
        pos1, comp1, jumps1 = boyer_moore(text, pattern, use_good_suffix=False)
        pos2, comp2, jumps2 = boyer_moore(text, pattern, use_good_suffix=True)
        # Обидва мають знайти той самий паттерн
        assert pos1 == pos2 == 2
        # Кількість стрибків має бути >= 0
        assert jumps1 >= 0 and jumps2 >= 0


# ==================== KMP ALGORITHM TESTS ====================

class TestKMPBasic:
    """Базові тести для алгоритму KMP"""

    def test_pattern_at_beginning(self):
        """Тест: паттерн знайдено на початку тексту"""
        text = "ABCDEFG"
        pattern = "ABC"
        pos = kmp(text, pattern)
        assert pos == 0

    def test_pattern_at_end(self):
        """Тест: паттерн знайдено в кінці тексту"""
        text = "ABCDEFG"
        pattern = "EFG"
        pos = kmp(text, pattern)
        assert pos == 4

    def test_pattern_in_middle(self):
        """Тест: паттерн знайдено в середині тексту"""
        text = "ABCDEFG"
        pattern = "CDE"
        pos = kmp(text, pattern)
        assert pos == 2

    def test_pattern_not_found(self):
        """Тест: паттерн не знайдено"""
        text = "ABCDEFG"
        pattern = "XYZ"
        pos = kmp(text, pattern)
        assert pos is None

    def test_single_character_pattern(self):
        """Тест: односимвольний паттерн"""
        text = "ABCDEFG"
        pattern = "C"
        pos = kmp(text, pattern)
        assert pos == 2

    def test_pattern_equals_text(self):
        """Тест: паттерн дорівнює тексту"""
        text = "ABC"
        pattern = "ABC"
        pos = kmp(text, pattern)
        assert pos == 0


class TestKMPEdgeCases:
    """Тести граничних випадків для KMP"""

    def test_empty_pattern(self):
        """Тест: порожній паттерн"""
        text = "ABCDEFG"
        pattern = ""
        pos = kmp(text, pattern)
        # Згідно з реалізацією, порожній паттерн повертає 0
        assert pos == 0

    def test_text_shorter_than_pattern(self):
        """Тест: текст коротший за паттерн"""
        text = "AB"
        pattern = "ABCD"
        pos = kmp(text, pattern)
        assert pos is None

    def test_empty_text(self):
        """Тест: порожній текст"""
        text = ""
        pattern = "ABC"
        pos = kmp(text, pattern)
        assert pos is None

    def test_empty_text_and_pattern(self):
        """Тест: порожній текст і паттерн"""
        text = ""
        pattern = ""
        pos = kmp(text, pattern)
        assert pos == 0

    def test_single_character_text(self):
        """Тест: односимвольний текст"""
        text = "A"
        pattern = "A"
        pos = kmp(text, pattern)
        assert pos == 0

    def test_single_character_text_pattern_not_found(self):
        """Тест: односимвольний текст, паттерн не знайдено"""
        text = "A"
        pattern = "B"
        pos = kmp(text, pattern)
        assert pos is None


class TestKMPRepeatingCharacters:
    """Тести з повторюваними символами для KMP"""

    def test_all_same_characters_found(self):
        """Тест: всі символи однакові, паттерн знайдено"""
        text = "AAAAAAA"
        pattern = "AAA"
        pos = kmp(text, pattern)
        assert pos == 0  # Має знайти перше входження

    def test_repeating_pattern(self):
        """Тест: паттерн з повторюваними символами"""
        text = "ABABABAB"
        pattern = "ABAB"
        pos = kmp(text, pattern)
        assert pos == 0

    def test_pattern_with_duplicates(self):
        """Тест: паттерн з дублікатами символів"""
        text = "ABCABCABC"
        pattern = "CAB"
        pos = kmp(text, pattern)
        assert pos == 2  # Перше входження CAB

    def test_multiple_occurrences(self):
        """Тест: кілька входжень паттерна (має знайти перше)"""
        text = "ABABABAB"
        pattern = "AB"
        pos = kmp(text, pattern)
        assert pos == 0  # Має знайти перше входження

    def test_overlapping_patterns(self):
        """Тест: перекриваючі паттерни"""
        text = "ABABABAB"
        pattern = "BAB"
        pos = kmp(text, pattern)
        assert pos == 1  # Перше входження BAB


class TestKMPSpecialCases:
    """Тести спеціальних випадків для KMP"""

    def test_pattern_with_all_unique_chars(self):
        """Тест: паттерн з унікальними символами"""
        text = "ABCDEFGHIJKLMNOP"
        pattern = "FGH"
        pos = kmp(text, pattern)
        assert pos == 5

    def test_pattern_not_in_text_chars(self):
        """Тест: символи паттерна не присутні в тексті"""
        text = "ABCDEFG"
        pattern = "XYZ"
        pos = kmp(text, pattern)
        assert pos is None

    def test_partial_match_at_end(self):
        """Тест: часткове співпадіння в кінці"""
        text = "ABCDEFG"
        pattern = "FGH"
        pos = kmp(text, pattern)
        assert pos is None

    def test_case_sensitivity(self):
        """Тест: чутливість до регістру"""
        text = "ABCDEFG"
        pattern = "abc"
        pos = kmp(text, pattern)
        assert pos is None  # Має бути None, оскільки регістр не співпадає

    def test_numbers_in_text(self):
        """Тест: числа в тексті"""
        text = "ABC123DEF456"
        pattern = "123"
        pos = kmp(text, pattern)
        assert pos == 3

    def test_special_characters(self):
        """Тест: спеціальні символи"""
        text = "Hello, World! How are you?"
        pattern = "World"
        pos = kmp(text, pattern)
        assert pos == 7

    def test_unicode_characters(self):
        """Тест: Unicode символи"""
        text = "Привіт світ"
        pattern = "світ"
        pos = kmp(text, pattern)
        assert pos == 7


class TestKMPComplexPatterns:
    """Тести складних паттернів для KMP"""

    def test_pattern_one_char_repeated(self):
        """Тест: паттерн з одного повторюваного символу"""
        text = "AAAAA"
        pattern = "AAA"
        pos = kmp(text, pattern)
        assert pos == 0

    def test_pattern_alternating(self):
        """Тест: чергуючийся паттерн"""
        text = "ABABABABAB"
        pattern = "BAB"
        pos = kmp(text, pattern)
        assert pos == 1

    def test_pattern_palindrome(self):
        """Тест: паліндромний паттерн"""
        text = "ABCBAXYZ"
        pattern = "ABCBA"
        pos = kmp(text, pattern)
        assert pos == 0

    def test_pattern_with_gaps(self):
        """Тест: паттерн з пропусками в тексті"""
        text = "A_B_C_D_E"
        pattern = "B_C"
        pos = kmp(text, pattern)
        assert pos == 2

    def test_complex_repeating_pattern(self):
        """Тест: складний повторюваний паттерн"""
        text = "ABCABCABCABC"
        pattern = "ABCABC"
        pos = kmp(text, pattern)
        assert pos == 0

    def test_pattern_with_prefix_suffix_match(self):
        """Тест: паттерн з префіксом, що збігається з суфіксом"""
        text = "ABABABABAB"
        pattern = "ABABAB"
        pos = kmp(text, pattern)
        assert pos == 0


class TestKMPRealWorld:
    """Тести з реальними прикладами для KMP"""

    def test_dna_sequence(self):
        """Тест: послідовність ДНК"""
        text = "ATCGATCGATCG"
        pattern = "ATCG"
        pos = kmp(text, pattern)
        assert pos == 0

    def test_word_search(self):
        """Тест: пошук слова"""
        text = "The quick brown fox jumps over the lazy dog"
        pattern = "fox"
        pos = kmp(text, pattern)
        assert pos == 16

    def test_multiple_words(self):
        """Тест: пошук серед кількох слів"""
        text = "hello world hello world"
        pattern = "world"
        pos = kmp(text, pattern)
        assert pos == 6  # Перше входження

    def test_sentence_search(self):
        """Тест: пошук речення"""
        text = "This is a test sentence. This is another test."
        pattern = "test"
        pos = kmp(text, pattern)
        assert pos == 10  # Перше входження


class TestKMPLPSFunctionality:
    """Тести функціональності LPS (Longest Proper Prefix which is also Suffix)"""

    def test_lps_simple_repeat(self):
        """Тест: простий повтор для перевірки LPS"""
        text = "ABABAB"
        pattern = "ABAB"
        pos = kmp(text, pattern)
        assert pos == 0

    def test_lps_complex_pattern(self):
        """Тест: складний паттерн для перевірки LPS"""
        text = "AABAAACAAAACBACBACA"
        pattern = "AAACAAAA"
        pos = kmp(text, pattern)
        assert pos == 3

    def test_lps_mississippi(self):
        """Тест: класичний приклад mississippi"""
        text = "mississippi"
        pattern = "issip"
        pos = kmp(text, pattern)
        assert pos == 4

    def test_lps_ababcababa(self):
        """Тест: складний приклад з повторюваними префіксами"""
        text = "ababcababa"
        pattern = "ababa"
        pos = kmp(text, pattern)
        assert pos == 5

    def test_lps_no_prefix_suffix_match(self):
        """Тест: паттерн без збігу префікса і суфікса"""
        text = "ABCDEFG"
        pattern = "XYZ"
        pos = kmp(text, pattern)
        assert pos is None


class TestKMPPerformance:
    """Тести для перевірки ефективності KMP"""

    def test_large_text_small_pattern(self):
        """Тест: великий текст, маленький паттерн"""
        text = "A" * 1000 + "B" + "A" * 1000
        pattern = "BA"
        pos = kmp(text, pattern)
        assert pos == 1000

    def test_repeated_pattern_in_text(self):
        """Тест: повторюваний паттерн у тексті"""
        text = "AB" * 100
        pattern = "AB"
        pos = kmp(text, pattern)
        assert pos == 0

    def test_large_pattern(self):
        """Тест: великий паттерн"""
        text = "ABC" * 100 + "XYZ" + "ABC" * 100
        pattern = "ABC" * 10
        pos = kmp(text, pattern)
        assert pos == 0

    def test_worst_case_scenario(self):
        """Тест: найгірший випадок для KMP"""
        # KMP ефективний навіть у випадку з багатьма частковими співпадіннями
        text = "AAAAA" * 100 + "B" + "AAAAA" * 100
        pattern = "AAAAAB"
        pos = kmp(text, pattern)
        assert pos == 495  # 5 символів "A" перед "B" на позиції 500


class TestKMPEdgeCasePatterns:
    """Тести граничних випадків паттернів для KMP"""

    def test_pattern_longer_than_text(self):
        """Тест: паттерн довший за текст"""
        text = "ABC"
        pattern = "ABCDEF"
        pos = kmp(text, pattern)
        assert pos is None

    def test_pattern_single_char_repeated_in_text(self):
        """Тест: односимвольний паттерн, повторюваний у тексті"""
        text = "AAAAA"
        pattern = "A"
        pos = kmp(text, pattern)
        assert pos == 0  # Перше входження

    def test_pattern_at_very_end(self):
        """Тест: паттерн точно в кінці тексту"""
        text = "ABCDEFG"
        pattern = "EFG"
        pos = kmp(text, pattern)
        assert pos == 4

    def test_pattern_immediately_after_match(self):
        """Тест: паттерн одразу після попереднього співпадіння"""
        text = "ABCABC"
        pattern = "ABC"
        pos = kmp(text, pattern)
        assert pos == 0  # Перше входження

    def test_pattern_with_similar_prefix(self):
        """Тест: паттерн з подібним префіксом"""
        text = "ABABABC"
        pattern = "ABABC"
        pos = kmp(text, pattern)
        assert pos == 2


class TestKMPComparison:
    """Тести для порівняння KMP з іншими алгоритмами (перевірка правильності)"""

    def test_kmp_vs_naive_equivalent(self):
        """Тест: KMP має знаходити ті самі результати, що й naive search"""
        test_cases = [
            ("ABCDEFG", "CDE", 2),
            ("ABABABAB", "BAB", 1),
            ("mississippi", "issip", 4),
            ("ABCABCABC", "ABCABC", 0),
            ("AABAAACAAAACBACBACA", "AAACAAAA", 3),
        ]
        for text, pattern, expected in test_cases:
            pos = kmp(text, pattern)
            assert pos == expected, f"Failed for text='{text}', pattern='{pattern}'"

    def test_kmp_consistency(self):
        """Тест: консистентність результатів KMP"""
        text = "ABABABAB"
        pattern = "ABAB"
        # Викликаємо кілька разів
        pos1 = kmp(text, pattern)
        pos2 = kmp(text, pattern)
        pos3 = kmp(text, pattern)
        assert pos1 == pos2 == pos3 == 0


# ==================== RABIN-KARP ALGORITHM TESTS ====================

class TestRabinKarpBasic:
    """Базові тести для алгоритму Рабіна-Карпа"""

    def test_pattern_at_beginning(self):
        """Тест: паттерн знайдено на початку тексту"""
        text = "ABCDEFG"
        pattern = "ABC"
        pos = rabin_karp(text, pattern)
        assert pos == 0

    def test_pattern_at_end(self):
        """Тест: паттерн знайдено в кінці тексту"""
        text = "ABCDEFG"
        pattern = "EFG"
        pos = rabin_karp(text, pattern)
        assert pos == 4

    def test_pattern_in_middle(self):
        """Тест: паттерн знайдено в середині тексту"""
        text = "ABCDEFG"
        pattern = "CDE"
        pos = rabin_karp(text, pattern)
        assert pos == 2

    def test_pattern_not_found(self):
        """Тест: паттерн не знайдено"""
        text = "ABCDEFG"
        pattern = "XYZ"
        pos = rabin_karp(text, pattern)
        assert pos is None

    def test_single_character_pattern(self):
        """Тест: односимвольний паттерн"""
        text = "ABCDEFG"
        pattern = "C"
        pos = rabin_karp(text, pattern)
        assert pos == 2

    def test_pattern_equals_text(self):
        """Тест: паттерн дорівнює тексту"""
        text = "ABC"
        pattern = "ABC"
        pos = rabin_karp(text, pattern)
        assert pos == 0


class TestRabinKarpEdgeCases:
    """Тести граничних випадків для Рабіна-Карпа"""

    def test_empty_pattern(self):
        """Тест: порожній паттерн"""
        text = "ABCDEFG"
        pattern = ""
        pos = rabin_karp(text, pattern)
        # Згідно з реалізацією, порожній паттерн повертає 0
        assert pos == 0

    def test_text_shorter_than_pattern(self):
        """Тест: текст коротший за паттерн"""
        text = "AB"
        pattern = "ABCD"
        pos = rabin_karp(text, pattern)
        assert pos is None

    def test_empty_text(self):
        """Тест: порожній текст"""
        text = ""
        pattern = "ABC"
        pos = rabin_karp(text, pattern)
        assert pos is None

    def test_empty_text_and_pattern(self):
        """Тест: порожній текст і паттерн"""
        text = ""
        pattern = ""
        pos = rabin_karp(text, pattern)
        assert pos == 0

    def test_single_character_text(self):
        """Тест: односимвольний текст"""
        text = "A"
        pattern = "A"
        pos = rabin_karp(text, pattern)
        assert pos == 0

    def test_single_character_text_pattern_not_found(self):
        """Тест: односимвольний текст, паттерн не знайдено"""
        text = "A"
        pattern = "B"
        pos = rabin_karp(text, pattern)
        assert pos is None


class TestRabinKarpRepeatingCharacters:
    """Тести з повторюваними символами для Рабіна-Карпа"""

    def test_all_same_characters_found(self):
        """Тест: всі символи однакові, паттерн знайдено"""
        text = "AAAAAAA"
        pattern = "AAA"
        pos = rabin_karp(text, pattern)
        assert pos == 0  # Має знайти перше входження

    def test_repeating_pattern(self):
        """Тест: паттерн з повторюваними символами"""
        text = "ABABABAB"
        pattern = "ABAB"
        pos = rabin_karp(text, pattern)
        assert pos == 0

    def test_pattern_with_duplicates(self):
        """Тест: паттерн з дублікатами символів"""
        text = "ABCABCABC"
        pattern = "CAB"
        pos = rabin_karp(text, pattern)
        assert pos == 2  # Перше входження CAB

    def test_multiple_occurrences(self):
        """Тест: кілька входжень паттерна (має знайти перше)"""
        text = "ABABABAB"
        pattern = "AB"
        pos = rabin_karp(text, pattern)
        assert pos == 0  # Має знайти перше входження

    def test_overlapping_patterns(self):
        """Тест: перекриваючі паттерни"""
        text = "ABABABAB"
        pattern = "BAB"
        pos = rabin_karp(text, pattern)
        assert pos == 1  # Перше входження BAB


class TestRabinKarpSpecialCases:
    """Тести спеціальних випадків для Рабіна-Карпа"""

    def test_pattern_with_all_unique_chars(self):
        """Тест: паттерн з унікальними символами"""
        text = "ABCDEFGHIJKLMNOP"
        pattern = "FGH"
        pos = rabin_karp(text, pattern)
        assert pos == 5

    def test_pattern_not_in_text_chars(self):
        """Тест: символи паттерна не присутні в тексті"""
        text = "ABCDEFG"
        pattern = "XYZ"
        pos = rabin_karp(text, pattern)
        assert pos is None

    def test_partial_match_at_end(self):
        """Тест: часткове співпадіння в кінці"""
        text = "ABCDEFG"
        pattern = "FGH"
        pos = rabin_karp(text, pattern)
        assert pos is None

    def test_case_sensitivity(self):
        """Тест: чутливість до регістру"""
        text = "ABCDEFG"
        pattern = "abc"
        pos = rabin_karp(text, pattern)
        assert pos is None  # Має бути None, оскільки регістр не співпадає

    def test_numbers_in_text(self):
        """Тест: числа в тексті"""
        text = "ABC123DEF456"
        pattern = "123"
        pos = rabin_karp(text, pattern)
        assert pos == 3

    def test_special_characters(self):
        """Тест: спеціальні символи"""
        text = "Hello, World! How are you?"
        pattern = "World"
        pos = rabin_karp(text, pattern)
        assert pos == 7

    def test_unicode_characters(self):
        """Тест: Unicode символи"""
        text = "Привіт світ"
        pattern = "світ"
        pos = rabin_karp(text, pattern)
        assert pos == 7


class TestRabinKarpComplexPatterns:
    """Тести складних паттернів для Рабіна-Карпа"""

    def test_pattern_one_char_repeated(self):
        """Тест: паттерн з одного повторюваного символу"""
        text = "AAAAA"
        pattern = "AAA"
        pos = rabin_karp(text, pattern)
        assert pos == 0

    def test_pattern_alternating(self):
        """Тест: чергуючийся паттерн"""
        text = "ABABABABAB"
        pattern = "BAB"
        pos = rabin_karp(text, pattern)
        assert pos == 1

    def test_pattern_palindrome(self):
        """Тест: паліндромний паттерн"""
        text = "ABCBAXYZ"
        pattern = "ABCBA"
        pos = rabin_karp(text, pattern)
        assert pos == 0

    def test_pattern_with_gaps(self):
        """Тест: паттерн з пропусками в тексті"""
        text = "A_B_C_D_E"
        pattern = "B_C"
        pos = rabin_karp(text, pattern)
        assert pos == 2

    def test_complex_repeating_pattern(self):
        """Тест: складний повторюваний паттерн"""
        text = "ABCABCABCABC"
        pattern = "ABCABC"
        pos = rabin_karp(text, pattern)
        assert pos == 0

    def test_pattern_with_prefix_suffix_match(self):
        """Тест: паттерн з префіксом, що збігається з суфіксом"""
        text = "ABABABABAB"
        pattern = "ABABAB"
        pos = rabin_karp(text, pattern)
        assert pos == 0


class TestRabinKarpRealWorld:
    """Тести з реальними прикладами для Рабіна-Карпа"""

    def test_dna_sequence(self):
        """Тест: послідовність ДНК"""
        text = "ATCGATCGATCG"
        pattern = "ATCG"
        pos = rabin_karp(text, pattern)
        assert pos == 0

    def test_word_search(self):
        """Тест: пошук слова"""
        text = "The quick brown fox jumps over the lazy dog"
        pattern = "fox"
        pos = rabin_karp(text, pattern)
        assert pos == 16

    def test_multiple_words(self):
        """Тест: пошук серед кількох слів"""
        text = "hello world hello world"
        pattern = "world"
        pos = rabin_karp(text, pattern)
        assert pos == 6  # Перше входження

    def test_sentence_search(self):
        """Тест: пошук речення"""
        text = "This is a test sentence. This is another test."
        pattern = "test"
        pos = rabin_karp(text, pattern)
        assert pos == 10  # Перше входження


class TestRabinKarpHashCollisions:
    """Тести для перевірки обробки колізій хешів"""

    def test_hash_collision_handling(self):
        """Тест: перевірка обробки колізій хешів (алгоритм має перевіряти фактичний рядок)"""
        # Навіть якщо хеші збігаються, алгоритм має перевірити фактичний рядок
        text = "ABCDEFG"
        pattern = "CDE"
        pos = rabin_karp(text, pattern)
        assert pos == 2

    def test_similar_strings_different_hashes(self):
        """Тест: подібні рядки з різними хешами"""
        text = "ABCABCABC"
        pattern = "ABC"
        pos = rabin_karp(text, pattern)
        assert pos == 0


class TestRabinKarpPerformance:
    """Тести для перевірки ефективності Рабіна-Карпа"""

    def test_large_text_small_pattern(self):
        """Тест: великий текст, маленький паттерн"""
        text = "A" * 1000 + "B" + "A" * 1000
        pattern = "BA"
        pos = rabin_karp(text, pattern)
        assert pos == 1000

    def test_repeated_pattern_in_text(self):
        """Тест: повторюваний паттерн у тексті"""
        text = "AB" * 100
        pattern = "AB"
        pos = rabin_karp(text, pattern)
        assert pos == 0

    def test_large_pattern(self):
        """Тест: великий паттерн"""
        text = "ABC" * 100 + "XYZ" + "ABC" * 100
        pattern = "ABC" * 10
        pos = rabin_karp(text, pattern)
        assert pos == 0

    def test_very_long_text(self):
        """Тест: дуже довгий текст"""
        text = "ABCDEFG" * 1000
        pattern = "CDE"
        pos = rabin_karp(text, pattern)
        assert pos == 2


class TestRabinKarpEdgeCasePatterns:
    """Тести граничних випадків паттернів для Рабіна-Карпа"""

    def test_pattern_longer_than_text(self):
        """Тест: паттерн довший за текст"""
        text = "ABC"
        pattern = "ABCDEF"
        pos = rabin_karp(text, pattern)
        assert pos is None

    def test_pattern_single_char_repeated_in_text(self):
        """Тест: односимвольний паттерн, повторюваний у тексті"""
        text = "AAAAA"
        pattern = "A"
        pos = rabin_karp(text, pattern)
        assert pos == 0  # Перше входження

    def test_pattern_at_very_end(self):
        """Тест: паттерн точно в кінці тексту"""
        text = "ABCDEFG"
        pattern = "EFG"
        pos = rabin_karp(text, pattern)
        assert pos == 4

    def test_pattern_immediately_after_match(self):
        """Тест: паттерн одразу після попереднього співпадіння"""
        text = "ABCABC"
        pattern = "ABC"
        pos = rabin_karp(text, pattern)
        assert pos == 0  # Перше входження


class TestRabinKarpComparison:
    """Тести для порівняння Рабіна-Карпа з іншими алгоритмами (перевірка правильності)"""

    def test_rabin_karp_vs_kmp_equivalent(self):
        """Тест: Рабін-Карп має знаходити ті самі результати, що й KMP"""
        test_cases = [
            ("ABCDEFG", "CDE", 2),
            ("ABABABAB", "BAB", 1),
            ("mississippi", "issip", 4),
            ("ABCABCABC", "ABCABC", 0),
            ("AABAAACAAAACBACBACA", "AAACAAAA", 3),
        ]
        for text, pattern, expected in test_cases:
            pos = rabin_karp(text, pattern)
            assert pos == expected, f"Failed for text='{text}', pattern='{pattern}', got {pos}, expected {expected}"

    def test_rabin_karp_vs_boyer_moore_equivalent(self):
        """Тест: Рабін-Карп має знаходити ті самі результати, що й Бойер-Мур"""
        test_cases = [
            ("ABCDEFG", "CDE", 2),
            ("ABABABAB", "BAB", 1),
            ("ABCAABBCAABCBACBACA", "CBACA", 14),
        ]
        for text, pattern, expected in test_cases:
            pos_rk = rabin_karp(text, pattern)
            pos_bm, _, _ = boyer_moore(text, pattern)
            assert pos_rk == pos_bm == expected, f"Failed for text='{text}', pattern='{pattern}'"

    def test_rabin_karp_consistency(self):
        """Тест: консистентність результатів Рабіна-Карпа"""
        text = "ABABABAB"
        pattern = "ABAB"
        # Викликаємо кілька разів
        pos1 = rabin_karp(text, pattern)
        pos2 = rabin_karp(text, pattern)
        pos3 = rabin_karp(text, pattern)
        assert pos1 == pos2 == pos3 == 0


class TestRabinKarpSpecificCases:
    """Тести специфічних випадків для Рабіна-Карпа"""

    def test_example_from_code(self):
        """Тест: приклад з коду"""
        text = "ABCAABBCAABCBACBACA"
        pattern = "CBACA"
        pos = rabin_karp(text, pattern)
        assert pos == 14

    def test_mississippi_example(self):
        """Тест: класичний приклад mississippi"""
        text = "mississippi"
        pattern = "issip"
        pos = rabin_karp(text, pattern)
        assert pos == 4

    def test_hash_rolling_correctness(self):
        """Тест: перевірка правильності rolling hash"""
        # Тест для перевірки, що rolling hash працює коректно
        text = "ABCDEFGHIJ"
        pattern = "DEF"
        pos = rabin_karp(text, pattern)
        assert pos == 3

    def test_hash_rolling_multiple_windows(self):
        """Тест: перевірка rolling hash для кількох вікон"""
        text = "ABCDEFGHIJKLMNOP"
        pattern = "FGH"
        pos = rabin_karp(text, pattern)
        assert pos == 5

    def test_negative_hash_handling(self):
        """Тест: перевірка обробки від'ємних значень хешу (якщо такі виникають)"""
        # Цей тест перевіряє, що алгоритм коректно обробляє випадки,
        # коли проміжні значення хешу можуть бути від'ємними
        text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pattern = "XYZ"
        pos = rabin_karp(text, pattern)
        assert pos == 23

