import os
from os.path import basename
from core.analyzer import ShingleAnalyzer
from core.parallel_engine import parallel_analyze_full

def run_file_comparison_test():
    print("--- 4.3 ВЕРИФІКАЦІЯ НА РЕАЛЬНИХ ТЕКСТОВИХ ФАЙЛАХ ---")
    
    k = 5
    num_procs = 4

    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

    base_file = os.path.join(data_dir, "data1.txt")
    compare_files = [
        os.path.join(data_dir, "data2.txt"),
        os.path.join(data_dir, "data3.txt"),
        os.path.join(data_dir, "data4.txt")
    ]

    for f_name in [base_file] + compare_files:
        if not os.path.exists(f_name):
            print(f"Помилка: Файл {f_name} не знайдено!")
            return

    with open(base_file, "r", encoding="utf-8") as f:
        text_base = f.read()

    analyzer = ShingleAnalyzer(shingle_size=k)

    print(f"{'Файли для порівняння':<30} | {'Послідовно':<12} | {'Паралельно':<12} | {'Статус'}")
    print("-" * 75)

    for other_file in compare_files:
        with open(other_file, "r", encoding="utf-8") as f:
            text_other = f.read()

        res_seq = analyzer.analyze(text_base, text_other)
        res_par = parallel_analyze_full(text_base, text_other, num_processes=num_procs, k_size=k)

        status = "✅ OK" if abs(res_seq - res_par) < 0.0001 else "❌ Error"
        
        comparison_text = f"{basename(base_file)} vs {basename(other_file)}"
        print(f"{comparison_text:<30} | {res_seq:>11.2f}% | {res_par:>11.2f}% | {status}")
