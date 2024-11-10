from collections import Counter
import os

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



def index():
    from gui import AnagramWindow

    trie = AnagramSolver.make_trie(AnagramSolver.read_words(DICTIONARY_FILENAME))
    letters = AnagramWindow.entry.get().lower()
    words = [word for word in AnagramSolver.anagram(letters, trie)]
    words = sorted(words, key=lambda x: (len(x), x))
    words = [word for word in words if len(word) >= 4]

    return words

if __name__ == "__main__":
    index()
    