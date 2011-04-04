import unittest, os.path, sys, logging

import lxml.etree, copy

from . import Tree    

import Element.Element

class test_getNeighbors_FirstValidationError(unittest.TestCase):
    """Test the equal() function"""
            
    def setUp(self):
        """set up data used in the tests, called before each test function execution"""
        
        self.testfile = os.path.join(os.path.dirname(__file__), 'testfiles', 'AStarTransform', 'NeighborsTest.xml')
        self.testtree = lxml.etree.parse(self.testfile)
        
        
        

class test_hScore_ValidationErrorsCount(unittest.TestCase):
    """Test the equal() function"""
            
    def setUp(self):
        """set up data used in the tests, called before each test function execution"""
        
        self.testfile = os.path.join(os.path.dirname(__file__), 'testfiles', 'AStarTransform', 'NeighborsTest.xml')
        self.testtree = lxml.etree.parse(self.testfile)