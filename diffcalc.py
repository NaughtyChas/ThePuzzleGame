def calculate_complexity(word):
    complexity = len(set(word))
    return complexity

def update_words_file():
    words = []
    with open('words.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:
                word, complexity = parts
            else:
                word = parts[0]
                complexity = None
            words.append((word, complexity))

    updated = False
    with open('words.txt', 'w') as file:
        for word, complexity in words:
            if complexity is None:
                complexity = calculate_complexity(word)
                updated = True
            file.write(f'{word},{complexity}\n')

    if updated:
        print("Words file updated with complexity levels.")
    else:
        print("All words already have complexity levels.")

if __name__ == "__main__":
    update_words_file()