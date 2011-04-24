import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree
from . import Errors
        
    
    
    
class test_processNeighbors(unittest.TestCase):
    """Test the AStarPathFinder.processNeighbors() function. """
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', 'testfiles', 'AStarTransform', 'Errors')
        self.log = logging.getLogger()
        
    def test_NeighborsOfRoot(self):
        pass