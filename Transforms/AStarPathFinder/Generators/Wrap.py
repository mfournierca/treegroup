#!/usr/bin/env python3

"""Generators are used to generate operands"""

import lxml.etree, logging, copy
import Tree.Tree, Element.Element

from . import Operand        
        
        

#===============================================================================
# Wrap Generator
#===============================================================================


class Generator:
    """Generate a wrap operand"""
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
        
#        self.log.debug('Generating wrap operand for  %s' % str(targetElement))
#        self.log.debug('wrap in: %s' % tag)
#        self.log.debug('created operand: %s' % str(self.operand))
        operand = self._generateOperand(Operand.Operand(targetElement), targetElement, tag)
        return operand
    
    def _generateOperand(self, operand, targetElement, tag):
        """generate the operand"""
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.warning('targetElement must be lxml.etree._Element object, aborting')
            return None
        else:
            pass
    
        
        #
        #create the operand
        #
        
#        self.log.debug('operand tree: %s' % lxml.etree.tostring(operand.getTree()))
#        self.log.debug('operand target: %s' % str(operand.getTarget()))
#        self.log.debug('operand target parent: %s' % str(operand.getTarget().getparent()))
#        self.log.debug('tag: %s' % tag)
        
        #change operand.target to inverse of targetElement.
        inversetarget = Tree.Tree.invert(copy.deepcopy(targetElement))
        operand.setTarget(inversetarget)

#        #this code is now replaced by code in the operand.setTarget() method.
#        if operand.getTarget().getparent() is None:
#            #the operand is the root, create a new root. The tree and target become
#            #the root, then proceed.
#            operand.setTarget(inversetarget)
#            operand.setTree(inversetarget)
#        else:
#            operand.setTarget(inversetarget)

        #add the wrap element
        operandtarget = operand.getTarget()
        wrapElement = lxml.etree.Element(tag)
        Tree.Tree.add(operandtarget, wrapElement)
        
        #append the target element to the new wrap element.
        #we need to copy the targetElement to ensure that no changes are made to the source tree 
        targetCopy = copy.deepcopy(targetElement) 
        if len(operandtarget) == 0:
            operandtarget.append(targetCopy)
#            self.log.debug('appended targetCopy to wrapElement')
        else:
            Tree.Tree.add(operandtarget[0], targetCopy)
#            self.log.debug('added targetCopy to wrapElement[0]')
        
        operand.setTarget(operandtarget)
        
        #done creating the operand
#        self.log.debug('operand tree is: %s' % lxml.etree.tostring(operand.getTree()))
#        self.log.debug('done')
#        self.log.debug('Generated wrap operand: %s' % str(operand))
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
            self.log.debug('no more wraps to generate')
            raise StopIteration
        #if optimizing, you may want to copy the operand here instead of creating a new one each time. 
        operand = self._generateOperand(Operand.Operand(self.targetElement), self.targetElement, self.acceptableTags[self.index])
        self.index += 1
        return operand









