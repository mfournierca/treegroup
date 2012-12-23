import unittest, os.path, sys, logging

from . import Text






class testaddText(unittest.TestCase):
    """Test the Text.addText() function"""
        
    def setUp(self):
        """set up data used in the tests, called before each test function execution"""
        pass
    
    
    
    #===========================================================================
    # simple tests
    #===========================================================================
    
    def test_WordInverted_1(self):
        word = "Audience"
        inverted = Text.textInverse(word)
        expected = ''
        
        result = Text.addText(word, inverted)
        self.assertEqual(expected, result, 'addText returned "%s", expected "%s"' % (result, expected))


    def test_WordInverted_2(self):
        word = "Sample XHTML Basic document"
        inverted = Text.textInverse(word)
        expected = ''
        
        result = Text.addText(word, inverted)
        self.assertEqual(expected, result, 'addText returned "%s", expected "%s"' % (result, expected))


    def test_WordInverted_3(self):
        word = "Contents"
        inverted = Text.textInverse(word)
        expected = ''
        
        result = Text.addText(word, inverted)
        self.assertEqual(expected, result, 'addText returned "%s", expected "%s"' % (result, expected))




class testtextInverse(unittest.TestCase):
    """test the invert text function"""
    
    def setUp(self):
        pass
    
    def test_invertCharacter(self):
        c = ' '
        expected = ' ' #equivalent to ''
        
        result = Text.textInverse(c)
        self.assertTrue(Text.equal(c, result), 'textInverse returned "%s", expected "%s"' % (result, expected))