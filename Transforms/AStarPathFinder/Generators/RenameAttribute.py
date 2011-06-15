#!/usr/bin/env python3

"""Rename generators are used to generate rename operands"""

import lxml.etree, logging, copy
import Tree.Tree, Element.Element

from . import Operand


    
class Generator:
    """Generate a rename operand"""
    def __init__(self):       
        self.log = logging.getLogger()
        
        
    def generateOperand(self, targetElement, currentAttributeName, newAttributeName):
        """Generate an operand for the targetElement and tag"""
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.error('targetElement must be lxml.etree._Element object, is %s. Aborting' % str(targetElement))
            return None
        elif not isinstance(currentAttributeName, str):
            self.log.error('currentAttributeName must be str object, is %s. Aborting' % str(currentAttributeName))
            return None
        elif not isinstance(newAttributeName, str):
            self.log.error('newAttributeName must be str object, is %s. Aborting' % str(newAttributeName))
            return None
        else:
            pass
        
        operand = self._generateOperand(Operand.Operand(targetElement), targetElement, currentAttributeName, newAttributeName)
        return operand
    
    
    def _generateOperand(self, operand, targetElement, currentAttributeName, newAttributeName):        
        #generate the operand
        currentAttributeValue = targetElement.get(currentAttributeName)
        currentCopy = lxml.etree.Element('_', attrib={currentAttributeName: currentAttributeValue})
        Element.Element.invert(currentCopy)
        if (currentCopy.get(newAttributeName) is not None) or currentCopy.get(newAttributeName) == '':
            #problem - the new attribute already exists, and combining them is probably meaningless. 
            #Warn and return the unit. 
            self.log.warning('element %s; tried to rename attribute to %s, attribute with that name already exists. Skipping' % (str(targetElement), newAttributeName))
            return operand
        elif newAttributeName == '' or newAttributeName == '_':
            pass
        else:
            currentCopy.set(newAttributeName, currentAttributeValue)
        
        renameAttributeNode = currentCopy
        operand.setTarget(renameAttributeNode)
#        self.log.debug('Generated attributeRename operand: %s\tTarget: %s' % (str(operand), operand.getTarget()))
        return operand
    
    
    
class Iterator(Generator):
    """An iterator class for generating rename operands. This used the same 
    generating functions as the RenameGenerator class"""
    
    def __init__(self, targetElement, acceptableAttributes):       
        self.log = logging.getLogger() 
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.error('targetElement must be lxml.etree._Element object, is %s. Aborting' % str(targetElement))
            #raise StopIteration #?
            return None
        elif not isinstance(acceptableAttributes, list):
            self.log.error('acceptableAttributes must be list object, is %s. Aborting' % str(acceptableAttributes))
            #raise StopIteration #?
            return None
        else:
            pass
        self.targetElement = targetElement
        self.acceptableAttributes = acceptableAttributes
        self.index = 0
    
        
    def __iter__(self):
        return self
        
    def __next__(self):
        """Generate and return a rename operand. This function can be used for iteration
        over the accpetableTags list"""
        if self.index >= len(self.acceptableAttributes): 
            self.log.debug('no more renames to generate')
            raise StopIteration
        #if optimizing, you may want to copy the operand here instead of creating a new one each time. 
        operand = self._generateOperand(Operand.Operand(self.targetElement), self.targetElement, self.acceptableAttributes[self.index])
        self.index += 1
        return operand