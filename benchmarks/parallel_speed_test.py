import time
import statistics
import multiprocessing
import csv
import gc
from core.analyzer import ShingleAnalyzer
from core.parallel_engine import parallel_analyze_database 
from data.generator import generate_vocabulary, generate_test_database 

def run_parallel_benchmarks():
    iterations = 20
    words_per_file = 20000 
    db_sizes = [24, 49, 124, 249, 499]
    process_configs = [2, 4, 8, 12]
    k = 7
    
    cpu_count = multiprocessing.cpu_count()
    vocab = generate_vocabulary(50000)
    analyzer_seq = ShingleAnalyzer(shingle_size=k)
    
    csv_filename = "benchmark_database_results.csv"
    csv_header = ['DB_Size_Files', 'Total_Words', 'Processes', 'Avg_Time', 'Speedup', 'Efficiency']
    results_to_save = []

    print(f"--- ЕКСПЕРИМЕНТ: ПОРІВНЯННЯ З БАЗОЮ ДАНИХ (1 to N) ---")
    print(f"Логічних ядер CPU: {cpu_count}")
    print(f"Слів у кожному файлі: {words_per_file}")
    print(f"Кількість ітерацій для осереднення: {iterations}\n")

    for num_files in db_sizes:
        target_text, db_texts = generate_test_database(words_per_file, num_files, vocab)
        total_words = words_per_file * (num_files + 1)
        
        print(f"{'='*75}")
        print(f"ТЕСТ: База з {num_files+1} файлів (Всього обробляється: {total_words} слів)")
        
        seq_times = []
        seq_results = analyzer_seq.analyze_database_sequential(target_text, db_texts)
        
        for i in range(4):
            start = time.perf_counter()
            analyzer_seq.analyze_database_sequential(target_text, db_texts)
            seq_times.append(time.perf_counter() - start)
        
        avg_seq = statistics.mean(seq_times)
        print(f"ПОСЛІДОВНО (P=1): {avg_seq:.4f} сек")
        results_to_save.append([num_files, total_words, 1, avg_seq, 1.0, 1.0])
        
        print(f"{'-'*75}")
        print(f"{'Ядра (P)':<10} | {'Статус':<15} | {'Час Par (сек)':<15} | {'S (Speedup)':<10} | {'E (Eff)'}")
        print(f"{'-'*75}")
        
        for p in process_configs:
            par_results = parallel_analyze_database(target_text, db_texts, num_processes=p, k_size=k)
            
            is_correct = all(abs(s - pr) < 0.1 for s, pr in zip(seq_results, par_results))
            
            if is_correct:
                v_status = "✅ OK"
            else:
                v_status = "❌ ERROR"
                print(f"Критична розбіжність! \nSeq: {seq_results[:3]}...\nPar: {par_results[:3]}...")
                continue

            par_times = []
            for _ in range(iterations):
                start = time.perf_counter()
                parallel_analyze_database(target_text, db_texts, num_processes=p, k_size=k)
                par_times.append(time.perf_counter() - start)
            
            avg_par = statistics.mean(par_times)
            speedup = avg_seq / avg_par
            efficiency = speedup / p
            
            print(f"{p:<10} | {v_status:<15} | {avg_par:<15.4f} | {speedup:<10.2f} | {efficiency:.2f}")
            results_to_save.append([num_files, total_words, p, avg_par, speedup, efficiency])

        print(f"{'='*75}")
        print(f"Очищення пам'яті для тесту {num_files+1} файлів...")
        del target_text, db_texts
        gc.collect() 

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
        writer.writerows(results_to_save)
    
    print(f"\n✅ Експеримент завершено успішно. Результати: {csv_filename}")