#!/usr/bin/env python3

"""Generators are used to generate operands"""

import lxml.etree, logging, copy, sys
import Tree.Tree, Element.Element


class Operand:
    """An operand is used to operate on a tree in order to change or transform
    that tree"""
    
    def __init__(self, targetElement):
        """Initialize the operand. Create the operand tree, targetElement, position"""
        
        self.targetPosition = Element.Element.position(targetElement)
        
        tree = lxml.etree.fromstring('<_/>')    #the operand tree, in lxml.etree._ElementTree form
        #build unit nodes down to position. Recall that the position list always starts with 1
        current = tree
        for entry in self.targetPosition[1:]:
            for i in range(0, entry):
                new = lxml.etree.Element('_') 
                current.append(new)
            current = new
        #tree is now a tree of unit nodes down to the target. The last unit
        #node in the tree, i.e. the last appended, i.e current, is at the targetElement
        #position. Therefore, this is the targetElement that the operand will try to change
        
#        self.setTarget(current)
        self._target = current
        self.setTree(tree)
        
    #===========================================================================
    # accessor methods
    #===========================================================================
    
    #in the future, we are going to use this program to process large trees, which will 
    #require lots of large operands. Since some documents can reach 5 MB with hundreds of
    #elements, we may run into memory problems when storing lots of operands. These problems
    #can be solved by handling things more intelligently, ie writing to disk when necessary, 
    #storing compressed versions, etc. Accessor methods are provided here to allow this to be
    #done easily in the future. 
    
    def setTree(self, tree):
        """Set the operand tree."""
        self._tree = tree
        
    def getTree(self):
        """Get the operand tree. There is no guarantee that any changes made on the returned 
        tree will persist. To guarantee this, use the setTree() method"""
        return self._tree
    
    def setTarget(self, newtarget):
        """Set the target element. This inserts or replaces the target element in the 
        operand tree"""
        targetbyposition = Tree.Tree.getNode(self.getTree(), self.targetPosition)
        targetbyfunction = self.getTarget()
        if not targetbyposition is targetbyfunction:
            #consistency error, this should never happen
            self.log.error('targetPosition in tree did not match self.getTarget()')
            sys.exit(0)
        targetparent = targetbyposition.getparent()
        if targetparent is None:
            #target is root
            self.setTree(newtarget)
            self._target = newtarget
        else:
            targetbyposition.getparent().replace(targetbyposition, newtarget)
            self._target = newtarget
            self.setTree(newtarget.getroottree())
        
    def getTarget(self):
        """Get the target element. There is no guarantee that any changes made on the returned 
        element will persist. To guarantee this, use the setTarget() method"""
        return self._target
    
    
        
        