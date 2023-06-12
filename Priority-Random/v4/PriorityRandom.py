from itertools import repeat
from random import shuffle, choice
from pprint import pprint


class PriorityRandom:
    """
    item , 1-...
    
    (
        (item1, 1), (item2, 5), (item3, 8), (item4, 2), ...
    )
    """
    
    def __init__(self, items):
        self.items = items
        self.the_list = self.make_the_list(items)
    
    @classmethod
    def make_the_list(cls, items):
        the_list = []
        for index, item in enumerate(items):
            the_list.extend(
                list(
                    repeat(index, item[1]) # item[1] = Priority
                )
            )
        shuffle(the_list)
        return the_list
    
    def choice(self):
        index = choice(self.the_list)
        return self.items[index][0]
    
    def choices(self, n):
        return (
            item() for item in repeat(self.choice, n)
        )


# EXAMPLE
items = (
    ('item-1', 1),
    ('item-2', 3),
    ('item-3', 5),
    ('item-4', 10),
    ('item-5', 15),
)

pr = PriorityRandom(items)
pprint(
    tuple(
        pr.choices(10)
    )
)
