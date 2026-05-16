import hashlib
import string

def canonicalize_logic(text, stop_words):
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator).lower()
    words = text.split()
    return [w for w in words if w not in stop_words]

class ShingleAnalyzer:
    def analyze_database_sequential(self, target_text, db_texts):
        """Послідовно порівнює цільовий файл із базою"""
        target_tokens = self.canonicalize(target_text)
        target_hashes = self.create_hashes(target_tokens)
        
        results = []
        for db_text in db_texts:
            db_tokens = self.canonicalize(db_text)
            db_hashes = self.create_hashes(db_tokens)
            sim = self.get_similarity(target_hashes, db_hashes)
            results.append(sim)
        return results
    
    def __init__(self, shingle_size=7):
        self.k = shingle_size
        self.stop_words = {'і', 'та', 'на', 'в', 'що', 'як', 'якщо', 'але', 'це', 'про', 'до', 'для'}
        self.translator = str.maketrans('', '', string.punctuation)

    def canonicalize(self, text):
        return canonicalize_logic(text, self.stop_words)

    def create_hashes(self, words):
        if len(words) < self.k:
            return set()
        hashes = set()
        for i in range(len(words) - self.k + 1):
            shingle = " ".join(words[i : i + self.k]).encode('utf-8')
            h = int.from_bytes(hashlib.md5(shingle).digest()[:8], 'little')
            hashes.add(h)
        return hashes

    def get_similarity(self, set_a, set_b):
        if not set_a or not set_b:
            return 0.0
        intersection = len(set_a.intersection(set_b))
        union = len(set_a.union(set_b))
        return (intersection / union) * 100

    def analyze(self, text_a, text_b):
        tokens_a = self.canonicalize(text_a)
        tokens_b = self.canonicalize(text_b)
        hashes_a = self.create_hashes(tokens_a)
        hashes_b = self.create_hashes(tokens_b)
        return self.get_similarity(hashes_a, hashes_b)