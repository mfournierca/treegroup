import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree

from . import AStarPathFinder, Neighbors
        
    
    
    
class test_processNeighbors(unittest.TestCase):
    """Test the AStarPathFinder.processNeighbors() function. """
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', 'testfiles', 'AStarTransform', 'Neighbors')
        self.log = logging.getLogger()
        
    def test_NeighborsOfRoot(self):
        testfile = os.path.join(self.testfilesdir, 'NeighborsTest1.xml')
        pathfinder = AStarPathFinder.AStarPathFinder(testfile)
        tree = lxml.etree.parse(testfile)
        t = Neighbors.Neighbor(tree)
        t.setGScore(0)
        t.setGeneration(0)
        pathfinder.processNeighbors(t)
        
        #check open set, should only contain one entry
        openset = pathfinder._openset
        expectedopensetlength = 3
        self.assertEqual(len(openset), expectedopensetlength, "processNeighbors created open set of length %i, expected %i" % (len(openset), expectedopensetlength))
        for o in openset:
            pass
            #check gscores
            #check hscores
            #check fscores
            #check camefrom
    
    def test_NeighborsOfMisnamedTopic(self):
        pass
    
    def test_NeighborsOfMissingBody(self):
        pass
    