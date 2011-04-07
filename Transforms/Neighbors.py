"""Functions to find the neighbors of a tree. Allowed operations are defined here"""

def findNeighbors_FirstValidationError(sourcetree):
    """Find Neighbors by fixing the first validation error. 
    
    Neighbors are defined as a tree that can be reached by some operation
    on the source tree. (this means any tree, in effect). 
    
    The first validation error is the first error in the list created by a 
    validator. By fixing this first error, we find neighbors that are the 
    result of fixing the first invalid element in the tree. """
    
    pass



#===============================================================================
# Start Operation definitions
#
# The following functions examine the source tree and generate an operand to 
# perform the desired operation. The target element is the element being modified, 
# e.g. the element that generated the first validation error. For example, the 
# Rename operation needs both the source tree and the target element because it 
# needs to know which element to rename (it cannot rename the whole tree) but the
# operand it generates is applied to the entire tree. 
#
#===============================================================================

def Rename(sourcetree, targetelement):
    pass


def Unwrap():
    pass

def Wrap():
    pass

def InsertBefore():
    pass

def AppendBefore():
    pass
