"""Functions to find the neighbors of a tree. Allowed operations are defined here"""

import logging, lxml.etree, re

import Element.Element
import Tree.Tree

from . import Errors, Generators

def findNeighbors_FirstValidationError(sourcetree):
    """Find Neighbors by fixing the first validation error. 
    
    Neighbors are defined as a tree that can be reached by some operation
    on the source tree. (this means any tree, in effect). 
    
    The first validation error is the first error in the list created by a 
    validator. By fixing this first error, we find neighbors that are the 
    result of fixing the first invalid element in the tree. """
    
    neighbors = []
    
    #Error parser
    errorParser = Errors.ErrorParser(tree)
    errorParser.parse()
    
    #get operands
    
    #apply operands
    
    #return neighbors.
    
    



