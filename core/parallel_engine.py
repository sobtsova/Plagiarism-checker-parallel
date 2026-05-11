import multiprocessing
import hashlib
from core.analyzer import ShingleAnalyzer

def _worker_hashing(args):
    tokens_chunk, k = args
    hashes = set()
    
    for i in range(len(tokens_chunk) - k + 1):
        shingle = " ".join(tokens_chunk[i : i + k])
        h = hashlib.sha256(shingle.encode('utf-8')).hexdigest()
        hashes.add(h)
    return hashes

def parallel_analyze_full(text_a, text_b, num_processes, k_size=7):
    analyzer = ShingleAnalyzer(shingle_size=k_size)

    tokens_a = analyzer.canonicalize(text_a)
    tokens_b = analyzer.canonicalize(text_b)

    def get_token_chunks(tokens, n, k):
        if not tokens or len(tokens) < k: return []
        chunk_size = max(len(tokens) // n, 1)
        chunks = []
        for i in range(n):
            start = i * chunk_size
            end = len(tokens) if i == n - 1 else (i + 1) * chunk_size + (k - 1)
            chunks.append(tokens[start:end])
        return chunks
    
    chunks_a = get_token_chunks(tokens_a, num_processes, k_size)
    chunks_b = get_token_chunks(tokens_b, num_processes, k_size)

    with multiprocessing.Pool(processes=num_processes) as pool:
        res_a = pool.map(_worker_hashing, [(c, k_size) for c in chunks_a])
        res_b = pool.map(_worker_hashing, [(c, k_size) for c in chunks_b])

    final_a = set().union(*res_a) if res_a else set()
    final_b = set().union(*res_b) if res_b else set()

    return analyzer.get_similarity(final_a, final_b)