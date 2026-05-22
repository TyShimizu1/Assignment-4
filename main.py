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
# Return the words that have mappings in 'ht'.
# The returned list should not contain duplicates, but need not be sorted.
def hash_keys(ht: HashTable) -> List[str]:
pass
# Given a hash table 'stop_words' containing stop words as keys, plus
# a sequence of strings 'lines' representing the lines of a document,
# return a hash table representing a concordance of that document.
def make_concordance(stop_words: HashTable, lines: List[str]) -> HashTable:
pass
# Given an input file path, a stop-words file path, and an output file path,
# overwrite the indicated output file with a sorted concordance of the input
file.
def full_concordance(in_file: str, stop_words_file: str, out_file: str) -> None:
pass

class Tests(unittest.TestCase):
pass
if (__name__ == '__main__'):
unittest.main()
