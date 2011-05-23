#!/usr/bin/env python3

"""Rename generators are used to generate rename operands"""

import lxml.etree, logging, copy
import Tree.Tree, Element.Element

from . import Operand


    
class Generator:
    """Generate a rename operand"""
    def __init__(self):       
        self.log = logging.getLogger()
        
        
    def generateOperand(self, targetElement, tag):
        """Generate an operand for the targetElement and tag"""
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.warning('targetElement must be lxml.etree._Element object, is %s. Aborting' % str(targetElement))
            return None
        elif not isinstance(tag, str):
            self.log.warning('tag must be str object, is %s. Aborting' % str(tag))
            return None
        else:
            pass
        
        self.log.debug('Generating rename operand for  %s' % str(targetElement))
        self.log.debug('Rename to: %s' % tag)
        operand = self._generateOperand(Operand.Operand(targetElement), targetElement, tag)
        return operand
    
    
    def _generateOperand(self, operand, targetElement, tag):        

        #note that this method creates the operand tree, but indirectly. 
        #Usually, if we want A + B = C, we use C - A = B to find B. But in 
        #this case, A and C are full trees, and we don't know what C is. 
        #The method used here builds the operand, B, directly which avoids finding 
        #the full trees and saves time and headaches.    
        self.log.debug('generating rename operand tree')
        self.log.debug('targetElement: %s' % targetElement)
        self.log.debug('rename to: %s' % tag)
        #we exclude the attributes from the inverted element, below, because we only
        #want the generated operand to affect the tag. 
        renamenode = Element.Element.add(lxml.etree.Element(tag), Element.Element.invert(lxml.etree.Element(targetElement.tag)))#, targetElement.attrib)))
#        operand.target.tag = renamenode.tag
#        for a in renamenode.attrib.keys():
#            operand.target.attrib[a] = renamenode.attrib[a]
        operand.setTarget(renamenode)
        self.log.debug('result: %s' % lxml.etree.tostring(operand.getTree()))
        #done
        return operand
    
    
    
class Iterator(Generator):
    """An iterator class for generating rename operands. This used the same 
    generating functions as the RenameGenerator class"""
    
    def __init__(self, targetElement, acceptableTags):       
        self.log = logging.getLogger() 
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.warning('targetElement must be lxml.etree._Element object, is %s. Aborting' % str(targetElement))
            #raise StopIteration #?
            return None
        elif not isinstance(acceptableTags, list):
            self.log.warning('acceptableTags must be list object, is %s. Aborting' % str(acceptableTags))
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
        operand = self._generateOperand(Operand.Operand(self.targetElement), self.targetElement, self.acceptableTags[self.index])
        self.index += 1
        return operand