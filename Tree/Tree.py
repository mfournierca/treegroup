import lxml.etree
import copy, logging, re, sys, os.path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
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
    
    if isinstance(tree, lxml.etree._Element):
        iterateover = tree
    else:
        iterateover = tree.getroot()
    for element in iterateover.iter():
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
    
    #log.debug('ordering1: %s' % str(ordering1))
    #log.debug('ordering2: %s' % str(ordering2))
    
    #iterate over ordering2, apply to ordering1
#    for index, position2 in enumerate(ordering2):
    index = 0
    while index < len(ordering2):
        position2 = ordering2[index]
                                    
        #log.debug('index: %s\tposition2: %s' % (str(index), str(position2)))
        
        node2 = getNode(tree2, position2)
        
        #if index greater then len(ordering1), append to appropriate node. 
        #if positions not equal, append to appropriate node 
        if index == 1 and len(ordering1) == 1 and len(ordering2) == 1:
            pass
        
        elif index == len(ordering1):
            #log.debug('\tindex == len(ordering1)')
            
            node3 = lxml.etree.Element(node2.tag, node2.attrib) #copy.copy(node2)
            #log.debug('\tnode3: %s' % str(node3))
                      
            parent1 = getNode(tree1, position2[:-1])
            #log.debug('\tparent1: %s' % str(parent1))
                
            parent1.append(node3)
            
            position3 = Element.Element.position(node3, root=tree1)
            #log.debug('\tposition3: %s' % str(position3))
            
            if position3 != position2:
                log.error('\t\tposition2 != position3, fail')
                #raise exception?
                return None
            else:
                ordering1.insert(index, position3)
                #log.debug('\tordering1: %s' % str(ordering1))
                
     
 
        elif position2 != ordering1[index]:
            #log.debug('\tposition2 != ordering1[index]')
            
            #search for corresponding position later on in ordering1
            #if found, add nodes 
            newindex = None
            for e, p in enumerate(ordering1[index:]):
                if p == position2:
                    newindex = e + index
                    break
            if newindex:
                #log.debug('\tfound position2 in ordering1 at index %s, adding nodes' % str(newindex))
                position1 = ordering1[newindex]
                node1 = getNode(tree1, position1)
                #log.debug('\tnode1: %s\tnode2: %s' % (str(node1), str(node2)))
                Element.Element.add(node1, node2) 
            else:
                node3 = lxml.etree.Element(node2.tag, node2.attrib)
                node3.text = node2.text
                node3.tail = node2.tail
                #log.debug('\tnode3: %s' % str(node3))
                
                parent1 = getNode(tree1, position2[:-1])
                #log.debug('\tparent1: %s' % str(parent1))
                    
                parent1.append(node3)
                
                position3 = Element.Element.position(node3, root=tree1)
                #log.debug('\tposition3: %s' % str(position3))
                
                if position3 != position2:
                    log.error('\t\tposition2 != position3, fail')
                    #raise exception?
                    return None
                else:
                    ordering1.insert(index, position3)
                    #log.debug('\tordering1: %s' % str(ordering1))
                

        
        elif position2 == ordering1[index]:
            #if positions equal, add
            #log.debug('\tposition2 == ordering1[index], add elements')
            #get positions
            position1 = ordering1[index]
            node1 = getNode(tree1, position1)
            #log.debug('\tnode1: %s\tnode2: %s' % (str(node1), str(node2)))
            Element.Element.add(node1, node2) 
        
        
        else:
            #this should never happen
            log.error('inconsistency in tree orderings, position2 does not correspond to any possibilities in ordering1')
            return None
                
        index += 1
        continue
               
               
               
    #done. Now remove trailing units
    #easiest way to do this is to iterate over the tree in reverse. 
    reversed = []
    ##log.debug('removing trailing unit nodes')
    if isinstance(tree1, lxml.etree._ElementTree): 
        for i in tree1.getroot().iter(): reversed.insert(0, i)
    elif isinstance(tree1, lxml.etree._Element):
        for i in tree1.iter(): reversed.insert(0, i)
    else:
        log.warning('tree1 is %s, expected lxml.etree._Element or lxml.etree._ElementTree' % str(tree1))
        
    for i in reversed:
        #log.debug('testing: %s' % str(i))
        if not (i.tag == '_'):
            #log.debug('\ttag is not _, skip')
            continue
        
        if not (i.attrib == {}):
            #log.debug('\tattributes not blank, skip')
            continue
        
        if not (len(i) == 0):
            #log.debug('\tlength is not 0, skip')
            continue
         
        if not (i.text is None or re.match(r'^\s*$', i.text)):
            #log.debug('\ttext is %s, skip' % str(i.text))
            continue
        
        if not (i.tail is None or re.match(r'^\s*$', i.tail)):
            #log.debug('\ttail is %s, skip' % str(i.tail))
            continue
        
        #log.debug('removing unit node: %s' % str(i))
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

    #check that correct object is passed. 
    #In lxml, ElementTrees are distinct from Elements in that ElementTrees have doc information
    #like xml and dtd declaration, entity decalarations, etc. For our purposes of the Tree Group 
    #theory, these differences are irrelevant, so we can treat lxml ElementTree and Element objects 
    #the same. 
    if not (isinstance(tree1, lxml.etree._ElementTree) or isinstance(tree1, lxml.etree._Element)):
        return False
    elif not (isinstance(tree2, lxml.etree._ElementTree) or isinstance(tree2, lxml.etree._Element)):
        return False
    
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
        result.append(Element.Element.position(i, root=root))
    return result




def getNode(tree, position):
    """Get a node from the position. Return the node."""
    
    log = logging.getLogger()
    
    if not position[0] == 1:
        #fail, this is a required property of te position
        return False
    
    ##log.debug('position is: %s' % str(position))
    position = position[1:]
        
    if isinstance(tree, lxml.etree._ElementTree):
        current = tree.getroot()
    else:
        current = tree
        
    for i in position:
        ##log.debug('current: %s' % str(current))
        ##log.debug('index: %i' % i)
        if i == 0: 
            return current
        current = current[i - 1]
        
    return current
        
        
        

def metric(tree1, tree2):
    """Metric of tree1 and tree2 is defined as the number of non-unit nodes
    in tree1 - tree2. 
    
    This function satisfies all the conditions of a metric. """
    treecopy = copy.deepcopy(tree2)
    add(invert(treecopy), tree1)
    return countNonUnitNodes(treecopy)




def countNonUnitNodes(tree):
    """The size of a tree is defined as the number of non-unit nodes within the tree. 
    This function should satisfy all the conditions of a modulus, but that has not been 
    proven. """
    log = logging.getLogger()    
    if isinstance(tree, lxml.etree._ElementTree):
        t = tree.getroot()
    else:
        t = tree
#    #log.debug('%s' % lxml.etree.tostring(t))
    count = 0
    for i in t.iter():
        alltext = ''
        if i.text: alltext = alltext.join(i.text)
        if i.tail: alltext = alltext.join(i.tail)
        if i.tag == '_' and len(i.attrib) == 0 and re.search(r'^\s*$', alltext): continue
        else: count += 1
    return count




