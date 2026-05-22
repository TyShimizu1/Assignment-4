from typing import *
from dataclasses import dataclass
import unittest
import sys
import string
sys.setrecursionlimit(10**6)

@dataclass(frozen=True)
class IntList:
    first: int
    rest: Optional["IntList"]


@dataclass
class WordLines:
    word: str
    lines: Optional[IntList]


@dataclass(frozen=True)
class WordLinesList:
    first: WordLines
    rest: Optional["WordLinesList"]


@dataclass
class HashTable:
    bins: List[Optional[WordLinesList]]
    count: int

def intlist_contains(lst: Optional[IntList], n: int) -> bool:
    if lst is None:
        return False
    if lst.first == n:
        return True
    return intlist_contains(lst.rest, n)

def intlist_to_list(lst: Optional[IntList]) -> List[int]:
    result: List[int] = []
    result= []
    while lst is not None:
        result.append(lst.first)
        lst = lst.rest
    return result


# Return the hash code of 's' (see assignment description).
def hash_fn(s: str) -> int:
    hash_val:int =0 

    for char in s:
        hash_val= hash_val *31 +ord(char)

    return hash_val 
# Make a fresh hash table with the given number of bins 'size',
# containing no elements.
def make_hash(size: int) -> HashTable:
    return HashTable([None] * size, 0)

# Return the number of bins in 'ht'.
def hash_size(ht: HashTable) -> int:
    return len(ht.bins)

# Return the number of elements (key-value pairs) in 'ht'.
def hash_count(ht: HashTable) -> int:
    return ht.count 

# Return whether 'ht' contains a mapping for the given 'word'.
def has_key(ht: HashTable, word: str) -> bool:
    idx:int = hash_fn(word) % hash_size(ht)

    current_node:Optional[WordLinesList] = ht.bins[idx]

    while current_node is not None:
        if current_node.first.word == word:
            return True
        current_node = current_node.rest
    return False

# Return the line numbers associated with the key 'word' in 'ht'.
# The returned list should not contain duplicates, but need not be sorted.
def lookup(ht: HashTable, word: str) -> List[int]:
    idx:int = hash_fn(word) % hash_size(ht)
    chain: Optional[WordLinesList] = ht.bins[idx]
    while chain is not None:
        if chain.first.word == word:
            return intlist_to_list(chain.first.lines)
        chain = chain.rest
    return []

# Record in 'ht' that 'word' has an occurrence on line 'line'.
def add(ht: HashTable, word: str, line: int) -> None:
    idx:int = hash_fn(word) % hash_size(ht)
    chain:Optional[WordLinesList] = ht.bins[idx]
    node:Optional[WordLinesList] = chain
    while node is not None:
        if node.first.word == word:
            if not intlist_contains(node.first.lines, line):
                node.first.lines = IntList(line, node.first.lines)
            return
        node = node.rest
    wl:WordLines = WordLines(word, IntList(line, None))
    ht.bins[idx] = WordLinesList(wl, chain)
    ht.count += 1
    if ht.count >= hash_size(ht):
        resize(ht)

def resize(ht: HashTable) -> None:
    old_bins:List[Optional[WordLinesList]] = ht.bins
    new_size:int = hash_size(ht) * 2
    ht.bins = [None] * new_size
    ht.count = 0
    for chain in old_bins:
        while chain is not None:
            wl = chain.first
            for line in intlist_to_list(wl.lines):
                add(ht, wl.word, line)
            chain = chain.rest


# Returns a list of all keys stored in the hash table
def hash_keys(ht: HashTable) -> List[str]:
    keys:List[str] = []
    for chain in ht.bins:
        while chain is not None:
            keys.append(chain.first.word)
            chain = chain.rest
    return keys

# Strips punctuation, lowercases, and returns alphabetic tokens from a line
def _clean_line(line: str) -> List[str]:
    line = line.replace("'", "")
    for ch in string.punctuation:
        line = line.replace(ch, " ")
    line = line.lower()
    return [tok for tok in line.split() if tok.isalpha()]

# Builds and returns a concordance hash table from a list of document lines, excluding stop words
def make_concordance(stop_words: HashTable, lines: List[str]) -> HashTable:
    concordance:HashTable = make_hash(128)
    for line_num, line in enumerate(lines, start=1):
        for word in _clean_line(line):
            if not has_key(stop_words, word):
                add(concordance, word, line_num)
    return concordance

# Reads input, stop-words, and output file paths and writes a sorted concordance to the output file
def full_concordance(in_file: str, stop_words_file: str, out_file: str) -> None:
    stop_words:HashTable = make_hash(128)
    with open(stop_words_file, 'r') as f:
        for word in f.read().splitlines():
            word = word.strip().lower()
            if word:
                add(stop_words, word, 0)

    with open(in_file, 'r') as f:
        lines = f.read().splitlines()

    concordance:HashTable = make_concordance(stop_words, lines)

    keys = sorted(hash_keys(concordance))
    with open(out_file, 'w') as f:
        for word in keys:
            line_nums = sorted(lookup(concordance, word))
            f.write(word + ": " + " ".join(str(n) for n in line_nums) + "\n")
class Tests(unittest.TestCase):
    def test_hash_fn_consistent(self):
        self.assertEqual(hash_fn("hello"), hash_fn("hello"))

    def test_hash_fn_different(self):
        self.assertNotEqual(hash_fn("hello"), hash_fn("world"))

    def test_make_hash_empty(self):
        ht = make_hash(128)
        self.assertEqual(hash_size(ht), 128)
        self.assertEqual(hash_count(ht), 0)

    def test_hash_size(self):
        self.assertEqual(hash_size(make_hash(64)), 64)

    def test_hash_count_after_adds(self):
        ht = make_hash(128)
        add(ht, "cat", 1)
        add(ht, "dog", 2)
        self.assertEqual(hash_count(ht), 2)

    def test_has_key_true(self):
        ht = make_hash(128)
        add(ht, "cat", 1)
        self.assertTrue(has_key(ht, "cat"))

    def test_has_key_false(self):
        ht = make_hash(128)
        self.assertFalse(has_key(ht, "cat"))

    def test_lookup_basic(self):
        ht = make_hash(128)
        add(ht, "cat", 1)
        add(ht, "cat", 3)
        self.assertEqual(sorted(lookup(ht, "cat")), [1, 3])

    def test_lookup_no_duplicates(self):
        ht = make_hash(128)
        add(ht, "cat", 1)
        add(ht, "cat", 1)
        self.assertEqual(lookup(ht, "cat"), [1])

    def test_lookup_missing_key(self):
        ht = make_hash(128)
        self.assertEqual(lookup(ht, "cat"), [])

    def test_add_multiple_words(self):
        ht = make_hash(128)
        add(ht, "cat", 1)
        add(ht, "dog", 2)
        self.assertTrue(has_key(ht, "cat"))
        self.assertTrue(has_key(ht, "dog"))

    def test_resize(self):
        ht = make_hash(4)
        for w in ["a", "b", "c", "d", "e"]:
            add(ht, w, 1)
        self.assertTrue(hash_size(ht) > 4)
        self.assertTrue(has_key(ht, "a"))
        self.assertTrue(has_key(ht, "e"))

    def test_hash_keys_empty(self):
        self.assertEqual(hash_keys(make_hash(128)), [])

    def test_hash_keys_multiple(self):
        ht = make_hash(128)
        for w in ["apple", "banana", "cherry"]:
            add(ht, w, 1)
        self.assertEqual(sorted(hash_keys(ht)), ["apple", "banana", "cherry"])

    def test_make_concordance_basic(self):
        stop_words = make_hash(128)
        add(stop_words, "is", 0)
        add(stop_words, "a", 0)
        conc = make_concordance(stop_words, ["this is a test", "test line two"])
        self.assertIn("test", hash_keys(conc))
        self.assertNotIn("is", hash_keys(conc))

    def test_make_concordance_line_numbers(self):
        conc = make_concordance(make_hash(128), ["hello world", "hello again"])
        self.assertEqual(sorted(lookup(conc, "hello")), [1, 2])

    def test_make_concordance_no_duplicate_lines(self):
        conc = make_concordance(make_hash(128), ["cat cat cat"])
        self.assertEqual(lookup(conc, "cat"), [1])

    def test_make_concordance_punctuation(self):
        conc = make_concordance(make_hash(128), ["hello, world!!!"])
        self.assertIn("hello", hash_keys(conc))
        self.assertIn("world", hash_keys(conc))

    def test_make_concordance_blank_lines_counted(self):
        conc = make_concordance(make_hash(128), ["hello", "", "world"])
        self.assertEqual(lookup(conc, "hello"), [1])
        self.assertEqual(lookup(conc, "world"), [3])

    def test_full_concordance(self):
        import tempfile
        import os

        doc = (
            "This is a sample data ((text)) file, to be\n"
            "processed by your word-concordance program!!!\n"
            "A REAL data file is MUCH bigger. Gr8!\n"
        )
        stops = "a\nbe\nby\nis\nit\nof\non\nthe\nthis\nto\nwas\n"

        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as df:
            df.write(doc)
            doc_path = df.name

        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as sf:
            sf.write(stops)
            stop_path = sf.name

        out_path = tempfile.mktemp(suffix=".txt")

        try:
            full_concordance(doc_path, stop_path, out_path)

            with open(out_path) as of:
                result = of.read()

            self.assertIn("sample: 1", result)
            self.assertIn("bigger: 3", result)
            self.assertIn("data: 1 3", result)

        finally:
            os.unlink(doc_path)
            os.unlink(stop_path)

            if os.path.exists(out_path):
                os.unlink(out_path)
if (__name__ == '__main__'):
    unittest.main()
