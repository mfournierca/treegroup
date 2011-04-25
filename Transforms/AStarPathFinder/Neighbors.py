"""Functions to find the neighbors of a tree. Allowed operations are defined here"""

import logging, lxml.etree, re

import Element.Element
import Tree.Tree

from . import Errors

import Generators.Rename
import Generators.Unwrap
import Generators.Wrap


class Neighbor:
    def __init__(self):
        self.gscore = None
        self.hscore = None
        self.fscore = None
        self.camefrom = None
        
        self.dist = None
        
        self._tree = None
        self._operand = None
    
    
    #===========================================================================
    # accessor methods
    #===========================================================================
    
    #note: since the AStarPathFinder will be used to transform trees, 
    #we have to be able to handle large trees. Some documents get up to 
    #5 MB, with hundreds of elements - if we stored the full tree of each neighbor
    #in memory, we would reach GB quickly. Therefore, it will be necessary at some 
    #point to do something more clever, ie only store the operand and only
    #calculate the full neighbor tree when needed, or write the trees to disk 
    #and retrieve them when needed. 
    #If in the future it is necessary to do this, it should be done here by changing
    #the accessor methods to write or read to disk, or calculate the neighbor 
    #tree as needed. These accessor methods are already created, although rather 
    #simple at this point. But changing them in the future will not require changes
    #in any other part of the program. 
        
    def getOperandTree(self):
        return self._operand
    
    def setOperandTree(self, tree):
        self._operand = tree
    
    def getTree(self):
        return self._tree
    
    def setTree(self, tree):
        self._tree = tree
        
    
    
    
    
def findNeighbors_FirstValidationError(sourcetree):
    """Find Neighbors by fixing the first validation error. 
    
    Neighbors are defined as a tree that can be reached by some operation
    on the source tree. (this means any tree, in effect). 
    
    The first validation error is the first error in the list created by a 
    validator. By fixing this first error, we find neighbors that are the 
    result of fixing the first invalid element in the tree. """
    
    log = logging.getLogger()
    
    #Error parser
    errorParser = Errors.ErrorParser(sourcetree)
    errorParser.parse()
    
    #get operands
    log.debug('finding operands')
    operands = []
    for o in Generators.Rename.Iterator(errorParser.targetElement, errorParser.acceptableTags):
        operands.append(o)
    
    for o in Generators.Wrap.Iterator(errorParser.targetElement, errorParser.acceptableTags):
        operands.append(o)
        
    for o in Generators.Unwrap.Iterator(errorParser.targetElement):
        operands.append(o)
       
    #apply operands to tree to get neighbors
    log.debug('creating neighbors')
    neighbors = []
    for  o in operands:
        neighbor = Neighbor()
#        neighbor.operand = copy.deepcopy(o.tree)
        neighbor.setTree(Tree.Tree.add(o.getTree(), sourcetree))
        log.debug('\tneighbor: %s' % lxml.etree.tostring(neighbor.getTree()))
        neighbors.append(neighbor)
        
    #return neighbors.
    return neighbors
    
    



