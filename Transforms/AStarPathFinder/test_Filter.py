import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree
from . import Filter
        
        
#===============================================================================
# test findNeighbors_FirstValidationError
#===============================================================================
    
class test_ElementTagFilter(unittest.TestCase):
    """Test the element tag filter"""
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', 'testfiles', 'AStarTransform', 'Filter')
        #set test file, target, tree
        self.log = logging.getLogger()
        
        
    def test_Train(self):
        #test training a database on a set of files
        pass
    
    
    def test_Filter(self):
        #test the filter, ensure that it returns the proper tags for a given element
        pass
    
    
    def test_getTagScore(self):
        #get the score of a tag, ie the probability that the tag is the proper one for 
        #the target element
        pass
    
    
    def test_getProbaTagGivenParentTag(self):
        #test the conditional probability of a tag given the target's parent.
        pass
         
         
    