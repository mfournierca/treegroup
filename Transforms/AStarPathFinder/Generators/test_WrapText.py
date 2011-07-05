import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree
from . import WrapText
        
        

#===============================================================================
# test the rename generator 
#===============================================================================
    
class test_Generator(unittest.TestCase):
    """Test the Generator class """
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'testfiles', 'AStarTransform', 'WrapText')
        self.log = logging.getLogger()
        self.generator = WrapText.Generator()
        
    def test_WrapText1(self):
        """Rename the root element"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'WrapText1.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        acceptableTags = ['title']
        text = True
        tail = False
        
        expectedTree = lxml.etree.fromstring('''<dita><topic id="id-1"><title>cdata</title><body id="id-11"/></topic></dita>'''
                                            )
        operand = self.generator.generateOperand(targetElement, acceptableTags[0])
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.getTree())), "WrapText Generator created wrong result. \nExpected \n%s \ngot\n%s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(tree)))
      
      
      
      
      
      

class test_Iterator(unittest.TestCase):
    """Test the RenameGeneratorIterator class """
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'testfiles', 'AStarTransform', 'WrapText')
        self.log = logging.getLogger()
        
        
    def test_IteratorRenameBodyP(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'WrapText1.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        acceptableTags = ['title']
        expectedTrees = ['''<dita><topic id="id-1"><title>cdata</title><body id="id-11"/></topic></dita>'''] 

        iterator = WrapText.Iterator(targetElement, acceptableTags)
        index = 0
        for operand in iterator:
            expectedTree = lxml.etree.fromstring(expectedTrees[index])
            self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(operand.getTree(), tree)), "WrapText generated the wrong operand. Expected \n%s \ngot \n%s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.getTree())))
            index += 1
    
    