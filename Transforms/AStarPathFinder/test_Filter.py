import unittest, os.path, sys, logging, lxml.etree, copy

import Tree.Tree
from . import Filter
        
        
#===============================================================================
# test findNeighbors_FirstValidationError
#===============================================================================
    
class test_ElementTagFilter(unittest.TestCase):
    """Test the element tag filter. 
    
    Note that all the tests in this class assume that the filter database has been trained using
    the file trainfile.dita and only that file. """
    
    def setUp(self):
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', '..', 'testfiles', 'AStarTransform', 'Filter', 'ElementTagFilter')
        #set test file, target, tree, db
        self.db = os.path.join(self.testfilesdir, 'tagfiltertest.db')
        self.file = os.path.join(self.testfilesdir, 'testfile1.dita')
        self.tree = lxml.etree.parse(self.file)
        self.target = self.tree.getroot()[0][2]  #second topic in file
        self.log = logging.getLogger()
        
        self.filter = Filter.ElementTagFilter(self.db)
        
        
        
    def test_Train(self):
        #test training a database on a file
        self.filter.resetDB()
        self.filter.train(os.path.join(self.testfilesdir, 'trainfile.dita'))
        
        #check some records
        expected = ('dita', 'topic', 1, 0.0)
        record = self.filter.dbconnection.execute("select * from parenttagtable where parenttag='dita' and targettag='topic'").fetchall()[0]
        self.assertEqual(expected, record, "train() created incorrect record, expected %s got %s" % (str(expected), str(record)))
        
        expected = ('topic', 'title', 134, 0.0)
        record = self.filter.dbconnection.execute("select * from parenttagtable where parenttag='topic' and targettag='title'").fetchall()[0]
        self.assertEqual(expected, record, "train() created incorrect record, expected %s got %s" % (str(expected), str(record)))
        
        expected = ('task', 'title', 7, 0.0)
        record = self.filter.dbconnection.execute("select * from parenttagtable where parenttag='task' and targettag='title'").fetchall()[0]
        self.assertEqual(expected, record, "train() created incorrect record, expected %s got %s" % (str(expected), str(record)))
        
        expected = ('body', 'p', 244, 0.0)
        record = self.filter.dbconnection.execute("select * from parenttagtable where parenttag='body' and targettag='p'").fetchall()[0]
        self.assertEqual(expected, record, "train() created incorrect record, expected %s got %s" % (str(expected), str(record)))
      
        expected = ('body', 'ul', 110, 0.0)
        record = self.filter.dbconnection.execute("select * from parenttagtable where parenttag='body' and targettag='ul'").fetchall()[0]
        self.assertEqual(expected, record, "train() created incorrect record, expected %s got %s" % (str(expected), str(record)))

        expected = ('ul', 'li', 696, 0.0)
        record = self.filter.dbconnection.execute("select * from parenttagtable where parenttag='ul' and targettag='li'").fetchall()[0]
        self.assertEqual(expected, record, "train() created incorrect record, expected %s got %s" % (str(expected), str(record)))
        
        
    
    def test_Filter(self):
        #test the filter, ensure that it returns the proper tags for a given element
        pass
    
    
    
    def test_getTagScore(self):
        #get the score of a tag, ie the probability that the tag is the proper one for 
        #the target element
        pass
    
    
    
    def test_getProbaTagGivenParentTag(self):
        #test the conditional probability of a tag given the target's parent.
        result = self.filter.getProbaTagGivenParentTag('title', 'topic')
        expected = float(0.328431372549)
        self.assertEqual(round(expected, 12), round(result, 12), "getProbaGivenParentTag('title', 'topic') returned the wrong value, expected %s, got %s" % (str(expected), str(result)))
        
        result = self.filter.getProbaTagGivenParentTag('task', 'topic')
        expected = 0.0171568627451
        self.assertEqual(round(expected, 12), round(result, 12), "getProbaGivenParentTag('title', 'topic') returned the wrong value, expected %s, got %s" % (str(expected), str(result)))
        
        result = self.filter.getProbaTagGivenParentTag('li', 'ul')
        expected = 1.0
        self.assertEqual(round(expected, 12), round(result, 12), "getProbaGivenParentTag('title', 'topic') returned the wrong value, expected %s, got %s" % (str(expected), str(result)))
          
        result = self.filter.getProbaTagGivenParentTag('p', 'body')
        expected = 0.541019955654
        self.assertEqual(round(expected, 12), round(result, 12), "getProbaGivenParentTag('title', 'topic') returned the wrong value, expected %s, got %s" % (str(expected), str(result)))
                   
        result = self.filter.getProbaTagGivenParentTag('fig', 'body')
        expected = 0.079822616408
        self.assertEqual(round(expected, 12), round(result, 12), "getProbaGivenParentTag('title', 'topic') returned the wrong value, expected %s, got %s" % (str(expected), str(result)))
                 
        result = self.filter.getProbaTagGivenParentTag('title', 'body')
        expected = 0.0
        self.assertEqual(round(expected, 12), round(result, 12), "getProbaGivenParentTag('title', 'topic') returned the wrong value, expected %s, got %s" % (str(expected), str(result)))
         
         
         
         
    def test_getProbaTagGivenTextWord(self):
        vars = ('p', 'operation')
        result = self.filter.getProbaTagGivenTextWord(vars[0], vars[1])
        expected = 0.6
        self.assertEqual(round(expected, 12), round(result, 12), "getProbaGivenTextWord('%s', '%s') \
        returned the wrong value, expected %s, got %s" % (vars[0], vars[1], str(expected), str(result)))
        
        vars = ('b', 'operation')
        result = self.filter.getProbaTagGivenTextWord(vars[0], vars[1])
        expected = 0.2
        self.assertEqual(round(expected, 12), round(result, 12), "getProbaGivenTextWord('%s', '%s') \
        returned the wrong value, expected %s, got %s" % (vars[0], vars[1], str(expected), str(result)))
        
        vars = ('p', 'operation')
        result = self.filter.getProbaTagGivenTextWord(vars[0], vars[1])
        expected = 0.6
        self.assertEqual(round(expected, 12), round(result, 12), "getProbaGivenTextWord('%s', '%s') \
        returned the wrong value, expected %s, got %s" % (vars[0], vars[1], str(expected), str(result)))
         
        vars = ('p', 'steps')
        result = self.filter.getProbaTagGivenTextWord(vars[0], vars[1])
        expected = 1.0
        self.assertEqual(round(expected, 12), round(result, 12), "getProbaGivenTextWord('%s', '%s') \
        returned the wrong value, expected %s, got %s" % (vars[0], vars[1], str(expected), str(result)))
         
        vars = ('title', 'steps')
        result = self.filter.getProbaTagGivenTextWord(vars[0], vars[1])
        expected = 0.0
        self.assertEqual(round(expected, 12), round(result, 12), "getProbaGivenTextWord('%s', '%s') \
        returned the wrong value, expected %s, got %s" % (vars[0], vars[1], str(expected), str(result)))
        
         
    def test_getProbaTagGivenText(self):
        pass
         
         
         
         
    