# Helper script for gaining access to the main bot module
# You probably shouldn't change what is already here.

import sys
Bot = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
