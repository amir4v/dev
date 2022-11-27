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


from .error import e


def separate(p):
    p = p.replace(' ', '')
    key = p.split('>')[0]
    validations = p.split('>')[1]
    validations = validations.split('|')
    for v in validations:
        if ':' in v:
            # pass # validation_name is just v
            yield v
        else:
            validation_name, validation_args = tuple(v.split(':'))
            validation_args = validation_args.split(',')
            yield validation_name, validation_args


class String:
    _az = 'qazwsxedcrfvtgbyhnujmikolp'
    _number = '1234567890'
    _value = None
    _pattern = ''

    def _len(self, x, y=None):
        if y == None:
            if not len(self._value) == x:
                e('len:x')
        else:
            if not (
                len(self._value) >= x
                and
                len(self._value) <= y
            ):
                e('len:x,y')
    
    def az(self):
        for c in self._value:
            if not c in self._az:
                e('az')
    