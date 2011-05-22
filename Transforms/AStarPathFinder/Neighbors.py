"""Functions to find the neighbors of a tree. Allowed operations are defined here"""

import logging, lxml.etree, re

import Element.Element
import Tree.Tree

import Errors

import Generators.Rename
import Generators.Unwrap
import Generators.Wrap


class Neighbor:
    def __init__(self, tree):
        self._gscore = None
        self._hscore = None
        self._fscore = None
        self._camefrom = None
        
#        self.dist = None
        
        self._tree = None
        self.setTree(tree)
#        self._operand = None
    
    
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
        
#    def getOperandTree(self):
#        """Return the operand tree of this neighbor, ie the operand that when added to the
#        camefrom tree creates this neighbor tree. There is no guarantee that any changes
#        made on the return tree will persist, to guarantee that, use the setOperandTree() method."""
#        return self._operand
#    
#    def setOperandTree(self, tree):
#        """Set the operand tree"""
#        self._operand = tree
    
    
    def getTree(self):
        """Return the tree of this neighbor. There is no guarantee that any changes made on the 
        returned tree will persist - to guarantee that, use the setTree() method"""
        return self._tree
    
    def setTree(self, tree):
        """Set the neighbor tree."""
        self._tree = tree
        
        
    def setCameFrom(self, x):
        self._camefrom = x
        
    def getCameFrom(self):
        return self._camefrom
    
    
    def setGScore(self, g):
        self._gscore = g
    
    def getGScore(self):
        return self._gscore
    
    
    def setHScore(self, h):
        self._hscore = h
        
    def getHScore(self):
        return self._hscore
    
    
    def setFScore(self, f):
        self._fscore = f
        
    def getFScore(self):
        return self._fscore
    
    
    def setCameFrom(self, c):
        self._camefrom = c 
    
    def getCameFrom(self):
        return self._camefrom
    
    
def findNeighbors_FirstValidationError(n):
    """Find Neighbors by fixing the first validation error. 
    
    Neighbors are defined as a tree that can be reached by some operation
    on the source tree. (this means any tree, in effect). 
    
    The first validation error is the first error in the list created by a 
    validator. By fixing this first error, we find neighbors that are the 
    result of fixing the first invalid element in the tree. """
    
    log = logging.getLogger()
    
    #Error parser
    errorParser = Errors.ErrorParser(n.getTree())
    errorParser.parse()
    
    #get operands
    log.debug('finding operands')
    operands = []
    iterator = Generators.Rename.Iterator(errorParser.targetElement, errorParser.acceptableTags)
    for o in iterator:
        operands.append(o)
    
    iterator = Generators.Wrap.Iterator(errorParser.targetElement, errorParser.acceptableTags)
    for o in iterator:
        operands.append(o)
        
    iterator = Generators.Unwrap.Iterator(errorParser.targetElement)
    for o in iterator:
        operands.append(o)
       
    #apply operands to tree to get neighbors
    log.debug('creating neighbors')
    neighbors = []
    for  o in operands:
        neighbor = Neighbor(Tree.Tree.add(o.getTree(), n.getTree()))
        log.debug('\tneighbor: %s' % lxml.etree.tostring(neighbor.getTree()))
        neighbors.append(neighbor)
        
    #return neighbors.
    return neighbors
    
    



