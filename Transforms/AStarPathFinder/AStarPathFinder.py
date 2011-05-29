"""Transform a tree into dita using an adapted A* pathfinding algorithm"""


import logging, lxml.etree, sys, optparse, re, copy, os.path, tempfile, shutil

import DitaTools.Tree.File.Dita

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import Tree.Tree, Element.Element, Neighbors



#===============================================================================
# #classes
#===============================================================================

class AStarPathFinder:
    """A class that carries out the A* pathfinding algorithm. .
    
    The A* pathfinding algorithm is commonly used in video games to find 
    paths for NPCs, etc. It can be used on trees as well, since the functions
    defined in the Tree.Tree module define a group, a metric, addition, etc, 
    which are what the pathfinding algorithm uses. 
    
    There are some differences, however. The main one is that this pathfinding 
    algorithm finds a path, and it is a series of operands that can be added to 
    the tree to get dita. The path can be thought of as these operands all in 
    order, or a single operand consisiting of all the operands added together. 
    This is thanks to the fact that tree addition is associative. 
    
    So this can be thought of as a pathdinfer or a transformer, the transform
    being the operands all added together. I am going to use the word pathfinder, 
    since it copies a pathfinding algorithm.  """
    
    def __init__(self, file, tempdir=None):
        self.log = logging.getLogger()
        
        self.inputfile = file
        self.inputtree = lxml.etree.parse(self.inputfile)
        self.tempdir = tempdir
        
        self.start = Neighbors.Neighbor(self.inputtree)
        self.start.setGScore(0)
        self.start.setHScore(0)
        self.start.setFScore(0)
        self._openset = set([self.start])
        self.log.debug('self._openset: %s' % str(self._openset))
        
        self._closedset = set()
        self.log.debug('self._closedset: %s' % str(self._closedset))
        
        #step number is used to keep track of the process. 
        self.stepnumber = 0
        
    def findPath(self):
        
        while len(self._openset) > 0:
            #get member of open set with lowest fscore
            t = self.findLowestFscore()
            self.log.debug('lowest FScore: %s' % str(t))
            self.log.debug('tree: %s' % lxml.etree.tostring(t.getTree()))
            
            if self.tempdir is not None:
                steptrackingout = open(os.path.join(self.tempdir, str(self.stepnumber) + '.xml'), 'wb')
                steptrackingout.write(lxml.etree.tostring(t.getTree()))
                steptrackingout.close() 
            
            
            #check if t is dita
            errors = DitaTools.Tree.File.Dita.v11_validate(t.getTree())
            if len(errors) == 0:
                #if t is dita, the algorithm is complete.
    #            finalOperand = self.backTrackBuildOperand(self, t)
    #            return finalOperand
                self.log.debug('transformation complete')
                return t.getTree()
            
            
            #remove t from openset
            self._removeFromOpenSet(t)
            
            #add t to closed set
            self._addToClosedSet(t)
            
            #process neighbors of t
            self.processNeighbors(t)
            
            self.stepnumber += 1
        
        self.log.debug('transformation failed')
        return False
    
    
    
    def processNeighbors(self, t):
        #process the neighbors of t - find them, add to openset if necessary, 
        #calculate scores, etc. Note that t itself is an instance of the Neighbors.Neighbor class
        self.log.debug('processing neighbors of %s' % str(t))
        neighbors = Neighbors.findNeighbors_FirstValidationError(t)
        self.log.debug('found %i neighbors' % len(neighbors))
        
        for n in neighbors: 
            self.log.debug('\t%s' % str(n))
            
            #if n in closed set, continue
            if self._inClosedSet(n): 
                self.log.debug('\tin closed set, continue')
                continue
            
            
            #because of the program flow and the way neighbors are generated, two neighbor 
            #objects could represent the same tree, ie the same point in tree space. 
            #This must be dealt with. 
            #Get the member in the openset that matches n, if any
            oMember = self._inOpenSet(n)
            if oMember is False:
                pass
            else:
                #otherwise replace n. 
                del n
                n = oMember
            
            
            #get tentativeGScore = n.getGScore() + Tree.Tree.metric(t, n)
            tentativeGScore = t.getGScore() + Tree.Tree.metric(n.getTree(), t.getTree())
            self.log.debug('\ttentative gscore: %s' % str(tentativeGScore))
            
         
            if oMember is False:
                self.log.debug('\tnot in open set, adding to open set')
                self._addToOpenSet(n)
                tentativeIsBetter = True
            elif tentativeGScore < n.getGScore(): #if n is in the openset, it already has a GScore
                tentativeIsBetter = True
            else:
                tentativeIsBetter = False
                
                
            if tentativeIsBetter is True: 
                self.log.debug('tentative is better')
                n.setCameFrom(t)
                n.setGScore(tentativeGScore)
                n.setHScore(len(DitaTools.Tree.File.Dita.v11_validate(n.getTree())))
                n.setFScore(n.getGScore() + n.getHScore())
                
                #update closed and open set #?
            



    def findLowestFscore(self):
        """Find the element of the open set with the lowest fscore"""
        lowest = None
        for n in self._openset:
            if lowest is None:
                lowest = n
                continue
            
            if n.getFScore() < lowest.getFScore():
                lowest = n
                continue
            
        return lowest


    def _inClosedSet(self, x):
        #return True if x is in the closed set, False otherwise.
        inClosedSet = False
        for c in self._closedset:
            if Tree.Tree.equal(c.getTree(), x.getTree()):
                #then n is in closed set. 
                return c
        return False

    def _addToClosedSet(self, x):
        self._closedset.add(x)
    
#    def _removeFromClosedSet(self, x):
#        pass



    def _inOpenSet(self, x):
        #return True if x is in the open set, False otherwiseinOpenSet = False
        for o in self._openset:
            if Tree.Tree.equal(o.getTree(), x.getTree()):
                #then n is in closed set. 
                return o
        return False
        
    def _addToOpenSet(self, x):
        self._openset.add(x)
    
    def _removeFromOpenSet(self, x):
        self._openset.remove(x
                             )



    
#    def backTrackBuildOperand(self, x):
#        operand = copy.deepcopy(x.getOperandTree())
#        while x.getCameFrom() is not None:
#            x = x.getCameFrom()
#            Tree.Tree.add(operand, x.getOperandTree())
#        return operand

    
    
    


#===============================================================================
# main
#===============================================================================

if __name__ == "__main__":
    #called from a command line
    optparser=optparse.OptionParser()
    
    optparser.add_option("-i", "--input", type="string", dest="input", default='', 
    help="Path to the input file")
    optparser.add_option("-o", "--output", type="string", dest="output", default=None, 
    help="Path to the input file")
    optparser.add_option("--debug", action="store_true", dest="debug",
    help="Turn this on to activate debug logging.")
    optparser.add_option( "-t", "--tempdir", type="string", dest="tempdir", default=None, 
    help="path to the tempdir")
    
    (options, args) = optparser.parse_args()
    input = options.input
    debug = options.debug
    output = options.output
    tempdir = options.tempdir
    
    #this next block ensures that the user can pass the input as a positional
    #argument, without the -i
    try:
        input = args[0]
    except:
        pass
    
    if output is None:
        output = input + '.dita'
        
    if tempdir is None:
#        tempdir = tempfile.mkdtemp(prefix="AStarTransform-", dir=os.path.dirname(input))
        tempdir = os.path.join(os.path.dirname(input), 'AStarTransformTemp') 
        if os.path.exists(tempdir): shutil.rmtree(tempdir)
        os.mkdir(tempdir)
        
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




    #===========================================================================
    # #begin transformation
    #===========================================================================
    
    log.debug("transforming file: %s" % input)
        
    #initialize transformation object
    pathfinder = AStarPathFinder(input, tempdir)
    
    #perform transformation
    result = pathfinder.findPath()
    
    print(lxml.etree.tostring(result))
    
    #add path to input
    
#    DitaTools.Tree.File.Dita.write_tree_to_file(transformer.tree, output)
    