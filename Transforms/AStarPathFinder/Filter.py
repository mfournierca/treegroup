#!/usr/bin/env python3

"""This file implements a bayesian filter used to determine the most likely
operations that can be used when generating operands. """

import sqlite3, os.path, logging


class ElementTagFilter:
    """This filter is used to choose the 'best' tags that an element can be assigned. """
    
    #if adding a new token to the filter, remember to:
    #    create training function and add to self.train()
    #    create probability generating functiand add to self.getTagScore()
    #    add the appropriate table to the self.resetDB() function
    def __init__(self, database=os.path.join(os.path.dirname(__file__), 'FilterDB', 'tagfilter.db')):
        """initialize the filter"""
        self.log = logging.getLogger()
        
        if not os.path.exists(database):
            self.log.error('database does not exist: %s' % database)
        self.database = os.path.abspath(database)
        self.dbconnection = sqlite3.connect(database) 
        
        #ensure database schema is correct
        try: 
            self.dbconnection.execute("select * from parenttagtable")
        except sqlite3.OperationalError: 
            self.dbconnection.execute("create table parenttagtable(parenttag, targettag, count INTEGER, proba FLOAT)")
            self.dbconnection.commit()
        
        try: 
            self.dbconnection.execute("select * from targettexttable")
        except sqlite3.OperationalError: 
            self.dbconnection.execute("create table targettexttable(word, targettag, count INTEGER, proba FLOAT)")
            self.dbconnection.commit()
            
        #base probability is used when the filter has no information about a tag-token pair. 
        #eg, if the word "foo" does not appear anywhere under the tag "bar" in the files 
        #that were used to train the filter, then the filter thinks that P(tag="bar"|word="foo") = 0
        #This would cause the cumulative score of this tag to be zero, regardless of what the other 
        #tokens may indicate. See the bayesian formula in self.getTagScore() to realize this. 
        #This situation, of course, is not what we want because the files used to train the filter 
        #are not completely representative of all possible files - there are gaps in the information. 
        #therefore we cannot assume that any probability is zero, so we have to assign a "base probability" 
        #to be used when the filter has no information. 
        #This value will be tweaked as time goes on, and it would be very nice if we could somehow 
        #prove what the correct value is. For now, we guess. 
        self.baseproba = 0.1
            
    
    
    
    def filter(self, target=None, tree=None, acceptableTags=[]):
        """Apply the filter and return the most likely operations"""
        self.target = target
        self.tree = tree

        #acceptableTags.sort() using self.getTagScore
        
        #if no entries above 0.95 probability, ask for user input.
        #add user input into the tag table, train the filter. 
        
        #take top x entries in acceptableTags and return. x can be set by user
     
        pass
    
    
    
    
    def getTagScore(self, tag, target):
        """Get the score of an tag, ie the probability that the tag
        is the correct one to use for the target element"""
        #get all the conditional probabilities and combine them using Bayes' formula. Return the result
        #Derived from Bayes' formula, used to combine conditional probabilities:
        #                                  P(T|C1)P(T|C2) ... P(T|Cn)
        # p   =                    ------------------------------------------
        #            P(T|C1)P(T|C2) ... P(T|Cn) + (1 - P(T|C1))(1 - P(T|C2)) ... (1 - P(T|Cn))
        #
        #where P(T|Ci) is the probability that tag T is the correct one given the condition Ci, where Ci is one of
        #parent tag value, child tag value, text, etc. 
        #Note this formula assumes that the conditions are independant. 
        
        probas = []
        probas.append(self.getProbaTagGivenParentTag(tag, target.getparent().tag))
        for word in self._getWordsFromText(target.text):
            probas.append(self.getProbaTagGivenTextWord(tag, word))
        
        p1 = 1
        for i in probas: p1 = p1*i
        p2 = 1
        for i in probas: p2 = p2*(1 - i)
        
        p = p1 / (p1 + p2)
        self.log.debug('tag score: %s / (%s + %s) = %s' % (p1, p1, p2, p))
        return p
        
    
    
    
    def getProbaTagGivenParentTag(self, tag, parenttag):
        #find P(tag|parent) and return it
        #P(tag|parent) = number of times tag appears under parent / #number of times any tag appears under parent. 
        #need some code to control what happens if tag or parenttag is not in database - probably set to 
        #0 and wait for user input, or define a "base probability" that is used in the absence of information. 
        
        tagcountdbslice = self.dbconnection.execute("select count from parenttagtable where targettag=? and parenttag=?", \
                                             (tag, parenttag)).fetchall()
        if len(tagcountdbslice) == 0:
            #no information, return base probability. (or ask for user input?)
            self.log.debug('no information, return base proba: %s' % str(self.baseproba))
            return self.baseproba
        else:
            tagcount = tagcountdbslice[0][0]
            
        totalcount = 0
        for i in self.dbconnection.execute("select count from parenttagtable where parenttag=?",\
                                               (parenttag,)).fetchall():
            totalcount += i[0]
            
        if not totalcount >= tagcount: 
            self.log.error("impossible probability generated, totalcount < tagcount: %i < %i" % (totalcount, tagcount))
            return None
        
        p = float(tagcount) / float(totalcount)
        self.log.debug('tag: %s\tparenttag: %s\tproba: %s / %s =  %s' % (tag, parenttag, str(tagcount), str(totalcount), str(p)))
        return p
    
    
    
    
    def getProbaTagGivenTextWord(self, tag, word):
        #find P(tag|word in target.text) and return
        tagcountdbslice = self.dbconnection.execute("select count from targettexttable where targettag=? and word=?", \
                                                    (tag, word)).fetchall()
        if len(tagcountdbslice) == 0:
            #no information, return base probability. (or ask for user input?)
            self.log.debug('no information, return base proba: %s' % str(self.baseproba))
            return self.baseproba
        else:
            tagcount = tagcountdbslice[0][0]
            
        totalcount = 0
        for i in self.dbconnection.execute("select count from targettexttable where word=?",\
                                               (word,)).fetchall():
            totalcount += i[0]
            
        if not totalcount >= tagcount: 
            self.log.error("impossible probability generated, totalcount < tagcount: %i < %i" % (totalcount, tagcount))
            return None
        
        p = float(tagcount) / float(totalcount)
        self.log.debug('tag: %s\tword: %s\tproba: %s/%s =  %s' % (tag, word, str(tagcount), str(totalcount), str(p)))
        return p
    
    
    
    
    def getProbaTagGivenChild(self, tag, child):
        #find P(tag|child) and return
        pass
    
    
    
    
    
    def getProbaTagGivenChildText(self, tag, word):
        #find P(tag|word in any child) and return
        pass
    
    
    
    
    
    def train(self, ditafile):
        """Used to train the filter automatically. Take a dita file, and iterate the 
        elements one by one. For each element, get tokens and add to the databases."""
        import lxml.etree
        
        if not os.path.exists(ditafile):
            self.log.error('file does not exist: %s' % ditafile)
            return
        elif not ditafile.endswith('.dita'):
            self.log.error('file must be dita: %s' % ditafile)
            return
        
        try:
            #parse the dita file
            tree = lxml.etree.parse(ditafile, parser=lxml.etree.XMLParser(resolve_entities=False))
        except lxml.etree.XMLSyntaxError:
            self.log.warning('syntax error in file: %s' % ditafile)
            return
        
        for element in tree.iter():         #iterate over the elements
            self._trainParentTagTable(element)
            self._trainTargetText(element)
        
        self.dbconnection.commit()
    
    
    
    
    def _trainParentTagTable(self, element):
        if element.getparent() is None: return
        if (not isinstance(element.tag, str)) or (not isinstance(element.getparent().tag, str)): return
        #if parent-tag record is in database, add to count. Otherwise add new record
        dbslice = self.dbconnection.execute("select count from parenttagtable where parenttag=? and targettag=?", (element.getparent().tag, element.tag)).fetchall()
        if len(dbslice) == 0:
            self.dbconnection.execute("insert into parenttagtable values(?, ?, 1, 0)", (element.getparent().tag, element.tag))
            self.dbconnection.commit()
        elif len(dbslice) > 1:
            self.log.error('len(dbslice) > 1, this means that there is more than one record for the parenttag-targettag pair (%s, %s).\
             This should not happen, please fix the database' % (element.getparent().tag, element.tag))
        else:
            #update record
            newcount = dbslice[0][0] + 1
            self.dbconnection.execute("update parenttagtable set count=? where parenttag=? and targettag=?", (newcount, element.getparent().tag, element.tag))
            self.dbconnection.commit()
    
    
    
    
    def _trainTargetText(self, element):
        if not element.text: return
        if not isinstance(element.text, str): return
        if not isinstance(element.tag, str): return
        
        for word in self._getWordsFromText(element.text):
            if not isinstance(word, str): continue
            #if word-tag record is in database, update count. Otherwise create record. 
            dbslice = self.dbconnection.execute("select count from targettexttable where word=? and targettag=?", (word, element.tag)).fetchall()
            if len(dbslice) == 0:
                self.dbconnection.execute("insert into targettexttable values(?, ?, 1, 0)", (word, element.tag))
                self.dbconnection.commit()
            elif len(dbslice) > 1:
                self.log.error('len(dbslice) > 1, this means that there is more than one record for the word-targettag pair (%s, %s).\
                 This should not happen, please fix the database' % (word, element.tag))
            else:
                #update record
                newcount = dbslice[0][0] + 1
                self.dbconnection.execute("update targettexttable set count=? where word=? and targettag=?", (newcount, word, element.tag))
                self.dbconnection.commit()
  
    
    
    
    def _getWordsFromText(self, text):
        import string
        words = []
        for word in text.split(' '):
            word = word.lower()
            for letter in word: 
                if (letter not in string.ascii_lowercase) and (letter not in string.digits) and (letter not in ['-', '_']):
                    word = word.replace(letter, '')
            if len(word) == 0: continue
            if not isinstance(word, str): continue
            words.append(word) 
        return words
    
    
    
    
    def backup(self):
        """backup the database"""
        pass
    
    
    
    
    def rollback(self):
        """rollback the database"""
        pass
    
    
    
    def resetDB(self):
        """Remove all records from the database"""
        self.dbconnection.execute("delete from parenttagtable")
        self.dbconnection.execute("delete from targettexttable")
        self.dbconnection.commit()
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    
    import optparse, sys
    
    #parse args
    optparser=optparse.OptionParser()
    optparser.add_option("-i", "--input", type="string", dest="inputpath", default='', 
    help="Path to the input file / dir")
    optparser.add_option("--trainfile", action="store_true", dest="trainfile",
    help="Turn this on to train the filter(s) using the input file")
    optparser.add_option("--traindir", action="store_true", dest="traindir",
    help="Turn this on to train the filter(s) using the input directory")
    optparser.add_option("--resetdb", action="store_true", dest="resetdb",
    help="Turn this on to reset the filter database, ie remove all records from the database. USE WITH CAUTION.")
    (options, args) = optparser.parse_args()
    inputpath = options.inputpath
    trainfile = options.trainfile
    traindir = options.traindir
    resetdb = options.resetdb
    #this next block ensures that the user can pass the input as a positional
    #argument, without the -i
    try:
        inputpath = args[0]
    except:
        pass
        
    #===============================================================================
    # #prepare logging
    #===============================================================================
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
     
    warninghandler = logging.StreamHandler(sys.stdout)
    warninghandler.setLevel(logging.WARNING)
    warningformatter = logging.Formatter("%(module)8.8s.%(funcName)20.20s%(levelname)10.10s\t%(message)s")
    warninghandler.setFormatter(warningformatter)
    log.addHandler(warninghandler)
    
    infohandler = logging.StreamHandler(sys.stdout)
    infohandler.setLevel(logging.INFO)
#    infoformatter = logging.Formatter("%(message)s")
    infoformatter = logging.Formatter("%(module)8.8s.%(funcName)20.20s%(levelname)10.10s\t%(message)s")
    infohandler.setFormatter(infoformatter)
    log.addHandler(infohandler)
    
    if resetdb:
        response = input("are you sure you want to reset the filter DB? All records will be lost. (y/n)")
        if response == 'y':
            print("RESETTING FILTER DATABASE")
            filter = ElementTagFilter()
            filter.resetDB()
            print("FILTER DATABASE RESET")
        else:
            print("NOT RESETTING FILTER DATABASE: DATABASE WILL NOT BE ALTERED")
        
    if trainfile:
        if not os.path.isfile(inputpath):
            log.error("--trainfile passed, but input is not a file: %s" % inputpath)
            sys.exit(1)
        if not os.path.exists(inputpath):
            log.error("input does not exist: %s" % inputpath)
            sys.exit(1)
        filter = ElementTagFilter()
        filter.train(inputpath)
        
    if traindir:
        if not os.path.isdir(inputpath):
            log.error("--traindir passed, but input is not a dir: %s" % inputpath)
            sys.exit(1)
        if not os.path.exists(inputpath):
            log.error("input does not exist: %s" % inputpath)
            sys.exit(1)
            
        import DirAndFileTools.Find
        dirs, files = DirAndFileTools.Find.dirs_and_files(searchroot=inputpath, 
                                                          extensions=['dita'], 
                                                          ignorefilenames=['.recover', '.bak', '.backup'], 
                                                          ignoredirnames=['backup', 'Backup'], 
                                                          includepathfromcwd=True,
                                                          )
        del dirs
        filter = ElementTagFilter()
        for file in files: 
            log.info("training with file: %s" % file)
            filter.train(file)