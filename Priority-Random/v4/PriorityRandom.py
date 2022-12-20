from itertools import groupby, repeat
from random import shuffle, choice, randint, randrange
from pprint import pprint
import string


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
            """
            item:
                item[0]: KEY
                item[1]: LIST
                        item[1][0]: ITEM
                        item[1][1]: KEY
            """
            if grouped_dict.get(item[0]):
                grouped_dict[ item[0] ] = grouped_dict[ item[0] ] + [element[0] for element in item[1]]
            else:
                grouped_dict[ item[0] ] = [element[0] for element in item[1]]
        
        # TEST
        print(grouped_dict, end='\n\n')
        
        return grouped_dict
    
    @classmethod
    def make_the_list(cls, grouped_dict):
        the_list = []
        for item in grouped_dict:
            the_list.extend(list(repeat(item, item)))
        
        # TEST
        print(the_list, end='\n\n')
        
        shuffle(the_list)
        return the_list
    
    def choice(self):
        group_key = choice(self.the_list)
        item = choice(
            self.grouped_dict.get(group_key)
            ) # from the bucket
        return item
    
    def choices(self, n):
        return [item() for item in repeat(self.choice, n)]


# TEST
a_list = dict([
    (choice(string.ascii_uppercase) , choice(list(range(3, 13))))
    for _ in range(100)
])

pr = PriorityRandom(a_list)
pprint(pr.choices(10))
