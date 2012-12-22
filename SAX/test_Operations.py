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
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'SAX', 'Operations', 'Ordering')
        
    def test_SimpleXML(self):
        tree = "<xml><a/></xml>"
        expected = [[0], [0, 0], [0, 1], [1]]
        
        parser = Operations.SAXIterator(tree)
        ordering = Operations.Ordering()
        for e in parser: 
            ordering.updateOrdering(e)
        
        self.assertEqual(expected, ordering.getOrdering(), "Expected: \n%s\nGot:\n%s\n" % (str(expected), str(ordering.getOrdering())))
        
    def test_2(self):
        testfile = os.path.join(self.testfilesdir, 'test1', 'test1.xml')
        string = ''.join(open(testfile, 'r'))
        ordering = Operations.getOrdering(string)
        
        expected = [
                     [0],
                     [0, 0],
                     [0, 0, 0],
                     [0, 0, 1],
                     [0, 1],
                     [0, 2],
                     [0, 2, 0],
                     [0, 2, 1], 
                     [0, 2, 2], 
                     [0, 2, 3],
                     [0, 2, 4],
                     [0, 2, 4, 0],
                     [0, 2, 4, 0, 0],
                     [0, 2, 4, 0, 1],
                     [0, 2, 4, 1],
                     [0, 2, 5], 
                     [0, 3],
                     [1]
                    ]  
        
        self.assertEqual(ordering, expected, "expected: \n%s\nGot: \n%s\n" % (str(expected), str(ordering)))
        
        
        

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
        
        
    def test_SimpleXML4_Text(self):
        tree1 = "<a>a</a>"
        tree2 = "<d>a</d>"
        
        expected = '<e>C</e>'
        
        result = Operations.add(tree1, tree2)
        self.assertTrue(Operations.equal(result, expected), "Expected:\n%s\nGot:\n%s\n" % (expected, result))
        
        
    def test_SimpleXML4_TextLeading(self):
        tree1 = "<a>a<a/></a>"
        tree2 = "<d>a<a/></d>"
        
        expected = '<e>C<b/></e>'
        
        result = Operations.add(tree1, tree2)
        self.assertTrue(Operations.equal(result, expected), "Expected:\n%s\nGot:\n%s\n" % (expected, result))
        
        
    def test_SimpleXML4_TextTrailing(self):
        tree1 = "<a><a/>a</a>"
        tree2 = "<d><a/>a</d>"
        
        expected = '<e><b/>C</e>'
        
        result = Operations.add(tree1, tree2)
        self.assertTrue(Operations.equal(result, expected), "Expected:\n%s\nGot:\n%s\n" % (expected, result))
        
        
    def test_SimpleXML4_TextLeadingAndTrailing(self):
        tree1 = "<a>a<a/>a</a>"
        tree2 = "<d>a<a/>a</d>"
        
        expected = '<e>C<b/>C</e>'
        
        result = Operations.add(tree1, tree2)
        self.assertTrue(Operations.equal(result, expected), "Expected:\n%s\nGot:\n%s\n" % (expected, result))
        
    
    def test_DifferentStructureXML1_Text(self):
        tree1 = "<a><a>a</a>a</a>"
        tree2 = "<d>a</d>"
        
        expected = '<e>a<a>a</a>a</e>'
        
        result = Operations.add(tree1, tree2)
        self.assertTrue(Operations.equal(result, expected), "Expected:\n%s\nGot:\n%s\n" % (expected, result))
        
    def test_SimpleTrees_EqualStructures(self):
    
        expectedtree  = ''.join(open(os.path.join(self.testfilesdir, 'test1', 'expected_add1.xml'), 'r'))
        
        tree1 = ''.join(open(os.path.join(self.testfilesdir, 'test1', 'TreeTestFile_add1.xml'), 'r'))
        tree2 = ''.join(open(os.path.join(self.testfilesdir, 'test1', 'TreeTestFile_add2.xml'), 'r'))
        result = Operations.add(tree1, tree2)
        self.assertTrue(Operations.equal(result, expectedtree), "Expected: \n%s\nGot: \n%s\n" % (expectedtree, result))
                   
        #test commutativity    
        result = Operations.add(tree2, tree1)
        self.assertTrue(Operations.equal(result, expectedtree), "Expected: \n%s\nGot: \n%s\n" % (expectedtree, result))
        
        
        