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
            
        try: 
            self.dbconnection.execute("select * from targettextlengthtable")
        except sqlite3.OperationalError: 
            self.dbconnection.execute("create table targettextlengthtable(length INTEGER, targettag, count INTEGER, proba FLOAT)")
            self.dbconnection.commit()  
                      
        try: 
            self.dbconnection.execute("select * from targetindextable")
        except sqlite3.OperationalError: 
            self.dbconnection.execute("create table targetindextable(targetindex INTEGER, targettag, count INTEGER, proba FLOAT)")
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
        #Note also that this formula is unbiased, ie it treats any possible outcome the same. 
        
        #Note also that if any of the getProba functions returns 0 or 1, 
        #then p will equal 0 or 1, respectively. This can be seen just by looking at the equation. 
        #If you are experiencing weird results, or see that a certain tag is being taken or rejected
        #when it shouldn't be, this could be the cause. 
            
        probas = []
        probas.append(self.getProbaTagGivenParentTag(tag, target.getparent().tag))
        probas.append(self.getProbaTagGivenIndexUnderParent(tag, self._getElementIndex(target)))
                                                           
        words = self._getWordsFromText(target.text)
        probas.append(self.getProbaGivenTextLengthInterval(tag, len(words))) 
#        for word in words:
#            probas.append(self.getProbaTagGivenTextWord(tag, word))
        
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
        
        tagcount = self.dbconnection.execute("select sum(count) from parenttagtable where targettag=? and parenttag=?", \
                                             (tag, parenttag)).fetchone()[0]
        
        if tagcount is None:
            #no information, return base probability. (or ask for user input?)
            self.log.debug('no information, return base proba: %s' % str(self.baseproba))
            return self.baseproba
        
        totalcount = self.dbconnection.execute("select sum(count) from parenttagtable where parenttag=?", \
                                       (parenttag,)).fetchone()[0]    
            
        if not totalcount >= tagcount: 
            self.log.error("impossible probability generated, totalcount < tagcount: %i < %i" % (totalcount, tagcount))
            return None
        
        p = float(tagcount) / float(totalcount)
        self.log.debug('tag: %s\tparenttag: %s\tproba: %s / %s =  %s' % (tag, parenttag, str(tagcount), str(totalcount), str(p)))
        return p
    
    
    
    
    def getProbaTagGivenTextWord(self, tag, word):
        #find P(tag|word in target.text) and return
        tagcount = self.dbconnection.execute("select sum(count) from targettexttable where targettag=? and word=?",\
                                             (tag, word)).fetchone()[0]
        
        if tagcount is None:
            #no information, return base probability. (or ask for user input?)
            self.log.debug('no information, return base proba: %s' % str(self.baseproba))
            return self.baseproba
            
        totalcount = self.dbconnection.execute("select sum(count) from targettexttable where word=?", (word,)).fetchone()[0]
            
        if not totalcount >= tagcount: 
            self.log.error("impossible probability generated, totalcount < tagcount: %i < %i" % (totalcount, tagcount))
            return None
        
        p = float(tagcount) / float(totalcount)
        self.log.debug('tag: %s\tword: %s\tproba: %s/%s =  %s' % (tag, word, str(tagcount), str(totalcount), str(p)))
        return p
    
    
    
    
    def getProbaGivenTextLengthInterval(self, tag, length):
        #get the text length based on how close it is to the lengths stored in the filter db, 
        #ie, given interval = some integer, calculate and return
        #P(target tag | text length is within +/- interval of target text length)
        
        #define interval. Interval could be defined with a function over the text length, so interval gets larger as 
        #text gets larger, vice versa, etc. 
        interval = 2
        
        count = self.dbconnection.execute("select sum(count) from targettextlengthtable where targettag=? and length>? and length<?", \
                                          (tag, length - interval, length + interval)).fetchone()[0]
                                          
        if count is None:
            self.log.debug("no information, return base proba: %s" % str(self.baseproba))
            return self.baseproba
        
        totalcount = self.dbconnection.execute("select sum(count) from targettextlengthtable where length>? and length<?", \
                                               (length - interval, length + interval)).fetchone()[0]
                                                    
        p = float(count) / float(totalcount)
        self.log.debug('tag: %s\tlength: %s\tinterval: %s\tproba: %s/%s =  %s' % (tag, str(length), str(interval), str(count), str(totalcount), str(p)))
        return p
    
        
        
        
        
    def getProbaTagGivenIndexUnderParent(self, tag, index):
        #get P(target tag = tag | target is at index "index" under its parent)
        #Should use intervals for this function, as in getProbaGivenTextLengthInterval()
        indexcountdbslice = self.dbconnection.execute("select count from targetindextable where targettag=? and targetindex=?", \
                                                    (tag, index)).fetchall()
                                                    
        indexcount = self.dbconnection.execute("select sum(count) from targetindextable where targettag=? and targetindex=?",\
                                          (tag, index)).fetchone()[0]
                                          
        if indexcount is None:
            #no information, return base probability. (or ask for user input?)
            self.log.debug('no information, return base proba: %s' % str(self.baseproba))
            return self.baseproba
            
        totalcount = self.dbconnection.execute("select sum(count) from targetindextable where targetindex=?", \
                                               (index,)).fetchone()[0]
                                               
        if not totalcount >= indexcount: 
            self.log.error("impossible probability generated, totalcount < indexcount: %i < %i" % (totalcount, indexcount))
            return None
        
        p = float(indexcount) / float(totalcount)
        self.log.debug('tag: %s\tindex: %s\tproba: %s/%s =  %s' % (tag, index, str(indexcount), str(totalcount), str(p)))
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
        self.log.info("training with file: %s" % ditafile)
        
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
            
        #functionbelow all loop over the tree - could be sped up by combining them. 
        #keeping them separate for now for ease of coding, refactoring, adding new conditions,
        #etc
        self._trainParentTag_Tree(tree)
        self._trainTargetTextLength_Tree(tree)
        self._trainTargetText_Tree(tree)
        self._trainTargetIndexUnderParent_Tree(tree)
        
        self.dbconnection.commit()
    
    
    
    
    
    def _trainParentTag_Tree(self, tree):
        d = {}
        for e in tree.iter():
            if e.getparent() is None: continue
            if not isinstance(e.tag, str): continue
            
            if not e.tag in d.keys(): d[e.tag] = {}
            
            if not e.getparent().tag in d[e.tag].keys(): 
                d[e.tag][e.getparent().tag] = 1
            else: 
                d[e.tag][e.getparent().tag] += 1                      

        for tag in d.keys():
            for parenttag in d[tag].keys():
                record = self.dbconnection.execute("select count from parenttagtable where parenttag=? and targettag=?", \
                                                    (parenttag, tag)).fetchone() #.fetchall
                if record is None:
                    self.dbconnection.execute("insert into parenttagtable values(?, ?, 1, 0)", (parenttag, tag))
#                elif len(record) > 1:
#                    self.log.error('len(dbslice) > 1, this means that there is more than one record for the word-targettag pair (%s, %s).\
#                                     This should not happen, please fix the database' % (word, element.tag))
                else:
                    newcount = record[0] + d[tag][parenttag]
                    self.dbconnection.execute("update parenttagtable set count=? where parenttag=? and targettag=?", \
                                              (newcount, parenttag, tag))
        self.dbconnection.commit()
                
                
    
    
    
    def _trainTargetText_Tree(self, tree):
        """Training the filter with text, and adding words one by one to the database 
        (the strategy used for other tokens) takes too long. This function counts words 
        over the whole tree and stores them in a dictionary, and adds to the database at
        the end"""
        
        d = {}
        for e in tree.iter():
            if not e.text: continue
            if not isinstance(e.text, str): continue
            if not isinstance(e.tag, str): continue
            
            if not e.tag in d.keys(): d[e.tag] = {}
            for word in self._getWordsFromText(e.text):
                if not word in d[e.tag].keys(): 
                    d[e.tag][word] = 1
                else: 
                    d[e.tag][word] += 1
                    
        for tag in d.keys():
            for word in d[tag].keys():
                record = self.dbconnection.execute("select count from targettexttable where word=? and targettag=?", \
                                                    (word, tag)).fetchone() #.fetchall
                if record is None:
                    self.dbconnection.execute("insert into targettexttable values(?, ?, 1, 0)", (word, tag))
#                elif len(record) > 1:
#                    self.log.error('len(dbslice) > 1, this means that there is more than one record for the word-targettag pair (%s, %s).\
#                                     This should not happen, please fix the database' % (word, element.tag))
                else:
                    newcount = record[0] + d[tag][word]
                    self.dbconnection.execute("update targettexttable set count=? where word=? and targettag=?", \
                                              (newcount, word, tag))
        self.dbconnection.commit()
        
                
                
    
    
    def _trainTargetTextLength_Tree(self, tree):
        d = {}
        for e in tree.iter():
            if not e.text: continue
            if not isinstance(e.text, str): continue
            if not isinstance(e.tag, str): continue
            
            if not e.tag in d.keys(): d[e.tag] = {}
            
            textlength = len(self._getWordsFromText(e.text))
        
            if not textlength in d[e.tag].keys(): 
                d[e.tag][textlength] = 1
            else: 
                d[e.tag][textlength] += 1
                    
        for tag in d.keys():
            for textlength in d[tag].keys():
                record = self.dbconnection.execute("select count from targettextlengthtable where length=? and targettag=?", \
                                                    (textlength, tag)).fetchone() #.fetchall
                if record is None:
                    self.dbconnection.execute("insert into targettextlengthtable values(?, ?, 1, 0)", (textlength, tag))
#                elif len(record) > 1:
#                    self.log.error('len(dbslice) > 1, this means that there is more than one record for the word-targettag pair (%s, %s).\
#                                     This should not happen, please fix the database' % (word, element.tag))
                else:
                    newcount = record[0] + d[tag][textlength]
                    self.dbconnection.execute("update targettextlengthtable set count=? where length=? and targettag=?", \
                                              (newcount, textlength, tag))
        self.dbconnection.commit()
              
              
            
    
    def _trainTargetIndexUnderParent_Tree(self, tree):
        d = {}
        for e in tree.iter():
            if e.getparent() is None: continue
            if not isinstance(e.tag, str): continue
            
            if not e.tag in d.keys(): d[e.tag] = {}
   
            index = self._getElementIndex(e)
        
            if not index in d[e.tag].keys(): 
                d[e.tag][index] = 1
            else: 
                d[e.tag][index] += 1
                    
        for tag in d.keys():
            for index in d[tag].keys():
                record = self.dbconnection.execute("select count from targetindextable where targetindex=? and targettag=?", \
                                                    (index, tag)).fetchone() #.fetchall
                if record is None:
                    self.dbconnection.execute("insert into targetindextable values(?, ?, 1, 0)", (index, tag))
#                elif len(record) > 1:
#                    self.log.error('len(dbslice) > 1, this means that there is more than one record for the word-targettag pair (%s, %s).\
#                                     This should not happen, please fix the database' % (word, element.tag))
                else:
                    newcount = record[0] + d[tag][index]
                    self.dbconnection.execute("update targetindextable set count=? where targetindex=? and targettag=?", \
                                              (newcount, index, tag))
        self.dbconnection.commit()
              
    
    
        
        
        
    def _getElementIndex(self, element):
        index = 0
        for i in element.getparent():
            if element is i: break
            index += 1
        else:
            #element not found
            self.log.warning("index could not be found for element %s" % str(element))
            return False
        
        return index
    
    
    
    
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
        self.dbconnection.execute("delete from targettextlengthtable")
        self.dbconnection.execute("delete from targetindextable")
        self.dbconnection.commit()
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    
    import optparse, sys
    
    #parse args
    optparser=optparse.OptionParser()
    optparser.add_option("-q", "--query", type="string", dest="query", default='',
                         help="Query the tag filter database with the provided sql query")
    optparser.add_option("-d", "--database", type="string", dest="database", 
                         default=os.path.join(os.path.dirname(__file__), 'FilterDB', 'tagfilter.db'),
                         help="The database that the filter will use. Defaults to %s" % \
                         os.path.join(os.path.dirname(__file__), 'FilterDB', 'tagfilter.db')) 
    
    optparser.add_option("-i", "--input", type="string", dest="inputpath", default='', 
                         help="Path to the input file / dir used to train the filter")
    optparser.add_option("--trainfile", action="store_true", dest="trainfile",
                         help="Activate to train the filter(s) using the input file")
    optparser.add_option("--traindir", action="store_true", dest="traindir",
                         help="Activate to train the filter(s) using the input directory. All dita files below the \
                         input dir will be used to train the filter.")
    optparser.add_option("--resetdb", action="store_true", dest="resetdb",
                         help="Activate to reset the filter database, ie remove all records from the database. USE WITH CAUTION.")
    
    optparser.add_option("--probataggiventext", type="string", default='',
                         help="Comma separated list of two values 'tag,word'. Returns P(element tag = tag | word is in element text")
    optparser.add_option("--probataggivenparent", type="string", default='',
                         help="Comma separated list of two values 'tag,parent'. Returns P(element tag = tag | parent tag = parent")
    
    optparser.add_option("--profile", action="store_true", dest="profile",
                         help="Use to activate profiling.")
    
    (options, args) = optparser.parse_args()
    inputpath = options.inputpath
    trainfile = options.trainfile
    traindir = options.traindir
    resetdb = options.resetdb
    query = options.query
    profile = options.profile
    database=options.database
    
    probataggiventext = options.probataggiventext.split(',')
    probataggivenparent = options.probataggivenparent.split(',')
    
    
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
    
    
    filter = ElementTagFilter(database)
        
    #
    #database query, reset, etc
    #
    if resetdb:
        response = input("are you sure you want to reset the filter DB? All records will be lost. (y/n)")
        if response == 'y':
            print("RESETTING FILTER DATABASE")
            filter.resetDB()
            print("FILTER DATABASE RESET")
        else:
            print("NOT RESETTING FILTER DATABASE: DATABASE WILL NOT BE ALTERED")
        
    if query != '':
        try:
            l = filter.dbconnection.execute(query).fetchall()
        except sqlite3.OperationalError:
            log.error("error processing query: %s" % query)
            log.error(sys.exc_info()[1])
            sys.exit(2)
        for i in l:
            print(str(i))
    
    
    #
    #calculate probabilities
    #
    if len(probataggiventext) == 2:
        print(filter.getProbaTagGivenTextWord(probataggiventext[0], probataggiventext[1]))
        
    if len(probataggivenparent) == 2:
        print(filter.getProbaTagGivenParentTag(probataggivenparent[0], probataggivenparent[1]))
    
    
    #
    #training
    #
    if trainfile:
        if not os.path.isfile(inputpath):
            log.error("--trainfile passed, but input is not a file: %s" % inputpath)
            sys.exit(1)
        if not os.path.exists(inputpath):
            log.error("input does not exist: %s" % inputpath)
            sys.exit(1)
            
        if profile:
            import cProfile, pstats
            cProfile.run("""filter.train(inputpath)""", os.path.join(os.getcwd(), 'profile.txt'))
            p = pstats.Stats('profile.txt')
            p.sort_stats('cumulative').print_stats(20)
        else:
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
        
        if profile:
            import cProfile, pstats
            cProfile.run("""for file in files: filter.train(file)""", os.path.join(os.getcwd(), 'profile.txt'))
            p = pstats.Stats('profile.txt')
            p.sort_stats('cumulative').print_stats(20)
        else:
            for file in files: filter.train(file)