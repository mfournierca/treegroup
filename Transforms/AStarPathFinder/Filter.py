#!/usr/bin/env python3

"""This file implements a bayesian filter used to determine the most likely
operations that can be used when generating operands. """

import sqlite3, os.path, logging, sys
import lxml.etree


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
            self.dbconnection.execute("select * from descendanttexttable")
        except sqlite3.OperationalError:
            self.dbconnection.execute("create table descendanttexttable(word, targettag, depth INTEGER, count INTEGER, proba FLOAT)")
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
            
        try:
            self.dbconnection.execute("select * from siblingcounttable")
        except sqlite3.OperationalError:
            self.dbconnection.execute("create table siblingcounttable(siblingcount INTEGER, targettag, count INTEGER, proba FLOAT)")
            self.dbconnection.commit()
            
        try:
            self.dbconnection.execute("select * from childcounttable")
        except sqlite3.OperationalError:
            self.dbconnection.execute("create table childcounttable(childcount INTEGER, targettag, count INTEGER, proba FLOAT)")
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
        #A value of 0.5 essentially returns no information, and does not bias the filter in either
        #direction 
        self.floorproba = 0.1
            
        #similarly, by looking at the function in self.getTagScore() you can see that if any of the
        #probas is 1, then the entire result becomes 1. This is also not desirable for the same reason as 
        #above. Therefore, we need to assign an upper limit on the probability. 
        self.ceilingproba = 0.9
            
        #excludewords is used to exclude common or very rare words from computation
        self.excludewords = ['I', \
                             'a', 'about', 'after', 'all', 'also', 'an', 'and', 'any', 'as', 'at', \
                             'back', 'be', 'because', 'but', 'by', \
                             'can', 'come', 'could', \
                             'day', 'do', \
                             'even', \
                             'first', 'for', 'from', \
                             'get', 'give', 'go', 'good', \
                             'have', 'he', 'her', 'him', 'his', 'how', \
                             'if', 'in', 'into', 'it', 'its', \
                             'just', \
                             'know', \
                             'like', 'look', \
                             'make', 'me', 'most', 'my', \
                             'new', 'no', 'not', 'now', \
                             'of', 'on', 'one', 'only', 'or', 'other', 'our', 'out', 'over', \
                             'person', 'say', 'see', 'she', 'so', 'some', \
                             'take', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'think', 'this', 'time', 'to', 'two', \
                             'up', 'us', 'use', \
                             'want', 'way', 'we', 'well', 'what', 'when', 'which', 'who', 'will', 'with', 'work', 'would', \
                             'year', 'you', 'your']
        
        
        #bias the filter in favor of positive results. When calculating probabilities the conditional probabilities, 
        #P(X | Y), the sum from the db that gives X is multiplied by biasfactor, and the subdomain Y is expanded by the 
        #appropriate amount. 
        self.biasfactor = 2
        
        
        #width determines how many tags are returned. Tags are sorted by score, the score comes from the filter. 
        #the width determines how many are returned, ie if width = 3, then the top 3 tags are returned. 
        #If 0 or negative, all tags are returned
        self.width = 3
        
        
        #set proba threshold, beyond which the user is asked for input?
        
        
        
    
    def filter(self, target=None, acceptableTags=[]):
        """Apply the filter and return the most likely operations"""
        
        self.target = target
        
        #get scores
        scores = {}
        for t in acceptableTags:
            if t in scores.keys():
                self.log.error('repeated tag %s' % t)
                sys.exit()
            scores[t] = self.getTagScore(t, target)
        
        #sort tags
        sortedtags = acceptableTags[:]
        sortedtags.sort(key=lambda t: scores[t], reverse=True) #sort by filter score, highest first
        
        #if no entries above 0.95 probability, ask for user input.
        #add user input into the tag table, train the filter. 
        
        #take top self.width entries in acceptableTags and return. self.width can be set in __init__()
        #want to pass the completed tag list and the scores back.
        
        #
        #Want to include tags that have the same score as the bottom of the slice created below - even if the
        #slice gets longer as a result. 
        #
        if self.width <= 0:
            self.log.info("filteredtags: %s" % str(sortedtags))
            return sortedtags, scores
        else:
            self.log.info("filteredtags: %s" % str(sortedtags[:self.width]))
            return sortedtags[:self.width], scores
    
    
    
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
        
        #solved by self.baseproba and self.ceilingproba
        ####Note also that if any of the getProba functions returns 0 or 1, 
        ####then p will equal 0 or 1, respectively. This can be seen just by looking at the equation. 
        ####If you are experiencing weird results, or see that a certain tag is being taken or rejected
        ####when it shouldn't be, this could be the cause. 
        
        probas = []
        
        #parent info
        if target.getparent() is not None:
            probas.append(self.getProbaTagGivenParentTag(tag, target.getparent().tag))
        probas.append(self.getProbaTagGivenIndexUnderParentRange(tag, self._getElementIndex(target)))
        
        #text info                                       
        words = self._getWordsFromText(target.text)
        probas.append(self.getProbaTagGivenTextLengthRange(tag, len(words))) 
        for word in words:
            probas.append(self.getProbaTagGivenTextWord(tag, word))
        
        #siblings
        if target.getparent() is not None:
            probas.append(self.getProbaTagGivenNumberOfSiblingsRange(tag, len(target.getparent())))
        
        #descendants
        probas.append(self.getProbaTagGivenNumberOfChildrenRange(tag, len(target)))
    
        #remove 'uninteresting' entries from probas, ie probas that are too close to 0.5
        
        p1 = 1.0
        for i in probas: p1 = p1*i
        p2 = 1.0
        for i in probas: p2 = p2*(1 - i)
        
        p = p1 / (p1 + p2)
        self.log.info('tag score: %12.20s / (%12.20s + %12.20s) = %12.20s' % (str(p1), str(p1), str(p2), str(p)))
        return p
        
    
    
    
    
    def _setFloorCieling(self, p):
        if p < self.floorproba: 
            return self.floorproba
        elif p > self.ceilingproba:
            return self.ceilingproba
        else:
            return p
    
    
    
    
    def getProbaTagGivenParentTag(self, tag, parenttag):
        #find P(tag|parent) and return it
        #P(tag|parent) = number of times tag appears under parent / #number of times any tag appears under parent. 
        #need some code to control what happens if tag or parenttag is not in database - probably set to 
        #0 and wait for user input, or define a "base probability" that is used in the absence of information. 
        tagcount = self.dbconnection.execute("select sum(count) from parenttagtable where targettag=? and parenttag=?", \
                                             (tag, parenttag)).fetchone()[0]
        if tagcount is None: tagcount = 0
        
        totalcount = self.dbconnection.execute("select sum(count) from parenttagtable where parenttag=?", \
                                       (parenttag,)).fetchone()[0]    
        if totalcount is None: return self.floorproba
        
        totalcount += (self.biasfactor - 1) *tagcount
        tagcount *= self.biasfactor
        
        if not totalcount >= tagcount: 
            self.log.error("impossible probability generated, totalcount < tagcount: %i < %i" % (totalcount, tagcount))
            return None
        
        p = float(tagcount) / float(totalcount)
        p = self._setFloorCieling(p)
        self.log.info('P(tag = %10.20s | parenttag = %20.20s) = %6.10s / %6.10s = %2.10s' % (tag, parenttag, str(tagcount), str(totalcount), str(p)))
        return p
    
        
        
        
    def getProbaTagGivenIndexUnderParentRange(self, tag, index):
        #get P(target tag = tag | target is within range under its parent)

        #define range. Range could be defined with a function over the index size, so interval gets larger as 
        #index gets larger, vice versa, etc. Or as the index get longer, the upper bound of the range goes up, 
        #but the lower bound does not go down.
        lowerbound = index - 1
        upperbound = index + 1
        
        indexcount = self.dbconnection.execute("select sum(count) from targetindextable where targettag=? and targetindex>=? and targetindex<=?",\
                                          (tag, lowerbound, upperbound)).fetchone()[0]   
        if indexcount is None: indexcount = 0
            
        totalcount = self.dbconnection.execute("select sum(count) from targetindextable where targetindex>=? and targetindex<=?", \
                                               (lowerbound, upperbound)).fetchone()[0]
               
        #bias the filter in favour of positive results, double the count. total count already contains count, 
        #so we only need to add once to compensate
        totalcount += (self.biasfactor - 1) * indexcount 
        indexcount *= self.biasfactor 
        
        if not totalcount >= indexcount: 
            self.log.error("impossible probability generated, totalcount < indexcount: %i < %i" % (totalcount, indexcount))
            return None
        
        p = float(indexcount) / float(totalcount)
        p = self._setFloorCieling(p)
        self.log.info('P(tag = %10.20s | %3.10s <= index under parent <= %3.10s) = %6.10s / %6.10s = %2.10s' % (tag, str(lowerbound), str(upperbound), str(indexcount), str(totalcount), str(p)))
        return p
    
    
    
    
    def getProbaTagGivenTextWord(self, tag, word):
        #find P(tag|word in target.text) and return
        tagcount = self.dbconnection.execute("select sum(count) from targettexttable where targettag=? and word=?",\
                                             (tag, word)).fetchone()[0]
        if tagcount is None: tagcount = 0
            
        totalcount = self.dbconnection.execute("select sum(count) from targettexttable where word=?", (word,)).fetchone()[0]
        if totalcount is None: return self.floorproba
        
        #bias the filter in favour of positive results, double the count. total count already contains tagcount, 
        #so we only need to add once to compensate
        totalcount += (self.biasfactor - 1) * tagcount 
        tagcount *= self.biasfactor
        
        if not totalcount >= tagcount: 
            self.log.error("impossible probability generated, totalcount < tagcount: %i < %i" % (totalcount, tagcount))
            return None
        
        p = float(tagcount) / float(totalcount)
        p = self._setFloorCieling(p)
        self.log.info('P(tag = %10.20s | word "%s" is in text) = %6.10s / %6.10s = %2.10s' % (tag, word, str(tagcount), str(totalcount), str(p)))
        #self.log.debug('tag: %s\tword: %s\tproba: %s/%s =  %s' % (tag, word, str(tagcount), str(totalcount), str(p)))
        return p
    
    
    
    
    def getProbaTagGivenTextLengthRange(self, tag, length):
        #get the text length based on how close it is to the lengths stored in the filter db, 
        #ie, given interval = some integer, calculate and return
        #P(target tag | text length is within +/- interval of target text length)
        
        #define range. Range could be defined with a function over the text length, so interval gets larger as 
        #text gets larger, vice versa, etc. Or as the text get longer, the upper bound of the range goes up, 
        #but the lower bound does not go down. 
        lowerbound = length - 1
        upperbound = length + 1
        
        count = self.dbconnection.execute("select sum(count) from targettextlengthtable where targettag=? and length>=? and length<=?", \
                                          (tag, lowerbound, upperbound)).fetchone()[0]                                          
        if count is None: count = 0
        
        totalcount = self.dbconnection.execute("select sum(count) from targettextlengthtable where length>=? and length<=?", \
                                               (lowerbound, upperbound)).fetchone()[0]
                                                    
        totalcount += (self.biasfactor - 1) * count
        count *= self.biasfactor
        
        p = float(count) / float(totalcount)
        p = self._setFloorCieling(p)
        self.log.info("P(tag = %10.20s | %3.10s <= text length <= %10.10s) = %6.10s / %6.10s = %2.10s" % (tag, str(lowerbound), str(upperbound), str(count), str(totalcount), str(p)))
        #self.log.debug('tag: %s\tlength: %s\tlowerbound: %s\tupperbound: %s\tproba: %s/%s =  %s' % (tag, str(length), str(lowerbound), str(upperbound), str(count), str(totalcount), str(p)))
        return p
    
        
        
        
    
    def getProbaTagGivenNumberOfSiblingsRange(self, tag, number):
        #get P(target tag = tag | target has number of siblings within range)
        
        lowerbound = number - 2
        upperbound = number + 2
        
        siblingcount = self.dbconnection.execute("select sum(count) from siblingcounttable where targettag=? and siblingcount>=? and siblingcount<=?", \
                                                 (tag, lowerbound, upperbound)).fetchone()[0]
        if siblingcount is None: siblingcount = 0
        
        totalcount = self.dbconnection.execute("select sum(count) from siblingcounttable where siblingcount>=? and siblingcount<=?",\
                                               (lowerbound, upperbound)).fetchone()[0]
                           
        totalcount += (self.biasfactor - 1) * siblingcount
        siblingcount *= self.biasfactor
                            
        if not totalcount >= siblingcount:
            self.log.error("impossible probability generated, totalcount < siblingcount: %i < %i" % (totalcount, siblingcount))
            
        p = float(siblingcount) / float(totalcount)
        p = self._setFloorCieling(p)
        self.log.info("P(tag = %10.20s | %3.10s <= number of siblings <= %3.5s) = %6.10s / %6.10s = %2.10s" % (tag, str(lowerbound), str(upperbound), str(siblingcount), str(totalcount), str(p)))
        #self.log.debug('tag: %s\tnumber: %s\tlowerbound: %s\tupperbound: %s\tproba: %s/%s =  %s' % (tag, number, str(lowerbound), str(upperbound), str(siblingcount), str(totalcount), str(p)))
        return p
    
    
    
    
    
    def getProbaTagGivenNumberOfChildrenRange(self, tag, number):
        #get P(target tag = tag | target has number of children within range)
        
        lowerbound = number - 2
        upperbound = number + 2
        
        subcount = self.dbconnection.execute("select sum(count) from childcounttable where targettag=? and childcount>=? and childcount<=?",\
                                             (tag, lowerbound, upperbound)).fetchone()[0]
        if subcount is None: subcount = 0
        
        totalcount = self.dbconnection.execute("select sum(count) from childcounttable where childcount>=? and childcount<=?",\
                                             (lowerbound, upperbound)).fetchone()[0]
        
        totalcount += (self.biasfactor - 1) * subcount
        subcount *= self.biasfactor
        
        if not totalcount >= subcount:
            self.log.error("impossible probability generated, totalcount < siblingcount: %i < %i" % (totalcount, subcount))
            
        p = float(subcount) / float(totalcount)
        p = self._setFloorCieling(p)
        self.log.info("P(tag = %10.20s | %3.10s <= number of children <= %3.10s) = %6.10s / %6.10s = %2.10s" % (tag, str(lowerbound), str(upperbound), str(subcount), str(totalcount), str(p)))
        #self.log.debug('tag: %s\tnumber: %s\tlowerbound: %s\tupperbound: %s\tproba: %s/%s =  %s' % (tag, number, str(lowerbound), str(upperbound), str(subcount), str(totalcount), str(p)))
        return p
    
    
    
    
    
    def getProbaTagGivenDescendantTextDepthRange(self, tag, word, depth):
        #find P(tag|word in any descendant in depth range) and return
        
        lowerbound = depth - 1
        upperbount = depth + 1
        
        subcount = self.dbconnection.execute("select sum(count) from descendanttexttable where targettag=? and word=? and depth>=? and depth<=?",\
                                             (tag, word, lowerbound, upperbound)).fetchone()[0]
        if subcount is None: subcount = 0
        
        totalcount = self.dbconnection.execute("select sum(count) from descendanttexttable where word=? and depth=>=? and depth<=?",\
                                               (word, lowerbound, upperbound)).fetchone()[0]
        
        totalcount += (self.biascount - 1) * subcount
        subcount *= self.biasfactor
        
        if not toalcount >= subcount: 
            self.log.error("impossible probability generated, totalcount < siblingcount: %i < %i" % (totalcount, subcount))
        
        p = float(subcount) / float(totalcount)
        p = self._setFloorCieling(p)
        self.log.info("P(tag = %10.20s | text within descendant between levels %3.10s -> %3.10s) = %6.10s / %6.10s = %2.10s" % (tag, str(lowerbound), str(upperbound), str(subcount), str(totalcount), str(p))) 
        #self.log.debug('tag: %s\tword: %s\tdepth: %s\tlowerbound: %s\tupperbound: %s\tproba: %s/%s =  %s' % (tag, word, str(depth), str(lowerbound), str(upperbound), str(subcount), str(totalcount), str(p)))
        return p
        
                                            
    
    
    
    
    
    def getProbaTagGivenChildTag(self, tag, child):
        #find P(tag|childtag) and return
        pass
    
    
    
    
    
    def processDB(self):
        pass
        
        #process the db - prepare for calculations
        
        #check for dupes
        
        #suggestions for changes to the db here come from 
        #http://www.paulgraham.com/spam.html
        
        #remove points with insufficient data, ie where count < 5
        #(arbitrary and must be tweaked with experience)
        
        #increase some entries to increase their weight?
    
        #pre-compute probabilities
    
    
    
    
    
    def train(self, ditafile):
        """Used to train the filter automatically. Take a dita file, and iterate the 
        elements one by one. For each element, get tokens and add to the databases."""
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
        self._trainParentTag(tree)
        self._trainTargetTextLength(tree)
        self._trainTargetText(tree)
        self._trainTargetIndexUnderParent(tree)
        self._trainNumberOfSiblings(tree)
        self._trainNumberOfChildren(tree)
        self._trainTargetDescendantText(tree)
        
        self.dbconnection.commit()
    
    
    
    def _trainNumberOfChildren(self, tree):
        d = {}
        for e in tree.iter():
            if not isinstance(e, lxml.etree._Element): continue
            if isinstance(e, lxml.etree._ProcessingInstruction): continue
            if isinstance(e, lxml.etree._Entity): continue
            
            childcount = len(e)
            if childcount is None: continue
            
            if not e.tag in d.keys(): d[e.tag] = {}
    
            if not childcount in d[e.tag].keys():
                d[e.tag][childcount] = 1
            else:
                d[e.tag][childcount] += 1
                
        for tag in d.keys():
            for childcount in d[tag].keys():
                try:
                    record = self.dbconnection.execute("select count from childcounttable where childcount=? and targettag=?", \
                                                       (childcount, tag)).fetchone()
                except sqlite3.InterfaceError:
                    log.warning(sys.exc_info()[1])
                    log.warning("select count from childcounttable where childcount=%s and targettag=%s" % (str(childcount), tag))
                    continue
                
                if record is None: 
                    #self.log.debug("adding record: (%i, %s, %i, 0)" % (childcount, tag, d[tag][childcount]))
                    self.dbconnection.execute("insert into childcounttable values(?, ?, ?, 0)", (childcount, tag, d[tag][childcount]))
                else:
                    newcount = record[0] + d[tag][childcount]
                    #self.log.debug("updating record: (%i, %s, %i, 0)" % (childcount, tag, newcount))
                    self.dbconnection.execute("update childcounttable set count=? where childcount=? and targettag=?", \
                                              (newcount, childcount, tag))
        self.dbconnection.commit()
        
    
    
    
    
    
    def _trainNumberOfSiblings(self, tree):
        d = {}
        for e in tree.iter():
            if e.getparent() is None: continue
            if not isinstance(e, lxml.etree._Element): continue
            if isinstance(e, lxml.etree._ProcessingInstruction): continue
            if isinstance(e, lxml.etree._Entity): continue
            
            siblingcount = len(e.getparent())
            if siblingcount is None: continue
            
            if not e.tag in d.keys(): d[e.tag] = {}
            
            if not siblingcount in d[e.tag].keys():
                d[e.tag][siblingcount] = 1
            else:
                d[e.tag][siblingcount] += 1
                
        for tag in d.keys():
            for siblingcount in d[tag].keys():
                try:
                    record = self.dbconnection.execute("select count from siblingcounttable where siblingcount=? and targettag=?", \
                                                       (siblingcount, tag)).fetchone()
                except sqlite3.InterfaceError:
                    log.warning(sys.exc_info()[1])
                    log.warning("select count from siblingcounttable where siblingcount=%s and targettag=%s" % (str(siblingcount), tag))
                    continue
                
                if record is None: 
                    #self.log.debug("adding record: (%i, %s, %i, 0)" % (siblingcount, tag, d[tag][siblingcount]))
                    self.dbconnection.execute("insert into siblingcounttable values(?, ?, ?, 0)", (siblingcount, tag, d[tag][siblingcount]))
                else:
                    newcount = record[0] + d[tag][siblingcount]
                    #self.log.debug("updating record: (%i, %s, %i, 0)" % (siblingcount, tag, newcount))
                    self.dbconnection.execute("update siblingcounttable set count=? where siblingcount=? and targettag=?", \
                                              (newcount, siblingcount, tag))
        self.dbconnection.commit()
        
                    
                    
                    
    
    def _trainParentTag(self, tree):
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
                    #self.log.debug('adding record: (%s, %s, %i, 0)' % (parenttag, tag, d[tag][parenttag]))
                    self.dbconnection.execute("insert into parenttagtable values(?, ?, ?, 0)", (parenttag, tag, d[tag][parenttag]))
#                elif len(record) > 1:
#                    self.log.error('len(dbslice) > 1, this means that there is more than one record for the word-targettag pair (%s, %s).\
#                                     This should not happen, please fix the database' % (word, element.tag))
                else:
                    newcount = record[0] + d[tag][parenttag]
                    #self.log.debug('updating record: (%s, %s, %i, 0' % (parenttag, tag, newcount))
                    self.dbconnection.execute("update parenttagtable set count=? where parenttag=? and targettag=?", \
                                              (newcount, parenttag, tag))
        self.dbconnection.commit()
                
                
    
    
    
    def _trainTargetText(self, tree):
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
                    self.dbconnection.execute("insert into targettexttable values(?, ?, ?, 0)", (word, tag, d[tag][word]))
#                elif len(record) > 1:
#                    self.log.error('len(dbslice) > 1, this means that there is more than one record for the word-targettag pair (%s, %s).\
#                                     This should not happen, please fix the database' % (word, element.tag))
                else:
                    newcount = record[0] + d[tag][word]
                    self.dbconnection.execute("update targettexttable set count=? where word=? and targettag=?", \
                                              (newcount, word, tag))
        self.dbconnection.commit()
        
                
                
    
    
    def _trainTargetTextLength(self, tree):
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
                    self.dbconnection.execute("insert into targettextlengthtable values(?, ?, ?, 0)", (textlength, tag, d[tag][textlength]))
#                elif len(record) > 1:
#                    self.log.error('len(dbslice) > 1, this means that there is more than one record for the word-targettag pair (%s, %s).\
#                                     This should not happen, please fix the database' % (word, element.tag))
                else:
                    newcount = record[0] + d[tag][textlength]
                    self.dbconnection.execute("update targettextlengthtable set count=? where length=? and targettag=?", \
                                              (newcount, textlength, tag))
        self.dbconnection.commit()
              
              
            
    
    def _trainTargetIndexUnderParent(self, tree):
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
                    self.dbconnection.execute("insert into targetindextable values(?, ?, ?, 0)", (index, tag, d[tag][index]))
#                elif len(record) > 1:
#                    self.log.error('len(dbslice) > 1, this means that there is more than one record for the word-targettag pair (%s, %s).\
#                                     This should not happen, please fix the database' % (word, element.tag))
                else:
                    newcount = record[0] + d[tag][index]
                    self.dbconnection.execute("update targetindextable set count=? where targetindex=? and targettag=?", \
                                              (newcount, index, tag))
        self.dbconnection.commit()
              
    
    
        
        
    def _trainTargetDescendantText(self, tree):
        stack = [tree.getroot()]
        targettextdict = {}
        descendanttextdict = {}
        for element in tree.getroot().iter():
            parent = element.getparent()
            if parent is None: continue
            if not isinstance(element, lxml.etree._Element): continue
            if isinstance(element, lxml.etree._ProcessingInstruction): continue
            if isinstance(element, lxml.etree._Entity): continue
            
            #search stack for parent, take slice and append element
            try:
                parentindex = stack.index(parent)
            except ValueError:
                self.log.error('could not find parent index')
                sys.exit()
            stack = stack[:parentindex + 1]
            stack.append(element)
            
            #get words
            if not element.text: continue
            if not isinstance(element.text, str): continue
            words = self._getWordsFromText(element.text)
                
            for ancestor in stack[:-1]: #exclude the element
                depth = len(stack) - stack.index(ancestor)
                if not ancestor.tag in descendanttextdict.keys(): descendanttextdict[ancestor.tag] = {}
                if not depth in descendanttextdict[ancestor.tag].keys(): descendanttextdict[ancestor.tag][depth] = {}
                for word in words:
                    if not word in descendanttextdict[ancestor.tag][depth].keys(): 
                        descendanttextdict[ancestor.tag][depth][word] = 1
                    else:
                        descendanttextdict[ancestor.tag][depth][word] += 1
        
        #add dict(s) to db    
        for tag in descendanttextdict.keys():
            for depth in descendanttextdict[tag].keys():
                for word in descendanttextdict[tag][depth].keys():
                    record = self.dbconnection.execute("select count from descendanttexttable where word=? and targettag=? and depth=?",\
                                                       (word, tag, depth)).fetchone()
                    if record is None: 
                        self.dbconnection.execute("insert into descendanttexttable values(?,?,?,?,0)", (word, tag, depth, descendanttextdict[tag][depth][word]))
                    else:
                        newcount = record[0] + descendanttextdict[tag][word]
                        self.dbconnection.execute("update descendanttexttable set count=? where word=? and targettag=? and depth=?", \
                                                  (newcount, word, tag, depth))
        self.dbconnection.commit()
        
    
    
    
        
    def _getElementIndex(self, element):
        index = 0
        if element.getparent() is None: return 0
        for i in element.getparent():
            if element is i: break
            index += 1
        else:
            #element not found
            self.log.warning("index could not be found for element %s" % str(element))
            return False
        
        return index
    
    
    
    
    def _getWordsFromText(self, text):
        if text is None: return []
        import string
        words = []
        for word in text.split(' '):
            word = word.lower()
            for letter in word: 
                if (letter not in string.ascii_lowercase) and (letter not in string.digits) and (letter not in ['-', '_']):
                    word = word.replace(letter, '')
            if len(word) == 0: continue
            if not isinstance(word, str): continue
            if word in self.excludewords: continue
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
        self.dbconnection.execute("delete from descendanttexttable")
        self.dbconnection.execute("delete from targettextlengthtable")
        self.dbconnection.execute("delete from targetindextable")
        self.dbconnection.execute("delete from siblingcounttable")
        self.dbconnection.execute("delete from childcounttable")
        self.dbconnection.commit()
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    
    import optparse, sys
    
    #parse args
    optparser=optparse.OptionParser()
    optparser.add_option("-i", "--input", type="string", dest="inputpath", default='', 
                         help="Path to the input file / dir used to train the filter")
    
    optparser.add_option("-q", "--query", type="string", dest="query", default='',
                         help="Query the tag filter database with the provided sql query")
    optparser.add_option("-d", "--database", type="string", dest="database", 
                         default=os.path.join(os.path.dirname(__file__), 'FilterDB', 'tagfilter.db'),
                         help="The database that the filter will use. Defaults to %s" % \
                         os.path.join(os.path.dirname(__file__), 'FilterDB', 'tagfilter.db')) 
    
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
    optparser.add_option("--debug", action="store_true", dest="debug",
                         help="Use to activate debugging.")
    optparser.add_option("--testonfile", action="store_true", dest="testonfile", 
                         help="Use to get a score report on every element in a file" )
    
    (options, args) = optparser.parse_args()
    inputpath = options.inputpath
    trainfile = options.trainfile
    traindir = options.traindir
    resetdb = options.resetdb
    query = options.query
    profile = options.profile
    database = options.database
    debug = options.debug
    
    probataggiventext = options.probataggiventext.split(',')
    probataggivenparent = options.probataggivenparent.split(',')
    
    testonfile = options.testonfile
    
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
    
    if debug:
        debughandler = logging.StreamHandler(sys.stdout)
        debughandler.setLevel(logging.DEBUG)
    #    debugformatter = logging.Formatter("%(message)s")
        debugformatter = logging.Formatter("%(module)8.8s.%(funcName)20.20s%(levelname)10.10s\t%(message)s")
        debughandler.setFormatter(debugformatter)
        log.addHandler(debughandler)
    
    
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
    #test on file
    #
    if testonfile:
        tree = lxml.etree.parse(inputpath)
        for e in tree.getroot().iter():
            score = filter.getTagScore(e.tag, e)
            print("element: %s\tscore: %s\n" % (str(e), str(score)))
    
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