"""This file implements a bayesian filter used to determine the most likely
operations that can be used when generating operands. """

import sqlite3, os.path, logging


class ElementTagFilter:
    """This filter is used to choose the 'best' tags that an element can be assigned. """
    
    def __init__(self, tagfilterdb=os.path.join(os.path.dirname(__file__), 'FilterDB', 'tagfilter.db')):
        """initialize the filter"""
        self.dbconnection = sqlite3.connect(tagfilterdb) 
        self.log = logging.getLogger()
        
        self.parenttag_tablename = "parenttagtable"
    
    
    
    def filter(self, target=None, tree=None, acceptableTags=[]):
        """Apply the filter and return the most likely operations"""
        self.target = target
        self.tree = tree

        #acceptableTags.sort() using self.getTagScore
        
        #if no entries above 0.95 probability, ask for user input.
        #add user input into the tag table, train the filter. 
        
        #take top x entries in acceptableTags and return. x can be set by user
     
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
        
        tree = lxml.etree.parse(ditafile)   #parse the dita file
        for element in tree.iter():         #iterate over the elements
            if not element.getparent(): continue
            #if parent-tag record is in database, add to count. Otherwise add new record
            dbslice = [i for i in self.dbconnection.execute("select count from ? where parenttag=? and targettag=?", \
                                                            (self.parenttag_tablename, element.getparent().tag, element.tag))]
            if len(dbslice) == 0:
                self.dbconnection.execute("insert into ? values(?, ?, 1, 0)", \
                                          (self.parenttag_tablename, element.getparent().tag, element.tag))
            elif len(dbslice) > 1:
                self.log.error('len(dbslice) > 1, this means that there is more than one record for the parenttag-targettag pair (%s, %s).\
                 This should not happen, please fix the database' % (element.getparent().tag, element.tag))
            else:
                #update record
                newcount = dbslice[0][0] + 1
                self.dbconnection.execute("update ? set count=? where parenttag=? and targettag=?", \
                                          (self.parenttag_tablename, newcount, element.getparent().tag, element.tag))
        self.dbconnection.commit()
    
    
    
#    def addData(self):
#        """Add data to the databases"""
    
    
    
    def getTagScore(self, tag, target, tree):
        """Get the score of an tag, ie the probability that the tag
        is the correct one to use for the target element"""
        #get all the conditional probabilities and combine them using Bayes' formula. Return the result
        #Derived from Bayes' formula, used to combine conditional probabilities:
        #                                 P(T|C1)P(T|C2) ... P(T|Cn)
        # p =                          ------------------------------------------
        #            P(T|C1)P(T|C2) ... P(T|Cn) + (1 - P(T|C1))(1 - P(T|C2)) ... (1 - P(T|Cn))
        #
        #where P(T|Ci) is the probability that tag T is the correct one given the condition Ci, where Ci is one of
        #parent tag value, child tag value, text, etc. 
        #Note this formula assumes that the conditions are independant. 
        
        probas = []
        probas.append(self.getProbaTagGivenParentTag(tag, target.getparent().tag))
        
        p1 = 1
        for i in probas: p1 = p1*i
        
        p2 = 1
        for i in probas: p2 = p2*(1 - i)

        p = p1 / (p1 + p2)
        
        return p
    
    
    
    def getProbaTagGivenParentTag(self, tag, parenttag):
        #find P(tag|parent) and return it
        #P(tag|parent) = #times tag appears under parent / #number of times any tag appears under parent. 
        
        tagcount = self.dbconnection.execute("select count from ? where targettag=? and parenttag=?", \
                                             (self.parenttag_tablename, tag, parenttag)).fetchall()[0][0]
        totalcount = 0
        for i in self.dbconnection.execute("select count from ? where parenttag=?",\
                                               (self.parenttag_tablename, parenttag)).fetchall():
            totalcount += i[0]
            
        if not totalcount >= tagcount: 
            self.log.error("impossible probability generated, totalcount < tagcount: %i < %i" % (totalcount, tagcount))
            return None
        
        return float(tagcount) / float(totalcount)
    
    
    
    def getProbaTagGivenChild(self, tag, child):
        #find P(tag|child) and return
        pass
    
    
    
    def getProbaTagGivenText(self, tag, word):
        #find P(tag|word in target.text) and return
        pass
    
    
    
    def getProbaTagGivenChildText(self, tag, word):
        #find P(tag|word in any child) and return
        pass
    
    
    
    def getTokens(self):
        """A function used to ensure that the same tokens are used whether we are training the 
        filter or calculating probabilities"""
        
        #parent tag, child tags, text, text length, descendant text, descendant depth
        #shape of tree? How would this be accomplished?
    
        pass
    
    
    
    
    def backup(self):
        """backup the database"""
        pass
    
    
    
    
    def rollback(self):
        """rollback the database"""
        pass
    
    
    
    def reset(self):
        """reset the database"""
        pass
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    
    #parse args
    optparser.add_option("-i", "--input", type="string", dest="input", default='', 
    help="Path to the input file")
    optparser.add_option("--train", action="store_true", dest="train",
    help="Turn this on to train the filter(s) using the input file")
    (options, args) = optparser.parse_args()
    input = options.input
    debug = options.train
    
    #this next block ensures that the user can pass the input as a positional
    #argument, without the -i
    try:
        input = args[0]
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
    
    if train:
        filter = ElementTagFilter()
        filter.train(input)
    