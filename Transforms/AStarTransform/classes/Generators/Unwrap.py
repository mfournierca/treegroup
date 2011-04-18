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
        """generate the operand"""
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.warning('targetElement must be lxml.etree._Element object, aborting')
            return None
        else:
            pass
        
        self.log.debug('Generating unwrap operand for  %s' % str(targetElement))
        operand = Operand.Operand(targetElement)
        self.log.debug('created operand: %s' % str(operand))
        
        #
        #create the operand
        #
        
        self.log.debug('operand tree: %s' % lxml.etree.tostring(operand.tree))
        self.log.debug('operand target: %s' % str(operand.target))
        self.log.debug('operand target parent: %s' % str(operand.target.getparent()))
        
        #change operand.target to inverse of targetElement.
        inversetarget = Tree.Tree.invert(copy.deepcopy(targetElement))
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
        self.log.debug('Target index is: %i. Target parent length is: %i' % (index, len(operand.target.getparent()))) 
        for child in targetElement:
            #if you don't copy the child, it gets moved out of the target tree and into the operand, which may cause problems
            #depending on what the user is doing. This function should not alter the target tree (that the user passes), 
            #it should only create an operand. Therefore make a copy of the child before adding it to the operand, so that 
            #the target tree does not change. 
            child = copy.deepcopy(child)
            if len(operand.target.getparent()) > index:
                Tree.Tree.add(operand.target.getparent()[index], child)
                self.log.debug('\tadded child %s at index %i' % (str(child), index))
            else:
                operand.target.getparent().append(child)
                self.log.debug('\tindex is %i, parent length is %i, appended child %s' % (index, len(operand.target.getparent()), str(child)))
            index += 1

        self.log.debug('added target children, tree is: %s' % lxml.etree.tostring(operand.tree))

        #add sibling trees of targetElement to operand.target
        self.log.debug('adding target siblings')
        self.log.debug('Index is: %i. Target parent length is: %i' % (index, len(operand.target.getparent())))
        for sibling in targetElement.itersiblings():
            #if you don't copy the sibling, it gets moved out of the target tree and into the operand, which may cause problems
            #depending on what the user is doing. This function should not alter the target tree (that the user passes), 
            #it should only create an operand. Therefore make a copy of the sibling before adding it to the operand, so that 
            #the target tree does not change. 
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
    def __init__(self):
        pass