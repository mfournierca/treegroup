import lxml.etree
import copy, logging, re

import Element.Element




def invert(tree):
    """Invert the tree. 
    
    Note that this function modifies the tree in place _and_ returns it. 
    
    Modifying the tree in place is important since it avoids multiple copies
    of a tree being created in more complicated programs. 
    
    Returning the tree allows this function to be used in compound statements, such 
    as
        add(tree1, invert(add(tree2, tree1)))
        
    Remember that the tree itself is not returned, only a reference to it. 
    """
    for element in tree.getroot().iter():
        Element.Element.invert(element)

    return tree



def add(tree1, tree2):
    """Add tree2 to tree1, modify tree1 in place.
    
    Note that this function modifies tree1 in place _and_ returns it. 
    
    Modifying the tree in place is important since it avoids multiple copies
    of a tree being created in more complicated programs. 
    
    Returning the tree allows this function to be used in compound statements, such 
    as
        add(tree3, invert(add(tree1, tree2)))
        
    Remember that the tree itself is not returned, only a reference to it. 
    """
    
    log = logging.getLogger()
    
    #get orderings
    ordering1 = ordering(tree1)
    ordering2 = ordering(tree2)
    
    log.debug('ordering1: %s' % str(ordering1))
    log.debug('ordering2: %s' % str(ordering2))
    
    #iterate over ordering2, apply to ordering1
    for index, position2 in enumerate(ordering2):
        log.debug('index: %s\tposition2: %s' % (str(index), str(position2)))
        
        node2 = getNode(tree2, position2)
        
        #if index greater then len(ordering1), append to appropriate node. 
        #if positions not equal, append to appropriate node 
        if index == len(ordering1):
            log.debug('\tindex == len(ordering1)')
            
            node3 = lxml.etree.Element(node2.tag, node2.attrib) #copy.copy(node2)
            log.debug('\tnode3: %s' % str(node3))
                      
            parent1 = getNode(tree1, position2[:-1])
            log.debug('\tparent1: %s' % str(parent1))
                
            parent1.append(node3)
            
            position3 = Element.Element.position(node3)
            log.debug('\tposition3: %s' % str(position3))
            
            if not position3 == position2:
                log.debug('\t\tposition2 != position3, fail')
                continue
            
            ordering1.insert(index, position3)
            log.debug('\tordering1: %s' % str(ordering1))
            continue
 
 
        elif position2 != ordering1[index]:
            log.debug('\tposition2 != ordering1[index]')
            
            node3 = lxml.etree.Element(node2.tag, node2.attrib) #copy.copy(node2)
            log.debug('\tnode3: %s' % str(node3))
            
            parent1 = getNode(tree1, position2[:-1])
            log.debug('\tparent1: %s' % str(parent1))
                
            parent1.append(node3)
            
            position3 = Element.Element.position(node3)
            log.debug('\tposition3: %s' % str(position3))
            
            if not position3 == position2:
                log.debug('\t\tposition2 != position3, fail')
                continue
            
            ordering1.insert(index, position3)
            log.debug('\tordering1: %s' % str(ordering1))
            continue

        
        #if positions equal, add
        
        #get positions
        position1 = ordering1[index]
        node1 = getNode(tree1, position1)
        
        #if the positions match, add
        if position2 == position1:
            Element.Element.add(node1, node2) 
            continue
        
    #done. Now remove trailing units
    #easiest way to do this is to iterate over the tree in reverse. 
    reversed = []
    log.debug('removing trailing unit nodes')
    for i in tree1.getroot().iter(): reversed.insert(0, i)
    for i in reversed:
        log.debug('testing: %s' % str(i))
        if not (i.tag == '_'):
            log.debug('\ttag is not _, skip')
            continue
        
        if not (i.attrib == {}):
            log.debug('\tattributes not blank, skip')
            continue
        
        if not (len(i) == 0):
            log.debug('\tlength is not 0, skip')
            continue
         
        if not (i.text is None or re.match(r'^\s*$', i.text)):
            log.debug('\ttext is %s, skip' % str(i.text))
            continue
        
        if not (i.tail is None or re.match(r'^\s*$', i.tail)):
            log.debug('\ttail is %s, skip' % str(i.tail))
            continue
        
        log.debug('removing unit node: %s' % str(i))
        parent = i.getparent()
        if parent is None:
            #happens if i is the root
            pass
        else:
            parent.remove(i)

    return tree1



def equal(tree1, tree2):
    """Return True if the trees are equal, False otherwise"""
    #trees are equal if their orderings are of the same length, have the same 
    #positions in the same order, and point to equal nodes. 
    
    ordering1 = ordering(tree1)
    ordering2 = ordering(tree2)
    
    if not len(ordering1) == len(ordering2):
        return False
    
    for index, p1 in enumerate(ordering1):
        p2 = ordering2[index]
        if not p1 == p2:
            return False        
        if not Element.Element.equal(getNode(tree1, p1), getNode(tree2, p2)):
            return False
    
    return True





def ordering(tree):
    result = [] 
    
    if isinstance(tree, lxml.etree._ElementTree):
        root = tree.getroot()
    else:
        root = tree
    
    for i in root.iter():
        result.append(Element.Element.position(i))
    return result




def getNode(tree, position):
    """Get a node from the position. Return the node."""
    
    if not position[0] == 1:
        #fail
        return False
    
    position = position[1:]
        
    if isinstance(tree, lxml.etree._ElementTree):
        current = tree.getroot()
    else:
        current = tree
        
    for i in position:
        if i == 0: 
            return current
        current = current[i - 1]
        
    return current
        
        
        
