import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree
from . import Neighbors
        
    
    
    
class test_RenameGenerator(unittest.TestCase):
    """Test the Rename() operation"""
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'AStarTransform', 'Rename')
        self.log = logging.getLogger()
        
    def test_1(self):
        """RenameTest1.xml has only the root element, the rename operand 
        should just rename this root"""
        
        testfile = os.path.join(self.testfilesdir, 'RenameTest1.xml')
        tree = lxml.etree.parse(testfile)
        targetelement = tree.getroot()
        expectedtree = lxml.etree.fromstring('<cita/>')
        #error message was generated on the command line, if there are problems with the errormessage 
        #in the future, then this is probably out of date. 
        errormessage = 'file1.xml:2:0:ERROR:VALID:DTD_UNKNOWN_ELEM: No declaration for element a'
        
        generator = Neighbors.RenameGenerator()
        result = generator.generateRenameOperands(tree, targetelement, errormessage)
        self.assertTrue(Tree.Tree.equal(result, expectedtree), 'Rename() returned %s, expected %s' % (lxml.etree.tostring(result), lxml.etree.tostring(expectedtree)))

        
#    def test_2(self):
#        """RenameTest2.xml has a misnamed element beneath dita."""
#        
#        testfile = os.path.join(self.testfilesdir, 'RenameTest2.xml')
#        tree = lxml.etree.parse(testfile)
#        targetelement = tree.getroot()[0]
#        
#        expectedtree = lxml.etree.fromstring("""<_>
#                                                    <sopic/>
#                                                </_>
#                                            """)
#        
#        result = Neighbors.Rename(tree, targetelement)
#        self.assertTrue(Tree.Tree.equal(result, expectedtree), 'Rename() returned the wrong tree')
        