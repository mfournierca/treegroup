#!/usr/bin/env python3

"""Generators are used to generate operands"""

import lxml.etree, logging, copy
import Tree.Tree, Element.Element, Element.Text

from . import Operand        
        
        

#===============================================================================
# Wrap Generator
#===============================================================================


class Generator:
    """Generate a wrap tail operand"""
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
        
        self.log.debug('Generating tail wrap operand for  %s' % str(targetElement))
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
        
        #invert tail
        operand.getTarget().tail = Element.Text._textinverse(targetElement.tail)
        
        #invert following siblings
        targetindex = operand.getTarget().getparent().index(operand.getTarget())
        index = targetindex
        for sibling in targetElement.itersiblings():
            index += 1
            siblingcopy = copy.deepcopy(sibling)
            siblingcopy = Tree.Tree.invert(siblingcopy)
            operand.getTarget().getparent().insert(index, siblingcopy)
            
        #add wrap operand after target
        wrapElement = lxml.etree.Element(tag)
        wrapElement.text = targetElement.tail
        if targetindex + 1 >= len(operand.getTarget().getparent()):
            operand.getTarget().getparent().append(wrapElement)
        else:
            Tree.Tree.add(operand.getTarget().getparent()[targetindex + 1], wrapElement)
        
        #add siblings after wrap operand.
        index = targetindex + 2
        for sibling in targetElement.itersiblings():
            siblingcopy = copy.deepcopy(sibling)
            if index >= len(operand.getTarget().getparent()):
                operand.getTarget().getparent().append(siblingcopy)
            else:
                Tree.Tree.add(operand.getTarget().getparent()[index], siblingcopy)
            index += 1
            
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









