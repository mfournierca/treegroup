import unittest, os.path, sys, logging

from . import Tag






class test_addtags(unittest.TestCase):
    """Test the Tag._addtags() function"""
        
    def setUp(self):
        """set up data used in the tests, called before each test function execution"""
        self.unitchar = '_'
        
    #===========================================================================
    # simple tests
    #===========================================================================
    
    def test_SimpleTag(self):
        tag1 = 'a'
        tag2 = 'a'
        expected = 'b' 
        result = Tag._addtags(tag1, tag2)
        self.assertEqual(expected, result, "_addtags returned %s, expected %s" % (result, expected))
    
    def test_OneTagBlank(self):
        tag1 = self.unitchar
        tag2 = 'a'
        expected = 'a' 
        result = Tag._addtags(tag1, tag2)
        self.assertEqual(expected, result, "_addtags returned %s, expected %s" % (result, expected))
    
    def test_ShouldCycle(self):
        tag1 = 'Z'
        tag2 = 'b'
        expected = 'a' 
        result = Tag._addtags(tag1, tag2)
        self.assertEqual(expected, result, "_addtags returned %s, expected %s" % (result, expected))
    
    def test_ShouldCycleToBlank(self):
        tag1 = 'Z'
        tag2 = 'a'
        expected = self.unitchar 
        result = Tag._addtags(tag1, tag2)
        self.assertEqual(expected, result, "_addtags returned '%s', expected '%s'" % (result, expected))

    def test_NoTag_ShouldFail(self):
        tag1 = ''
        tag2 = 'b'
        expected = 'a' 
        result = Tag._addtags(tag1, tag2)
        self.assertFalse(result, '_addtags() should return False, got %s' % str(result))

    def test_BlankNoChange(self):
        tag1 = self.unitchar
        tag2 = self.unitchar
        expected = self.unitchar 
        result = Tag._addtags(tag1, tag2)
        self.assertEqual(expected, result, "_addtags returned '%s', expected '%s'" % (result, expected))
        
    def test_LongTags(self):
        tag1 = 'aaaaa'
        tag2 = 'aaaaa'
        expected = 'bbbbb' 
        result = Tag._addtags(tag1, tag2)
        self.assertEqual(expected, result, "_addtags returned '%s', expected '%s'" % (result, expected))
        
    def test_MixedTags(self):
        tag1 = 'abcde'
        tag2 = 'abcde'
        expected = 'bdfhj' 
        result = Tag._addtags(tag1, tag2)
        self.assertEqual(expected, result, "_addtags returned '%s', expected '%s'" % (result, expected))
        
    def test_MixedTagsDifferentLengths(self):
        tag1 = 'abcdeZ'
        tag2 = 'abcde'
        expected = 'acegid' 
        result = Tag._addtags(tag1, tag2)
        self.assertEqual(expected, result, "_addtags returned '%s', expected '%s'" % (result, expected))
                
    def test_MixedTagsProducesATrailingUnit(self):
        tag1 = 'abcdeZ'
        tag2 = 'abcdea'
        expected = 'bdfhj_' 
        result = Tag._addtags(tag1, tag2)
        self.assertEqual(expected, result, "_addtags returned '%s', expected '%s'" % (result, expected))
        
    def test_MixedTagsProducesLeadingUnit(self):
        tag1 = 'aabcde'
        tag2 = 'Zabcde'
        expected = 'bdfhj' 
        result = Tag._addtags(tag1, tag2)
        self.assertEqual(expected, result, "_addtags returned '%s', expected '%s'" % (result, expected))
        
    def test_MixedTagsProducesHyphen(self):
        tag1 = 'a'
        tag2 = 'z'
        expected = '_-'
        result = Tag._addtags(tag1, tag2)
        self.assertEqual(expected, result, "_addtags returned '%s', expected '%s'" % (result, expected))
        
    def test_MixedLongTagsProducesHyphen(self):
        tag1 = 'aa'
        tag2 = 'za'
        expected = '_-b'
        result = Tag._addtags(tag1, tag2)
        self.assertEqual(expected, result, "_addtags returned '%s', expected '%s'" % (result, expected))
        
    def test_Digit(self):
        tag1 = 'a'
        tag2 = '1'
        expected = '_2'
        result = Tag._addtags(tag1, tag2)
        self.assertEqual(expected, result, "_addtags returned '%s', expected '%s'" % (result, expected))
        
        
    def test_LeadingDigitLetter(self):
        tag1 = '1a'
        tag2 = 'aa'
        expected = '_2b'
        result = Tag._addtags(tag1, tag2)
        self.assertEqual(expected, result, "_addtags returned '%s', expected '%s'" % (result, expected))
        
    





class test_taginverse(unittest.TestCase):
    """Test the Node._taginverse() function"""
        
    def setUp(self):
        """set up data used in the tests, called before each test function execution"""
        self.unitchar = '_'
    
    def test_SingleChar(self):
        tag = 'a'
        expected = 'Z'
        result = Tag._taginverse(tag)
        self.assertEqual(result, expected, "_taginverse() returned %s, expected %s" % (result, expected))
    
    def test_LongString(self):
        tag = 'abcdef'
        expected = 'ZYXWVU'
        result = Tag._taginverse(tag)
        self.assertEqual(result, expected, "_taginverse() returned %s, expected %s" % (result, expected))
    
    def test_InverseAddition(self):
        tag = 'abcdef'
        inverse = Tag._taginverse(tag)
        expected = self.unitchar
        result = Tag._addtags(tag, inverse)
        self.assertEqual(expected, result, "inverse() returned a tag that is not the inverse")
        
        
        
#    #===========================================================================
#    # test group theory conditions
#    #===========================================================================
#    
#    a + b element of whatever
#    
#    a + (b + c) = (a + b) + c
#    
#    unit exists
#    
#    all a have inverse

