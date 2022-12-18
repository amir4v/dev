"""
::: url ::: (str)
url
http
https
ip
ipv4
ipv6
ipv46
email
"""



"""
::: string ::: str

len:x
len:x,y

az
lower

min-len:x

max-len:x

upper
AZ

any

[x,y,z] , [xyz]

alphabet
aZ

number

alphanum
"""



"""
::: number ::: number, int, float
min:x
max:x
range:x,y
int
float
decimal
"""




"""
::: file :::
ext:x
exts:x,y,z
img
mp3
mp4
jpg
png
pdf
len:x
len:x,y
min:x , min-size:x
max:x , max-size:x
range:x,y , range-size:x,y
width:x
height:x
"""




"""
regex
re

username
password
"""

import string
from rest_framework.serializers import ValidationError
import re


ALPHABET = string.ascii_letters
az = string.ascii_lowercase
AZ = string.ascii_uppercase
DIGITS = string.digits
WHITESPACE = string.whitespace


class String:
    @staticmethod
    def not_null(value):
        if value == None:
            return ValidationError
    
    def not_blank(value):
        if value.strip() == '':
            return ValidationError
    
    class len:
        def __init__(self, exact, to=None):
            self.exact = exact
            self.to = to
        
        def __call__(self, value):
            value_len = len(value)
            
            if self.to == None:
                if value_len != self.exact:
                    raise ValidationError
            else:
                if value_len < self.exact or value_len > self.to:
                    raise ValidationError
    
    @staticmethod
    def alphabet(value):
        pattern = rf'^[{ALPHABET}]+$'
        match = bool(re.match(pattern, value))
        if not match:
            raise ValidationError
    
    @staticmethod
    def aZ(value):
        pattern = rf'^[{ALPHABET}]+$'
        match = bool(re.match(pattern, value))
        if not match:
            raise ValidationError
    
    @staticmethod
    def az(value):
        pattern = rf'^[{az}]+$'
        match = bool(re.match(pattern, value))
        if not match:
            raise ValidationError
    
    @staticmethod
    def AZ(value):
        pattern = rf'^[{AZ}]+$'
        match = bool(re.match(pattern, value))
        if not match:
            raise ValidationError
    
    @staticmethod
    def digit(value):
        pattern = rf'^[{DIGITS}]+$'
        match = bool(re.match(pattern, value))
        if not match:
            raise ValidationError
    
    @staticmethod
    class In:
        def __init__(self, elements):
            self.elements = elements
        
        def __call__(self, value):
            pattern = rf'^[{self.elements}]+$'
            match = bool(re.match(pattern, value))
            if not match:
                raise ValidationError


class Web:
    @staticmethod
    def ipv4(value):
        f, s, t, f = value.split('.')
        for n in (f, s, t, f):
            n = int(n)
            if n < 0 or n > 255:
                raise ValidationError



class Number:
    def __init__(self, value):
        try:
            value + 123
            value + 12.34
        except:
            raise ValidationError
