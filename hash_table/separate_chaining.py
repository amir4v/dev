import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath('./a_hash.py'))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from a_hash import a_hash, reverse_a_hash


class HashTableSeparateChaining:
    _table = {}
    _size = 10
    
    def __init__(self, size=10):
        self.size = size
    
    @property
    def table(self):
        return self._table
    
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, value):
        self._size = value
    
    def add(self, value):
        value = value.lower()
        key = a_hash(value) % self.size
        bucket = self.table.get(key, None)
        if bucket:
            if value in bucket:
                return None
            else:
                bucket.append(value)
        else:
            self.table[key] = [value]
    
    def find(self, value):
        value = value.lower()
        key = a_hash(value) % self.size
        bucket = self.table.get(key, None)
        if bucket is None:
            return None
        else:
            for i, v in enumerate(bucket):
                if v == value:
                    return (key, i)
            return None
    
    def get(self, key, index):
        bucket = self.table.get(key, None)
        if bucket is None:
            return None
        else:
            return bucket[index]
    
    def remove(self, address=None, value=None):
        if address is None and value is None:
            return None
        elif address:
            key, index = address
            bucket = self.table.get(key, None)
            if bucket is None:
                return None
            else:
                return bucket.pop(index)
        else:
            """
            key = a_hash(value) % self.size
            bucket = self.table.get(key, None)
            if bucket is None:
                return None
            else:
                return bucket.remove(value)
            """
            value = value.lower()
            key, index = self.find(value)
            return self.remove(address=(key, index))

class HashTable(HashTableSeparateChaining):
    pass

class HT(HashTable):
    pass


# TEST
from random import randint
from random_str import random_str
ht = HT(100)
for i in range(100_000):
    ht.add(
        random_str(
            randint(6, 16)
        )
    )
