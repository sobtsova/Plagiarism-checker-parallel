import multiprocessing
import hashlib
from core.analyzer import canonicalize_logic

_target_hashes = None
_k = None
_stop_words = None

def _init_worker(target_hashes, k, stop_words):
    global _target_hashes, _k, _stop_words
    _target_hashes = target_hashes
    _k = k
    _stop_words = stop_words

def _worker_task(db_text):
    global _target_hashes, _k, _stop_words
    tokens = canonicalize_logic(db_text, _stop_words)
    
    db_hashes = set()
    for i in range(len(tokens) - _k + 1):
        shingle = " ".join(tokens[i : i + _k]).encode('utf-8')
        h = int.from_bytes(hashlib.md5(shingle).digest()[:8], 'little')
        db_hashes.add(h)
    
    if not _target_hashes or not db_hashes: return 0.0
    return (len(_target_hashes & db_hashes) / len(_target_hashes | db_hashes)) * 100

def parallel_analyze_database(target_text, db_texts, num_processes, k_size=7):
    from core.analyzer import ShingleAnalyzer
    analyzer = ShingleAnalyzer(shingle_size=k_size)
    
    target_tokens = analyzer.canonicalize(target_text)
    target_hashes = analyzer.create_hashes(target_tokens)

    with multiprocessing.Pool(
        processes=num_processes,
        initializer=_init_worker,
        initargs=(target_hashes, k_size, analyzer.stop_words)
    ) as pool:
        results = pool.map(_worker_task, db_texts)

    return results

def parallel_analyze_full(text_a, text_b, num_processes, k_size=7):
    results = parallel_analyze_database(text_a, [text_b], num_processes, k_size)

    return results[0] if results else 0.0