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
    
    if isinstance(tree1, lxml.etree._ProcessingInstruction):
        self.log.error('%s is ProcessingInstruction' % str(tree1))
        raise TypeError
    elif isinstance(tree2, lxml.etree._ProcessingInstruction):
        self.log.error("%s is ProcessingInstruction, cannot add" % str(tree2))
        raise TypeError
    
    #get orderings
    ordering1 = ordering(tree1)
    ordering2 = ordering(tree2)
    
#    log.debug('ordering1: %s' % str(ordering1))
#    log.debug('ordering2: %s' % str(ordering2))
    
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
            
            try:
                node3 = lxml.etree.Element(node2.tag, node2.attrib) #copy.copy(node2)
            except TypeError:
                log.error('TypeError: %s' % str(sys.exc_info()[1]))
                log.error('%s\t%s' % (node2.tag, str(node2.attrib)))
                raise
            
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
        elif not i is parent[-1]:
            #only remove trailing units. 
            pass
        else:
            parent.remove(i)
    
#    log.debug('result: %s' % lxml.etree.tostring(tree1))
    return tree1



def equal(tree1, tree2):
    """Return True if the trees are equal, False otherwise"""
    #determine if trees are equal, without using the orderings. This function should be faster 
    #that the old ones.     
    log = logging.getLogger()
    
    #check that correct object is passed. 
    #In lxml, ElementTrees are distinct from Elements in that ElementTrees have doc information
    #like xml and dtd declaration, entity decalarations, etc. For our purposes of the Tree Group 
    #theory, these differences are irrelevant, so we can treat lxml ElementTree and Element objects 
    #the same. 
    if not (isinstance(tree1, lxml.etree._ElementTree) or isinstance(tree1, lxml.etree._Element)):
        return False
    elif not (isinstance(tree2, lxml.etree._ElementTree) or isinstance(tree2, lxml.etree._Element)):
        return False
    
    tree1iterator = tree1.iter()
    tree2iterator = tree2.iter()
    p1 = []
    p2 = []
    stack1 = []
    stack2 = []
    index = 0
#    while True:
#        try: 
#            e1 = tree1iterator.__next__()
#        except StopIteration:
#            break
    for e1 in tree1iterator:
        #log.debug('e1: %s' % str(e1))
        
        try:
            e2 = tree2iterator.__next__()
        except StopIteration: 
            #log.debug('no e2, return False')
            return False
        #log.debug('e2: %s' % str(e2))
        
        if not Element.Element.equal(e1, e2): 
            #log.debug('e1 != e2, return False')
            return False
        
#        p1 = Element.Element.position(e1, root=tree1)
#        p2 = Element.Element.position(e2, root=tree2)
        
        #get position 1 and position 2, compare. 
        if (p1 == []) and (index != 0):
            log.warning('p1 == [], e1 is not root')
            raise TypeError
        elif index == 0:
            stack1 = [e1]
            p1 = [1]
        else:
            parent1index = stack1.index(e1.getparent())
            p1 = p1[:parent1index + 1]
            p1.append(e1.getparent().index(e1) + 1)
            stack1 = stack1[:parent1index + 1]
            stack1.append(e1)
                    
        if (p2 == []) and (index != 0):
            log.warning('p2 == [], e2 is not root')
            raise TypeError
        elif index == 0:
            stack2 = [e2]
            p2 = [1]
        else:
            parent2index = stack2.index(e2.getparent())
            p2 = p2[:parent2index + 1]
            p2.append(e2.getparent().index(e2) + 1)
            stack2 = stack2[:parent2index + 1]
            stack2.append(e2)

        #log.debug('p1: %s' % str(p1))
        #log.debug('p2: %s' % str(p2))
        if p1 != p2: 
            #log.debug('p1 != p2, return False')
            return False
    #log.debug('tree1 iteration finished')
    
    try:
        e2 = tree2iterator.__next__()
    except StopIteration:
        #log.debug('tree2 iteration finished, return True')
        return True
    
    if e2 is not None: 
        #log.debug('tree2 iteration not finished, return False')
        return False
    
    #log.debug('return True')
    return True


def equal_old(tree1, tree2):
    """Return True if the trees are equal, False otherwise"""
    #trees are equal if their orderings are of the same length, have the same 
    #positions in the same order, and point to equal nodes. 

    log = logging.getLogger()

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
#    #log.debug("ordering1: %s" % str(ordering1))
#    log.debug("ordering2: %s" % str(ordering2))
    
    if not len(ordering1) == len(ordering2):
        return False
    
    for index, p1 in enumerate(ordering1):
        p2 = ordering2[index]
        if not p1 == p2:
            return False        
        if not Element.Element.equal(getNode(tree1, p1), getNode(tree2, p2)):
            return False
    
    return True




def ordering_sax(file, startingposition):
    """Build the ordering of the tree using the sax parser."""
    
    #this is great, and it works, but it only works when reading the file 
    #directly from disk. This means that this ordering function cannot be used
    #when performing compound operations, because those changes happen in memory, 
    #not on disk, so the the sax parser here will not pick up the changes. 
    #Can sax parse a tree serialized from the etree model in memory? Would that be faster?
    #Probably not. 
    
    import xml.sax, lxml.etree, os.path, urllib.parse, copy
    import DitaTools.Exceptions
    
    log = logging.getLogger()
    
    #define sax content handlers
    class ContentHandlers(xml.sax.handler.ContentHandler):
        
        def __init__(self, startingposition):
            #startingposition is used to decide when to start building the ordering
            self.startingposition = startingposition
            self.buildordering = False
            #stack is used to build each position, which is then added to the ordering
            self.stack = [] 
            self.stackindex = 0
            #ordering is what we generate
            self.ordering = []
            self.log = logging.getLogger()
            
     
        def startElement(self, name, attrs):
            #self.log.debug('found element: %s' % name)
            if self.stackindex == len(self.stack):
                #append / insert
                #self.log.debug('\tappending to stack at index %s' % str(self.stackindex))
                self.stack.insert(self.stackindex, 1)
                self.stackindex += 1
            elif self.stackindex < len(self.stack):
                #add
                #self.log.debug('\tadding to stack at index %s' % str(self.stackindex))
                self.stack[self.stackindex] += 1
                self.stackindex += 1
            elif self.stackindex > len(self.stack):
                #should never happen
                self.log.error('self.stackindex > len(self.stack)')
            #add current stack onto ordering
            #self.log.debug('\tstack: %s' % str(self.stack))
            #self.log.debug('\tstackindex: %s' % str(self.stackindex))
            if not self.buildordering:
                if self.stack == self.startingposition:
                    self.stack = [1]
                    self.stackindex = 1
                    self.buildordering = True
            if self.buildordering:
                self.ordering.append(copy.copy(self.stack))
            
        def endElement(self, name):
            #self.log.debug('ending element %s' % name)
            if self.stackindex == len(self.stack):
                pass
            elif self.stackindex == len(self.stack) - 1:
                discard = self.stack.pop(-1)
            else:
                #should not happen
                pass
            self.stackindex -= 1
            #self.log.debug('\tstack: %s' % str(self.stack))
            #self.log.debug('\tstackindex: %s' % str(self.stackindex))
            if len(self.stack) == 0:
                #could happen if we take the ordering of an element that is not the root
                raise StopIteration

        def endDocument(self):
            raise StopIteration

    #start sax parser
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_external_ges, False)
    contenthandlers = ContentHandlers(startingposition)
    parser.setContentHandler(contenthandlers)
    try:
        parser.parse(file)
    except IOError:
        log.error("IOError when parsing file %s: %s" % (file, str(sys.exc_info()[0])))
        return False
    except StopIteration:
        pass
    
#    log.debug('ordering:')
#    for i in parser.getContentHandler().ordering:
#        log.debug(str(i))
    return parser.getContentHandler().ordering




def ordering_etree(tree):
    """Build the ordering of the tree by iterating over the elements in the tree"""
#    #this can be made much more effecient by using a stack and 
#    #building each position while iterating, instead of calling 
#    #Element.Element.position each time, which iterates over the 
#    #tree for each element. 
#    result = [] 
#    
#    if isinstance(tree, lxml.etree._ElementTree):
#        root = tree.getroot()
#    else:
#        root = tree
#    
#    for i in root.iter():
#        result.append(Element.Element.position(i, root=root))
#    return result

    log = logging.getLogger()
    ordering = []
    currentposition = []
    stack = []
    for element in tree.iter():
        #log.debug('found element: %s' % element.tag)
        if len(stack) == 0:
            stack = [element]
            currentposition = [1]
            ordering = [copy.copy(currentposition)]
            #log.debug('\tcurrentposition: %s' % str(currentposition))
            #log.debug('\tstack: %s' % str(stack))
            continue
        
        #search backward in stack until parent found. 
        while len(stack) > 0:
            if stack[-1] is element.getparent():
                break
            stack.pop(-1)
        else:
            #done
            break
        stack.append(element)
        
        if len(stack) > len(currentposition):
            currentposition.append(1)
        elif len(stack) < len(currentposition):
            currentposition = currentposition[:len(stack)]
            currentposition[-1] += 1
        elif len(stack) == len(currentposition):
            currentposition[-1] += 1
        
        ordering.append(copy.copy(currentposition))
        #log.debug('\tcurrentposition: %s' % str(currentposition))
        #log.debug('\tstack: %s' % str(stack))
    
    #log.debug('ordering:')
#    for i in ordering: 
        #log.debug('\t%s' % str(i))
    return ordering



def ordering(tree):
    import urllib.parse
    
#    if isinstance(tree, lxml.etree._ElementTree):
#        url = tree.docinfo.URL
#        startingposition = [1]
#    elif isinstance(tree, lxml.etree._Element):
#        url = tree.getroottree().docinfo.URL
#        startingposition = Element.Element.position(tree)
#        
#    if url:
#        file = urllib.parse.unquote(url, encoding='utf-8')
#        return ordering_sax(file, startingposition)
#    else:
#        return ordering_etree(tree)
    return ordering_etree(tree)
    
        

    



def getNode(tree, position):
    """Get a node from the position. Return the node."""
    
    log = logging.getLogger()
    
    if not position[0] == 1:
        #fail, this is a required property of te position
        return False
    
    #log.debug('position is: %s' % str(position))
    position = position[1:]
        
    if isinstance(tree, lxml.etree._ElementTree):
        current = tree.getroot()
    else:
        current = tree
        
    for i in position:
        #log.debug('index: %i' % i)
        #log.debug('\tcurrent: %s' % str(current))
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




