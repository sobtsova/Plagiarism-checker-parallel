import time
import statistics
import multiprocessing
import csv
import gc
from core.analyzer import ShingleAnalyzer
from core.parallel_engine import parallel_analyze_full
from data.generator import generate_vocabulary, generate_test_data

def run_parallel_benchmarks():
    iterations = 20
    sizes = [100000, 500000, 1000000, 2500000, 5000000, 10000000] 
    process_configs = [4, 8, 12, 20]
    k = 7
    
    cpu_count = multiprocessing.cpu_count()
    vocab = generate_vocabulary(50000)
    analyzer_seq = ShingleAnalyzer(shingle_size=k)
    
    csv_filename = "benchmark_results.csv"
    csv_header = ['Size_Words', 'Size_MB', 'Processes', 'Avg_Time', 'Speedup', 'Efficiency']
    results_to_save = []

    print(f"--- ПОВНИЙ ЕКСПЕРИМЕНТ ПАРАЛЕЛЬНИХ ОБЧИСЛЕНЬ ---")
    print(f"Логічних ядер CPU: {cpu_count}")
    print(f"Метод верифікації: Порівняння хеш-сум (точність 1e-7)")
    print(f"Кількість ітерацій для осереднення: {iterations}\n")

    for size in sizes:
        text_a, text_b = generate_test_data(size, vocab, "partial")
        mb_size = (len(text_a.encode('utf-8')) + len(text_b.encode('utf-8'))) / (1024 * 1024)
        
        print(f"{'='*70}")
        print(f"ТЕСТ: {size} слів ({mb_size:.2f} MB)")
        
        seq_times = []
        seq_result = analyzer_seq.analyze(text_a, text_b)
        
        for i in range(iterations):
            start = time.perf_counter()
            analyzer_seq.analyze(text_a, text_b)
            seq_times.append(time.perf_counter() - start)
        
        avg_seq = statistics.mean(seq_times)
        print(f"ПОСЛІДОВНО (P=1): {avg_seq:.4f} сек")
        results_to_save.append([size, mb_size, 1, avg_seq, 1.0, 1.0])
        
        print(f"{'-'*70}")
        print(f"{'Ядра (P)':<10} | {'Статус':<15} | {'Час Par (сек)':<15} | {'S (Speedup)':<10} | {'E (Eff)'}")
        print(f"{'-'*70}")
        
        for p in process_configs:
            par_result = parallel_analyze_full(text_a, text_b, num_processes=p, k_size=k)
            
            if abs(seq_result - par_result) < 1e-7:
                v_status = "✅ OK"
            else:
                v_status = "❌ ERROR"
                print(f"Критична розбіжність: Seq={seq_result}, Par={par_result}")
                continue

            par_times = []
            for _ in range(iterations):
                start = time.perf_counter()
                parallel_analyze_full(text_a, text_b, num_processes=p, k_size=k)
                par_times.append(time.perf_counter() - start)
            
            avg_par = statistics.mean(par_times)
            speedup = avg_seq / avg_par
            efficiency = speedup / p
            
            print(f"{p:<10} | {v_status:<15} | {avg_par:<15.4f} | {speedup:<10.2f} | {efficiency:.2f}")
            results_to_save.append([size, mb_size, p, avg_par, speedup, efficiency])

        print(f"{'='*70}")
        print(f"Очищення пам'яті для тесту {size} слів...")
        del text_a, text_b
        gc.collect() 

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
        writer.writerows(results_to_save)
    
    print(f"\n✅ Експеримент завершено успішно. Результати: {csv_filename}")
