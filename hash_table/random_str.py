
import string
from random import shuffle, sample, choices
# import secrets
def random_str(length=62, lowercase=True, uppercase=True, digits=True, symbols=False, chars=''):
    # secrets.choice()
    # secrets.token_urlsafe()
    # secrets.token_hex()
    # secrets.token_bytes()
    
    if lowercase:
        chars += string.ascii_lowercase
    if uppercase:
        chars +=  string.ascii_uppercase
    if digits:
        chars += string.digits
    if symbols:
        chars += string.punctuation
    
    chars = list(chars)
    shuffle(chars)
    
    if length > len(chars):
        return ''.join(choices(chars, k=length))
    return ''.join(sample(chars, length))
