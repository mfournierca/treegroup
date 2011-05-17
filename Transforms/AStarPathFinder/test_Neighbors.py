import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree
from . import Neighbors
        
        

#===============================================================================
# test findNeighbors_FirstValidationError
#===============================================================================
    
class test_findNeighbors_FirstValidationError(unittest.TestCase):
    """Test the findNeighbors_FirstValidationError function"""
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', 'testfiles', 'AStarTransform', 'Neighbors')
        self.log = logging.getLogger()
        
        
    def test_EmptyMisnamedRootNeighbors(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'NeighborsTest1.xml')
        tree = lxml.etree.parse(testfile)
        neighbors = Neighbors.findNeighbors_FirstValidationError(Neighbors.Neighbor(tree))
        expectedneighbors = ['<dita/>', '<dita><a/></dita>']
        index = 0
        self.assertEqual(len(expectedneighbors), len(neighbors), "findNeighbors_FirstValidationError returned a neighbors list of the wrong lenght: expected %i, got %i" % (len(expectedneighbors), len(neighbors))) 
        for n in neighbors:
            self.assertTrue(Tree.Tree.equal(lxml.etree.fromstring(expectedneighbors[index]), n.getTree()), "findNeighbors_FirstValidationError returned the wrong tree: expected %s, got %s" % (expectedneighbors[index], lxml.etree.tostring(n.getTree())))
            index += 1
            
                
    def test_MisnamedChildOfRoot(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'NeighborsTest2.xml')
        tree = lxml.etree.parse(testfile)
        neighbors = Neighbors.findNeighbors_FirstValidationError(Neighbors.Neighbor(tree))
        expectedneighbors = ['<dita><concept/></dita>', \
                            '<dita><glossentry/></dita>',\
                            '<dita><reference/></dita>',\
                            '<dita><task/></dita>',\
                            '<dita><topic/></dita>',\
                            '<dita><concept><a/>\n</concept>\n</dita>',\
                            '<dita><glossentry><a/>\n</glossentry>\n</dita>',\
                            '<dita><reference><a/>\n</reference>\n</dita>',\
                            '<dita><task><a/>\n</task>\n</dita>',\
                            '<dita><topic><a/>\n</topic>\n</dita>',\
                            '<dita/>'\
                            ]
        index = 0
        self.assertEqual(len(expectedneighbors), len(neighbors), "findNeighbors_FirstValidationError returned a neighbors list of the wrong lenght: expected %i, got %i" % (len(expectedneighbors), len(neighbors))) 
        for n in neighbors:
            self.assertTrue(Tree.Tree.equal(lxml.etree.fromstring(expectedneighbors[index]), n.getTree()), "findNeighbors_FirstValidationError returned the wrong tree: expected %s, got %s" % (expectedneighbors[index], lxml.etree.tostring(n.getTree())))
            index += 1
               
               
    def test_TwoMisnamedChildrenOfRoot(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'NeighborsTest3.xml')
        tree = lxml.etree.parse(testfile)
        neighbors = Neighbors.findNeighbors_FirstValidationError(Neighbors.Neighbor(tree))
        expectedneighbors = ['<dita><concept/><b/></dita>', \
                            '<dita><glossentry/><b/></dita>',\
                            '<dita><reference/><b/></dita>',\
                            '<dita><task/><b/></dita>',\
                            '<dita><topic/><b/></dita>',\
                            '<dita><concept><a/>\n</concept>\n<b/></dita>',\
                            '<dita><glossentry><a/>\n</glossentry>\n<b/></dita>',\
                            '<dita><reference><a/>\n</reference>\n<b/></dita>',\
                            '<dita><task><a/>\n</task>\n<b/></dita>',\
                            '<dita><topic><a/>\n</topic>\n<b/></dita>',\
                            '<dita><b/></dita>'\
                            ]
        index = 0
        self.assertEqual(len(expectedneighbors), len(neighbors), "findNeighbors_FirstValidationError returned a neighbors list of the wrong lenght: expected %i, got %i" % (len(expectedneighbors), len(neighbors))) 
        for n in neighbors:
            self.assertTrue(Tree.Tree.equal(lxml.etree.fromstring(expectedneighbors[index]), n.getTree()), "findNeighbors_FirstValidationError returned the wrong tree: expected %s, got %s" % (expectedneighbors[index], lxml.etree.tostring(n.getTree())))
            index += 1
        
    
                
    def test_MisnamedChildOfTopic(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'NeighborsTest4.xml')
        tree = lxml.etree.parse(testfile)
        neighbors = Neighbors.findNeighbors_FirstValidationError(Neighbors.Neighbor(tree))
        expectedneighbors = ['<dita><topic><title/></topic></dita>', '<dita><topic><title><a/></title></topic></dita>', '<dita><topic/></dita>']
        index = 0
        self.assertEqual(len(expectedneighbors), len(neighbors), "findNeighbors_FirstValidationError returned a neighbors list of the wrong lenght: expected %i, got %i" % (len(expectedneighbors), len(neighbors))) 
        for n in neighbors:
            self.assertTrue(Tree.Tree.equal(lxml.etree.fromstring(expectedneighbors[index]), n.getTree()), "findNeighbors_FirstValidationError returned the wrong tree: expected %s, got %s" % (expectedneighbors[index], lxml.etree.tostring(n.getTree())))
            index += 1
            
    
                
    def test_MisnamedChildOfTopicAfterTitle(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'NeighborsTest5.xml')
        tree = lxml.etree.parse(testfile)
        neighbors = Neighbors.findNeighbors_FirstValidationError(Neighbors.Neighbor(tree))
        expectedneighbors = ['<dita><topic><title/><abstract/></topic></dita>',
                             '<dita><topic><title/><body/></topic></dita>',   
                             '<dita><topic><title/><concept/></topic></dita>',
                             '<dita><topic><title/><glossentry/></topic></dita>',        
                             '<dita><topic><title/><prolog/></topic></dita>',        
                             '<dita><topic><title/><reference/></topic></dita>',        
#                             '<dita><topic><title/><related-links/></topic></dita>',        
                             '<dita><topic><title/><shortdesc/></topic></dita>',        
                             '<dita><topic><title/><task/></topic></dita>',        
                             '<dita><topic><title/><titlealts/></topic></dita>',        
                             '<dita><topic><title/><topic/></topic></dita>',
                             '<dita><topic><title/><abstract><a/></abstract></topic></dita>',        
                             '<dita><topic><title/><body><a/></body></topic></dita>',        
                             '<dita><topic><title/><concept><a/></concept></topic></dita>',        
                             '<dita><topic><title/><glossentry><a/></glossentry></topic></dita>',        
                             '<dita><topic><title/><prolog><a/></prolog></topic></dita>',        
                             '<dita><topic><title/><reference><a/></reference></topic></dita>',        
#                             '<dita><topic><title/><related-links><a/></related-links></topic></dita>',        
                             '<dita><topic><title/><shortdesc><a/></shortdesc></topic></dita>',        
                             '<dita><topic><title/><task><a/></task></topic></dita>',        
                             '<dita><topic><title/><titlealts><a/></titlealts></topic></dita>',        
                             '<dita><topic><title/><topic><a/></topic></topic></dita>',
                             '<dita><topic><title/></topic></dita>',        
                             ]
                                    
        index = 0
        self.assertEqual(len(expectedneighbors), len(neighbors),\
                          "findNeighbors_FirstValidationError returned a neighbors list of the wrong length: expected %i, got %i" % (len(expectedneighbors), len(neighbors))) 
        for n in neighbors:
            self.assertTrue(Tree.Tree.equal(lxml.etree.fromstring(expectedneighbors[index]), n.getTree()), \
                            "Index %i: findNeighbors_FirstValidationError returned the wrong tree: expected %s, got %s" % (index, expectedneighbors[index], lxml.etree.tostring(n.getTree())))
            index += 1