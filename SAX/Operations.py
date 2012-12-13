import xml.sax, xml.sax.handler, xml.sax.xmlreader


class SAXIteratorEvent:
    def __init__(self, type=None, **kwargs):
        self._type = type
        self.values = {}
        for key in kwargs.keys():
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
        
    def startElement(self, name, attr):
        self.list.append(StartElementEvent(name=name, attr=attr))
            
    def endElement(self, name): 
        self.list.append(EndElementEvent(name=name))

    def startDocument(self):
        self.list.append(StartDocumentEvent())
        
    def endDocument(self):
        self.list.append(EndDocumentEvent())
        
    def characters(self, content):
        self.list.append(CharactersEvent(content=content))
            
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
#            
#    def ignorableWhitespace(self, whitespace):
#        self.list.append({
#                          "type": "ignorableWhitespace",
#                          "whitespace": whitespace
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
    #the position of an element is list of integers that specifies an element in a tree
    #by it's "coordinates", each integer represents a node in the tree, the value of the 
    #integer is that node's position under the parent node. [0] is the root node, [0, 0] 
    #is the first element under the root node, etc. 
    #The ordering of a tree is a list of all the positions of every element in the tree, 
    #in document order. 
    
    def __init__(self):
        self._position = []
        self._ordering = []
        self.index = -1
        
    def updateOrdering(self, event):
        self.updatePosition(event)
        self._ordering.append(self.getCurrentPosition())    
    
    def updatePosition(self, event):
        if event is None:
            return
    
        if event.getType() == "startElement":
            #this lengthens the position, lengthens the index.
            self.index += 1
            
            if self.index == len(self._position):
                #if index is the lenght of _position, then this 
                #startElement should go under the last element, 
                #ie the last in _position 
                self._position.append(0)
            elif self.index < len(self._position):
                #if index is less then the length of position, 
                #it means that this start elemenet has preceding siblings, 
                #so add to the end of position
                self._position[self.index + 1] += 1
            else: 
                #index should never be greater than the length of _position
                raise ValueError
            
        if event.getType() == "endElement":
            self._position = self._position[:self.index + 1]
            self.index -= 1  
        
    def getOrdering(self):
        return self._ordering
        
    def __str__(self):
        return str(self._ordering)
       
    def getCurrentPosition(self):
        return self._position[:self.index + 1]
    



def add(string1, string2):
    """Given two trees defined by string1 and string2, add them together and return the result"""
    #this function models a central controller that handles all of the parsers and output building.
    iterator1 = SAXIterator(string1)
    iterator2 = SAXIterator(string2)
    
    position1 = []
    position2 = []
    
    result = ""
    
    while True:
        try:
            event1 = iterator1.next()
        except StopIteration:
            event1 = None #signal that iterator is stopped
        try:
            event2 = iterator2.next()
        except StopIteration:
            event2 = None
        
        #get positions, or more accurately keep track of positions
        position1 = updateOrdering(event1)
        position2 = updateOrdering(event2)
        
        #if positions are the same and event types are the same, add and continue
        
        #if positions are the same and event types are not add appropriately. IE, element should be added after text (?)
        
        #if positions are not equal, start with closest to root position, and call __next__ while adding (appending?) to result
        #until other position is reached or parser stops. If other position is reached, add nodes and continue
        
        #if parser stopped, call __next__ on other tree while adding to result. 
        
        
        
        