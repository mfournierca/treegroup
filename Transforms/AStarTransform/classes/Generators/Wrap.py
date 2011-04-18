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
        """generate the operand"""
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.warning('targetElement must be lxml.etree._Element object, aborting')
            return None
        else:
            pass
        
        self.log.debug('Generating wrap operand for  %s' % str(targetElement))
        operand = Operand.Operand(targetElement)
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
    
    
    




class Iterator(Generator):
    def __init__(self):
        pass

