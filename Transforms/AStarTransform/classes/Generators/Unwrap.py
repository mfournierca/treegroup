#!/usr/bin/env python3

"""Generators are used to generate operands"""

import lxml.etree, logging, copy
import Tree.Tree, Element.Element

import DitaTools.Element.Functions

from . import Operand
        


class Generator:
    """Generate an unwrap operand"""
    def __init__(self):
        self.log = logging.getLogger()
        pass
    
    
    def generateOperand(self, targetElement):
        """Generate an operand for the targetElement and tag"""
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.warning('targetElement must be lxml.etree._Element object, aborting')
            return None
        else:
            pass
        
        self.log.debug('Generating unwrap operand for  %s' % str(targetElement))
#        self.log.debug('created operand: %s' % str(self.operand))
        operand = self._generateOperand(Operand.Operand(targetElement), targetElement)
        return operand
    
    
    
    def _generateOperand(self, operand, targetElement):
        """generate the operand"""
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.warning('targetElement must be lxml.etree._Element object, aborting')
            return None
        else:
            pass
        
#        self.log.debug('Generating unwrap operand for  %s' % str(targetElement))
#        operand = Operand.Operand(targetElement)
#        self.log.debug('created operand: %s' % str(operand))
        
        #
        #create the operand
        #
        
        self.log.debug('operand tree: %s' % lxml.etree.tostring(operand.tree))
        self.log.debug('operand target: %s' % str(operand.target))
        self.log.debug('operand target parent: %s' % str(operand.target.getparent()))
        
        #change operand.target to inverse of targetElement.
        inversetarget = Tree.Tree.invert(copy.deepcopy(targetElement))
        if operand.target.getparent() is None:
            #the target is the root
            if len(targetElement) > 1: 
                #the target is the root and has more than one child - cannot unwrap
                self.log.debug('target is root and has more than one child, cannot unwrap')
                return None
            elif len(targetElement) == 0: 
                #the target is the root and has no child - cannot unwrap
                self.log.debug('target is root and has no child, cannot unwrap')
                return None
            operand.target = inversetarget
            operand.tree = operand.target
        else:
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
        self.log.debug('Target index is: %s. Target parent length is: %s' % (str(index), str(None) if operand.target.getparent() is None else str(len(operand.target.getparent())))) 
        for child in targetElement:
            #if you don't copy the child, it gets moved out of the target tree and into the operand, which may cause problems
            #depending on what the user is doing. This function should not alter the target tree (that the user passes), 
            #it should only create an operand. Therefore make a copy of the child before adding it to the operand, so that 
            #the target tree does not change. 
            child = copy.deepcopy(child)
            if operand.target.getparent() is None and len(operand.target) > 1:
                #cannot do this. This was already dealt with above.
                pass
            elif operand.target.getparent() is None and len(operand.target) <= 1:
                Tree.Tree.add(operand.target, child)
                self.log.debug('\ttarget is root, added single child')
                break
            elif len(operand.target.getparent()) > index:
                Tree.Tree.add(operand.target.getparent()[index], child)
                self.log.debug('\tadded child %s at index %i' % (str(child), index))
            else:
                operand.target.getparent().append(child)
                self.log.debug('\tindex is %i, parent length is %i, appended child %s' % (index, len(operand.target.getparent()), str(child)))
            index += 1

        self.log.debug('added target children, tree is: %s' % lxml.etree.tostring(operand.tree))

        #add sibling trees of targetElement to operand.target
        self.log.debug('adding target siblings')
        self.log.debug('Target index is: %s. Target parent length is: %s' % (str(index), str(None) if operand.target.getparent() is None else str(len(operand.target.getparent()))))
        for sibling in targetElement.itersiblings():
            #if you don't copy the sibling, it gets moved out of the target tree and into the operand, which may cause problems
            #depending on what the user is doing. This function should not alter the target tree (that the user passes), 
            #it should only create an operand. Therefore make a copy of the sibling before adding it to the operand, so that 
            #the target tree does not change.
            if operand.target.getparent() is None:
                #the target is the root and has no children
                break 
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
    
    
    









class Iterator(Generator):
    """An iterator class for the unwrap generator"""
    
    def __init__(self, targetElement):       
        self.log = logging.getLogger() 
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.warning('targetElement must be lxml.etree._Element object, aborting')
            #raise StopIteration #?
            return None
        else:
            pass
        self.targetElement = targetElement
        self.index = 0
    
        
    def __iter__(self):
        return self


    def __next__(self):
        """Generate and return a unwrap operand. This function can be used for iteration"""
        if self.index >= 1:
            #there is only 1 unwrap operand that can be generated, obviously. So this iterator
            #iterates once, and then stops. Not strictly necessary, but designed to be consistent
            #with the other generators, which do need iterators. 
            self.log.debug('no more unwraps to generate')
            raise StopIteration 
        operand = self._generateOperand(Operand.Operand(self.targetElement), self.targetElement)
        self.index += 1
        #the unwrap generator sometimes returns None
        if operand is None: self.__next__()
        return operand

