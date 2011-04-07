"""Functions to find the neighbors of a tree. Allowed operations are defined here"""

import logging, lxml.etree, re

import Element.Element
import Tree.Tree

def findNeighbors_FirstValidationError(sourcetree):
    """Find Neighbors by fixing the first validation error. 
    
    Neighbors are defined as a tree that can be reached by some operation
    on the source tree. (this means any tree, in effect). 
    
    The first validation error is the first error in the list created by a 
    validator. By fixing this first error, we find neighbors that are the 
    result of fixing the first invalid element in the tree. """
    
    #validate
    #take first validation error
    #parse validation error
    #get target element
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

class RenameGenerator:
    def __init__(self):
        self.log = logging.getLogger()
    
    def generateRenameOperands(self, sourcetree, targetelement, errormessage):
        self.sourcetree = sourcetree
        self.targetelement = targetelement
        self.errormessage = errormessage
        
        #parse the error message for suggested names
        suggestedrenames = self.parseErrorMessage()
         
        if len(suggestedrenames) == 0:
            #if no names, and target element is root, generate rename to dita operand. Otherwise abort.    
            if self.sourcetree.getroot() is self.targetelement:
                operand = Tree.Tree.add(lxml.etree.fromstring('<dita/>'), lxml.etree.Element(self.targetelement.tag, self.targetelement.attrib)) 
                return [operand]
            else:
                return None
            
        #for each suggested name
            #apply to target element:
            #get target element position
            #build unit nodes down to position
            #add in rename node at target element
            
            #note that this method creates the operand tree, but indirectly. 
            #Usually, if we want A + B = C, we use C - A = B to find B. But in 
            #this case, A and C are full trees, and we don't know what C is. 
            #The method used here builds the operand, B, directly which avoids finding 
            #the full trees and saves time and headaches.              
        pass

    def parseErrorMessage(self):
        
        pattern = r'.*?\:\d*\:\d*:ERROR:VALID:DTD_CONTENT_MODEL: Element (.*?) content does not follow the DTD, expecting (.*?)\+, got \((.*?)\)'
        self.log.debug('testing pattern: %s' % str(pattern))
        match = re.search(pattern, self.errormessage)
        if match:
            self.log.debug('matched pattern')
            if not self.group(1) == self.targetelement.tag:
                #these should be equal. If not, it indicates a problem in the program flow somewhere upstream. 
                self.log.warning('tag name found in error message does not match target element')
                return False
            tags = [i.rstrip() for i in match.group(2).split('|')]
            self.log.debug('found suggested renames: %s' % str(tags))
            return suggestedrenames
        else: 
            return []
    
    
    
    
    
    

def Unwrap():
    pass


def Wrap():
    pass


def InsertBefore():
    pass


def AppendBefore():
    pass
