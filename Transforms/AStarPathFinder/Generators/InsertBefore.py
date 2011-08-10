#!/usr/bin/env python3

"""insertbefore generators are used to generate insertbefore operands"""

import lxml.etree, logging, copy
import Tree.Tree, Element.Element

from . import Operand

import DitaTools.Element.Functions

    
class Generator:
    """Generate a insertbefore operand"""
    def __init__(self):       
        self.log = logging.getLogger()
        
        
    def generateOperand(self, targetElement, tag):
        """Generate an operand for the targetElement and tag"""
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.error('targetElement must be lxml.etree._Element object, is %s. Aborting' % str(targetElement))
            return None
        elif not isinstance(tag, str):
            self.log.error('tag must be str object, is %s. Aborting' % str(tag))
            return None
        else:
            pass
        
        ##self.log.debug('Generating insertbefore operand for  %s' % str(targetElement))
        #self.log.debug('insertbefore to: %s' % tag)
        operand = self._generateOperand(Operand.Operand(targetElement), targetElement, tag)
#        self.log.info('Generated operand: %s' % str(operand))
        return operand
    
    
    def _generateOperand(self, operand, targetElement, tag):        

        #note that this method creates the operand tree, but indirectly. 
        #Usually, if we want A + B = C, we use C - A = B to find B. But in 
        #this case, A and C are full trees, and we don't know what C is. 
        #The method used here builds the operand, B, directly which avoids finding 
        #the full trees and saves time and headaches.    
        #self.log.debug('generating insertbefore operand')
        #self.log.debug('targetElement: %s' % targetElement)
        #self.log.debug('insertbefore: %s' % tag)
        
        if targetElement.getparent() is None:
            #target is root
            return None
        
        #copy, invert and set the target element
        operand.setTarget(Tree.Tree.invert(copy.deepcopy(targetElement)))
        
        #take inverse of siblings of target, append after target
        for sibling in targetElement.itersiblings():
            siblingcopy = copy.deepcopy(sibling)
            operand.getTarget().getparent().append(Tree.Tree.invert(siblingcopy))
            
        #add new element to target
        Element.Element.add(operand.getTarget(), lxml.etree.Element(tag))
        
        #add target after operand target
        index = DitaTools.Element.Functions.get_index(targetElement) + 1
        if len(operand.getTarget().getparent()) > index:
            Tree.Tree.add(operand.getTarget().getparent()[index], targetElement)
        else:
            operand.getTarget().getparent().append(copy.deepcopy(targetElement))
        index += 1
        
        #add siblings after operand target
        for sibling in targetElement.itersiblings():
            if operand.getTarget().getparent() is None:
                #the target is the root and has no siblings
                break 
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

        #self.log.debug('Generated insertbefore operand: %s\tTarget: %s' % (str(operand), operand.getTarget()))
        #done
        return operand
    
    
    
class Iterator(Generator):
    """An iterator class for generating insertbefore operands. This used the same 
    generating functions as the insertbeforeGenerator class"""
    
    def __init__(self, targetElement, acceptableTags):       
        self.log = logging.getLogger() 
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.error('targetElement must be lxml.etree._Element object, is %s. Aborting' % str(targetElement))
            #raise StopIteration #?
            return None
        elif not isinstance(acceptableTags, list):
            self.log.error('acceptableTags must be list object, is %s. Aborting' % str(acceptableTags))
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
        """Generate and return a insertbefore operand. This function can be used for iteration
        over the accpetableTags list"""
        if self.index >= len(self.acceptableTags): 
            #self.log.debug('no more insertbefores to generate')
            raise StopIteration
        #if optimizing, you may want to copy the operand here instead of creating a new one each time. 
        operand = self._generateOperand(Operand.Operand(self.targetElement), self.targetElement, self.acceptableTags[self.index])
        self.index += 1
        return operand