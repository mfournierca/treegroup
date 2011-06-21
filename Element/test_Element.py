import unittest, os.path, sys, logging

import lxml.etree
from . import Element

    
    
class test_equal(unittest.TestCase):
    """Test the Node.equal() function"""
        
    def setUp(self):
        """set up data used in the tests, called before each test function execution"""
        self.testfile = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'Node', 'NodeTestFile_equal.xml')
        self.testtree = lxml.etree.parse(self.testfile)
    
    #note the indices of the elements being testing do not increase be 1 each time - you
    #have to account for comments. See the self.testfile for details. 
            
    def test_SimpleEqual(self):
        element1 = self.testtree.getroot()[2]
        element2 = self.testtree.getroot()[3]
        result = Element.equal(element1, element2)
        self.assertTrue(result, "equal() returned %s, expected True" % str(result))

    def test_SimpleUnequal_AttribDiffer(self):
        element1 = self.testtree.getroot()[5]
        element2 = self.testtree.getroot()[6]
        result = Element.equal(element1, element2)
        self.assertFalse(result, "equal() returned %s, expected False" % str(result))
    
    def test_SimpleUnequal_TagsDiffer(self):
        element1 = self.testtree.getroot()[7]
        element2 = self.testtree.getroot()[8]
        result = Element.equal(element1, element2)
        self.assertFalse(result, "equal() returned %s, expected False" % str(result))

    def test_SimpleUnequal_TagsAndAttribsDiffer(self):
        element1 = self.testtree.getroot()[9]
        element2 = self.testtree.getroot()[10]
        result = Element.equal(element1, element2)
        self.assertFalse(result, "equal() returned %s, expected False" % str(result))

        
    def test_ComplexEqual(self):
        element1 = self.testtree.getroot()[12]
        element2 = self.testtree.getroot()[13]
        result = Element.equal(element1, element2)
        self.assertTrue(result, "equal() returned %s, expected True" % str(result))

    def test_ComplexUnequal_AttribDiffer(self):
        element1 = self.testtree.getroot()[15]
        element2 = self.testtree.getroot()[16]
        result = Element.equal(element1, element2)
        self.assertFalse(result, "equal() returned %s, expected False" % str(result))

    def test_ComplexUnequal_OtherAttribDiffer(self):
        element1 = self.testtree.getroot()[17]
        element2 = self.testtree.getroot()[18]
        result = Element.equal(element1, element2)
        self.assertFalse(result, "equal() returned %s, expected False" % str(result))

    def test_ComplexUnequal_TagsDiffer(self):
        element1 = self.testtree.getroot()[19]
        element2 = self.testtree.getroot()[20]
        result = Element.equal(element1, element2)
        self.assertFalse(result, "equal() returned %s, expected False" % str(result))

    def test_ComplexUnequal_TagsAndAttribsDiffer(self):
        element1 = self.testtree.getroot()[21]
        element2 = self.testtree.getroot()[22]
        result = Element.equal(element1, element2)
        self.assertFalse(result, "equal() returned %s, expected False" % str(result))

    def test_EqualText(self):
        element1 = self.testtree.getroot()[24]
        element2 = self.testtree.getroot()[25]
        result = Element.equal(element1, element2)
        self.assertTrue(result, "equal() returned %s, expected True" % str(result))
    
    def test_EqualTextAndTail(self):
        element1 = self.testtree.getroot()[26]
        element2 = self.testtree.getroot()[27]
        result = Element.equal(element1, element2)
        self.assertTrue(result, "equal() returned %s, expected True" % str(result))
    
    def test_UnequalText(self):
        element1 = self.testtree.getroot()[29]
        element2 = self.testtree.getroot()[30]
        result = Element.equal(element1, element2)
        self.assertFalse(result, "equal() returned %s, expected False" % str(result))
    
    def test_EqualTextMissingTail(self):
        element1 = self.testtree.getroot()[31]
        element2 = self.testtree.getroot()[32]
        result = Element.equal(element1, element2)
        self.assertFalse(result, "equal() returned %s, expected False" % str(result))
    
    def test_EqualTextUnequalTail(self):
        element1 = self.testtree.getroot()[33]
        element2 = self.testtree.getroot()[34]
        result = Element.equal(element1, element2)
        self.assertFalse(result, "equal() returned %s, expected False" % str(result))
    
    def test_UnequalTextEqualTail(self):
        element1 = self.testtree.getroot()[35]
        element2 = self.testtree.getroot()[36]
        result = Element.equal(element1, element2)
        self.assertFalse(result, "equal() returned %s, expected False" % str(result))
    
    

    
  
    
    
    
class test_add(unittest.TestCase):
    """Test the Node.add() function"""
        
    def setUp(self):
        """set up data used in the tests, called before each test function execution"""
        self.testfile = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'Node', 'NodeTestFile_add.xml')
        self.testtree = lxml.etree.parse(self.testfile)
    
    #note the indices of the elements being tested do not increase be 1 each time - you
    #have to account for comments. See the self.testfile for details. 
    
    def test_SimpleNodes(self):
        element1 = self.testtree.getroot()[2]
        element2 = self.testtree.getroot()[3]

        Element.add(element1, element2)
        expected = lxml.etree.Element('c', {'id': 'c'})
        
        self.assertTrue(Element.equal(element1, expected), 'add() failed: expected %s, got %s'\
                         % (expected.tag + ' ' + str(expected.attrib), element1.tag + ' ' + str(element1.attrib)))
                        
                           
    def test_ComplexNode(self):
        element1 = self.testtree.getroot()[5]
        element2 = self.testtree.getroot()[6]
        
        Element.add(element1, element2)
        expected = lxml.etree.Element('d', {'id': 'b', 'property': 'b'})
        
        self.assertTrue(Element.equal(element1, expected), 'add() failed: expected %s, got %s'\
                         % (expected.tag + ' ' + str(expected.attrib), element1.tag + ' ' + str(element1.attrib)))
    
    
    def test_LongComplex(self):
        element1 = self.testtree.getroot()[7]
        element2 = self.testtree.getroot()[8]
        
        Element.add(element1, element2)
        expected = lxml.etree.Element('df', {'id': 'bdfhj'})
        
        self.assertTrue(Element.equal(element1, expected), 'add() failed: expected %s, got %s' \
                        % (expected.tag + ' ' + str(expected.attrib), element1.tag + ' ' + str(element1.attrib)))
    
    
    def test_AttributeShouldDissapear(self):
        element1 = self.testtree.getroot()[9]
        element2 = self.testtree.getroot()[10]
        
        Element.add(element1, element2)
        expected = lxml.etree.Element('c')
        
        self.assertTrue(Element.equal(element1, expected), 'add() failed: expected %s, got %s' \
                        % (expected.tag + ' ' + str(expected.attrib), element1.tag + ' ' + str(element1.attrib)))
    
    
    def test_AddingUnit(self):
        element1 = self.testtree.getroot()[12]
        element2 = self.testtree.getroot()[13]
        
        Element.add(element1, element2)
        expected = lxml.etree.Element('a', {'id': 'a'})
        
        self.assertTrue(Element.equal(element1, expected), 'add() failed: expected %s, got %s'\
                         % (expected.tag + ' ' + str(expected.attrib), element1.tag + ' ' + str(element1.attrib)))
    
    
    def test_AddingElementsWithText(self):
        element1 = self.testtree.getroot()[15]
        element2 = self.testtree.getroot()[16]
        
        Element.add(element1, element2)
        expected = lxml.etree.fromstring('<a>C</a>')
        Element.equal(element1, expected)
       
        self.assertTrue(Element.equal(element1, expected), 'add() failed: expected %s, got %s'\
                         % (lxml.etree.tostring(expected), lxml.etree.tostring(element1)))
        
    def test_AddingElementsWithTextAndTail(self):
        element1 = self.testtree.getroot()[17]
        element2 = self.testtree.getroot()[18]
        
        Element.add(element1, element2)
        expected = lxml.etree.Element('a')
        expected.text = 'CEG'
        expected.tail = 'I K M'
        Element.equal(element1, expected)
       
        self.assertTrue(Element.equal(element1, expected), 'add() failed: expected %s, got %s'\
                         % (lxml.etree.tostring(expected), lxml.etree.tostring(element1)))
        
    

    
    
    
class test_invert(unittest.TestCase):
    """Test the Node.inverse() function"""
        
    #note the indices of the elements being tested do not increase be 1 each time - you
    #have to account for comments. See the self.testfile for details. 
    
    def setUp(self):
        """set up data used in the tests, called before each test function execution"""
        self.testfile = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'Node', 'NodeTestFile_inverse.xml')
        self.testtree = lxml.etree.parse(self.testfile)
        

    def test_SimpleNode(self):
        element1 = self.testtree.getroot()[2]
        
        Element.invert(element1)
        expected = lxml.etree.Element('Z', {'id': '9'})
        
        self.assertTrue(Element.equal(element1, expected), 'inverse() failed: expected %s, got %s'\
                         % (expected.tag + ' ' + str(expected.attrib), element1.tag + ' ' + str(element1.attrib)))

    
    def test_ComplexNode(self):
        element1 = self.testtree.getroot()[4]
        
        Element.invert(element1)
        expected = lxml.etree.Element('Y', {'id': '9', 'property': '9'})
        
        self.assertTrue(Element.equal(element1, expected), 'inverse() failed: expected %s, got %s' \
                        % (expected.tag + ' ' + str(expected.attrib), element1.tag + ' ' + str(element1.attrib)))

    
    def test_LongComplexNode(self):
        element1 = self.testtree.getroot()[5]
        
        Element.invert(element1)
        expected = lxml.etree.Element('ZY', {'id': '98765'})
        
        self.assertTrue(Element.equal(element1, expected), 'inverse() failed: expected %s, got %s' \
                        % (expected.tag + ' ' + str(expected.attrib), element1.tag + ' ' + str(element1.attrib)))


    
    def test_Unit(self):
        element1 = self.testtree.getroot()[7]
        
        Element.invert(element1)
        expected = lxml.etree.Element('_')
        
        self.assertTrue(Element.equal(element1, expected), 'inverse() failed: expected %s, got %s'\
                         % (expected.tag + ' ' + str(expected.attrib), element1.tag + ' ' + str(element1.attrib)))

    
    def test_InverseAddition(self):
        element1 = self.testtree.getroot()[2]
        element2 = lxml.etree.Element(element1.tag, element1.attrib)
        
        Element.invert(element1)
        Element.add(element1, element2)
        expected = lxml.etree.Element('_')
        
        self.assertTrue(Element.equal(element1, expected), 'inverse() failed: expected %s, got %s'\
                         % (expected.tag + ' ' + str(expected.attrib), element1.tag + ' ' + str(element1.attrib)))

    
    def test_InvertNodeWithTextAndTail(self):
        element1 = self.testtree.getroot()[9]
        Element.invert(element1)
        
        expected = lxml.etree.Element('Z')
        expected.text = '<;:9'
        expected.tail = '8765'
        
        self.assertTrue(Element.equal(element1, expected), 'inverse() failed: expected %s, got %s'\
                         % (lxml.etree.tostring(expected), lxml.etree.tostring(element1)))

    
        
    
    

class test_position(unittest.TestCase):
    """Test the Node.position() function"""
        
    #note the indices of the elements being tested do not increase be 1 each time - you
    #have to account for comments. See the self.testfile for details. 
    
    def setUp(self):
        """set up data used in the tests, called before each test function execution"""
        self.testfile = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'Node', 'NodeTestFile1.xml')
        self.testtree = lxml.etree.parse(self.testfile)
        
            
    def test_Root(self):
        expected = [1]
        result = Element.position(self.testtree.getroot())
        self.assertEqual(expected, result, 'position() failed: expected %s, got %s' % (str(expected), str(result)))
        
        
    def test_FirstChild(self):
        expected = [1, 1]
        result = Element.position(self.testtree.getroot()[0])
        self.assertEqual(expected, result, 'position() failed: expected %s, got %s' % (str(expected), str(result)))
    
        
    def test_SecondChild(self):
        expected = [1, 2]
        result = Element.position(self.testtree.getroot()[1])
        self.assertEqual(expected, result, 'position() failed: expected %s, got %s' % (str(expected), str(result)))
    
    
    def test_DeeplyNested(self):
        expected = [1, 3, 3, 1, 1]
        result = Element.position(self.testtree.xpath('//newborn[@id="8"]')[0])
        self.assertEqual(expected, result, 'position() failed: expected %s, got %s' % (str(expected), str(result)))
    
    
    def test_DifferentRootNode_Grandchild(self):
        expected = [1, 3, 1, 1]
        result = Element.position(self.testtree.xpath('//newborn[@id="8"]')[0], root=self.testtree.getroot()[2])
        self.assertEqual(expected, result, 'position() failed: expected %s, got %s' % (str(expected), str(result)))
        
        
    def test_DifferentRootNode_RootNode(self):
        expected = [1]
        result = Element.position(self.testtree.getroot()[2], root=self.testtree.getroot()[2])
        self.assertEqual(expected, result, 'position() failed: expected %s, got %s' % (str(expected), str(result)))
        
    
    