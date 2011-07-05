#!/usr/bin/env python3

"""Generators are used to generate operands"""

import lxml.etree, logging, copy
import Tree.Tree, Element.Element, Element.Text

from . import Operand        
        
        

#===============================================================================
# Wrap Generator
#===============================================================================


class Generator:
    """Generate a wrap text operand"""
    def __init__(self):
        self.log = logging.getLogger()
        pass
            
    def generateOperand(self, targetElement, tag):
        """Generate an operand for the targetElement and tag"""
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.error('targetElement must be lxml.etree._Element object, aborting')
            return None
        elif not isinstance(tag, str):
            self.log.error('tag must be str object, aborting')
            return None
        else:
            pass
        
        self.log.debug('Generating text wrap operand for  %s' % str(targetElement))
        self.log.debug('wrap in: %s' % tag)
        
        operand = self._generateOperand(Operand.Operand(targetElement), targetElement, tag)
        
        self.log.debug('created operand: %s' % str(operand))
        
        return operand
    
    def _generateOperand(self, operand, targetElement, tag):
        """generate the operand"""
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.warning('targetElement must be lxml.etree._Element object, aborting')
            return None
        elif not isinstance(tag, str):
            self.log.warning('tag must be str, is %s, aborting' % str(tag))
            return None
        else:
            pass
        
        #invert the element
        for i in targetElement:
            operand.getTarget().append(Tree.Tree.invert(copy.deepcopy(i)))
            
        operand.getTarget().text = Element.Text._textinverse(targetElement.text)
        
        #insert new element to operand target.
        newelement = lxml.etree.Element(tag)
        newelement.text = targetElement.text 
        
        queue = [newelement] + [copy.deepcopy(i) for i in targetElement]
        for index, e in enumerate(queue):
            if index < len(operand.getTarget()):
                Tree.Tree.add(operand.getTarget()[index], e)
            else:
                operand.getTarget().append(e)
                        
        return operand
    
    
    




class Iterator(Generator):
    """An iterator class for the wrap generator"""
    
    def __init__(self, targetElement, acceptableTags):       
        self.log = logging.getLogger() 
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.error('targetElement must be lxml.etree._Element object, aborting')
            #raise StopIteration #?
            return None
        elif not isinstance(acceptableTags, list):
            self.log.error('acceptableTags must be list object, aborting')
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
        """Generate and return a wrap operand. This function can be used for iteration
        over the accpetableTags list"""
        if self.index >= len(self.acceptableTags): 
            #self.log.debug('no more wraps to generate')
            raise StopIteration
        #if optimizing, you may want to copy the operand here instead of creating a new one each time. 
        operand = self._generateOperand(Operand.Operand(self.targetElement), self.targetElement, self.acceptableTags[self.index])
        self.index += 1
        return operand









