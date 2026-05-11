from core.analyzer import ShingleAnalyzer
from core.parallel_engine import parallel_analyze_full
from data.generator import generate_vocabulary, generate_test_data

def run_stress_test():
    print("--- СТРЕС-ТЕСТ (1 000 000 слів) ---")
    vocab = generate_vocabulary(100000)
    t1, t2 = generate_test_data(1000000, vocab, similarity_type="partial")
    
    analyzer = ShingleAnalyzer(shingle_size=7)
    
    seq_res = analyzer.analyze(t1, t2)
    par_res = parallel_analyze_full(t1, t2, num_processes=4, k_size=7)
    
    print(f"Послідовно: {seq_res:.4f}%")
    print(f"Паралельно: {par_res:.4f}%")
    print("ВЕРИФІКАЦІЯ УСПІШНА" if seq_res == par_res else "ПОМИЛКА!")
