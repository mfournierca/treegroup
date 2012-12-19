import xml.sax, xml.sax.handler, xml.sax.xmlreader, logging, copy

import TreeGroup.SAX.Operations

#you've got to be careful - to have a coherent algebra, every element
#must be able to act on every other. In the Tree functions, this is accomplished
#by viewing the tree as a non-cyclic graph of nodes, each nodes having the same 
#properties: tag, attributes, text, tail. 
#Processing instructions etc had to be ignored / removed because I couldn't 
#think of a way of coherently defining the notion of adding a processing 
#instruction to an element. Or, maybe I could define it coherently, but not
#usefully. The point of these operations is to get a useful tree at the end, 
#and how do you do that if you add PIs to elements, etc? 
#So below, we assume that trees are composed of nodes, which are composed of 
#tags, attributes, text and tail, and nothing else.  


class SAXIteratorEvent:
    def __init__(self, type=None, **kwargs):
        self._type = type
        self.values = {}
        for key in kwargs.keys():
            if isinstance(kwargs[key], xml.sax.xmlreader.AttributesImpl):
                #set the attributes to a dict - that's what they are, but
                #having the type be xml.sax.xmlreader.AttributesImpl makes 
                #checking equality, adding and inverting harder. 
                self.set(key, dict(kwargs[key]))
            else:
                self.set(key, kwargs[key])
    
    def getType(self):
        return self._type
    
    def set(self, key, value):
        self.values[key] = value
        
    def get(self, key):
        return self.values[key]
    
    def __str__(self):
        s = "%s" % self.__class__
        for k in self.values.keys():
            if isinstance(self.values[k], xml.sax.xmlreader.AttributesImpl):
                s += " %s: '%s'" % (k, str(dict(self.values[k])))
            else:
                s += " %s: '%s'" % (k, str(self.values[k]))
        return s
    
    def __eq__(self, o):
        if not isinstance(o, TreeGroup.SAX.Operations.SAXIteratorEvent):
            print('wrong type')
            return False
        
        if not self.values == o.values:
            print('wrong values: %s\t %s' % (str(self.values), str(o.values)))
            return False
        
        return True
    
    def __ne__(self, o):
        return not self.__eq__(o)
    
    
    
    
class StartDocumentEvent(SAXIteratorEvent):
    def __init__(self):
        super(StartDocumentEvent, self).__init__(type="startDocument")
        
class EndDocumentEvent(SAXIteratorEvent):
    def __init__(self):
        super(EndDocumentEvent, self).__init__(type="endDocument")
        
class StartElementEvent(SAXIteratorEvent):
    def __init__(self, name=None, attr=None):
        super(StartElementEvent, self).__init__(type="startElement", name=name, attr=attr)
        
class EndElementEvent(SAXIteratorEvent):
    def __init__(self, name=None):
        super(EndElementEvent, self).__init__(type="endElement", name=name)
    
class CharactersEvent(SAXIteratorEvent):
    def __init__(self, content=None):
        super(CharactersEvent, self).__init__(type="characters", content=content)



class SAXIterateContentHandler(xml.sax.handler.ContentHandler):
    def __init__(self, list):
        self.list = list

    def startDocument(self):
        pass
        
    def endDocument(self):
        pass
                
    def startElement(self, name, attr):
        self.list.append(StartElementEvent(name=name, attr=attr))
            
    def endElement(self, name): 
        self.list.append(EndElementEvent(name=name))

    def characters(self, content):
        self.list.append(CharactersEvent(content=content))
            
    
#    #not sure if we should keep this one or not. 
#    def ignorableWhitespace(self, whitespace):
#        self.list.append({
#                          "type": "ignorableWhitespace",
#                          "whitespace": whitespace
#                          })

            
    #should raise errors when any of the following are encountered
    #can't have these because we need consistent algebra as outlined 
    #above.         
    
#    def startPrefixMapping(self, prefix, uri):
#        self.list.append({
#                          "type": "startPrefixMapping",
#                          "prefix": prefix,
#                          "uri": uri,
#                          })
#                    
#    def endPrefixMapping(self, prefix):
#        self.list.append({
#                          "type": "endPrefixMapping",
#                          "prefix": prefix,
#                          })
#            
#    def startElementNS(self, name, qname, attrs):
#        self.list.append({
#                          "type": "startElementNS",
#                          "name": name,
#                          "qname": qname,
#                          "attrs": attrs,
#                          })
#            
#    def endElementNS(self, name, qname):
#        self.list.append({
#                          "type": "endElementNS",
#                          "name": name,
#                          "qname": qname,
#                          })
#            
#    def processingInstruction(self, target, data):
#        self.list.append({
#                          "type": "processingInstruction",
#                          "target": target,
#                          "data": data,
#                          })
#    
#    def skippedEntity(self, name):
#        self.list.append({
#                          "type": "skippedEntity",
#                          "name": name,
#                          })
    
    
    
    
    
    
    
class SAXIterator():
    def __init__(self, string):
        self.stringlist = string.split('\n')
        self.stringindex = 0
        
        self.list = []
        self.parser = xml.sax.make_parser()
        self.parser.setContentHandler(SAXIterateContentHandler(self.list))
        
        
    def feedParser(self):
        #nice and simple. We can modify this so that memory is no wasted on the stringlist,
        #and we only work with the string. 
        #does using feed mean that the endDocument event is never created / handled?
        try:
            self.parser.feed(self.stringlist[self.stringindex])
        except IndexError:
            #can't raise StopIteration here because that would cause any remaining content
            #in self.list to not be processed. StopIteration is raised in next()
            pass  
        self.stringindex += 1
        self.joinCharacters()
        
            
    def joinCharacters(self):
        #the sax parser does not necessarily trigger one event for one contiguous string of characters
        #in a document. there may be an element that contains one string that triggers two parsing 
        #events, and therefore two entries in self.list. This is not what we want because it will 
        #make the addition of string much more complicated. This function fixes this. 
        last = 0
        current = 1
        while current < len(self.list):
            if self.list[last].getType() == "characters" and self.list[current].getType() == "characters":
                self.list[last].set("content", self.list[last].get('content') + self.list[current].get('content'))
                self.list.pop(current) #important, pop current not last, otherwise new content is lost. 
            last += 1
            current += 1
            
        
    def next(self):
        #if there is no new content and the list is empty, raise StopIteration
        if len(self.list) == 0 and self.stringindex >= len(self.stringlist):
            raise StopIteration
        
        #if list is empty, feed new content into the sax parser, which 
        #causes the SAXIterateContentHandler to populate the list
        if len(self.list) == 0:
            self.feedParser()
        
        #if the last element in the list is characters, feed more content in
        #until the last element is something else. This avoid problems with the
        #parser not taking all character data all at once
        while self.list[-1].getType() == "characters":
            self.feedParser()
    
        #pop the first item off the list and return it
        return self.list.pop(0)
        
    def __next__(self):
        return self.next()
        
    def __iter__(self):
        return self
        
       



class Ordering:
    #the position of an event is list of integers that specifies an event in a tree
    #by it's "coordinates", each integer represents a node in the tree, the value of the 
    #integer is that node's position under the parent node. [0] is the root node, [0, 0] 
    #is the first element under the root node, [0, 1] is the first element's closing tag etc. 
    #The ordering of a tree is a list of all the positions of every event in the tree, 
    #in document order. 
    #We can't make an ordering as done in the Tree module, because we are not dealing with nodes
    #here. We are dealing with events, so we need a way of comparing two positions to see
    #if we should add two events. It's no good to add an opening tag to a closing tag, 
    #so we need some way of distinguishing them. So the position of an event is a list of
    #integers, each integer being the number of events on that level since the parents 
    #opening tag.  
    #One consequence of this algorithm is that startElements are always in even positions, 
    #closing elements in odd positions. 
    
    #if you want to check syntax while doing the other operations (ie make sure all closing 
    #tags are present, have the right value etc) then this class is the place to do it.
    
    def __init__(self):
        self._position = []
        self._ordering = []
        self.index = -1
        self.log = logging.getLogger()
        
    def updateOrdering(self, event):
        self.updatePosition(event)
        self._ordering.append(copy.copy(self.getCurrentPosition()))    
        
    def updatePosition(self, event):
        if event is None:
            return
    
        log = logging.getLogger()
    
        if event.getType() == "startElement":
            #this lengthens the position, lengthens the index.
            log.debug('found startElement: %s %s' % (str(self.index), str(self._position)))
            
            if self.index + 1 == len(self._position):
                log.debug('\tbranch 1')
                self._position.append(0)
                self.index += 1
            
            elif self.index + 1 < len(self._position):
                #if index is less then the length of position, 
                #it means that this start elemenet has preceding siblings, 
                #so add to the end of position
                log.debug('\tbranch 2')
                self._position[self.index + 1] += 1
                self.index += 1
                
            else: 
                #index should never be greater than the length of _position
                raise ValueError
            
        if event.getType() == "endElement":
            log.debug('found endElement: %s %s' % (str(self.index), str(self._position)))
            self._position = self._position[:self.index + 1]
            self._position[self.index] += 1
            self.index -= 1  
        
        log.debug('\tresult: %s %s' % (str(self.index), str(self._position)))
        
    def getOrdering(self):
        return self._ordering
        
    def __str__(self):
        return str(self._ordering)
       
    def getCurrentPosition(self):
        #copy?
        return self._position
    
    
    
    
class SAXEventAndOrderingIterator:
    """This class combines the SAXIterator and Ordering class functions
    to provide a unified interface for dealing with events and positions. 
    It is very rare that we will want to deal with orderings without also
    dealing with events, and vice versa. This class makes it easy (and  less 
    error prone) to use both together."""
    
    #could use this class to check syntax of tree, also use self._iterator and
    #catch StopIteration, make sure that everything is consistent before raising 
    #it again
    
    def __init__(self, string):
        self._iterator = SAXIterator(string)
        self._ordering = Ordering()
        self._currentevent = None
        
    def next(self):
        """go to the next iteration in the SAXIterator"""
        self._currentevent = self._iterator.next()
        self._ordering.updateOrdering(self._currentevent)
        return self.getCurrentEvent(), self.getCurrentPosition()
    
    def getCurrentEvent(self):
        return self._currentevent
    
    def getCurrentPosition(self):
        return self._ordering.getCurrentPosition() 




def equal(string1, string2):
    """Given two trees defined by string1 and string2, return True if they are equal, False otherwise"""
    iterator1 = SAXIterator(string1)
    iterator2 = SAXIterator(string2)
    
    events1 = []
    for e in iterator1: events1.append(e)
    
    events2 = []
    for e in iterator2: events2.append(e)
    
    if len(events1) != len(events2):
        return False
    
    for i, e in enumerate(events1):
        if e != events2[i]:
            print('%s != %s' % (str(e), str(events2[i])))
            return False
        
    return True
    
    

def addEvents(event1, event2):
    """Add the two events and return a new event. Raise ValueError if the event
    types do not match."""    
    if not type(event1) == type(event2):
        print("%s != %s" % (type(event1), type(event2)))
        raise ValueError
    
    if type(event1).__name__ == "StartElementEvent":
        pass
    
    if type(event1).__name__ == "EndElementEvent":
        pass
    
    


def add(string1, string2):
    """Given two trees defined by string1 and string2, add them together and return the result"""
    iterator1 = SAXEventAndOrderingIterator(string1)
    iterator2 = SAXEventAndOrderingIterator(string2)
    
    result = ""
    
    while True:
        try:
            event1, position1 = iterator1.next()
        except StopIteration:
            event1, position1 = None, None #signal that iterator is stopped
        try:
            event2, position2 = iterator2.next()
        except StopIteration:
            event2, position2 = None, None
        
        #if positions are the same and event types are the same, add and continue
        if position1 == position2:
            new = addEvents(event1, event2)
            
        #if positions are the same and event types are not add appropriately. IE, element should be added after text (?)
        
        #if positions are not equal, start with closest to root position, and call __next__ while adding (appending?) to result
        #until other position is reached or parser stops. If other position is reached, add nodes and continue
        
        #if parser stopped, call __next__ on other tree while adding to result. 
        
        
        
        