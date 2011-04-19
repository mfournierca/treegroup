import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree
from . import Unwrap
        


#===============================================================================
# test the unwrap generator
#===============================================================================

class test_Generator(unittest.TestCase):
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'testfiles', 'AStarTransform', 'Unwrap')
        self.log = logging.getLogger()
        
        
    def test_UnwrapEmptyElement(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running UnwrapEmptyElement')
        testfile = os.path.join(self.testfilesdir, 'UnwrapTest1.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        expectedTree = lxml.etree.fromstring('''<dita></dita>''')
        generator = Unwrap.Generator()
        operand = generator.generateOperand(targetElement)
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.tree)), "UnwrapGenerator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(tree), lxml.etree.tostring(expectedTree)))
    
        
    def test_UnwrapEmptyElementWithSibling(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running UnwrapEmptyElementWithSibling')
        testfile = os.path.join(self.testfilesdir, 'UnwrapTest2.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        expectedTree = lxml.etree.fromstring('''<dita><b/></dita>''')
        generator = Unwrap.Generator()
        operand = generator.generateOperand(targetElement)
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.tree)), "UnwrapGenerator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(tree), lxml.etree.tostring(expectedTree)))
    
    
    def test_UnwrapElementWithChildren(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running UnwrapElementWithChildren')
        testfile = os.path.join(self.testfilesdir, 'UnwrapTest3.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        expectedTree = lxml.etree.fromstring('''<dita><b/><c/></dita>''')
        generator = Unwrap.Generator()
        operand = generator.generateOperand(targetElement)
        self.log.debug('test tree: %s' % lxml.etree.tostring(tree))
        self.log.debug('got operand tree: %s' % lxml.etree.tostring(operand.tree))
        result = Tree.Tree.add(tree, operand.tree)
        self.log.debug('addition result: %s' % lxml.etree.tostring(result))
        self.assertTrue(Tree.Tree.equal(expectedTree, result), "UnwrapGenerator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(result), lxml.etree.tostring(expectedTree)))
    
    
    
    def test_UnwrapElementWithChildrenAndSiblings(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running UnwrapElementWithChildrenAndSiblings')
        testfile = os.path.join(self.testfilesdir, 'UnwrapTest4.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        expectedTree = lxml.etree.fromstring('''<dita><b/><c/><d/></dita>''')
        generator = Unwrap.Generator()
        operand = generator.generateOperand(targetElement)
        self.log.debug('test tree: %s' % lxml.etree.tostring(tree))
        self.log.debug('got operand tree: %s' % lxml.etree.tostring(operand.tree))
        result = Tree.Tree.add(tree, operand.tree)
        self.log.debug('addition result: %s' % lxml.etree.tostring(result))
        self.assertTrue(Tree.Tree.equal(expectedTree, result), "UnwrapGenerator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(result), lxml.etree.tostring(expectedTree)))
        
    
    def test_UnwrapElementWithChildrenAndSiblingsDeepHierarchy(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running UnwrapElementWithChildrenAndSiblingsDeepHierarchy')
        testfile = os.path.join(self.testfilesdir, 'UnwrapTest5.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        expectedTree = lxml.etree.fromstring('''<dita>
                                                    <b>
                                                        <c/>
                                                    </b>
                                                    <d/>
                                                    <e>
                                                        <f>
                                                            <g/>
                                                        </f>
                                                        <h/>
                                                    </e>
                                                </dita>
                                            ''')
        generator = Unwrap.Generator()
        operand = generator.generateOperand(targetElement)
        self.log.debug('test tree: %s' % lxml.etree.tostring(tree))
        self.log.debug('got operand tree: %s' % lxml.etree.tostring(operand.tree))
        result = Tree.Tree.add(tree, operand.tree)
        self.log.debug('addition result: %s' % lxml.etree.tostring(result))
        self.assertTrue(Tree.Tree.equal(expectedTree, result), "UnwrapGenerator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(result), lxml.etree.tostring(expectedTree)))
    
    
    
    
    
    
class test_Iterator(unittest.TestCase):
    """Test the Unwrap Iterator class """
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'testfiles', 'AStarTransform', 'Unwrap')
        self.log = logging.getLogger()
        
        
    def test_IteratorUnwrapFirstElement(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'UnwrapTest1.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.xpath('//a')[0]
        expectedTrees = ['<dita/>'] 

        iterator = Unwrap.Iterator(targetElement)
        index = 0
        for operand in iterator:
            expectedTree = lxml.etree.fromstring(expectedTrees[index])
            self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(operand.tree, tree)), "Wrap Generator generated the wrong operand. Expected %s, got %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.tree)))
            index += 1
    