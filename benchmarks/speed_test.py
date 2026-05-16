import time
from core.analyzer import ShingleAnalyzer
from data.generator import generate_vocabulary, generate_test_database

def run_benchmarks():
    analyzer = ShingleAnalyzer(shingle_size=7)
    vocabulary = generate_vocabulary(50000)
    
    print("--- 2.4 ЕКСПЕРИМЕНТАЛЬНІ ЗАМІРИ ШВИДКОДІЇ (Послідовний алгоритм) ---")
    
    words_per_file = 20000  
    db_sizes = [24, 49, 124, 249, 499]
    iterations = 20 
    
    print(f"Фіксований розмір файлу: {words_per_file} слів")
    print(f"{'Кількість файлів':<18} | {'Загалом слів':<15} | {'Середній час (сек)':<20}")
    print("-" * 60)
    
    for num_files in db_sizes:
        target_text, db_texts = generate_test_database(words_per_file, num_files, vocabulary)
        analyzer.analyze_database_sequential(target_text, db_texts)
        total_words = words_per_file * (num_files + 1)
        
        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            analyzer.analyze_database_sequential(target_text, db_texts)
            times.append(time.perf_counter() - start)
        
        avg_time = sum(times) / len(times)
        print(f"{num_files+1:<18} | {total_words:<15} | {avg_time:.6f}")