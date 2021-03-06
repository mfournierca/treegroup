import unittest, os.path, sys, logging

from . import Attrib



    
    
class testaddAttribs(unittest.TestCase):
    """Test the Node.addAttribs() function"""
        
    def setUp(self):
        """set up data used in the tests, called before each test function execution"""
        pass
    
    def test_SameAttribs(self):
        attrib1 = {'a': 'a'}
        attrib2 = {'a': 'a'}
        expected = {'a': 'b'}
        result = Attrib.addAttribs(attrib1, attrib2)
        self.assertEqual(expected, result, "addAttribs() returned %s, expected %s" % (str(result), str(expected)))
    
    def test_DifferentValues(self):
        attrib1 = {'a': 'a'}
        attrib2 = {'a': 'b'}
        expected = {'a': 'c'}
        result = Attrib.addAttribs(attrib1, attrib2)
        self.assertEqual(expected, result, "addAttribs() returned %s, expected %s" % (str(result), str(expected)))
    
    def test_DifferentKeys(self):
        attrib1 = {'a': 'a'}
        attrib2 = {'b': 'a'}
        expected = {'a': 'a', 'b': 'a'}
        result = Attrib.addAttribs(attrib1, attrib2)
        self.assertEqual(expected, result, "addAttribs() returned %s, expected %s" % (str(result), str(expected)))
    
    def test_MixedKeys(self):
        attrib1 = {'a': 'a', 'b': 'b', 'd': 'a'}
        attrib2 = {'a': 'a', 'c': 'c', 'd': '9'}
        expected = {'a': 'b', 'b': 'b', 'c': 'c'}
        result = Attrib.addAttribs(attrib1, attrib2)
        self.assertEqual(expected, result, "addAttribs() returned %s, expected %s" % (str(result), str(expected)))
    
    def test_ValueGoesBlank(self):
        attrib1 = {'a': 'a'}
        attrib2 = {'a': '9'}
        expected = {}
        result = Attrib.addAttribs(attrib1, attrib2)
        self.assertEqual(expected, result, "addAttribs() returned %s, expected %s" % (str(result), str(expected)))





class testattribInverse(unittest.TestCase):
      
    def setUp(self):
        """set up data used in the tests, called before each test function execution"""
        pass
    
    def test_SimpleAttrib(self):
        attrib1 = {'a': 'a'}
        expected = {'a': '9'}
        result = Attrib.attribInverse(attrib1)
        self.assertEqual(expected, result, "_attrininverse() returned %s, expected %s" % (str(result), str(expected)))

    def test_MultipleKeys(self):
        attrib1 = {'a': 'a', 'b': 'b'}
        expected = {'a': '9', 'b': '8'}
        result = Attrib.attribInverse(attrib1)
        self.assertEqual(expected, result, "_attrininverse() returned %s, expected %s" % (str(result), str(expected)))
    
    def test_InverseAddition(self):
        attrib1 = {'a': 'a'}
        inverse = Attrib.attribInverse(attrib1)
        result = Attrib.addAttribs(attrib1, inverse)
        expected = {}
        self.assertEqual(expected, result, "_attrininverse() returned an attrib that is not the inverse")
