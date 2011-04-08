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
                operand = Tree.Tree.add(lxml.etree.fromstring('<dita/>'), Tree.Tree.invert(lxml.etree.Element(self.targetelement.tag, self.targetelement.attrib))) 
                return [operand]
            else:
                return None
        
        operands = []
        #get target element position
        targetposition = Element.Element.position(self.targetelement) 
        #for each suggested name
        for name in suggestedrenames:
            #apply to target element:
            #build unit nodes down to position. Recall that the position list always starts with 1
            operand = lxml.etree.fromstring('<_/>')
            current = operand
            for entry in targetposition[1:]:
                for i in range(0, entry):
                    new = lxml.etree.Element('_') 
                    current.append(new)
                current = new
            #after building all the unit nodes, the last unit node built (current) is the one 
            #we targets the target element, the one we want to operate on. Therefore, change current
            #into the rename node
            renamenode = Element.Element.add(lxml.etree.Element(name), Element.Element.invert(lxml.etree.Element(self.targetelement.tag, self.targetelement.attrib)))
            current.tag = renamenode.tag
            for a in renamenode.attrib.keys():
                current.attrib[a] = renamenode.attrib[a]
            operands.append(operand)
            
            #note that this method creates the operand tree, but indirectly. 
            #Usually, if we want A + B = C, we use C - A = B to find B. But in 
            #this case, A and C are full trees, and we don't know what C is. 
            #The method used here builds the operand, B, directly which avoids finding 
            #the full trees and saves time and headaches.              
    
        return operands
    

    def parseErrorMessage(self):
        
        pattern = r'.*?\:\d*\:\d*:ERROR:VALID:DTD_CONTENT_MODEL: Element (.*?) content does not follow the DTD, expecting \((.*?)\)\+, got \((.*?)\)'
        self.log.debug('testing pattern: %s' % str(pattern))
        match = re.search(pattern, self.errormessage)
        if match:
            self.log.debug('matched pattern')
            #we need to massage the suggested renames, which is group 2. Group 2 may turn out to be 
            #quite complicated, but the goal is always the same: build a list of tags that the
            #target element should be changed to. 
            acceptabletags = match.group(2).split(',')
            #childlist appears in the error message and is a list of elements that appear beneath the 
            #parent of the target element, in order. 
            childlist = match.group(3).split(' ')
            
            #remove superfluous entries from the acceptabletags.
            #going over the childlist and checking against the acceptabletags
            #will remove suggested tags we don't need, i.e. ones that already appear beneath the
            #parent of self.targetelement in the correct place. 
            for index, entry in enumerate(childlist):
                try:
                    if acceptabletags[index].find(entry) != -1: 
                        del acceptabletags[index]
                        continue
                    else:
                        break
                except: 
                    break
                
            #at this point, it may be useful to separate entries that have a trailing ? or * from
            #those that don't, and assign a different cost to each. We ignore this for now.  
            suggestedrenames = []
            for index, entry in enumerate(acceptabletags):
                for i in ['?', '*', '(', ')']: acceptabletags[index] = acceptabletags[index].replace(i, '')
                acceptabletags[index] = acceptabletags[index].replace('|', ',')
                suggestedrenames += [i.strip() for i in entry.split('|')]
     
            self.log.debug('found suggested renames: %s' % str(suggestedrenames))
            return suggestedrenames
    
        #else
        return []
    
    
    
    
    
    

def Unwrap():
    pass


def Wrap():
    pass


def InsertBefore():
    pass


def AppendBefore():
    pass
