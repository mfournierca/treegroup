import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree
from . import AppendBefore
        
        

#===============================================================================
# test the AppendBefore generator 
#===============================================================================
    
class test_Generator(unittest.TestCase):
    """Test the Generator class """
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'testfiles', 'AStarTransform', 'AppendBefore')
        self.log = logging.getLogger()
        self.generator = AppendBefore.Generator()
        
        
    def test_SimpleAppendBefore(self):
        """Simple test of append before"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'AppendBeforeTest1.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[1]
        expectedTree = lxml.etree.fromstring('<dita><a><b/></a></dita>')
        operand = self.generator.generateOperand(targetElement)
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(operand.getTree(), tree)), "AppendBefore Generator generated the wrong operand. \
        \nExpected %s\
        \n got %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.getTree())))
      
        
    def test_ComplexAppendBefore(self):
        """Simple test of append before"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'AppendBeforeTest2.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[1]
        expectedTree = lxml.etree.fromstring('''<dita>
                                                    <a>
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
                                                    </a>
                                                </dita>
                                                ''')
        operand = self.generator.generateOperand(targetElement)
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(operand.getTree(), tree)), "AppendBefore Generator generated the wrong operand. \
        \nExpected %s\
        \n got %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.getTree())))
      
        
        
        
        
        
        
        

class test_Iterator(unittest.TestCase):
    """Test the AppendBeforeGeneratorIterator class """
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'testfiles', 'AStarTransform', 'AppendBefore')
        self.log = logging.getLogger()
        
        
#    def test_IteratorAppendBeforeBodyP(self):
#        self.log.debug('')
#        self.log.debug('')
#        self.log.debug('running %s' % __name__)
#        testfile = os.path.join(self.testfilesdir, 'AppendBeforeTest1.xml')
#        tree = lxml.etree.parse(testfile)
#        targetElement = tree.getroot()[0]
#        acceptableTags = ['topic', 'concept', 'task', 'reference', 'glossentry', 'glossgroup']
#        expectedTrees = [
#                         '<dita> <topic/><a/> </dita>',
#                         '<dita> <concept/><a/> </dita>', 
#                         '<dita> <task/><a/> </dita>', 
#                         '<dita> <reference/><a/> </dita>',
#                         '<dita> <glossentry/><a/> </dita>',
#                         '<dita> <glossgroup/><a/> </dita>' 
#                          ] 
#
#        iterator = AppendBefore.Iterator(targetElement, acceptableTags)
#        index = 0
#        for operand in iterator:
#            expectedTree = lxml.etree.fromstring(expectedTrees[index])
#            self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(operand.getTree(), tree)), "AppendBeforeGenerator generated the wrong operand. \
#            \nExpected %s\
#            \ngot %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.getTree())))
#            index += 1
    
    