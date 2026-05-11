from core.analyzer import ShingleAnalyzer
from core.parallel_engine import parallel_analyze_full

def run_parallel_unit_tests():
    print("--- 4.3 ВЕРИФІКАЦІЯ КОРЕКТНОСТІ ПАРАЛЕЛЬНОГО АЛГОРИТМУ ---")
    k = 2
    analyzer = ShingleAnalyzer(shingle_size=k)
    
    t1 = "алгоритм обробляє текст для пошуку плагіату"
    t2 = "алгоритм обробляє текст для пошуку плагіату"
    
    seq_res1 = analyzer.analyze(t1, t2)
    par_res1 = parallel_analyze_full(t1, t2, num_processes=2, k_size=k)
    
    print(f"ТЕСТ 1 (Ідентичні): Послідовно {seq_res1:.1f}% | Паралельно {par_res1:.1f}%")
    
    t3 = "алгоритм виконує обробку текстових даних для аналізу"
    t4 = "алгоритм виконує аналіз текстових даних для перевірки"
    
    seq_res2 = analyzer.analyze(t3, t4)
    par_res2 = parallel_analyze_full(t3, t4, num_processes=2, k_size=k)
    
    print(f"ТЕСТ 2 (Часткова схожість): Послідовно {seq_res2:.2f}% | Паралельно {par_res2:.2f}%")
    
    t5 = "алгоритм працює з текстом для виявлення плагіату"
    t6 = "база даних зберігає інформацію про користувачів системи"
    
    seq_res3 = analyzer.analyze(t5, t6)
    par_res3 = parallel_analyze_full(t5, t6, num_processes=2, k_size=k)
    
    print(f"ТЕСТ 3 (Різні): Послідовно {seq_res3:.1f}% | Паралельно {par_res3:.1f}%")

    if seq_res1 == par_res1 and seq_res2 == par_res2 and seq_res3 == par_res3:
        print("\n✅ ПАРАЛЕЛЬНИЙ АЛГОРИТМ ПРАЦЮЄ КОРЕКТНО")
    else:
        print("\n❌ ПОМИЛКА: Результати паралельної версії відрізняються!")