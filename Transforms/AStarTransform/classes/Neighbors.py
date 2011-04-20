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
        self.tree = None
        
    
    
    
    
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
       
    #apply operands to tree to get neighbors
    neighbors = []
    for  o in operands:
        neighbor = Neighbor()
        neighbor.tree = Tree.Tree.add(o.tree, sourcetree)
        log.debug('got neighbor: %s' % lxml.etree.tostring(neighbor.tree))
        neighbors.append(neighbor)

    #return neighbors.
    return neighbors
    
    



