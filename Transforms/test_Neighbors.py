import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree
from . import Neighbors
        
    
    
    
class test_Rename(unittest.TestCase):
    """Test the Rename() operation"""
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'AStarTransform', 'Rename')
        self.log = logging.getLogger()
        
    def test_1(self):
        """RenameTest1.xml has only the root element, the rename operand 
        should just rename this root"""
        
        testfile = os.path.join(self.testfilesdir, 'RenameTest1.xml')
        tree = lxml.etree.parse(testfile)
        targetelement = tree.getroot()
        
        expectedtree = lxml.etree.fromstring('<cita/>')
        
        result = Neighbors.Rename(tree, targetelement)
        self.assertTrue(Tree.Tree.equal(result, expectedtree), 'Rename() returned the wrong tree')

        
        
        