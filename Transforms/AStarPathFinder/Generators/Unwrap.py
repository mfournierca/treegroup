#!/usr/bin/env python3

"""Generators are used to generate operands"""

import lxml.etree, logging, copy, re
import Tree.Tree, Element.Element, Element.Text

import DitaTools.Element.Functions

from . import Operand
        


class Generator:
    """Generate an unwrap operand"""
    def __init__(self):
        self.log = logging.getLogger()
        pass
    
    
    def generateOperand(self, targetElement):
        """Generate an operand for the targetElement and tag"""
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.error('targetElement must be lxml.etree._Element object, aborting')
            return None
        else:
            pass
        
#        self.log.debug('Generating unwrap operand for  %s' % str(targetElement))
#        self.log.debug('created operand: %s' % str(self.operand))
        operand = self._generateOperand(Operand.Operand(targetElement), targetElement)
#        self.log.info('Generated operand: %s' % str(operand))
        return operand
    
    
    
    def _generateOperand(self, operand, targetElement):
        """generate the operand"""
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.error('targetElement must be lxml.etree._Element object, aborting')
            return None
        else:
            pass
        
#        self.log.debug('Generating unwrap operand for  %s' % str(targetElement))
#        operand = Operand.Operand(targetElement)
#        self.log.debug('created operand: %s' % str(operand))
        
        #
        #create the operand
        #
        
        operandtarget = operand.getTarget()
#        self.log.debug('operand tree: %s' % lxml.etree.tostring(operand.getTree()))
#        self.log.debug('operand target: %s' % str(operandtarget))
#        self.log.debug('operand target parent: %s' % str(operandtarget.getparent()))
        
        #change operand.target to inverse of targetElement.
        inversetarget = Tree.Tree.invert(copy.deepcopy(targetElement))
        if operandtarget.getparent() is None:
            #the target is the root
            if len(targetElement) > 1: 
                self.log.debug('target is root and has more than one child, cannot unwrap')
                return None
            elif len(targetElement) == 0: 
                self.log.debug('target is root and has no child, cannot unwrap')
                return None
            elif (len(targetElement.text) != 0) and (not re.search(r'^\s*$', targetElement.text)):
                self.log.debug('target is root and has text, cannot unwrap')
                return None
            operand.setTarget(inversetarget)
            operand.setTree(inversetarget)
        else:
            operandtarget.getparent().replace(operandtarget, inversetarget)
            operand.setTarget(inversetarget)
        operandtarget = operand.getTarget()
#        self.log.debug('inverted target, tree is: %s' % lxml.etree.tostring(operand.getTree()))
        
        
        #append invert of siblings to parent of operand.target 
        for sibling in targetElement.itersiblings():
            siblingcopy = copy.deepcopy(sibling)
            operandtarget.getparent().append(Tree.Tree.invert(siblingcopy))
#        self.log.debug('inverted siblings, tree is: %s' % lxml.etree.tostring(operand.getTree()))
            
            
        #handling text is tricky, and it is best to do it here. I think. 
        #The problem is that the text and tail of the target element must be put in the right place. 
        
        #2 cases for the target in relation to parent:
        #    target is first child of parent. In this case, target text gets appended to the parent text
        #    target is not first child. In this case, target text gets appended to preceding sibling tail
        
        #2 cases for target in relation to children.
        #    no children. In this case, target tail gets appended to parent text / preceding sibling tail, depending on above. 
        #    children. In this case, target tail gets appended to last child tail. 
        
        #2*2 = 4 cases in total. Easiest to handle them here, directly. 
        
        #Take target text and append it in appropriate location directly. 
        #If no children, also append target tail. 
        #Both these operations are safe because unwrap operand will not affect parent / preceding sibling. 
        #These two operations take care of three cases, only one left: last child needs tail appended. 
        
        #handle target text
        if targetElement.getparent() is None: 
            pass
        elif (targetElement.getparent().index(targetElement) == 0) and (targetElement.text is not None):
            if (targetElement.getparent().text is None) or (len(targetElement.getparent().text) == 0) or (re.search(r'^\s*$', targetElement.getparent().text)): 
                parenttextlength = 0
            else: 
                parenttextlength = len(targetElement.getparent().text)
            #use Text._addtext here? Should be safe this way because unwrap does not affect parent. 
            operandtarget.getparent().text = ' ' * parenttextlength + targetElement.text
            if len(targetElement) == 0:
                operandtarget.getparent().text += targetElement.tail
            self.log.debug('operand parent text: %s' % operandtarget.getparent().text)
        
        elif (targetElement.getparent().index(targetElement) != 0) and (targetElement.text is not None):
            index = targetElement.getparent().index(targetElement)
            if (targetElement.getparent()[index - 1].tail is None) or (len(targetElement.getparent()[index - 1].tail) == 0) or (re.search(r'^\s*$', targetElement.getparent()[index - 1].tail)):
                precedingsiblingtaillength = 0
            else:
                precedingsiblingtaillength = len(targetElement.getparent()[index - 1].tail)
            #use Text._addtext here? Should be safe this way because unwrap does not affect preceding sibling. 
            operandtarget.getparent()[index - 1].tail = ' ' * precedingsiblingtaillength + targetElement.text
            if len(targetElement) == 0:
                operandtarget.getparent()[index - 1].tail += targetElement.tail
            self.log.debug('operand preceding sibling tail: %s' % operandtarget.getparent()[index - 1].tail)
        
        #only case remaining is if target has children, must deal with tail. 
        
        #add children of targetElement to parent of operand.target
        index = DitaTools.Element.Functions.get_index(targetElement)
        self.log.debug('adding target children.')
        self.log.debug('Target index is: %s. Target parent length is: %s' % (str(index), str(None) if operandtarget.getparent() is None else str(len(operandtarget.getparent())))) 
        lastchildOperand = None
        lastchildTarget = None
        for child in targetElement:
            #if you don't copy the child, it gets moved out of the target tree and into the operand, which may cause problems
            #depending on what the user is doing. This function should not alter the target tree (that the user passes), 
            #it should only create an operand. Therefore make a copy of the child before adding it to the operand, so that 
            #the target tree does not change. 
            childcopy = copy.deepcopy(child)
            lastchildTarget = child
            if operandtarget.getparent() is None and len(operandtarget) > 1:
                #cannot do this. This was already dealt with above.
                pass
            elif operandtarget.getparent() is None and len(operandtarget) <= 1:
                Tree.Tree.add(operandtarget, childcopy)
                self.log.debug('\ttarget is root, added single child')
                lastchildOperand = operandtarget
                break
            elif len(operandtarget.getparent()) > index:
                Tree.Tree.add(operandtarget.getparent()[index], childcopy)
                lastchildOperand = operandtarget.getparent()[index]
                self.log.debug('\tadded child %s at index %i' % (str(childcopy), index))
            else:
                operandtarget.getparent().append(childcopy)
                lastchildOperand = childcopy
                self.log.debug('\tindex is %i, parent length is %i, appended child %s' % (index, len(operandtarget.getparent()), str(childcopy)))
            index += 1
        
        if (lastchildOperand is not None) and (targetElement.tail is not None):
            self.log.debug('lastchildOperand: %s' % lxml.etree.tostring(lastchildOperand))
            if (targetElement[-1].tail is None) or (len(targetElement[-1].tail) == 0) or (re.search(r'^\s*$', targetElement[-1].tail)):
                lastchildOperand.tail = Element.Text._addtext(lastchildOperand.tail, targetElement.tail)    
            else:
                lastchildOperand.tail = Element.Text._addtext(lastchildOperand.tail, ' ' * len(lastchildTarget.tail) + targetElement.tail)
            
            
#        self.log.debug('added target children, tree is: %s' % lxml.etree.tostring(operand.getTree()))
        self.log.debug('last child: %s' % str(lastchildOperand))
        
        #add sibling trees of targetElement to operand.target
        self.log.debug('adding target siblings')
        self.log.debug('Target index is: %s. Target parent length is: %s' % (str(index), str(None) if operandtarget.getparent() is None else str(len(operandtarget.getparent()))))
        for sibling in targetElement.itersiblings():
            #if you don't copy the sibling, it gets moved out of the target tree and into the operand, which may cause problems
            #depending on what the user is doing. This function should not alter the target tree (that the user passes), 
            #it should only create an operand. Therefore make a copy of the sibling before adding it to the operand, so that 
            #the target tree does not change.
            if operandtarget.getparent() is None:
                #the target is the root and has no siblings
                break 
            sibling = copy.deepcopy(sibling)
            if len(operandtarget.getparent()) > index:
                self.log.debug('\tadding sibling %s at index %i' % (str(sibling), index))
                Tree.Tree.add(operandtarget.getparent()[index], sibling)
            else:
                self.log.debug('\tindex is %i, parent length is %i, appending sibling' % (index, len(operandtarget.getparent())))
                operandtarget.getparent().append(sibling)
            index += 1
            
#        self.log.debug('added target siblings, tree is: %s' % lxml.etree.tostring(operand.getTree()))
        
        
        #set the target so the changes persist
        operand.setTarget(operandtarget)
        
#        self.log.debug('done')
#        self.log.debug('Generated unwrap operand: %s' % str(operand))
        return operand
    
    
    









class Iterator(Generator):
    """An iterator class for the unwrap generator"""
    
    def __init__(self, targetElement):       
        self.log = logging.getLogger() 
        if not isinstance(targetElement, lxml.etree._Element):
            self.log.error('targetElement must be lxml.etree._Element object, aborting')
            #raise StopIteration #?
            return None
        else:
            pass
        self.targetElement = targetElement
        self.index = 0
    
        
    def __iter__(self):
        return self


    def __next__(self):
        """Generate and return a unwrap operand. This function can be used for iteration"""
        if self.index >= 1:
            #there is only 1 unwrap operand that can be generated, obviously. So this iterator
            #iterates once, and then stops. Not strictly necessary, but designed to be consistent
            #with the other generators, which do need iterators. 
            self.log.debug('no more unwraps to generate')
            raise StopIteration 
        operand = self._generateOperand(Operand.Operand(self.targetElement), self.targetElement)
        self.index += 1
        #the unwrap generator sometimes returns None
        if operand is None: self.__next__()
        return operand

