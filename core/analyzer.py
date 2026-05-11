import re
import hashlib

class ShingleAnalyzer:
    def __init__(self, shingle_size=7):
        self.k = shingle_size
        self.stop_words = {'і', 'та', 'на', 'в', 'що', 'як', 'якщо', 'але', 'це', 'про', 'до'}

    def canonicalize(self, text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        words = text.split()
        return [w for w in words if w not in self.stop_words]

    def create_hashes(self, words):
        if len(words) < self.k:
            return set()
        hashes = set()
        for i in range(len(words) - self.k + 1):
            shingle = " ".join(words[i : i + self.k])
            h = hashlib.sha256(shingle.encode('utf-8')).hexdigest()
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