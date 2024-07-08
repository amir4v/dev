# It has to be next to the manage.py file.

import os

os.environ['PYTEST_RUNNING'] = 'true'

from project.app.tests.fixtures import *
from project.accounts.tests.fixtures import *
