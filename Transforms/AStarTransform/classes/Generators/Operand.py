#!/usr/bin/env python3

"""Generators are used to generate operands"""

import lxml.etree, logging, copy
import Tree.Tree, Element.Element


class Operand:
    """An operand is used to operate on a tree in order to change or transform
    that tree"""
    
    def __init__(self, targetElement):
        """Initialize the operand. Create the operand tree, targetElement, position"""
        #distance? Metrics? 
        self.file = None                             #the file that the operand tree resides in, if any.
        
        self.targetPosition = Element.Element.position(targetElement)
        
        self.tree = lxml.etree.fromstring('<_/>')    #the operand tree, in lxml.etree._ElementTree form
        #build unit nodes down to position. Recall that the position list always starts with 1
        current = self.tree
        for entry in self.targetPosition[1:]:
            for i in range(0, entry):
                new = lxml.etree.Element('_') 
                current.append(new)
            current = new
        #operand.tree is now a tree of unit nodes down to the target. The last unit
        #node in the tree, i.e. the last appended, i.e current, is at the targetElement
        #position. Therefore, this is the targetElement that the operand will try to change
        self.target = current
        
        
        