"""Generators are used to generate operands"""

import lxml.etree, logging
import Tree.Tree, Element.Element


class Operand:
    """An operand is used to operate on a tree in order to change or transform
    that tree"""
    
    def __init__(self):
        self.tree = lxml.etree.fromstring('<_/>')    #the operand tree, in lxml.etree._ElementTree form
        self.file = None                             #the file that the operand tree resides in, if any. 
        #distance? Metrics? 
        
        
        
class RenameGenerator:
    """Generate a rename operand"""
    def __init__(self):       
        self.log = logging.getLogger()
        
        
    def generateOperand(self, targetElement, tag):
        """Generate an operand for the targetElement and tag"""

        #note that this method creates the operand tree, but indirectly. 
        #Usually, if we want A + B = C, we use C - A = B to find B. But in 
        #this case, A and C are full trees, and we don't know what C is. 
        #The method used here builds the operand, B, directly which avoids finding 
        #the full trees and saves time and headaches.    
        
        operand = Operand()
        #get target element position
        targetposition = Element.Element.position(targetElement) 
        #build unit nodes down to position. Recall that the position list always starts with 1
        current = operand.tree
        for entry in targetposition[1:]:
            for i in range(0, entry):
                new = lxml.etree.Element('_') 
                current.append(new)
            current = new
        #operand.tree is now a tree of unit nodes down to the target. The last unit
        #node in the tree, i.e. the last appended, i.e current, is at the targetElement
        #position. Therefore, change current into the rename node
        renamenode = Element.Element.add(lxml.etree.Element(tag), Element.Element.invert(lxml.etree.Element(targetElement.tag, targetElement.attrib)))
        current.tag = renamenode.tag
        for a in renamenode.attrib.keys():
            current.attrib[a] = renamenode.attrib[a]
        #done
        return operand
    
    
    
    
class RenameGeneratorIterator(RenameGenerator):
    """An iterator class for generating rename operands. This used the same 
    generating functions as the RenameGenerator class"""
    
    def __init__(self, targetElement, acceptableTags):       
        self.log = logging.getLogger() 
        if not isinstance(self.targetElement, lxml.etree._Element):
            self.log.warning('targetElement must be lxml.etree._Element object, aborting')
            #raise StopIteration #?
            return None
        elif isinstance(self.acceptableTags, list):
            self.log.warning('acceptableTags must be list object, aborting')
            #raise StopIteration #?
            return None
        else:
            pass
        self.targetElement = targetElement
        self.acceptableTags = acceptableTags
        self.index = 0
    
        
    def __next__(self):
        """Generate and return a rename operand. This function can be used for iteration
        over the accpetableTags list"""
        if self.index >= len(self.acceptableTags): 
            self.log.debug('no more renames to generate')
            raise StopIteration
        operand = self.generateOperand(self.targetElement, self.acceptableTags[self.index])
        self.index += 1
        return operand
        