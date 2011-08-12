import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree
from . import WrapTail
        
        

#===============================================================================
# test the rename generator 
#===============================================================================
    
class test_Generator(unittest.TestCase):
    """Test the Generator class """
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'testfiles', 'AStarTransform', 'WrapTail')
        self.log = logging.getLogger()
        self.generator = WrapTail.Generator()
        
    def test_WrapTail1(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'WrapTail1.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0][1][0]
        acceptableTags = ['p']
        Tail = True
        tail = False
        
        expectedTree = lxml.etree.fromstring('''<dita><topic id="id-1"><title/><body><p/><p>cdata</p></body></topic></dita>''')
        operand = self.generator.generateOperand(targetElement, acceptableTags[0])
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.getTree())), "WrapTail Generator created wrong result. \nExpected \n%s \ngot\n%s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(tree)))
      
      
      
    def test_WrapTail2(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'WrapTail2.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0][1][0]
        acceptableTags = ['p']
        Tail = True
        tail = False
        
        expectedTree = lxml.etree.fromstring('''<dita><topic id="id-1"><title/><body><p>Text 1</p><p>cdata</p><p>Text 2</p></body></topic></dita>''')
        operand = self.generator.generateOperand(targetElement, acceptableTags[0])
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.getTree())), "WrapTail Generator created wrong result. \nExpected \n%s \ngot\n%s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(tree)))
      
      
          
      
      

class test_Iterator(unittest.TestCase):
    """Test the RenameGeneratorIterator class """
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'testfiles', 'AStarTransform', 'WrapTail')
        self.log = logging.getLogger()
        
        
    def test_IteratorRenameBodyP(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'WrapTail1.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0][1][0]
        acceptableTags = ['p']
        expectedTrees = ['''<dita><topic id="id-1"><title/><body><p/><p>cdata</p></body></topic></dita>'''] 

        iterator = WrapTail.Iterator(targetElement, acceptableTags)
        index = 0
        for operand in iterator:
            expectedTree = lxml.etree.fromstring(expectedTrees[index])
            self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(operand.getTree(), tree)), "WrapTail generated the wrong operand. Expected \n%s \ngot \n%s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.getTree())))
            index += 1
    
    