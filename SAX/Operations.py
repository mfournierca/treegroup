import xml.sax, xml.sax.handler, xml.sax.xmlreader, logging, copy

import TreeGroup.SAX.Operations

import TreeGroup.Common.Tag as Tag
import TreeGroup.Common.Text as Text
import TreeGroup.Common.Attrib as Attrib

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
    def __init__(self):
        pass
    
    def getEventName(self):
        return type(self).__name__
    
    def __eq__(self, o):
        raise NotImplementedError
    
    def __ne__(self, o):
        return not self.__eq__(o)
    
    def toString(self):
        raise NotImplementedError
    
    
    
class StartDocumentEvent(SAXIteratorEvent):
    def __init__(self):
        super(StartDocumentEvent, self).__init__()
    
        
class EndDocumentEvent(SAXIteratorEvent):
    def __init__(self):
        super(EndDocumentEvent, self).__init__()
    
    
class StartElementEvent(SAXIteratorEvent):
    def __init__(self, tag, attr={}, text=''):
        super(StartElementEvent, self).__init__()
        self.tag = tag
        self.attr = dict(attr)
        self.text = text
        
    def toString(self):
        return "<%s%s>%s" % (self.tag, ''.join([" %s=\"%s\"" % (k, self.attr[k]) for k in self.attr.keys()]), self.text)
            
    def __eq__(self, o):
        if type(self) == type(o) and Tag.equal(self.tag, o.tag) and Attrib.equal(self.attr, o.attr) and Text.equal(self.text, o.text):
            return True
        else:
            return False
        
            
class EndElementEvent(SAXIteratorEvent):
    def __init__(self, tag, text=''):
        super(EndElementEvent, self).__init__()
        self.tag = tag
        self.text = text
        
    def toString(self):
        return "</%s>%s" % (self.tag, self.text)
    
    def __eq__(self, o):
        if type(self) == type(o) and Tag.equal(self.tag, o.tag) and Text.equal(self.text, o.text):
            return True
        else:
            return False
        


class SAXIterateContentHandler(xml.sax.handler.ContentHandler):
    def __init__(self, list):
        self._list = list

    def startDocument(self):
        pass
        
    def endDocument(self):
        pass
                
    def startElement(self, tag, attr):
        self._list.append(StartElementEvent(tag=tag, attr=attr))
            
    def endElement(self, tag): 
        self._list.append(EndElementEvent(tag=tag))

    def characters(self, content):
        #in the add() function below, if we include characters as a separate event then it makes the operation
        #much harder - we have to think about how to handle characters in the same position as opening and 
        #closing tags, etc. If we include the characters as part of the elements however, so they do 
        #not have a position or event associated with them, then it makes if much easier to operate on. 
        #So for all the character events, we move their text into the previous event, whether it be
        #an opening tag, closing tag, etc. 
        #also ignore leading / trailing whitepsace and newlines
        self._list[-1].text += content.strip()
            
    
    #not sure if we should keep this one or not. 
    def ignorableWhitespace(self, whitespace):\
        pass

            
    #should raise errors when any of the following are encountered
    #can't have these because we need consistent algebra as outlined 
    #above.         
    
#    def startPrefixMapping(self, prefix, uri):
#        self._list.append({
#                          "type": "startPrefixMapping",
#                          "prefix": prefix,
#                          "uri": uri,
#                          })
#                    
#    def endPrefixMapping(self, prefix):
#        self._list.append({
#                          "type": "endPrefixMapping",
#                          "prefix": prefix,
#                          })
#            
#    def startElementNS(self, name, qname, attrs):
#        self._list.append({
#                          "type": "startElementNS",
#                          "name": name,
#                          "qname": qname,
#                          "attrs": attrs,
#                          })
#            
#    def endElementNS(self, name, qname):
#        self._list.append({
#                          "type": "endElementNS",
#                          "name": name,
#                          "qname": qname,
#                          })
#            
#    def processingInstruction(self, target, data):
#        self._list.append({
#                          "type": "processingInstruction",
#                          "target": target,
#                          "data": data,
#                          })
#    
#    def skippedEntity(self, name):
#        self._list.append({
#                          "type": "skippedEntity",
#                          "name": name,
#                          })
    
    
    
    
    
    
    
class SAXIterator():
    def __init__(self, string):
        self.log = logging.getLogger()
        
        self._list = []
        self.parser = xml.sax.make_parser()
        self.parser.setContentHandler(SAXIterateContentHandler(self._list))
        
        #it would be good to have some sort of iterative parser using the parser.feed()
        #method to avoid loading all events in memory (ie self._list) at once. However, 
        #because of the way the content handler handles character events (it appends the
        #character data to the text attribute of the last seen event), it requires that 
        #there always be at least one event available to append character data to. So 
        #using the feed() method gets complicated - we've got to make sure there's always at 
        #least one element in the list. Would have to come up with something that always keeps
        #an event in the list until the endDocument event is found. 
        
        #skip this problem for now and do it the easy way. The command below
        #causes the parser to run, which causes the content handler to fill up self._list
        #with all the events in the tree. This is an obvious
        #place to implement a speed up / memory usage fix.
        xml.sax.parseString(string.encode('utf-8'), SAXIterateContentHandler(self._list))
        
    def setUpFeed(self, string):
        self.stringlist = string.split('\n')
        self.stringindex = 0
        
    def feedParser(self):
        #NOT CURRENTLY IN USE
        #nice and simple. We can modify this so that memory is no wasted on the stringlist,
        #and we only work with the string. 
        #does using feed mean that the endDocument event is never created / handled?
        #the use case for this function is in next(), whenever self._list is empty, 
        #feed some more content in. 
        while len(self._list) == 0:
            try:
                self.log.debug('feeding %i: %s' % (self.stringindex, str(self.stringlist[self.stringindex])))
                self.parser.feed(self.stringlist[self.stringindex])
            except IndexError:
                #can't raise StopIteration here because that would cause any remaining content
                #in self._list to not be processed. StopIteration is raised in next()
                self.log.debug('feeding %i: IndexError' % self.stringindex)
                return False
            self.stringindex += 1
        return True
    
        
    def next(self):
        try:
            return self._list.pop(0)
        except IndexError:
            raise StopIteration    
        
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
    
        if event.getEventName() == "StartElementEvent":
            #this lengthens the position, lengthens the index.
            if self.index + 1 == len(self._position):
                self._position.append(0)
                self.index += 1
            
            elif self.index + 1 < len(self._position):
                #if index is less then the length of position, 
                #it means that this start elemenet has preceding siblings, 
                #so add to the end of position
                self._position[self.index + 1] += 1
                self.index += 1
                
            else: 
                #index should never be greater than the length of _position
                raise ValueError
            
        elif event.getEventName() == "EndElementEvent":
            self._position = self._position[:self.index + 1]
            self._position[self.index] += 1
            self.index -= 1  
        
        else:
            raise ValueError
        
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
        self.log = logging.getLogger()
        self._iterator = SAXIterator(string)
        self._ordering = Ordering()
        self._currentevent = None
        
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()
        
    def next(self):
        """go to the next iteration in the SAXIterator"""
        self._currentevent = self._iterator.next()
        self._ordering.updateOrdering(self._currentevent)
        self.log.debug('%s %s' % (str(self.getCurrentEvent()), str(self.getCurrentPosition())))
        return self.getCurrentEvent(), self.getCurrentPosition()
    
    def getCurrentEvent(self):
        return self._currentevent
    
    def getCurrentPosition(self):
        return self._ordering.getCurrentPosition() 

    def getCurrentOrdering(self):
        return self._ordering.getOrdering()
    
    
    
    
    


def equal(string1, string2):
    """Given two trees defined by string1 and string2, return True if they are equal, False otherwise"""
    iterator1 = SAXIterator(string1)
    iterator2 = SAXIterator(string2)
    
    for event1 in iterator1:
        try:
            event2 = iterator2.next()
        except: 
            return False
        
        if event1 != event2:
            return False

    return True
    
    
    
    
    

def addEvents(event1, event2):
    """Add the two events and return a new event. Raise TypeError if the event
    types do not match."""    
    import TreeGroup.Common.Attrib as Attrib
    import TreeGroup.Common.Tag as Tag
    import TreeGroup.Common.Text as Text
    
    if not type(event1) == type(event2):
        print("%s != %s" % (type(event1), type(event2)))
        raise TypeError
    
    if event1.getEventName() == "StartElementEvent":
        newevent = StartElementEvent(Tag.addTags(event1.tag, event2.tag), Attrib.addAttribs(event1.attr, event2.attr), Text.addText(event1.text, event2.text))
        return newevent
    
    elif event1.getEventName() == "EndElementEvent":
        newevent = EndElementEvent(Tag.addTags(event1.tag, event2.tag), Text.addText(event1.text, event2.text))
        return newevent
    
    else:
        raise TypeError("Invalid event type: %s" % str(event1))





def getOrdering(tree):
    """just a convenience function initially built for unit tests"""
    iterator = SAXEventAndOrderingIterator(tree)
    for i in iterator:
        pass
    return iterator.getCurrentOrdering()





def add(string1, string2):
    """Given two trees defined by string1 and string2, add them together and return the result"""
    
    log = logging.getLogger()
    
    iterator1 = SAXEventAndOrderingIterator(string1)
    iterator2 = SAXEventAndOrderingIterator(string2)
    
    result = ""
    
    while True:
        
        #this method relies on the two iterators being in the same position 
        #at the start of every iteration through this loop. 
        
        try:
            event1, position1 = iterator1.next()
        except StopIteration:
            event1, position1 = None, None #signal that iterator is stopped
        try:
            event2, position2 = iterator2.next()
        except StopIteration:
            event2, position2 = None, None
        
        if event1 == None and event2 == None:
            break
        elif event1 == None and event2 != None:
            raise ValueError
        elif event1 != None and event2 == None:
            raise ValueError
        
        log.debug('')
        log.debug('position1: %s event1: %s' % (str(position1), event1.toString()))
        log.debug('position2: %s event2: %s' % (str(position2), event2.toString()))
        
        #if positions are the same and event types are the same, add and continue
        if position1 == position2 and type(event1) == type(event2):
            newevent = addEvents(event1, event2)
            
        #if positions are different, iterate over the lower event until the other positions is reached. 
        if position1 != position2:
            #figure out which one is before the other . . . should be the one with the longer position, deeper in the tree
            #will the positions always be of different lengths at this point? Yes - the iterators start at the same position
            #at the start of the loop. If after next()ing the iterators the positions are different, they must be of different
            #length because there are only three ways to go in the tree: down, sideways or up, each of which results in a position
            #of a different length. Since the positions started out the same, then only the last index will be different
            if len(position1) > len(position2):
                move = iterator1
                hold = iterator2
            elif len(position1) < len(position2):
                move = iterator2
                hold = iterator1
            else:
                raise ValueError
            
            while move.getCurrentPosition() != hold.getCurrentPosition():
                log.debug('\tposition: %s event: %s' % (str(move.getCurrentPosition()), move.getCurrentEvent().toString()))
                result += move.getCurrentEvent().toString()
                #should never encounter StopIteration here
                e, p = move.next()
            
            newevent = addEvents(e, hold.getCurrentEvent())
            
        #if positions are not equal, start with closest to root position, and call __next__ while adding (appending?) to result
        #until other position is reached or parser stops. If other position is reached, add nodes and continue
        
        #if parser stopped, call __next__ on other tree while adding to result. 
        
        result += newevent.toString()
    
    log.debug('')
    log.debug("result: %s" % result)
    return result
        
        
        