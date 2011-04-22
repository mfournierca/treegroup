"""Transform a tree into dita using an adapted A* pathfinding algorithm"""


import logging, lxml.etree, sys, optparse, re, copy

import DitaTools.Tree.File.Dita

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

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
    
    def __init__(self, file):
        self.inputfile = file
        self.inputtree = lxml.etree.parse(self.inputfile)
        
        self.start = 
        self.openset = set(lxml.etree.tostring(self.inputtree))
        self.closedset = set()
        
        
    def findPath(self):
        
        #get member of open set with lowest fscore
        t = self.findLowestFscore()
        
        #check if t is dita
        errors = DitaTools.Tree.File.Dita.v11_validate(t)
        if len(errors) = 0:
            #if t is dita, the algorithm is complete.
            finalOperand = self.backTrackBuildOperand(self, t)
            return finalOperand
        
        #remove t from openset
        
        #add t to closed set
        
        #process neighbors of t
        self.processNeighbors(t)
        
        pass
    
    
    def processNeighbors(self, t):
        #process the neighbors of t - find them, add to openset if necessary, 
        #calculate scores, etc. 
        neighbors = Neighbors.findNeighbors_FirstValidationError(t)
        pass

    def findLowestFscore(self):
        """Find the element of the open set with the lowest fscore"""
        pass


    def backTrackBuildOperand(self, x):
        pass





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
    
    if output == '':
        output = input + '.dita'
        
    
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
    pathfinder = AStarPathfinder(input)
    
    #perform transformation
    path = pathfinder.findPath()
    
    #add path to input
    
#    DitaTools.Tree.File.Dita.write_tree_to_file(transformer.tree, output)
    