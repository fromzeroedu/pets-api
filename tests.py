# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest

from app.tests import AppTest

if __name__ == '__main__':
    unittest.main()
