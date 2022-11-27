import string
from typing import Union


extra = ' ' + '-_' + "'" + '"'
alphabet = string.ascii_letters + extra


convdict = {
    " و " : " va " ,
    "ی " : "y " ,
    "ع " : " " ,
    
    "و" : "v" ,
    "ی" : "i" ,
    "ع" : "a" ,
    
    #
    
    "ض" : "z" ,
    "ش" : "sh" ,
    "ظ" : "z" ,
    "ط" : "t" ,
    "س" : "s" ,
    "ص" : "s" ,
    "ث" : "s" ,
    
    "ز" : "z" ,
    "ق" : "gh" ,
    "ب" : "b" ,
    "ر" : "r" ,
    "ف" : "f" ,
    "ل" : "l" ,
    "ذ" : "z" ,
    "غ" : "gh" ,
    "ا" : "a" ,
    "آ" : "a" ,
    "د" : "d" ,
    
    "ت" : "t" ,
    "ه" : "h" ,
    "ن" : "n" ,
    
    "خ" : "kh" ,
    "م" : "m" ,
    "ح" : "h" ,
    "ک" : "k" ,
    "ج" : "j" ,
    "چ" : "ch" ,
    "پ" : "p" ,
    "ژ" : "zh" ,
    "گ" : "g" ,
    "ئ" : "i" ,
    
    " " : " " ,
}


def isalpha(word):
        for c in word:
            if c not in alphabet:
                return False
        return True


def convert(text: Union[str, Union[list, tuple, set, dict]]):
    def inner(text):
        """
        fc: Farsi Character
        ec: English Character
        """
        for fc, ec in convdict.items():
            text = text.replace(fc, ec)
        
        # ASCii Checking/Replacing(with ' ')
        result = ''
        for c in text:
            if c in alphabet:
                result += c
            else:
                result += ' '

        # Replacing double spaces('  ') with a single space(' ')
        while result.find('  ') != -1 :
            result = result.replace('  ', ' ')
        
        return result.strip(extra)
    
    # Input is str
    if isinstance(text, str):
        return inner(text)
    
    # Input is iterable
    result = []
    for t in text:
        result.append(inner(t))
    
    return result