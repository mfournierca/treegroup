#!/usr/bin/env python3

"""appendbefore generators are used to generate appendbefore operands"""

import lxml.etree, logging, copy
import Tree.Tree, Element.Element

from . import Operand

import DitaTools.Element.Functions

    
class Generator:
    """Generate a appendbefore operand"""
    def __init__(self):       
        self.log = logging.getLogger()
        
        
    def generateOperand(self, targetElement):
        """Generate an operand for the targetElement"""
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.error('targetElement must be lxml.etree._Element object, is %s. Aborting' % str(targetElement))
            return None
        else:
            pass
        
        ##self.log.debug('Generating appendbefore operand for  %s' % str(targetElement))
        #self.log.debug('appendbefore to: %s' % tag)
        operand = self._generateOperand(Operand.Operand(targetElement), targetElement)
        #self.log.debug('Generated operand: %s' % str(operand))
        return operand
    
    
    def _generateOperand(self, operand, targetElement):        
            
#        self.log.debug('generating appendbefore operand')
#        self.log.debug('targetElement: %s' % targetElement)
        
        #if no preceding sibling or if target is root, return None
        if operand.getTarget().getparent() is None:
            #the target is the root
#            self.log.debug('target element is root, cannot generate operand')
            return None
        elif operand.getTarget().getprevious() is None:
#            self.log.debug('target element has no preceding sibling, cannot generate operand')
            return None
        
        #copy, invert and set the target element
        operand.setTarget(Tree.Tree.invert(copy.deepcopy(targetElement)))
        
        #invert siblings
        for sibling in targetElement.itersiblings():
            operand.getTarget().getparent().append(Tree.Tree.invert(copy.deepcopy(sibling)))

        #for children of previous sibling, append unit to previous sibling in operand. 
        for i in range(len(targetElement.getprevious())):
            operand.getTarget().getprevious().append(lxml.etree.Element('_'))
            
        #append target to previous sibling in operand 
        operand.getTarget().getprevious().append(copy.deepcopy(targetElement))
        
        #add siblings
        index = DitaTools.Element.Functions.get_index(targetElement)
        for sibling in targetElement.itersiblings():
            if len(operand.getTarget().getparent()) > index:
                #self.log.debug('\tadding sibling %s at index %i' % (str(sibling), index))
                Tree.Tree.add(operand.getTarget().getparent()[index], sibling)
            else:
                #if you don't copy the sibling, it gets moved out of the target tree and into the operand, which may cause problems
                #depending on what the user is doing. This function should not alter the target tree (that the user passes), 
                #it should only create an operand. Therefore make a copy of the sibling before adding it to the operand, so that 
                #the target tree does not change.
                #self.log.debug('\tindex is %i, parent length is %i, appending sibling' % (index, len(operand.getTarget().getparent())))
                operand.getTarget().getparent().append(copy.deepcopy(sibling))
            index += 1
            
        
        #self.log.debug('Generated appendbefore operand: %s\tTarget: %s' % (str(operand), operand.getTarget()))
        #done
        return operand
    
    
    
class Iterator(Generator):
    """An iterator class for generating appendbefore operands. This used the same 
    generating functions as the appendbeforeGenerator class"""
    
    def __init__(self, targetElement):       
        self.log = logging.getLogger() 
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.error('targetElement must be lxml.etree._Element object, is %s. Aborting' % str(targetElement))
            #raise StopIteration #?
            return None
        else:
            pass
        self.targetElement = targetElement
        self.index = 0
    
        
    def __iter__(self):
        return self
        
    def __next__(self):
        """Generate and return a appendbefore operand. This function can be used for iteration"""
        if self.index >= 1: 
            #self.log.debug('no more appendbefores to generate')
            raise StopIteration
        #if optimizing, you may want to copy the operand here instead of creating a new one each time. 
        operand = self._generateOperand(Operand.Operand(self.targetElement), self.targetElement)
        self.index += 1
        return operand