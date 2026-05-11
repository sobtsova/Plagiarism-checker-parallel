import random
import string

def generate_vocabulary(vocab_size=100000):
    vocabulary = set()
    while len(vocabulary) < vocab_size:
        word = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 30)))
        vocabulary.add(word)
    return list(vocabulary)

def generate_test_data(size, vocabulary, similarity_type="partial"):
    base_text = [random.choice(vocabulary) for _ in range(size)]
    
    if similarity_type == "partial":
        modified_text = base_text[:]
        for i in range(0, size, 10):
            original_word = modified_text[i]
            new_word = random.choice(vocabulary)
            
            while new_word == original_word:
                new_word = random.choice(vocabulary)
            
            modified_text[i] = new_word
            
        return " ".join(base_text), " ".join(modified_text)
    
    full_text = " ".join(base_text)
    return full_text, full_text