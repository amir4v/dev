import random


def get_random_username(length=9):
	return 'user_' + f'{random.randint(100000000, 1000000000)}'
