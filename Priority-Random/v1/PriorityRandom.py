from itertools import groupby, repeat
from random import shuffle, choice, choices, sample
from pprint import pprint


class PriorityRandom:
    """
    my_list is a dictionary like: (the numbers are Priorities)
                {
                    'A': 0,
                    'B': 1,
                    'C': 3,
                }
    """
    
    def __init__(self, my_list):
        self.my_list = self.clean_groupby(my_list)
        self.my_list = self.make_my_list(self.my_list)
    
    @classmethod
    def clean_groupby(cls, my_list):
        grouped_list = [
            (item[0], list(item[1]))
            for item in
            groupby(my_list.items(), key=lambda x: x[1])
        ]
        
        temp_grouped_list = []
        
        for item in grouped_list:
            temp_grouped_list.append(
                [
                    item[0],
                    [
                        element[0] for element in item[1]
                    ]
                ]
            )
        
        return temp_grouped_list
    
    @classmethod
    def make_my_list(cls, my_grouped_list):
        my_temp_list = []
        
        for item in my_grouped_list:
            for _ in range(item[0]):
                my_temp_list.extend(item[1])
        
        shuffle(my_temp_list)
        return my_temp_list
    
    def choice(self):
        return choice(self.my_list)
    
    def choices(self, n):
        return choices(self.my_list, k=n)
    
    def sample(self, n):
        return sample(self.my_list, k=n)


my_list = {
    'A': 15,
    
    'D': 1,
    'E': 1,
    'F': 1,
    'G': 1,
    'H': 1,
    
    'I': 0,
}

pr = PriorityRandom(my_list)
pprint(pr.choice())
