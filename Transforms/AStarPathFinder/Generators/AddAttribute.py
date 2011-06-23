#!/usr/bin/env python3

"""Rename generators are used to generate rename operands"""

import lxml.etree, logging, copy
import Tree.Tree, Element.Element

from . import Operand


    
class Generator:
    """Generate a rename operand"""
    def __init__(self):       
        self.log = logging.getLogger()
        
        
    def generateOperand(self, targetElement, newAttributeName):
        """Generate an operand for the targetElement and tag"""
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.error('targetElement must be lxml.etree._Element object, is %s. Aborting' % str(targetElement))
            return None
        elif not isinstance(newAttributeName, str):
            self.log.error('newAttributeName must be str object, is %s. Aborting' % str(newAttributeName))
            return None
        else:
            pass
        
        operand = self._generateOperand(Operand.Operand(targetElement), targetElement, newAttributeName)
        return operand
    
    
    def _generateOperand(self, operand, targetElement, newAttributeName):        
        #generate the operand
        if newAttributeName == 'id':
            #just assign a random number
            import random
            newAttributeValue = str(int(random.random() * 10000000000))
        else:
            newAttributeValue = 'defaultSetInAddAttributeGenerator'
        addAttributeNode = lxml.etree.Element('_', attrib={newAttributeName: newAttributeValue})
        operand.setTarget(addAttributeNode)
#        self.log.debug('Generated addAttribute operand: %s\tTarget: %s' % (str(operand), operand.getTarget()))
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