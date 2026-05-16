import random

def generate_vocabulary(vocab_size=50000):
    vocabulary = set()
    while len(vocabulary) < vocab_size:
        ukrainian_alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
        word = ''.join(random.choices(ukrainian_alphabet, k=random.randint(1, 30)))
        vocabulary.add(word)
    return list(vocabulary)

def generate_test_database(size_per_file, num_files, vocabulary):
    base_words = [random.choice(vocabulary) for _ in range(size_per_file)]
    target_text = " ".join(base_words)

    database_texts = []
    for i in range(num_files):
        if i % 3 == 0:
            modified = base_words[:]
            for j in range(0, size_per_file, 5):
                modified[j] = random.choice(vocabulary)
            database_texts.append(" ".join(modified))
        elif i % 3 == 1:
            random_text = [random.choice(vocabulary) for _ in range(size_per_file)]
            database_texts.append(" ".join(random_text))
        else:
            modified = base_words[:]
            for j in range(0, size_per_file, 20):
                modified[j] = random.choice(vocabulary)
            database_texts.append(" ".join(modified))

    return target_text, database_texts

def generate_test_data(size, vocabulary, similarity_type="partial"):
    import random
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