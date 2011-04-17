"""This file defines the Node objects functions."""

import lxml.etree, logging

from . import Tag, Attrib    

def invert(element1):
    """Invert the element, modify in place and return it.
    
    This function modifies the node in place to make ensure there are not 
    too many copies created in complicated programs. 
    
    The reason this function also returns the element is to allow this function
    to be used in compound statements, for example: 
    
        add(node1, invert(add(node2, node3)))
        
    """
    
#    inverted = lxml.etree.Element(Tag._taginverse(element1.tag), )
    element1.tag = Tag._taginverse(element1.tag) 
    newattribs = Attrib._attribinverse(dict(element1.attrib))
    for i in element1.attrib:
        del element1.attrib[i]
    for j in newattribs:
        element1.set(j, newattribs[j])
        
    return element1
        
    
def equal(element1, element2):
    """Return True if two elements are equal, false if they are not"""
    
    log = logging.getLogger()
    
    attrib1 = element1.attrib
    Attrib._cleankeys(attrib1)
    tag1 = Tag._cleantag(element1.tag)
    
    attrib2 = element2.attrib
    Attrib._cleankeys(attrib2) 
    tag2 = Tag._cleantag(element2.tag)
        
    if (tag1 == tag2) and (attrib1 == attrib2): 
        return True
    else:
        return False






def add(element1, element2):
    """Add element2 to element1, modify element1 in place and return it. 
    
    This function modifies the node in place to make ensure there are not 
    too many copies created in complicated programs. 
    
    The reason this function also returns the element is to allow this function
    to be used in compound statements, for example: 
    
        add(node1, invert(add(node2, node3)))"""
    
    newtag = Tag._addtags(element1.tag, element2.tag)
    
    #have to wrap the attributes in dict() to avoid a bus error
    newattribs = Attrib._addattribs(dict(element1.attrib), dict(element2.attrib))
    
    element1.tag = newtag
    
    for i in element1.attrib:
        del element1.attrib[i]
    for key in newattribs.keys():
        element1.set(key, newattribs[key])
    
    return element1




    
def position(element1, root=None):
    """Return the position of the element in its parent tree. 
    
    The position of a node is, essentially, the path to it from the root. 
    THe first number in the position must always be one, and represents the root. 
    Starting at the root and ignoring the first number, each number in the list 
    indicates the number of the child that should be travelled through to reach the node. 
    
    Note that the numbers in the position are the index of each child + 1. 
    
    You can specify another root node to use. The position generator will stop ascending
    the tree and inserting entries into the position when it reaches this node. This is 
    useful if you are trying to find the position of a node in a subtree, ie a tree
    defined by an element in a tree. In this case, the element is the root of its subtree,
    so you may not want to go up to the root of the tree as a whole. In this case, use the
    root= option. 
    
    The length of the position list is not relevant, we simply travel to the node
    represented by the last node in the list. """
    
    position = [] 
    current = element1
    while (current.getparent() is not None) and (current is not root):
        parent = current.getparent()
        #find the index of current under parent
        index = 0
        for i in parent:
            if i is current: break
            index += 1
        position.insert(0, index + 1)
        current = parent
    
    position.insert(0, 1) # for the root element
    return position
        