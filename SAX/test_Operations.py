import unittest, os.path, sys, logging

import lxml.etree, copy

import TreeGroup.SAX.Operations as Operations


#test join characters
#test all trees in ETree.Tree tests
#test iterator on large trees
#raise errors if something other than element or character found
#test ordering on large tree
#test ordering even and odd numbers for startElement and endElement

class test_SAXIterator(unittest.TestCase):
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'SAX', 'Operations', 'SAXIterator')
        
        
    def test_SimpleXML(self):
        tree ="<xml><a/></xml>"
        expected = [
                    #"<class 'TreeGroup.SAX.Operations.StartDocumentEvent'>", 
                    "<xml>", 
                    "<a>", 
                    "</a>", 
                    "</xml>",
                    #"<class 'TreeGroup.SAX.Operations.EndDocumentEvent'>", 
                    ]
        
        parser = Operations.SAXIterator(tree)
        result = []
        for e in parser:
            result.append(e.toString())
            
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
        
    def test_SimpleXML1(self):
        tree1 = "<a><b id='1'/></a>"
        tree2 = "<d><e id='a'/></d>"
        
        expected = '<e><g id="2"/></e>'
        
        result = Operations.add(tree1, tree2)
        self.assertTrue(Operations.equal(result, expected), "Expected:\n%s\nGot:\n%s\n" % (expected, result))
        
        
    def test_SimpleXML2_DifferentSiblings(self):
        tree1 = "<a><b id='1'/></a>"
        tree2 = "<d><e id='a'/><a/></d>"
        
        expected = '<e><g id="2"/><a/></e>'
        
        result = Operations.add(tree1, tree2)
        self.assertTrue(Operations.equal(result, expected), "Expected:\n%s\nGot:\n%s\n" % (expected, result))
        
        
    def test_SimpleXML3_DifferentChildren(self):
        tree1 = "<a><b id='1'/></a>"
        tree2 = "<d><e id='a'><a/></e></d>"
        
        expected = '<e><g id="2"><a/></g></e>'
        
        result = Operations.add(tree1, tree2)
        self.assertTrue(Operations.equal(result, expected), "Expected:\n%s\nGot:\n%s\n" % (expected, result))
        
        
        
        
        
        