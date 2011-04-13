import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree
from . import Generators
        
    
    
    
class test_RenameGenerator(unittest.TestCase):
    """Test the ErrorParser class """
    
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
        expectedTree = lxml.etree.fromstring('''<_>
                                                <sopic/>
                                            </_>''')
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
        expectedTree = lxml.etree.fromstring('''<_>
                                                    <_>
                                                        <_/>
                                                        <aody/>
                                                    </_>
                                                </_>''')
        generator = Generators.RenameGenerator()
        operand = generator.generateOperand(targetElement, acceptableTags[0])
        self.assertTrue(Tree.Tree.equal(expectedTree, operand.tree), "RenameGenerator generated the wrong operand. Expected %s, got %s" % (lxml.etree.tostring(expectedTree), lxml.etree.tostring(operand.tree)))
    