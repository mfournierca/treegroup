import unittest, os.path, sys, logging

import lxml.etree, copy

import TreeGroup.SAX.Operations as Operations



class test_SAXIterator(unittest.TestCase):
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'SAX', 'Operations', 'SAXIterator')
        
        
    def test_SimpleXML(self):
        tree ="<xml><a/></xml>"
        expected = [
                    #"<class 'TreeGroup.SAX.Operations.StartDocumentEvent'>", 
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
        
        
        
        
        
class test_Ordering(unittest.TestCase):
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'SAX', 'Operations', 'Position')
        
    def test_SimpleXML(self):
        tree = "<xml><a/></xml>"
        expected = [[0], [0, 0], [0, 1], [1]]
        
        parser = Operations.SAXIterator(tree)
        ordering = Operations.Ordering()
        for e in parser: 
            ordering.updateOrdering(e)
        
        self.assertEqual(expected, ordering.getOrdering(), "Expected: \n%s\nGot:\n%s\n" % (str(expected), str(ordering.getOrdering())))
        
        
        
        

class test_Equal(unittest.TestCase):
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'SAX', 'Operations', 'Equal')
        
    def test_SimpleXML_Equal(self):
        tree1 = "<xml><a/></xml>"
        tree2 = "<xml><a/></xml>"
        
        result = Operations.equal(tree1, tree2)
        self.assertTrue(result, 'equal() returned %s, expected True' % str(result))
        
        
    def test_SimpleXML_NotEqual(self):
        tree1 = "<xml><a/></xml>"
        tree2 = "<xml><b/></xml>"
        
        result = Operations.equal(tree1, tree2)
        self.assertFalse(result, 'equal() returned %s, expected False' % str(result))
        
        
        
class test_Add(unittest.TestCase):
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'SAX', 'Operations', 'Add')
        
#    def test_SimpleXML(self):
#        tree1 = "<a><b id='1'/></a>"
#        tree1 = "<d><e id='a'/></d>"
#        
#        expected = '<e><g id="2"/></e>'
#        
#        result = Operations.add(tree1, tree2)
#        self.assertTrue(Operations.equal(result, expected), "Expected:\n%s\nGot:\n%s\n" % (expected, result))
        
        
        
        
        
        
        