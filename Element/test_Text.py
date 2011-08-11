import unittest, os.path, sys, logging

from . import Text






class test_addtext(unittest.TestCase):
    """Test the Text._addtext() function"""
        
    def setUp(self):
        """set up data used in the tests, called before each test function execution"""
        pass
    
    
    
    #===========================================================================
    # simple tests
    #===========================================================================
    
    def test_WordInverted_1(self):
        word = "Audience"
        inverted = Text._textinverse(word)
        expected = ''
        
        result = Text._addtext(word, inverted)
        self.assertEqual(expected, result, '_addtext returned "%s", expected "%s"' % (result, expected))


    def test_WordInverted_2(self):
        word = "Sample XHTML Basic document"
        inverted = Text._textinverse(word)
        expected = ''
        
        result = Text._addtext(word, inverted)
        self.assertEqual(expected, result, '_addtext returned "%s", expected "%s"' % (result, expected))


    def test_WordInverted_3(self):
        word = "Contents"
        inverted = Text._textinverse(word)
        expected = ''
        
        result = Text._addtext(word, inverted)
        self.assertEqual(expected, result, '_addtext returned "%s", expected "%s"' % (result, expected))




class test_textinverse(unittest.TestCase):
    """test the invert text function"""
    
    def setUp(self):
        pass
    
    def test_invertCharacter(self):
        c = ' '
        expected = '~'
        
        result = Text._textinverse(c)
        self.assertEqual(c, result, '_textinverse returned "%s", expected "%s"' % (result, expected))