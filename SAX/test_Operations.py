import unittest, os.path, sys, logging

import lxml.etree, copy

import TreeGroup.SAX.Operations as Operations



class test_SAXIterator(unittest.TestCase):
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'SAX', 'SAXIterator')
        
        
    def test_SimpleXML(self):
        tree ="<xml><a/></xml>"
        expected = [
                    "<class 'TreeGroup.SAX.Operations.StartDocumentEvent'>", 
                    "<class 'TreeGroup.SAX.Operations.StartElementEvent'> name: 'xml' attr: '{}'", 
                    "<class 'TreeGroup.SAX.Operations.StartElementEvent'> name: 'a' attr: '{}'", 
                    "<class 'TreeGroup.SAX.Operations.EndElementEvent'> name: 'a'", 
                    "<class 'TreeGroup.SAX.Operations.EndElementEvent'> name: 'xml'",
                    #"<class 'TreeGroup.SAX.Operations.EndDocumentEvent'>", 
                    ]
        
        parser = Operations.SAXIterator(tree)
        result = []
        for e in parser:
            result.append(str(e))
            
        self.assertEqual(result, expected, "Expected: \n%s\nGot:\n%s\n" % (str(expected), str(result)))
        
        
        
class test_Position(unittest.TestCase):
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'SAX', 'Position')
        
    def test_SimpleXML(self):
        tree = "<xml><a/></xml>"
        expected = [[0], [0, 0], [0, 1], [1]]
        
        parser = Operations.SAXIterator(tree)
        ordering = Operations.Ordering()
        for e in parser: ordering.updateOrdering(e)
        
        self.assertEqual(expected, ordering.getOrdering(), "Expected: \n%s\nGot:\n%s\n" % (str(expected), str(ordering.getOrdering())))