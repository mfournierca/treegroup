"""This file defines the Node objects functions."""

import lxml.etree, logging

from . import Tag, Attrib    

def invert(element1):
    """Invert the element, modify in place"""
    
#    inverted = lxml.etree.Element(Tag._taginverse(element1.tag), )
    element1.tag = Tag._taginverse(element1.tag) 
    newattribs = Attrib._attribinverse(dict(element1.attrib))
    for i in element1.attrib:
        del element1.attrib[i]
    for j in newattribs:
        element1.set(j, newattribs[j])
        
        
        
    
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
    """Add element2 to element1, modify element1 in place"""
    
    newtag = Tag._addtags(element1.tag, element2.tag)
    
    #have to wrap the attributes in dict() to avoid a bus error
    newattribs = Attrib._addattribs(dict(element1.attrib), dict(element2.attrib))
    
    element1.tag = newtag
    
    for i in element1.attrib:
        del element1.attrib[i]
    for key in newattribs.keys():
        element1.set(key, newattribs[key])
    
    
    
def position(element1):
    """Return the position of the element in its parent tree. 
    
    The position of a node is, essentially, the path to it from the root. 
    THe first number in the position must always be one, and represents the root. 
    Starting at the root and ignoring the first number, each number in the list 
    indicates the number of the child that should be travelled through to reach the node. 
    
    Note that the numbers in the position are the index of each child + 1. 
    
    The length of the position list is not relevant, we simply travel to the node
    represented by the last node in the list. """
    
    position = [] 
    current = element1
    while current.getparent() is not None:
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
        