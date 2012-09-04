"""Contains code / initialization which is required by every modulde on the site"""


import os
import sys


# fix up pythonpath so that libraries can be directly used
sys.path.append('libs')


ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DEV = os.environ.get('SERVER_SOFTWARE', "Development").startswith('Development')
