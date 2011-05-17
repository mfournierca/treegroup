import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree
from . import Errors
        
    
    
    
class test_ErrorParser(unittest.TestCase):
    """Test the ErrorParser class """
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', 'testfiles', 'AStarTransform', 'Errors')
        self.log = logging.getLogger()
        
        
    def test_1(self):
        """Test the unknown element error message"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running test test_1')
        testfile = os.path.join(self.testfilesdir, 'ErrorTest1.xml')
        tree = lxml.etree.parse(testfile)
        expectedtargetelement = tree.getroot()
        expectederrormessage = '/Users/matt/work/programs/dev_workspace/TreeGroup/Transforms/AStarPathFinder/../../testfiles/AStarTransform/Errors/ErrorTest1.xml:2:0:ERROR:VALID:DTD_UNKNOWN_ELEM: No declaration for element a'
        expectedtags = ['dita']
        
        parser = Errors.ErrorParser(tree)
        parser.parse()
        
        self.assertEqual(parser.errorMessage, expectederrormessage, 'ErrorParser parsed the wrong error. Expected %s, got %s' % (expectederrormessage, parser.errorMessage))
        self.assertEqual(expectedtags, parser.acceptableTags, 'ErrorParser parsed the wrong tags. Expected %s, got %s' % (expectedtags, parser.acceptableTags))
        self.assertTrue(expectedtargetelement is parser.targetElement, 'ErrorParser parsed the wrong target element. Expected %s, got %s' % (expectedtargetelement, parser.targetElement))
    
    
    def test_2(self):
        """test a DTD_CONTENT_MODEL error message"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running test test_2')
        testfile = os.path.join(self.testfilesdir, 'ErrorTest2.xml')
        tree = lxml.etree.parse(testfile)
        expectedtargetelement = tree.getroot()[0]
        expectederrormessage = '/Users/matt/work/programs/dev_workspace/TreeGroup/Transforms/AStarPathFinder/../../testfiles/AStarTransform/Errors/ErrorTest2.xml:2:0:ERROR:VALID:DTD_CONTENT_MODEL: Element dita content does not follow the DTD, expecting (topic | concept | task | reference | glossentry)+, got (a )'
        expectedtags = ['concept', 'glossentry', 'reference', 'task', 'topic']
        
        parser = Errors.ErrorParser(tree)
        parser.parse()
        
        self.assertEqual(parser.errorMessage, expectederrormessage, 'ErrorParser parsed the wrong error. Expected %s, got %s' % (expectederrormessage, parser.errorMessage))
        self.assertEqual(expectedtags, parser.acceptableTags, 'ErrorParser parsed the wrong tags. Expected %s, got %s' % (expectedtags, parser.acceptableTags))
        self.assertTrue(expectedtargetelement is parser.targetElement, 'ErrorParser parsed the wrong target element. Expected %s, got %s' % (expectedtargetelement, parser.targetElement))

 
    def test_3(self):
        """test a DTD_CONTENT_MODEL error message"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running test test_3')
        testfile = os.path.join(self.testfilesdir, 'ErrorTest3.xml')
        tree = lxml.etree.parse(testfile)
        expectedtargetelement = tree.xpath('//a')[0]
        expectederrormessage = '/Users/matt/work/programs/dev_workspace/TreeGroup/Transforms/AStarPathFinder/../../testfiles/AStarTransform/Errors/ErrorTest3.xml:5:0:ERROR:VALID:DTD_CONTENT_MODEL: Element body content does not follow the DTD, expecting (p | lq | note | dl | parml | ul | ol | sl | pre | codeblock | msgblock | screen | lines | fig | syntaxdiagram | imagemap | image | object | table | simpletable | required-cleanup | data | data-about | foreign | unknown | section | example)*, got (p a p )'
        expectedtags = ['codeblock', 'data', 'dl', 'example', 'fig', 'foreign', 'image', 'imagemap', 'lines', 'lq', 'msgblock', 'note', 'object', 'ol', 'p', 'parml', 'pre', 'screen', 'section', 'simpletable', 'sl', 'syntaxdiagram', 'table', 'ul', 'unknown']
        #had to exclude 'required-cleanup' and 'data-about' because '-' does not work in the tag algebra: if it is allowed in the domain of characters
        #for the tag names, then group theory demands that an element can be named '-', however lxml does not allow this. Fixing this
        #would mean forcing lxml to accept it, somehow. 
        
        parser = Errors.ErrorParser(tree)
        parser.parse()
        
        self.assertEqual(parser.errorMessage, expectederrormessage, 'ErrorParser parsed the wrong error. Expected %s, got %s' % (expectederrormessage, parser.errorMessage))
        self.assertEqual(expectedtags, parser.acceptableTags, 'ErrorParser parsed the wrong tags. Expected %s, got %s' % (expectedtags, parser.acceptableTags))
        self.assertTrue(expectedtargetelement is parser.targetElement, 'ErrorParser parsed the wrong target element. Expected %s, got %s' % (expectedtargetelement, parser.targetElement))
  
    
    def test_4(self):
        """test a DTD_CONTENT_MODEL error message"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running test test_4')
        testfile = os.path.join(self.testfilesdir, 'ErrorTest4.xml')
        tree = lxml.etree.parse(testfile)
        expectedtargetelement = tree.xpath('//a')[0]
        expectederrormessage = '/Users/matt/work/programs/dev_workspace/TreeGroup/Transforms/AStarPathFinder/../../testfiles/AStarTransform/Errors/ErrorTest4.xml:3:0:ERROR:VALID:DTD_CONTENT_MODEL: Element topic content does not follow the DTD, expecting (title , titlealts? , (shortdesc | abstract)? , prolog? , body? , related-links? , (topic | concept | task | reference | glossentry)*), got (title a )'
        expectedtags = ['abstract', 'body', 'concept', 'glossentry', 'prolog', 'reference', 'shortdesc', 'task', 'titlealts', 'topic'] 
        #had to exclude 'related-links' because '-' does not work in the tag algebra: if it is allowed in the domain of characters
        #for the tag names, then group theory demands that an element can be named '-', however lxml does not allow this. Fixing this
        #would mean forcing lxml to accept it, somehow. 
        
        parser = Errors.ErrorParser(tree)
        parser.parse()
        
        self.assertEqual(parser.errorMessage, expectederrormessage, 'ErrorParser parsed the wrong error. Expected %s, got %s' % (expectederrormessage, parser.errorMessage))
        self.assertEqual(expectedtags, parser.acceptableTags, 'ErrorParser parsed the wrong tags. Expected %s, got %s' % (expectedtags, parser.acceptableTags))
        self.assertTrue(expectedtargetelement is parser.targetElement, 'ErrorParser parsed the wrong target element. Expected %s, got %s' % (expectedtargetelement, parser.targetElement))


    def test_5(self):
        """test a validation error due to a missing element"""        
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running test test_5')
        testfile = os.path.join(self.testfilesdir, 'ErrorTest5.xml')
        tree = lxml.etree.parse(testfile)
        expectedtargetelement = tree.xpath('//body')[0]
        expectederrormessage = '/Users/matt/work/programs/dev_workspace/TreeGroup/Transforms/AStarPathFinder/../../testfiles/AStarTransform/Errors/ErrorTest5.xml:3:0:ERROR:VALID:DTD_CONTENT_MODEL: Element topic content does not follow the DTD, expecting (title , titlealts? , (shortdesc | abstract)? , prolog? , body? , related-links? , (topic | concept | task | reference | glossentry)*), got (body )'
        expectedtags = ['title']
        
        parser = Errors.ErrorParser(tree)
        parser.parse()
        
        self.assertEqual(parser.errorMessage, expectederrormessage, 'ErrorParser parsed the wrong error. Expected %s, got %s' % (expectederrormessage, parser.errorMessage))
        self.assertEqual(expectedtags, parser.acceptableTags, 'ErrorParser parsed the wrong tags. Expected %s, got %s' % (expectedtags, parser.acceptableTags))
        self.assertTrue(expectedtargetelement is parser.targetElement, 'ErrorParser parsed the wrong target element. Expected %s, got %s' % (expectedtargetelement, parser.targetElement))


    def test_6(self):
        """test a validation error due to a missing element"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running test test_6')
        testfile = os.path.join(self.testfilesdir, 'ErrorTest6.xml')
        tree = lxml.etree.parse(testfile)
        expectedtargetelement = tree.xpath('//body')[0]
        expectederrormessage = '/Users/matt/work/programs/dev_workspace/TreeGroup/Transforms/AStarPathFinder/../../testfiles/AStarTransform/Errors/ErrorTest6.xml:3:0:ERROR:VALID:DTD_CONTENT_MODEL: Element topic content does not follow the DTD, expecting (title , titlealts? , (shortdesc | abstract)? , prolog? , body? , related-links? , (topic | concept | task | reference | glossentry)*), got (body )'
        expectedtags = ['title']
        
        parser = Errors.ErrorParser(tree)
        parser.parse()
        
        self.assertEqual(parser.errorMessage, expectederrormessage, 'ErrorParser parsed the wrong error. Expected %s, got %s' % (expectederrormessage, parser.errorMessage))
        self.assertEqual(expectedtags, parser.acceptableTags, 'ErrorParser parsed the wrong tags. Expected %s, got %s' % (expectedtags, parser.acceptableTags))
        self.assertTrue(expectedtargetelement is parser.targetElement, 'ErrorParser parsed the wrong target element. Expected %s, got %s' % (expectedtargetelement, parser.targetElement))


    def test_7(self):
        """"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running test test_7')
        testfile = os.path.join(self.testfilesdir, 'ErrorTest7.xml')
        tree = lxml.etree.parse(testfile)
        expectedtargetelement = tree.xpath('//a')[0]
        expectederrormessage = '/Users/matt/work/programs/dev_workspace/TreeGroup/Transforms/AStarPathFinder/../../testfiles/AStarTransform/Errors/ErrorTest7.xml:2:0:ERROR:VALID:DTD_CONTENT_MODEL: Element dita content does not follow the DTD, expecting (topic | concept | task | reference | glossentry)+, got (a topic )'
        expectedtags = ['concept', 'glossentry', 'reference', 'task', 'topic']
        
        parser = Errors.ErrorParser(tree)
        parser.parse()
        
        self.assertEqual(parser.errorMessage, expectederrormessage, 'ErrorParser parsed the wrong error. Expected %s, got %s' % (expectederrormessage, parser.errorMessage))
        self.assertEqual(expectedtags, parser.acceptableTags, 'ErrorParser parsed the wrong tags. Expected %s, got %s' % (expectedtags, parser.acceptableTags))
        self.assertTrue(expectedtargetelement is parser.targetElement, 'ErrorParser parsed the wrong target element. Expected %s, got %s' % (expectedtargetelement, parser.targetElement))


    def test_8(self):
        """"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running test test_8')
        testfile = os.path.join(self.testfilesdir, 'ErrorTest8.xml')
        tree = lxml.etree.parse(testfile)
        expectederrormessage = '/Users/matt/work/programs/dev_workspace/TreeGroup/Transforms/AStarPathFinder/../../testfiles/AStarTransform/Errors/ErrorTest8.xml:6:0:ERROR:VALID:DTD_CONTENT_MODEL: Element task content does not follow the DTD, expecting (title , titlealts? , (shortdesc | abstract)? , prolog? , taskbody? , related-links? , (topic | concept | task | reference | glossentry)*), got '
        expectedtags = ['title']
        
        parser = Errors.ErrorParser(tree)
        parser.parse()
        
        expectedtargetelement = tree.xpath('//task/_')[0]
        
        self.assertEqual(parser.errorMessage, expectederrormessage, 'ErrorParser parsed the wrong error. Expected %s, got %s' % (expectederrormessage, parser.errorMessage))
        self.assertEqual(expectedtags, parser.acceptableTags, 'ErrorParser parsed the wrong tags. Expected %s, got %s' % (expectedtags, parser.acceptableTags))
        self.assertTrue(expectedtargetelement is parser.targetElement, 'ErrorParser parsed the wrong target element. Expected %s, got %s' % (expectedtargetelement, parser.targetElement))


    def test_9(self):
        """Test the unknown element error message when passed an element"""
        self.log.debug('')
        self.log.debug('')
        self.log.debug('running test test_1')
        testfile = os.path.join(self.testfilesdir, 'ErrorTest1.xml')
        tree = lxml.etree.parse(testfile)
        expectedtargetelement = tree.getroot()
        expectederrormessage = '/Users/matt/work/programs/dev_workspace/TreeGroup/Transforms/AStarPathFinder/../../testfiles/AStarTransform/Errors/ErrorTest1.xml:2:0:ERROR:VALID:DTD_UNKNOWN_ELEM: No declaration for element a'
        expectedtags = ['dita']
        
        parser = Errors.ErrorParser(tree.getroot())
        parser.parse()
        
        self.assertEqual(parser.errorMessage, expectederrormessage, 'ErrorParser parsed the wrong error. Expected %s, got %s' % (expectederrormessage, parser.errorMessage))
        self.assertEqual(expectedtags, parser.acceptableTags, 'ErrorParser parsed the wrong tags. Expected %s, got %s' % (expectedtags, parser.acceptableTags))
        self.assertTrue(expectedtargetelement is parser.targetElement, 'ErrorParser parsed the wrong target element. Expected %s, got %s' % (expectedtargetelement, parser.targetElement))
    