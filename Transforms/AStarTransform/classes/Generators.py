#!/usr/bin/env python3

"""Generators are used to generate operands"""

import lxml.etree, logging, copy
import Tree.Tree, Element.Element

import DitaTools.Element.Functions

class Operand:
    """An operand is used to operate on a tree in order to change or transform
    that tree"""
    
    def __init__(self, targetElement):
        """Initialize the operand. Create the operand tree, targetElement, position"""
        #distance? Metrics? 
        self.file = None                             #the file that the operand tree resides in, if any.
        
        self.targetPosition = Element.Element.position(targetElement)
        
        self.tree = lxml.etree.fromstring('<_/>')    #the operand tree, in lxml.etree._ElementTree form
        #build unit nodes down to position. Recall that the position list always starts with 1
        current = self.tree
        for entry in self.targetPosition[1:]:
            for i in range(0, entry):
                new = lxml.etree.Element('_') 
                current.append(new)
            current = new
        #operand.tree is now a tree of unit nodes down to the target. The last unit
        #node in the tree, i.e. the last appended, i.e current, is at the targetElement
        #position. Therefore, this is the targetElement that the operand will try to change
        self.target = current
        
        
        
        
        
        

#===============================================================================
# Wrap Generator
#===============================================================================


class WrapGenerator:
    """Generate a wrap operand"""
    def __init__(self):
        self.log = logging.getLogger()
        pass
    
    
    def generateOperand(self, targetElement, tag):
        """generate the operand"""
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.warning('targetElement must be lxml.etree._Element object, aborting')
            return None
        else:
            pass
        
        self.log.debug('Generating wrap operand for  %s' % str(targetElement))
        operand = Operand(targetElement)
        self.log.debug('created operand: %s' % str(operand))
        
        #
        #create the operand
        #
        
        self.log.debug('operand tree: %s' % lxml.etree.tostring(operand.tree))
        self.log.debug('operand target: %s' % str(operand.target))
        self.log.debug('operand target parent: %s' % str(operand.target.getparent()))
        self.log.debug('tag: %s' % tag)
        
        #change operand.target to inverse of targetElement.
        inversetarget = Tree.Tree.invert(copy.deepcopy(targetElement))
        operand.target.getparent().replace(operand.target, inversetarget)
        operand.target = inversetarget
        
        #add the wrap element
        wrapElement = lxml.etree.Element(tag)
        Tree.Tree.add(operand.target, wrapElement)
        
        #append the target element to the new wrap element. 
        targetCopy = copy.deepcopy(targetElement)
        if len(operand.target) == 0:
            operand.target.append(targetCopy)
            self.log.debug('appended targetCopy to wrapElement')
        else:
            Tree.Tree.add(operand.target[0], targetCopy)
            self.log.debug('added targetCopy to wrapElement[0]')
            
        #done creating the operand
        self.log.debug('operand tree is: %s' % lxml.etree.tostring(operand.tree))
        self.log.debug('done')
        return operand
    
    
    







        
        
        
        
        


#===============================================================================
# #Unwrap Generator
#===============================================================================

class UnwrapGenerator:
    """Generate an unwrap operand"""
    def __init__(self):
        self.log = logging.getLogger()
        pass
    
    
    def generateOperand(self, targetElement):
        """generate the operand"""
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.warning('targetElement must be lxml.etree._Element object, aborting')
            return None
        else:
            pass
        
        self.log.debug('Generating unwrap operand for  %s' % str(targetElement))
        operand = Operand(targetElement)
        self.log.debug('created operand: %s' % str(operand))
        
        #
        #create the operand
        #
        
        self.log.debug('operand tree: %s' % lxml.etree.tostring(operand.tree))
        self.log.debug('operand target: %s' % str(operand.target))
        self.log.debug('operand target parent: %s' % str(operand.target.getparent()))
        
        #change operand.target to inverse of targetElement.
        inversetarget = Tree.Tree.invert(copy.deepcopy(targetElement))
        operand.target.getparent().replace(operand.target, inversetarget)
        operand.target = inversetarget
        
        self.log.debug('inverted target, tree is: %s' % lxml.etree.tostring(operand.tree))
        
        #append invert of siblings to parent of operand.target 
        for sibling in targetElement.itersiblings():
            siblingcopy = copy.deepcopy(sibling)
            operand.target.getparent().append(Tree.Tree.invert(siblingcopy))
        
        self.log.debug('inverted siblings, tree is: %s' % lxml.etree.tostring(operand.tree))
            
        #add children of targetElement to parent of operand.target
        index = DitaTools.Element.Functions.get_index(targetElement)
        self.log.debug('adding target children.')
        self.log.debug('Target index is: %i. Target parent length is: %i' % (index, len(operand.target.getparent()))) 
        for child in targetElement:
            #if you don't copy the child, it gets moved out of the target tree and into the operand, which may cause problems
            #depending on what the user is doing. This function should not alter the target tree (that the user passes), 
            #it should only create an operand. Therefore make a copy of the child before adding it to the operand, so that 
            #the target tree does not change. 
            child = copy.deepcopy(child)
            if len(operand.target.getparent()) > index:
                Tree.Tree.add(operand.target.getparent()[index], child)
                self.log.debug('\tadded child %s at index %i' % (str(child), index))
            else:
                operand.target.getparent().append(child)
                self.log.debug('\tindex is %i, parent length is %i, appended child %s' % (index, len(operand.target.getparent()), str(child)))
            index += 1

        self.log.debug('added target children, tree is: %s' % lxml.etree.tostring(operand.tree))

        #add sibling trees of targetElement to operand.target
        self.log.debug('adding target siblings')
        self.log.debug('Index is: %i. Target parent length is: %i' % (index, len(operand.target.getparent())))
        for sibling in targetElement.itersiblings():
            #if you don't copy the sibling, it gets moved out of the target tree and into the operand, which may cause problems
            #depending on what the user is doing. This function should not alter the target tree (that the user passes), 
            #it should only create an operand. Therefore make a copy of the sibling before adding it to the operand, so that 
            #the target tree does not change. 
            sibling = copy.deepcopy(sibling)
            if len(operand.target.getparent()) > index:
                self.log.debug('\tadding sibling %s at index %i' % (str(sibling), index))
                Tree.Tree.add(operand.target.getparent()[index], sibling)
            else:
                self.log.debug('\tindex is %i, parent length is %i, appending sibling' % (index, len(operand.target.getparent())))
                operand.target.getparent().append(sibling)
            index += 1
            
        self.log.debug('added target siblings, tree is: %s' % lxml.etree.tostring(operand.tree))
        
        self.log.debug('done')
        return operand
    
    
    













#===============================================================================
# #Rename Generators    
#===============================================================================
    
class RenameGenerator:
    """Generate a rename operand"""
    def __init__(self):       
        self.log = logging.getLogger()
        
        
    def generateOperand(self, targetElement, tag):
        """Generate an operand for the targetElement and tag"""
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.warning('targetElement must be lxml.etree._Element object, aborting')
            return None
        elif not isinstance(tag, str):
            self.log.warning('tag must be str object, aborting')
            return None
        else:
            pass
        
        self.log.debug('Generating rename operand for  %s' % str(targetElement))
        self.log.debug('Rename to: %s' % tag)
        self.operand = Operand(targetElement)
        self.log.debug('created operand: %s' % str(self.operand))
        self._generateOperand(self.operand, targetElement, tag)
        return self.operand
    
    
    def _generateOperand(self, operand, targetElement, tag):        

        #note that this method creates the operand tree, but indirectly. 
        #Usually, if we want A + B = C, we use C - A = B to find B. But in 
        #this case, A and C are full trees, and we don't know what C is. 
        #The method used here builds the operand, B, directly which avoids finding 
        #the full trees and saves time and headaches.    
        self.log.debug('generating rename operand tree')
        self.log.debug('targetElement: %s' % targetElement)
        self.log.debug('rename to: %s' % tag)
        renamenode = Element.Element.add(lxml.etree.Element(tag), Element.Element.invert(lxml.etree.Element(targetElement.tag, targetElement.attrib)))
        operand.target.tag = renamenode.tag
        for a in renamenode.attrib.keys():
            operand.target.attrib[a] = renamenode.attrib[a]
        self.log.debug('result: %s' % lxml.etree.tostring(operand.tree))
        #done
    
    
    
    
class RenameGeneratorIterator(RenameGenerator):
    """An iterator class for generating rename operands. This used the same 
    generating functions as the RenameGenerator class"""
    
    def __init__(self, targetElement, acceptableTags):       
        self.log = logging.getLogger() 
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.warning('targetElement must be lxml.etree._Element object, aborting')
            #raise StopIteration #?
            return None
        elif not isinstance(acceptableTags, list):
            self.log.warning('acceptableTags must be list object, aborting')
            #raise StopIteration #?
            return None
        else:
            pass
        self.targetElement = targetElement
        self.acceptableTags = acceptableTags
        self.index = 0
    
        
    def __iter__(self):
        return self
        
    def __next__(self):
        """Generate and return a rename operand. This function can be used for iteration
        over the accpetableTags list"""
        if self.index >= len(self.acceptableTags): 
            self.log.debug('no more renames to generate')
            raise StopIteration
        #if optimizing, you may want to copy the operand here instead of creating a new one each time. 
        operand = Operand(self.targetElement)
        self._generateOperand(operand, self.targetElement, self.acceptableTags[self.index])
        self.index += 1
        return operand
        