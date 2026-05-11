import time
from core.analyzer import ShingleAnalyzer
from data.generator import generate_vocabulary, generate_test_data

def run_benchmarks():
    analyzer = ShingleAnalyzer(shingle_size=7)
    vocabulary = generate_vocabulary(50000)
    
    print("--- 2.4 ЕКСПЕРИМЕНТАЛЬНІ ЗАМІРИ ШВИДКОДІЇ ---")
    sizes = [100000, 500000, 1000000, 2500000, 5000000, 10000000]
    
    print(f"{'Кількість слів':<15} | {'Обʼєм (МБ)':<12} | {'Середній час (сек)':<20}")
    print("-" * 55)
    
    for size in sizes:
        text_a, text_b = generate_test_data(size, vocabulary, "partial")
        
        bytes_size = (len(text_a.encode('utf-8')) + len(text_b.encode('utf-8')))
        mb_size = bytes_size / (1024 * 1024)
        
        times = []
        for _ in range(10):
            start = time.perf_counter()
            analyzer.analyze(text_a, text_b)
            times.append(time.perf_counter() - start)
        
        avg_time = sum(times) / len(times)
        print(f"{size:<15} | {mb_size:<12.2f} | {avg_time:.6f}")