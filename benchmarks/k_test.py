import time
import statistics
import multiprocessing
import csv
import gc
from core.analyzer import ShingleAnalyzer
from core.parallel_engine import parallel_analyze_database 
from data.generator import generate_vocabulary, generate_test_data

def run_k_benchmark():
    iterations = 10
    num_files = 500
    words_per_file = 20000
    processes = 12
    k_values = [2, 3, 5, 7, 10, 15, 20]
    
    cpu_count = multiprocessing.cpu_count()
    vocab = generate_vocabulary(50000)
    
    csv_filename = "benchmark_k_results.csv"
    csv_header = ['k', 'Similarity', 'Seq_Time', 'Par_Time', 'Speedup', 'Efficiency']
    results_to_save = []

    print(f"--- ЕКСПЕРИМЕНТ: ВПЛИВ ДОВЖИНИ ШИНГЛА (k) ---")
    print(f"Логічних ядер CPU: {cpu_count}")
    print(f"База даних: {num_files} файлів (загалом {num_files * words_per_file} слів)")
    print(f"Процесів: {processes} | Ітерацій: {iterations}\n")

    text_a, base_db_text = generate_test_data(words_per_file, vocab, "partial")
    db_texts = [base_db_text] * num_files
    
    print(f"{'='*90}")
    print(f"{'k':<10} | {'Схожість (%)':<15} | {'Час Seq (с)':<15} | {'Час Par (с)':<15} | {'S (Speedup)':<12} | {'E (Eff)'}")
    print(f"{'-'*90}")

    for k in k_values:
        analyzer_seq = ShingleAnalyzer(shingle_size=k)
        
        seq_warmup_results = analyzer_seq.analyze_database_sequential(text_a, db_texts)
        par_warmup_results = parallel_analyze_database(text_a, db_texts, num_processes=processes, k_size=k)
        
        seq_warmup = seq_warmup_results[0]
        par_warmup = par_warmup_results[0]
        
        if abs(seq_warmup - par_warmup) > 1e-7:
            print(f"❌ ERROR: Критична розбіжність для k={k}: Seq={seq_warmup}, Par={par_warmup}")
            continue
            
        gc.collect()
        
        seq_times = []
        for _ in range(iterations):
            start = time.perf_counter()
            analyzer_seq.analyze_database_sequential(text_a, db_texts)
            seq_times.append(time.perf_counter() - start)
            
        avg_seq = statistics.mean(seq_times)
        
        gc.collect()
        
        par_times = []
        for _ in range(iterations):
            start = time.perf_counter()
            parallel_analyze_database(text_a, db_texts, num_processes=processes, k_size=k)
            par_times.append(time.perf_counter() - start)
            
        avg_par = statistics.mean(par_times)
        
        speedup = avg_seq / avg_par
        efficiency = speedup / processes
        
        print(f"{k:<10} | {seq_warmup:<15.4f} | {avg_seq:<15.4f} | {avg_par:<15.4f} | {speedup:<12.2f} | {efficiency:.2f}")
        
        results_to_save.append([k, seq_warmup, avg_seq, avg_par, speedup, efficiency])
        
        gc.collect()

    del text_a, base_db_text, db_texts
    gc.collect() 

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
        writer.writerows(results_to_save)
    
    print(f"\n✅ Експеримент завершено успішно. Результати: {csv_filename}")