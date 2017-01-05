# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest

from app.tests import AppTest
from store.tests import StoreTest
from pet.tests import PetTest

if __name__ == '__main__':
    unittest.main()
