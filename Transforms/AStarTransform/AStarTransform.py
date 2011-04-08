"""Transform a tree into dita using an adapted A* pathfinding algorithm"""


import logging, lxml.etree, sys, optparse, re, copy

import DitaTools.Tree.File.Dita

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import Tree.Tree, Element.Element



    
class ValidationError():
    """The validation error object contains all the information about 
    the validation error being addressed - the message, the element 
    being addressed, the xpath to find that element and some hints for 
    the Operand Builder"""
    
    def __init__(self, tree):
        self.log = logging.getLogger()
        self.log.debug('getting validation error and element')
        #the following attributes can be retrieved by any other object
        #and are mainly used by OperandBuilder as hints as to what it
        #should do
        self._suggestedrename = None
        
        #retrieve the first validation error message
        validationerrors = DitaTools.Tree.File.Dita.v11_validate(tree)
        if len(validationerrors) == 0:
            #this will stop the main loop in Transform()
            self.log.debug('no errors found')
            raise StopIteration
        self.message = validationerrors[0]
        self.log.debug('message: %s' % self.message)    
        
        #try to parse the message, return if successful
        if self._noDeclarationParser(): pass
        elif self._ditaElementDoesNotFollowDTDParser(): pass
        else:
            self.log.error('message did not match any known errors, cannot initialize')
            raise NoErrorMatchException(self.message)
    
    #there are several patterns that an error can follow, all of which need to be
    #interpreted differently in order to find the correct element. 
    #Every validation error message must match a parser here. 
        
    def _noDeclarationParser(self):
        pattern = r'.*?\:\d*\:\d*:ERROR:VALID:DTD_UNKNOWN_ELEM: No declaration for element (.*)'
        match = re.search(pattern, self.message)
        if match:
            self.log.debug('\tmatched pattern: "%s"' % pattern)
            #in this case, "no declaration for element $1 means that this element should not 
            #appear in the tree at all, so every instance of this element will create an error, 
            #so the first instance of this element created first error. Therefore, we only need to 
            #find the first instance of this element
            self.xpath = '//%s' % match.group(1)
            self.suggestedrename = 'dita'
            return True
        else: 
            return False

    def _ditaElementDoesNotFollowDTDParser(self):
        pattern = r'.*?\:\d*\:\d*:ERROR:VALID:DTD_CONTENT_MODEL: Element dita content does not follow the DTD, expecting \(topic \| concept \| task \| reference \| glossentry\)\+, got \((.*?)\)'
        match = re.search(pattern, self.message)
        if match:
            self.log.debug('\tmatched pattern: "%s"' % pattern)
            tags = match.group(1).split(' ')
            self.log.debug('found tags: %s' % str(tags))
            for i in tags: 
                if i in ['topic', 'task', 'concept', 'reference']:
                    continue
                else:
                    tag = i
                    break
            self.xpath = '//%s' % tag
            self.suggestedrename = 'topic'
            return True
        else: 
            return False
    
    def _emptyTopicParser(self):
        pattern = r'.*?\:\d*\:\d*:ERROR:VALID:DTD_CONTENT_MODEL: Element topic content does not follow the DTD, expecting \(topic \| concept \| task \| reference \| glossentry\)\+, got '
        match = re.search(pattern, self.message)
        if match:
            self.log.debug('\tmatched pattern: "%s"' % pattern)
            self.xpath = '//%s' % 'topic'
            return True
        else: 
            return False
    
    
    
    
    
    
    
    
    
    
    
    


class AStarPathfinder():
    
    def __init__(self, file):
        """Initialize"""
        self.log = logging.getLogger()
        
        self.log.debug('Initializing')
        self.file = file
        self.tree = lxml.etree.parse(file)
        
        #the closed set is the set of trees that have already been travelled through
        self.closed = []
        
        #openset is the set of trees under consideration for the next movement
        start = SetMember(self.tree)
        start.costscore = 0
        start.calculateFScore()
        self.open = [start]
        
        
    def findPath(self):
        """Run the pathfinding algorithm and return the path"""
        self.log.debug('running pathfinder')
        
        while len(self.open) > 0:
            x = self.getLowestFScore()
            if len(DitaTools.Tree.File.Dita.v11_validate(x.tree)) == 0:
                #success
                self.log.debug('awwwwwwwwwwww  yeeeeeeeeaaaaaaahhh!!!!!!!!')
                return True
            self.open.remove(x)
            self.closed.append(x)
            #t is the tree the algorithm just "moved" to. We now have to consider
            #the neighbours of t and add them to the open set
            self.getNeighbors(x)
        #if open set is empty, failure
        return False
    
    def buildScores(neighbors):
        #build the h and g scores for all the neighbors
        pass
    
    def getLowestFScore(self):
        f = self.open[0].fscore
        result = self.open[0]
        for m in self.open[1:]:
            if m.fscore < f:
                f = m.fscore
                result = m
        return result

    def getNeighbors(self, x):
        #this function is also extremely important. Here we define the neighbors of
        #t, ie trees being considered for inclusion in the open set. 
        #The neighbors can be generated by looking at some, one or all of the validation
        #errors, or by any other scheme. This must remain flexible so either this funcion
        #or the function pointed to here can be changed
        neighbors = getNeighbors_FirstValidationError()
        #for each neighbor n
            #if n in closed set, continue
            #calculate tentative g score
            #if n not in open set #how do you test this? Test for equality of tree
                #add n to open set
                #tentative is better = True. The tentative is better is used to
                
                #compare different paths in the open set - g might be different for the same n
                #if approached from a different node in the closedset. If tentative is better is
                #true, then approaching n from x is better than approaching it from any other member
                #of the closed set.
            
            #elif tentative g score < n.gscore
                #if the first conditional is not matched, then n is in the open set, therefore it
                #has a g score already.  
                #tentative is better = True
                
            #else:
                #in this case, going to n from x is not a good option.
                #tentative is better = False
            
            #if tentative is better  
                #n.camefrom = x
                #n.gscore = tentative g score
                #n.hscore = calculate heuristic
                #n.fscore = n.gscore + n.hscore
                #update closed set and open set. 
                #calculate h score
            
        return neighbors





class SetMember():
    """A class used to represent the members of the open set and the
    closed set. This set stores tree, operand, cost and scores for 
    each instance, and provides functions to calculate them"""
    def __init__(self, tree):
        self.tree = tree
        self.operand = None
        
        self.costscore = None
        self.heuristicscore = self.calculateHScore()
        self.fscore = None
        
    def calculateHScore(self):
        #this is a call the the heuristic function. This heuristic is one 
        #of the key things about this algorithm, and can be changed or
        #pointed at another function as needed
        self.heuristicscore = hScore_ValidationErrorsCount(self.tree)
    
    def calculateFScore(self):
        self.fscore = self.costscore + self.heuristicscore







#===============================================================================
# possible neighbor finding functions
#===============================================================================

#finding neighbors is very important, since there are many many ways of altering each
#tree. Neighbors can be defined in many ways, and can be generated by looking at all, one
#or some of the validation errors. Also, the operand builder used to create the neighbors
#(by moving the tree) can be changed. 

class NeighborFinder():
    def __init__(self):
        pass
    
def getNeighbors_FirstValidationError(tree):
    #get the set of neighbors based on fixing the first validation error.
    pass


#===============================================================================
# end neighbor finding functions
#===============================================================================








#===============================================================================
# #possible heuristics
#===============================================================================

#heuristics are used to estimate the distance from a tree to the destination, ie a
#dita region. heuristics must be "admissible", which basically means they can 
#underestimate the real distance, but never overestimate

def hScore_ValidationErrorsCount(tree):
    """This heuristicscore algorithm simply counts the number of validation errors of the
    tree. 
    
    This is obviously admissible because every error message may take one or more 
    operations to fix, and every error message that gets fixed might lead to a new
    one, or more than one, being generated. So this heuristic function always 
    underestimates and is therefore admissible."""

    return len(DitaTools.Tree.File.Dita.v11_validate(tree))

#===============================================================================
# end heuristics
#===============================================================================











#===============================================================================
# main
#===============================================================================

if __name__ == "__main__":
    #called from a command line
    optparser=optparse.OptionParser()
    
    optparser.add_option("-i", "--input", type="string", dest="input", default='', 
    help="Path to the input file")
    optparser.add_option("-o", "--output", type="string", dest="output", default='', 
    help="Path to the input file")
    optparser.add_option("--debug", action="store_true", dest="debug",
    help="Turn this on to activate debug logging.")
    #optparser.add_option( "-t", "--tempdir", type="string", dest="tempdir", default=None, 
    #help="path to the tempdir")
    
    (options, args) = optparser.parse_args()
    input = options.input
    debug = options.debug
    output = options.output
    
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
    
    if debug:
#        debughandler = logging.FileHandler(os.path.basename(__file__).replace('.py', '-debug.txt'), 'w', encoding='utf-8')
        debughandler = logging.StreamHandler(sys.stdout)
        debughandler.setLevel(logging.DEBUG)
        debugformatter = logging.Formatter("%(module)8.8s.%(funcName)20.20s%(levelname)10.10s\t%(message)s")
        debughandler.setFormatter(debugformatter)
        log.addHandler(debughandler)
    else:
        pass

    log.debug("input file: %s" % input)
        
    #initialize transformation object
    pathfinder = AStarPathfinder(input)
    
    #perform transformation
    path = pathfinder.findPath()
    
    #add path to input
    
#    DitaTools.Tree.File.Dita.write_tree_to_file(transformer.tree, output)
    