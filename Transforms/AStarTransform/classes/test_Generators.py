import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree
from . import Generators
        
    
   
#===============================================================================
# test the rename generator 
#===============================================================================
    
class test_RenameGenerator(unittest.TestCase):
    """Test the RenameGenerator class """
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'testfiles', 'AStarTransform', 'Rename')
        self.log = logging.getLogger()
        
        
    def test_RenameRoot(self):
        """Rename the root element"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'RenameTest1.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()
        acceptableTags = ['dita']
        expectedTree = lxml.etree.fromstring('<cita/>')
        generator = Generators.RenameGenerator()
        operand = generator.generateOperand(targetElement, acceptableTags[0])
        self.assertTrue(Tree.Tree.equal(expectedTree, operand.tree), "RenameGenerator generated the wrong operand. Expected %s, got %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.tree)))
      
        
    def test_RenameFirstLevelTopic(self):
        """Rename the first level topic element"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'RenameTest2.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        acceptableTags = ['topic']
        expectedTree = lxml.etree.fromstring('''<_> <sopic/> </_>''')
        generator = Generators.RenameGenerator()
        operand = generator.generateOperand(targetElement, acceptableTags[0])
        self.assertTrue(Tree.Tree.equal(expectedTree, operand.tree), "RenameGenerator generated the wrong operand. Expected %s, got %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.tree)))

      
    def test_RenameTopicBody(self):
        """Rename an element that should be body"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'RenameTest3.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0][1]
        acceptableTags = ['body']
        expectedTree = lxml.etree.fromstring('''<_> <_> <_/> <aody/> </_> </_>''')
        generator = Generators.RenameGenerator()
        operand = generator.generateOperand(targetElement, acceptableTags[0])
        self.assertTrue(Tree.Tree.equal(expectedTree, operand.tree), "RenameGenerator generated the wrong operand. Expected %s, got %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.tree)))
    
    
    def test_RenameBodyP(self):
        """Rename an element that should be p"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'RenameTest4.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.xpath('//a')[0]
        acceptableTags = ['p']
        expectedTree = lxml.etree.fromstring('''<_> <_> <_/> <_> <_/> <o/> </_> </_> </_>''')
        generator = Generators.RenameGenerator()
        operand = generator.generateOperand(targetElement, acceptableTags[0])
        self.assertTrue(Tree.Tree.equal(expectedTree, operand.tree), "RenameGenerator generated the wrong operand. Expected %s, got %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.tree)))
    
    

class test_RenameGeneratorIterator(unittest.TestCase):
    """Test the RenameGeneratorIterator class """
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'testfiles', 'AStarTransform', 'Rename')
        self.log = logging.getLogger()
        
        
    def test_RenameBodyP(self):
        """Rename an element in a body"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running %s' % __name__)
        testfile = os.path.join(self.testfilesdir, 'RenameTest2.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.xpath('//a')[0]
        acceptableTags = ['topic', 'concept', 'task', 'reference', 'glossentry', 'glossgroup']
        expectedTrees = ['<_> <sopic/> </_>', '<_> <boncept/> </_>', '<_> <sask/> </_>', '<_> <qeference/> </_>', '<_> <flossentry/> </_>', '<_> <flossgroup/> </_>'] 

        iterator = Generators.RenameGeneratorIterator(targetElement, acceptableTags)
        index = 0
        for operand in iterator:
            expectedTree = lxml.etree.fromstring(expectedTrees[index])
            self.assertTrue(Tree.Tree.equal(expectedTree, operand.tree), "RenameGenerator generated the wrong operand. Expected %s, got %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.tree)))
            index += 1
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#===============================================================================
# test the unwrap generator
#===============================================================================

class test_UnwrapGenerator(unittest.TestCase):
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'testfiles', 'AStarTransform', 'Unwrap')
        self.log = logging.getLogger()
        
        
    def test_UnwrapEmptyElement(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running UnwrapEmptyElement')
        testfile = os.path.join(self.testfilesdir, 'UnwrapTest1.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        expectedTree = lxml.etree.fromstring('''<dita></dita>''')
        generator = Generators.UnwrapGenerator()
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
        generator = Generators.UnwrapGenerator()
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
        generator = Generators.UnwrapGenerator()
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
        generator = Generators.UnwrapGenerator()
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
        generator = Generators.UnwrapGenerator()
        operand = generator.generateOperand(targetElement)
        self.log.debug('test tree: %s' % lxml.etree.tostring(tree))
        self.log.debug('got operand tree: %s' % lxml.etree.tostring(operand.tree))
        result = Tree.Tree.add(tree, operand.tree)
        self.log.debug('addition result: %s' % lxml.etree.tostring(result))
        self.assertTrue(Tree.Tree.equal(expectedTree, result), "UnwrapGenerator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(result), lxml.etree.tostring(expectedTree)))
    
    
    
    
    
    
    
    
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
        generator = Generators.WrapGenerator()
        operand = generator.generateOperand(targetElement, tag)
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.tree)), "UnwrapGenerator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(tree), lxml.etree.tostring(expectedTree)))
    
            
        
    def test_WrapElementWithSibling(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running WrapElementWithSibling')
        testfile = os.path.join(self.testfilesdir, 'WrapTest2.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        tag = 'topic'
        expectedTree = lxml.etree.fromstring('''<dita><topic><a/></topic><b/></dita>''')
        generator = Generators.WrapGenerator()
        operand = generator.generateOperand(targetElement, tag)
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.tree)), "UnwrapGenerator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(tree), lxml.etree.tostring(expectedTree)))
    
        
            
    def test_WrapElementWithChildren(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running WrapElementWithChildren')
        testfile = os.path.join(self.testfilesdir, 'WrapTest3.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        tag = 'topic'
        expectedTree = lxml.etree.fromstring('''<dita><topic><a><b/><c/></a></topic></dita>''')
        generator = Generators.WrapGenerator()
        operand = generator.generateOperand(targetElement, tag)
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.tree)), "UnwrapGenerator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(tree), lxml.etree.tostring(expectedTree)))
    
            
        
    def test_WrapElementWithChildrenAndSibling(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running test_WrapElementWithChildrenAndSibling')
        testfile = os.path.join(self.testfilesdir, 'WrapTest4.xml')
        tree = lxml.etree.parse(testfile)
        targetElement = tree.getroot()[0]
        tag = 'topic'
        expectedTree = lxml.etree.fromstring('''<dita><topic><a><b/><c/></a></topic><d/></dita>''')
        generator = Generators.WrapGenerator()
        operand = generator.generateOperand(targetElement, tag)
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.tree)), "UnwrapGenerator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(tree), lxml.etree.tostring(expectedTree)))
    
    
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
        generator = Generators.WrapGenerator()
        operand = generator.generateOperand(targetElement, tag)
        self.assertTrue(Tree.Tree.equal(expectedTree, Tree.Tree.add(tree, operand.tree)), "UnwrapGenerator generated the wrong operand. Operand results in %s, expected %s" % (lxml.etree.tostring(tree), lxml.etree.tostring(expectedTree)))
    