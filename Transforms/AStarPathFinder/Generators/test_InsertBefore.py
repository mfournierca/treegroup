import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree
from . import InsertBefore
        
        

#===============================================================================
# test the InsertBefore generator 
#===============================================================================
    
class test_Generator(unittest.TestCase):
    """Test the Generator class """
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'testfiles', 'AStarTransform', 'InsertBefore')
        self.log = logging.getLogger()
        self.generator = InsertBefore.Generator()
        
        
    def test_SimpleInsertBefore(self):
        """Simple test of insert before"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'InsertBeforeTest1.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        expectedTree = lxml.etree.fromstring('<dita><b/><a/></dita>')
        operand = self.generator.generateOperand(targetElement, 'b')
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(operand.getTree(), tree)), "InsertBefore Generator generated the wrong operand. \
        \nExpected %s\
        \n got %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.getTree())))
      
        
    def test_ComplexTree(self):
        """Simple test of insert before"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'InsertBeforeTest2.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        expectedTree = lxml.etree.fromstring('''<dita>
                                                <b/>
                                                <a>
                                                    <b>
                                                        <c/>
                                                    </b>
                                                    <d/>
                                                </a>
                                                <e>
                                                    <f>
                                                        <g/>
                                                    </f>
                                                    <h/>
                                                </e>
                                            </dita>
                                            ''')
        operand = self.generator.generateOperand(targetElement, 'b')
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(operand.getTree(), tree)), "InsertBefore Generator generated the wrong operand. \
        \nExpected %s\
        \ngot %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.getTree())))
      
        
        
    def test_ComplexTreeOtherLocation(self):
        """Simple test of insert before"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'InsertBeforeTest2.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[1]
        expectedTree = lxml.etree.fromstring('''<dita>
                                                <a>
                                                    <b>
                                                        <c/>
                                                    </b>
                                                    <d/>
                                                </a>
                                                <b/>
                                                <e>
                                                    <f>
                                                        <g/>
                                                    </f>
                                                    <h/>
                                                </e>
                                            </dita>
                                            ''')
        operand = self.generator.generateOperand(targetElement, 'b')
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(operand.getTree(), tree)), "InsertBefore Generator generated the wrong operand. \
        \nExpected %s \
        \ngot %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.getTree())))
      
        
        
    def test_InsertBeforeRoot(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'InsertBeforeTest1.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()
        operand = self.generator.generateOperand(targetElement, 'b')
        self.assertTrue(operand is None, "InsertBefore Generator should have returned None, returned %s" % str(operand))
        
        
        
        
    def test_ComplexTreeWithText(self):
        """Simple test of insert before"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'InsertBeforeTest3.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[1]
        expectedTree = lxml.etree.fromstring('''<dita>
                                                <a>
                                                    <b>
                                                        <c>abcd</c>
                                                    </b>
                                                    <d/>
                                                </a>
                                                <b/>
                                                <e>
                                                    <f>
                                                        <g>efg</g>
                                                    </f>
                                                    <h/>
                                                </e>
                                                <a>
                                                    <b>hijk</b>
                                                </a>
                                            </dita>
                                            ''')
        operand = self.generator.generateOperand(targetElement, 'b')
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(operand.getTree(), tree)), "InsertBefore Generator generated the wrong operand. \
        \nExpected %s \
        \ngot %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.getTree())))
      
        
        
    def test_FullDitaFile(self):
        """Test on a full dita file"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        
        tree = lxml.etree.parse(os.path.join(self.testfilesdir, 'InsertBeforeTest4.xml'))
        targetElement = tree.getroot()[0][0]
        expectedTree = lxml.etree.parse(os.path.join(self.testfilesdir, 'InsertBeforeTest4_expected.xml'))
        
        operand = self.generator.generateOperand(targetElement, 'title')
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(operand.getTree(), tree)), "InsertBefore Generator generated the wrong operand. \
        \nExpected %s \
        \ngot %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.getTree())))
      
        
        
        
        
        
        

class test_Iterator(unittest.TestCase):
    """Test the InsertBeforeGeneratorIterator class """
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'testfiles', 'AStarTransform', 'InsertBefore')
        self.log = logging.getLogger()
        
        
    def test_IteratorInsertBeforeBodyP(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'InsertBeforeTest1.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        acceptableTags = ['topic', 'concept', 'task', 'reference', 'glossentry', 'glossgroup']
        expectedTrees = [
                         '<dita> <topic/><a/> </dita>',
                         '<dita> <concept/><a/> </dita>', 
                         '<dita> <task/><a/> </dita>', 
                         '<dita> <reference/><a/> </dita>',
                         '<dita> <glossentry/><a/> </dita>',
                         '<dita> <glossgroup/><a/> </dita>' 
                          ] 

        iterator = InsertBefore.Iterator(targetElement, acceptableTags)
        index = 0
        for operand in iterator:
            expectedTree = lxml.etree.fromstring(expectedTrees[index])
            self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(operand.getTree(), tree)), "InsertBeforeGenerator generated the wrong operand. \
            \nExpected %s\
            \ngot %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.getTree())))
            index += 1
    
    