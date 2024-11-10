from collections import Counter
import os
from wordup import *
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
DICTIONARY_FILENAME = os.path.join(ASSETS, "twl06.txt")

class AnagramSolver:
    def __init__(self):
        self.letters = None
        self.trie = None
        self.words = None

    def read_words(filename):
        return [line.strip().lower() for line in open(filename)]

    def make_trie(words):
        root = {}
        for word in words:
            this_dict = root
            for letter in word:
                this_dict = this_dict.setdefault(letter, {})
            this_dict[None] = None
        return root

    def anagram(letters, trie):
        def _anagram(letter_counts, path, root):
            if None in root.keys():
                word = ''.join(path)
                yield word
            for letter, this_dict in root.items():
                count = letter_counts.get(letter, 0)
                if count == 0:
                    continue
                letter_counts[letter] = count - 1
                path.append(letter)
                for word in _anagram(letter_counts, path, this_dict):
                    yield word
                path.pop()
                letter_counts[letter] = count

        # Build a dictionary of letter: count pairs from the input letters sequence
        letter_counts = Counter(letters)
        for word in _anagram(letter_counts, [], trie):
            yield word



if __name__ == "__main__":
    app = AnagramSolver()
    app.run()