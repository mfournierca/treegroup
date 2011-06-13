import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree
from . import RenameAttribute
        
        

#===============================================================================
# test the attribute rename generator 
#===============================================================================
    
class test_Generator(unittest.TestCase):
    """Test the Generator class """
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'testfiles', 'AStarTransform', 'RenameAttribute')
        self.log = logging.getLogger()
        
        
    def test_RenameRootAttribute(self):
        """Rename the root element"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'RenameAttributeTest1.xml')
        tree = lxml.etree.parse(testfile)
        
        targetElement = tree.getroot()
        currentAttributeName = 'id'
        newAttributeName = '_'
        
        expectedTree = lxml.etree.fromstring('<dita><topic id="id-2"><title/><body/></topic></dita>')
        generator = RenameAttribute.Generator()
        operand = generator.generateOperand(targetElement, currentAttributeName, newAttributeName)
        result = Tree.Tree.add(tree, operand.getTree())
        
        self.assertTrue(Tree.Tree.equal(expectedTree, result), "Rename Generator generated the wrong operand. Expected result %s, got %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(result)))
      
      
    def test_RenameTopicAttribute(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'RenameAttributeTest2.xml')
        tree = lxml.etree.parse(testfile)
        
        targetElement = tree.getroot()[0]
        currentAttributeName = 'foo'
        newAttributeName = 'id'
        
        expectedTree = lxml.etree.fromstring('<dita><topic id="id-2"><title/><body/></topic></dita>')
        generator = RenameAttribute.Generator()
        operand = generator.generateOperand(targetElement, currentAttributeName, newAttributeName)
        result = Tree.Tree.add(tree, operand.getTree())
        
        self.assertTrue(Tree.Tree.equal(expectedTree, result), "Rename Generator generated the wrong operand. Expected result %s, got %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(result)))
      