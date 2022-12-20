from itertools import groupby, repeat
from random import shuffle, choice, choices, sample
from pprint import pprint


class PriorityRandom:
    """
    a_dict is a dictionary like: (the numbers are Priorities)
                {
                    'Item-A': 0,
                    'Item-B': 1,
                    'Item-C': 3,
                }
    """
    
    def __init__(self, a_dict):
        self.grouped_dict = self.clean_groupby(a_dict)
        self.the_list = self.make_the_list(self.grouped_dict)
    
    @classmethod
    def clean_groupby(cls, a_dict):
        grouped_list = [
            (item[0], list(item[1]))
            for item in
            groupby(a_dict.items(), key=lambda x: x[1])
        ]
        
        grouped_dict = {}
        for item in grouped_list:
            grouped_dict[ item[0] ] = [element[0] for element in item[1]]
        
        return grouped_dict
    
    @classmethod
    def make_the_list(cls, grouped_dict):
        the_list = []
        for item in grouped_dict:
            the_list.extend(list(repeat(item, item)))
        
        shuffle(the_list)
        return the_list
    
    def choice(self):
        group_key = choice(self.the_list)
        item = choice(
            self.grouped_dict.get(group_key)
            )
        return item
    
    def choices(self, n):
        return [item() for item in repeat(self.choice, n)]


# EXAMPLE
the_list = {
    'A': 15,
    
    'D': 1,
    'E': 1,
    'F': 1,
    'G': 1,
    'H': 1,
    
    'I': 0,
}

pr = PriorityRandom(the_list)
pprint(pr.choices(5))
