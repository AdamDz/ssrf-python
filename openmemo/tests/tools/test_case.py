import unittest
import os
from fs.osfs import OSFS

class TestCase (unittest.TestCase):
    def setUp(self):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.data = OSFS(path)


    
