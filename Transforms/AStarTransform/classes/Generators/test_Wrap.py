import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree
from . import Wrap
        
    
   
    
    
    
    
    
    
    
    
    
    
    
#===============================================================================
# test the wrap generator
#===============================================================================


class test_WrapGenerator(unittest.TestCase):
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'testfiles', 'AStarTransform', 'Wrap')
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
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.tree)), "Wrap Generator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(tree), lxml.etree.tostring(expectedTree)))
    
            
        
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
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.tree)), "Wrap Generator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(tree), lxml.etree.tostring(expectedTree)))
    
        
            
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
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.tree)), "Wrap Generator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(tree), lxml.etree.tostring(expectedTree)))
    
            
        
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
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.tree)), "Wrap Generator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(tree), lxml.etree.tostring(expectedTree)))
    
    
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
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.tree)), "Wrap Generator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(tree), lxml.etree.tostring(expectedTree)))
    