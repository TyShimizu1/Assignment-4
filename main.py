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
pass
# Record in 'ht' that 'word' has an occurrence on line 'line'.
def add(ht: HashTable, word: str, line: int) -> None:
pass

# Returns a list of all keys stored in the hash table
def hash_keys(ht: HashTable) -> List[str]:
    keys = []
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
    concordance = make_hash(128)
    for line_num, line in enumerate(lines, start=1):
        for word in _clean_line(line):
            if not has_key(stop_words, word):
                add(concordance, word, line_num)
    return concordance

# Reads input, stop-words, and output file paths and writes a sorted concordance to the output file
def full_concordance(in_file: str, stop_words_file: str, out_file: str) -> None:
    stop_words = make_hash(128)
    with open(stop_words_file, 'r') as f:
        for word in f.read().splitlines():
            word = word.strip().lower()
            if word:
                add(stop_words, word, 0)

    with open(in_file, 'r') as f:
        lines = f.read().splitlines()

    concordance = make_concordance(stop_words, lines)

    keys = sorted(hash_keys(concordance))
    with open(out_file, 'w') as f:
        for word in keys:
            line_nums = sorted(lookup(concordance, word))
            f.write(word + ": " + " ".join(str(n) for n in line_nums) + "\n")
class Tests(unittest.TestCase):
pass
if (__name__ == '__main__'):
unittest.main()
