import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree
from . import Wrap
        
    

#===============================================================================
# test the wrap generator
#===============================================================================


class test_WrapGenerator(unittest.TestCase):
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'testfiles', 'AStarTransform', 'Wrap')
        self.log = logging.getLogger()
        
        
    def test_WrapSimpleElement(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running WrapSimpleElement')
        testfile = os.path.join(self.testfilesdir, 'WrapTest1.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        tag = 'topic'
        expectedTree = lxml.etree.fromstring('''<dita><topic><a/></topic></dita>''')
        generator = Wrap.Generator()
        operand = generator.generateOperand(targetElement, tag)
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.getTree())), "Wrap Generator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(tree), lxml.etree.tostring(expectedTree)))
    
            
    def test_WrapRoot(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running WrapSimpleElement')
        testfile = os.path.join(self.testfilesdir, 'WrapTest1.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()
        tag = 'dita'
        expectedTree = lxml.etree.fromstring('''<dita><dita><a/></dita></dita>''')
        generator = Wrap.Generator()
        operand = generator.generateOperand(targetElement, tag)
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.getTree())), "Wrap Generator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(tree), lxml.etree.tostring(expectedTree)))
    
        
    def test_WrapElementWithSibling(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running WrapElementWithSibling')
        testfile = os.path.join(self.testfilesdir, 'WrapTest2.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        tag = 'topic'
        expectedTree = lxml.etree.fromstring('''<dita><topic><a/></topic><b/></dita>''')
        generator = Wrap.Generator()
        operand = generator.generateOperand(targetElement, tag)
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.getTree())), "Wrap Generator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(tree), lxml.etree.tostring(expectedTree)))
    
        
            
    def test_WrapElementWithChildren(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running WrapElementWithChildren')
        testfile = os.path.join(self.testfilesdir, 'WrapTest3.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        tag = 'topic'
        expectedTree = lxml.etree.fromstring('''<dita><topic><a><b/><c/></a></topic></dita>''')
        generator = Wrap.Generator()
        operand = generator.generateOperand(targetElement, tag)
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.getTree())), "Wrap Generator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(tree), lxml.etree.tostring(expectedTree)))
    
            
        
    def test_WrapElementWithChildrenAndSibling(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running test_WrapElementWithChildrenAndSibling')
        testfile = os.path.join(self.testfilesdir, 'WrapTest4.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        tag = 'topic'
        expectedTree = lxml.etree.fromstring('''<dita><topic><a><b/><c/></a></topic><d/></dita>''')
        generator = Wrap.Generator()
        operand = generator.generateOperand(targetElement, tag)
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.getTree())), "Wrap Generator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(tree), lxml.etree.tostring(expectedTree)))
    
    
    def test_WrapElementWithChildrenAndSiblingDeepHierarchy(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running test_WrapElementWithChildrenAndSiblingDeepHierarchy')
        testfile = os.path.join(self.testfilesdir, 'WrapTest5.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        tag = 'topic'
        expectedTree = lxml.etree.fromstring('''<dita>
                                                    <topic>
                                                        <a>
                                                            <b>
                                                                <c/>
                                                            </b>
                                                            <d/>
                                                        </a>
                                                    </topic>
                                                    <e>
                                                        <f>
                                                            <g/>
                                                        </f>
                                                        <h/>
                                                    </e>
                                                </dita>''')
        generator = Wrap.Generator()
        operand = generator.generateOperand(targetElement, tag)
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.getTree())), "Wrap Generator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(tree), lxml.etree.tostring(expectedTree)))
    
    
    
    
    
    
    

class test_Iterator(unittest.TestCase):
    """Test the Wrap Iterator class """
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'testfiles', 'AStarTransform', 'Wrap')
        self.log = logging.getLogger()
        
        
    def test_IteratorWrapFirstElement(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'WrapTest1.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.xpath('//a')[0]
        acceptableTags = ['topic', 'concept', 'task', 'reference', 'glossentry', 'glossgroup']
        expectedTrees = ['<dita> <topic><a/></topic> </dita>', '<dita> <concept><a/></concept> </dita>', '<dita> <task><a/></task> </dita>', '<dita> <reference><a/></reference> </dita>', '<dita> <glossentry><a/></glossentry> </dita>', '<dita> <glossgroup><a/></glossgroup> </dita>'] 

        iterator = Wrap.Iterator(targetElement, acceptableTags)
        index = 0
        for operand in iterator:
            expectedTree = lxml.etree.fromstring(expectedTrees[index])
            self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(operand.getTree(), tree)), "Wrap Generator generated the wrong operand. Expected %s, got %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.getTree())))
            index += 1
