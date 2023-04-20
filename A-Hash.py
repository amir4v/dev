import string

CHARS = string.ascii_lowercase

BASE = len(CHARS)

chars_weight = dict([
    (s, i) for s, i in zip(CHARS, range(1, BASE+1))
])

reverse_chars_weight = dict([
    (i, s) for s, i in zip(CHARS, range(1, BASE+1))
])


"""
A function for Hash-Table
And the output is reversible to the original string
"""
def a_hash(string):
    string = string[::-1]
    result = 0
    for i, c in enumerate(string):
        result += (BASE ** i) * chars_weight.get(c)
    return result # f'{result:,}'


def reverse_a_hash(digits):
    result = ''
    while digits > 0:
        mod = digits % (BASE)
        digits = digits // BASE
        if mod == 0:
            mod = BASE
            digits -= 1
        result = reverse_chars_weight.get(mod) + result
    return result


def self_base_hash(string):
    CHARS = ''.join(sorted(set(string)))
    print(CHARS)
    BASE = len(CHARS)
    chars_weight = dict([
        (s, i) for s, i in zip(CHARS, range(1, BASE+1))
    ])
    
    string = string[::-1]
    result = 0
    for i, c in enumerate(string):
        result += (BASE ** i) * chars_weight.get(c)
    return result # f'{result:,}'
