import random
import time

from celery import shared_task


@shared_task
def latency_random_number():
	"""
	This function will return a random number with an artifact delay of 2 seconds.
	And how you use this method:
		latency_random_number.delay()
		or: latency_random_number.delay(*args, **kwargs)
	
	And this is how you run your Celery in background:
		celery -A project worker --loglevel=info
	"""
	time.sleep(2.0)
	return random.randint(0, 1001001)
