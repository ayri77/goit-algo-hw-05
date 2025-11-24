'''
Порівняйте ефективність алгоритмів пошуку підрядка: Боєра-Мура, Кнута-Морріса-Пратта та Рабіна-Карпа 
на основі двох текстових файлів (стаття 1, стаття 2). Використовуючи timeit, треба виміряти час виконання 
кожного алгоритму для двох видів підрядків: одного, що дійсно існує в тексті, та іншого — вигаданого 
(вибір підрядків за вашим бажанням). На основі отриманих даних визначте найшвидший алгоритм для кожного тексту окремо та в цілому.
'''

from pathlib import Path
import timeit
from substring_search import boyer_moore, kmp, rabin_karp
import pandas as pd

def load_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="ignore")

def pick_existing(text: str, length: int = 20) -> str:
    # deterministic: take a middle slice
    start = len(text) // 2
    return text[start:start+length]

def make_fake(existing: str) -> str:
    # guaranteed different (simple perturbation)
    return existing[::-1] + "XYZ"    

def measure(func, text, pattern, number=5, repeat=5):
    stmt = lambda: func(text, pattern)
    times = timeit.repeat(stmt, number=number, repeat=repeat)
    return min(times) / number  # avg best-run

def benchmark(algos, text, patterns):
    out = []
    for pname, pat in patterns.items():
        for aname, afunc in algos.items():
            t = measure(afunc, text, pat)
            out.append((aname, pname, t))
    return out    


def run_all(algos, text1, text2):
    ex1 = pick_existing(text1)
    fk1 = make_fake(ex1)
    ex2 = pick_existing(text2)
    fk2 = make_fake(ex2)

    patterns1 = {"existing": ex1, "fake": fk1}
    patterns2 = {"existing": ex2, "fake": fk2}

    res1 = benchmark(algos, text1, patterns1)
    res2 = benchmark(algos, text2, patterns2)

    df1 = pd.DataFrame(res1, columns=["algo", "pattern_type", "time_s"])
    df1["text"] = "article1"

    df2 = pd.DataFrame(res2, columns=["algo", "pattern_type", "time_s"])
    df2["text"] = "article2"

    return pd.concat([df1, df2], ignore_index=True)

def winners(df):
    by_text = df.groupby(["text", "pattern_type"])["time_s"].idxmin()
    overall = df.groupby(["pattern_type"])["time_s"].idxmin()
    return df.loc[by_text], df.loc[overall]

def main():
    algos = {
        "boyer_moore": boyer_moore,
        "kmp": kmp,
        "rabin_karp": rabin_karp,
    }

    text1 = load_text("./data/стаття 1.txt")
    text2 = load_text("./data/стаття 2.txt")

    # patterns
    ex1 = pick_existing(text1)
    fk1 = make_fake(ex1)
    ex2 = pick_existing(text2)
    fk2 = make_fake(ex2)

    assert ex1 in text1 and fk1 not in text1
    assert ex2 in text2 and fk2 not in text2

    patterns1 = {"existing": ex1, "fake": fk1}
    patterns2 = {"existing": ex2, "fake": fk2}

    res1 = benchmark(algos, text1, patterns1)
    res2 = benchmark(algos, text2, patterns2)

    df1 = pd.DataFrame(res1, columns=["algo", "pattern_type", "time_s"])
    df1["text"] = "article1"
    df2 = pd.DataFrame(res2, columns=["algo", "pattern_type", "time_s"])
    df2["text"] = "article2"
    df = pd.concat([df1, df2], ignore_index=True)

    by_text_winners, overall_winners = winners(df)

    print("\n=== Raw results ===")
    print(df.sort_values(["text", "pattern_type", "time_s"]))

    print("\n=== Winners per text & pattern type ===")
    print(by_text_winners.sort_values(["text", "pattern_type"]))

    print("\n=== Overall winners per pattern type ===")
    print(overall_winners.sort_values(["pattern_type"]))

    # optionally save
    df.to_csv("benchmark_results.csv", index=False)

if __name__ == "__main__":
    main()
