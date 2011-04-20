import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree
from . import Neighbors
        
        

#===============================================================================
# test findNeighbors_FirstValidationError
#===============================================================================
    
class test_findNeighbors_FirstValidationError(unittest.TestCase):
    """Test the findNeighbors_FirstValidationError function"""
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'testfiles', 'AStarTransform', 'Neighbors')
        self.log = logging.getLogger()
        
        
#    def test_MisnamedRootNeighbors(self):
#        self.log.debug('')
#        self.log.debug('')
#        self.log.debug('running %s' % __name__)
#        testfile = os.path.join(self.testfilesdir, 'NeighborsTest1.xml')
#        tree = lxml.etree.parse(testfile)
#        neighbors = Neighbors.findNeighbors_FirstValidationError(tree)
#        expectedneighbors = ['<dita/>']
#        index = 0
#        self.assertEqual(len(expectedneighbors), len(neighbors), "findNeighbors_FirstValidationError returned a neighbors list of the wrong lenght: expected %i, got %i" % (len(expectedneighbors), len(neighbors))) 
#        for n in neighbors:
#            self.assertTrue(Tree.Tree.equal(lxml.etree.fromstring(expectedneighbors[index]), n.tree), "findNeighbors_FirstValidationError returned the wrong tree: expected %s, got %s" % (expectedneighbors[index], lxml.etree.tostring(n.tree)))
#            index += 1
        