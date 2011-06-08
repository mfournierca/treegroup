#!/usr/bin/env python3

"""Classes to handle errors - parse error message, get target element, etc."""

import logging, lxml.etree, re

import DitaTools.Tree.File.Dita






#===============================================================================
# error parser root class
#===============================================================================






class ErrorParserRootClass:
    def __init__(self):
        pass
    
    






    
#===============================================================================
# error parser  
#===============================================================================

class ErrorParser(ErrorParserRootClass):
    
    def __init__(self, tree):
        self.tree = tree
        self.log = logging.getLogger()
    
    
    
    
    def parse(self):
        """validate the tree and parse the first error message. This must create 
        the target element and a list of acceptable tags for that element. """
        
        #this function assigns targetElement and acceptableTags if parsing is 
        #successful, otherwise they remain None
        self.targetElement = None
        self.acceptableTags = None
        
        self.log.debug('validating tree with dita version 1.1')
        errors = DitaTools.Tree.File.Dita.v11_validate(self.tree)
        self.errorMessage = errors[0]
        self.log.debug('first error message: %s' % self.errorMessage)
        
        patternparser = PatternParser()
        self._parentTag, self._expectedTags, self._actualTags = patternparser.parse(self.errorMessage, self.tree)
        if (self._expectedTags is None) and (self._actualTags is None):
            return False
        
        self.log.debug('finding targetElement')
        targetCandidate1, acceptableTagsCandidate1, actualIndex1 = self.parseActualTags()
        targetCandidate2, acceptableTagsCandidate2, actualIndex2 = self.parseExpectedTags()

        #choose which targetCandidate to use. 
        if targetCandidate2 is None: 
            self.log.debug('targetCandidate2 is None, targetCandidate1 is targetElement: %s' % str(targetCandidate1))
            self.targetElement = targetCandidate1
            self.acceptableTags = acceptableTagsCandidate1
            return True
        elif targetCandidate1 is None: 
            self.log.debug('targetCandidate1 is None, targetCandidate2 is targetElement: %s' % str(targetCandidate2))
            self.targetElement = targetCandidate2
            self.acceptableTags = acceptableTagsCandidate2
            return True
        else:
            #if both returned a target, then take the one that comes first in the actualTags
            if actualIndex1 <= actualIndex2:
                self.log.debug('actualIndex1 <= actualIndex2, targetCandidate1 is targetElement: %s' % str(targetCandidate1))
                self.targetElement = targetCandidate1
                self.acceptableTags = acceptableTagsCandidate1
                return True
            else:
                self.log.debug('actualIndex1 > actualIndex2, targetCandidate2 is targetElement: %s' % str(targetCandidate2))
                self.targetElement = targetCandidate2
                self.acceptableTags = acceptableTagsCandidate2
                return True
            
            
            
            
            
    def parseActualTags(self):
        """Parse the actual tags to determine the targetElement and acceptable tags"""
        
        targetElement = None
        acceptableTags = None
        
        self.log.debug('parsing actualTags')
        #set expectedIndex = 0. This will be used to determine the acceptable tags. 
        expectedIndex = 0
        for actualIndex, actualEntry in enumerate(self._actualTags):
        
            self.log.debug('checking actual entry %s' % actualEntry)
            self.log.debug('expectedTags remaining: %s' % str(self._expectedTags[expectedIndex:]))
            
            
            #check [expectedIndex:next mandatory or end] slice until match or end
            expectedSlice = self._buildExpectedSlice(expectedIndex)
            self.log.debug('\tcorresponding expected slice: %s' % str(expectedSlice))
            
            
            #now try to find a match
            matchIndex = None
            for i, e in enumerate(expectedSlice):
                #check for match
                if re.search(r'[\s\(]+%s[\s\)]+' % actualEntry, e):
                    #actualEntry was found in this expected entry.
                    #i is counted from the beginning of the slice, not the list. We need to account for this 
                    matchIndex = i + expectedIndex
                    break
            
    
            #match found?
            if matchIndex is not None:
                self.log.debug('\tfound match, %s is not target element' % actualEntry)
                #reset expectedIndex to match if necessary (on ? and mandatory, not + and *)
                #expectedIndex is what entry in expectedTags we check the acceptableTags against.
                #Since + and * in the expectedTags allows for more than on corresponding actualTag, 
                #we do not increment if those symbols are present. 
                if re.search(r'[\w|\?|\)]\s*$', self._expectedTags[matchIndex]):
                    self.log.debug('\texpected entry is non-repeating, resetting expectedIndex')
                    expectedIndex = matchIndex + 1
                else:
                    self.log.debug('\texpected entry is allowed to repeat')
                    pass
                continue
                
            else:
                #actualEntry is target element
                self.log.debug('\t%s is target element' % actualEntry)
                
                #now we need to decide on the acceptableTags. There are a few ways of doing
                #this, all with different effect. 
                
                #1) Just find the first mandatory entry in the array slice and take that. 
                #Obviously we want to use the mandatory entries, so that is an advantage. 
                #However, this ignores other 
                #information about the tree. If a non-mandatory entry is first in the slice, 
                #then we may actually want the tree to use that and then use the mandatory entry 
                #on a later element. Trying to make this decision here would be very complicated. 
                
                #2) Just return the whole slice. 
                #If we take this approach, then the AStarTransform program would have to implement
                #some kind of cost-assigning function at later steps. This is probably the best approach.
                
                #3) Take the slice up to and including the first mandatory. This is just a variation on the
                #other 2. 
                
                #There are more options here, this decision in the program is probably going to need
                #tweaking. 
                
                #We are taking option 2 for now. 
                acceptableTags = self._buildAcceptableTagsFromSlice(expectedSlice)
                targetElement = self._findTargetElementFromActualIndex(actualIndex)
                break
        
        self.log.debug('found targetElement: %s' % str(targetElement))
        self.log.debug('found acceptableTags: %s' % str(acceptableTags))
        return targetElement, acceptableTags, actualIndex
    
    
    
    
    
    
    
    def parseExpectedTags(self):
        targetElement = None
        acceptableTags = None
        
        #set actualIndex = 0
        actualIndex = 0
        expectedIndex = 0 
        
        self.log.debug('parsing expected Tags')
        
        while expectedIndex < len(self._expectedTags):
            #check if actualIndex has exceeded the length of actualTags
            if actualIndex >= len(self._actualTags): 
                #check if there are any mandatory entries left in expected tags, if so, last entry in
                #actual tags is target
                for i, e in enumerate(self._expectedTags[expectedIndex:]):
                    #check for mandatory
                    if re.search(r'[\w|+|\)]+\s*$', e):
                        #this is a mandatory element
                        self.log.debug('last actual tag reached, but still mandatory entries in expected')
                        break
                else:
                    self.log.debug('last actual reached and no mandatory in expected.')
                    return None, None, len(self._actualTags) - 1
                
                expectedSlice = self._buildExpectedSlice(expectedIndex)
                acceptableTags = self._buildAcceptableTagsFromSlice(expectedSlice)
                targetElement = self._findTargetElementFromActualIndex(len(self._actualTags) - 1)
                break
            else:
                pass
                
            self.log.debug('checking %s' % str(self._expectedTags[expectedIndex]))
            #check actualIndex. Match? 
            if re.search(r'[\s\(]+%s[\s\)]+' % self._actualTags[actualIndex], self._expectedTags[expectedIndex]):
                self.log.debug('\texpected entry matched actual entry: %s' % self._actualTags[actualIndex])
                #set actualIndex +=1 
                actualIndex += 1
                #if expected entry is * or +, keep index the same. Otherwise increment. 
                if re.search(r'[\w|\?|\)]\s*$', self._expectedTags[expectedIndex]):
                      expectedIndex += 1
                      self.log.debug('\texpected entry is mandatory, incrementing expectedIndex=%s' % str(expectedIndex))
                else:
                      self.log.debug('\texpected entry is not mandatory')
                 
            
            
            else:
                #check expected list [index:next mandatory or end] slice against actualIndex until match or end
                #find next mandatory and build slice
                self.log.debug('\texpected entry did not match actual')
                expectedSlice = self._buildExpectedSlice(expectedIndex)
                
                self.log.debug('\tsearching for matches in slice: %s' % str(expectedSlice))
                #now try to find a match
                matchIndex = None
                for i, e in enumerate(expectedSlice):
                    #check for match
                    if re.search(r'[\s\(]+%s[\s\)]+' % self._actualTags[actualIndex], e):
                        #actualEntry was found in this expected entry.
                        #i is counted from the beginning of the slice, not the list. We need to account for this 
                        matchIndex = i + expectedIndex
                        break
                
                if matchIndex is not None:
                    self.log.debug('\tfound match at index %i' % matchIndex)
                    #set actualIndex +=1 
                    actualIndex += 1
                    #set index to match index
                    expectedIndex = matchIndex + 1
                else:
                    #if no match, actualIndex is targetElement
                    self.log.debug('\tno match found, actual entry is target')
                    
                    #See above for discussion of how to decide acceptableTags
                    acceptableTags = self._buildAcceptableTagsFromSlice(expectedSlice)
                    targetElement = self._findTargetElementFromActualIndex(actualIndex)
                    break
                
                
            self.log.debug('expectedIndex = %i' % expectedIndex)
            self.log.debug('len(self._expectedTags = %i' % len(self._expectedTags))
            self.log.debug('actualIndex  = %i' % actualIndex)
            self.log.debug('len(self._actualTags) = %i' % len(self._actualTags))
            
        self.log.debug('found targetElement: %s' % str(targetElement))
        self.log.debug('found acceptableTags: %s' % str(acceptableTags))
        return targetElement, acceptableTags, actualIndex
            
         
         
    def _buildExpectedSlice(self, startIndex):
        for i, e in enumerate(self._expectedTags[startIndex:]):
            #check for mandatory
            if re.search(r'[\w|+|\)]+\s*$', e):
                #this is the next mandatory entry in the list.
                break
        #i counts from the beginning of the slice, so we have to account for this and 
        #add expectedIndex
        slice = self._expectedTags[startIndex:startIndex + i + 1]
        return slice
           
           
    def _buildAcceptableTagsFromSlice(self, slice):
        acceptableTags = []
        #clean up the expectedSlice
        for i, a in enumerate(slice): 
            temp = re.sub(r'[\*\?|\+|\(|\)\,]*', '', a).split(' ')
            for t in temp: 
                if t != '': acceptableTags.append(t) 
        acceptableTags.sort() 
        return acceptableTags
    
    
    def _findFirstMandatoryInSlice(self, slice):
        pass
    
    
    def _findFirstNonRepeatingInSlice(self, slice):
        pass
    
    

    def _findTargetElementFromActualIndex(self, targetActualIndex):
        #now we need to find the targetElement in the tree, which can be tricky. 
        #there may be many elements with the targetTag, not all of which are invalid. 
        #We need to build an xpath expression that will get the targetElement precisely. 
        #To do this, we use that fact that it is the particular arrangement of siblings 
        #and the parent around the targetElement that makes it invalid. So we create an 
        #xpath to find that particular arrangement. 
        #If the parentTag is None, we know that the targetElement is the root. 
        
#        self.log.debug('finding targetElement from actualTags')
        if self._parentTag is None:   # and len(actualTags) == 0: 
#            self.log.debug('\tparentTag is None, targetElement is root')
            try:
                #the funtion should work whether or not self.tree is an lxml.ElementTree
                #object or an lxml.Element object. The try statement deals with this. 
                #AttributeError is raised if self.tree is an element
                target = self.tree.getroot()
            except AttributeError:
                target = self.tree
        else:
            xpath = self._buildXpathFromActualIndex(targetActualIndex)
#            self.log.debug('\txpath: %s' % xpath)
            target = self.tree.xpath(xpath)[0]
#        self.log.debug('\tfound target: %s' % str(target))
        return target
                
                
    def _buildXpathFromActualIndex(self, targetActualIndex):
        #build the xpath expression
        
        self.log.debug('building xpath expression')
        xpath = '//%s/%s' % (self._parentTag, self._actualTags[targetActualIndex])
        self.log.debug('\txpath: %s' % xpath)
        #to build the xpath expression, we take each of the siblings in order and
        #add them to the appropriate spot in the expression
      
        #add previous siblings first.
        self.log.debug('\tbuilding expression for preceding siblings')
        index = targetActualIndex - 1
        bracketCount = 0
        precedingXpath = ''
        while index >= 0:
            self.log.debug('\t\tindex: %s\ttag: %s' % (str(index), self._actualTags[index]))
            precedingXpath = precedingXpath + '[preceding-sibling::*[1][self::%s]' % self._actualTags[index]
            index = index - 1
            bracketCount += 1
        for i in range(0, bracketCount): precedingXpath += ']'
        self.log.debug('\t\tpreviousXpath: %s' % precedingXpath)
            
        self.log.debug('\tbuildingexpression for following siblings')
        index = targetActualIndex + 1
        bracketCount = 0
        followingXpath = ''
        while index < len(self._actualTags) - 1:
            self.log.debug('\t\tindex: %s\ttag: %s' % (str(index), self._actualTags[index]))
            followingXpath = followingXpath + '[following-sibling::*[1][self::%s]' % self._actualTags[index]
            index = index + 1
            bracketCount += 1
        for i in range(0, bracketCount): followingXpath += ']'
        self.log.debug('\t\tfollowingXpath: %s' % followingXpath)
        
        xpath = xpath + precedingXpath + followingXpath
        self.log.debug('xpath: %s' % xpath)
        return xpath
                
        
  





















#===============================================================================
# class for parsing error patterns
#===============================================================================

            
            
class PatternParser:
    
    def __init__(self):
        """A class to control the parsing of the actual error strings"""
        self.log = logging.getLogger()
    
    def parse(self, error, tree):
        """parse the error string"""
        
        self.errorMessage = error
        self.tree = tree
        for f in [self._parsePattern1, self._parsePattern2, self._parsePattern3, self._parsePattern4]: 
            parentTag, expectedTags, actualTags = f()
            if (not expectedTags is None) and (not actualTags is None):
                break

        return parentTag, expectedTags, actualTags
    
    
    #===========================================================================
    # pattern parsers. Each pattern parser must parse the error and return the parentTag, 
    # the tag of the parent of the targetElement; the expectedTags, the order list of tags that
    # the validator expected for the children of the parent; and the actualTags, a list of tags
    # that the validator actually found under the parent.
    #===========================================================================
    
    def _parsePattern1(self):
        pattern = r'.*?\:\d*\:\d*\:ERROR:VALID\:DTD_CONTENT_MODEL\: Element (.*?) content does not follow the DTD, expecting (.*), got \((.*?)\)'
        self.log.debug('testing pattern: %s' % str(pattern))
        match = re.search(pattern, self.errorMessage)
        if not match: return None, None, None
        expectedTags = match.group(2).split(',')
        actualTags = match.group(3).strip().split(' ')
        parentTag = match.group(1)
        self.log.debug('pattern matched')
        self.log.debug('\tparentTag: %s' % parentTag)
        self.log.debug('\tactualTags: %s' % str(actualTags))
        self.log.debug('\texpectedTags: %s' % str(expectedTags))
        return parentTag, expectedTags, actualTags

    def _parsePattern2(self):
        pattern = r'.*?\:\d*\:\d*\:ERROR:VALID\:DTD_UNKNOWN_ELEM\: No declaration for element (.*)'
        self.log.debug('testing pattern: %s' % str(pattern))
        match = re.search(pattern, self.errorMessage)
        if not match: return None, None, None
        actualTag = match.group(1)
        candidates = self.tree.xpath('//%s' % actualTag)
        try:
            #This functions should work if passed an lxml tree object or an element is passed. 
            #We need to test against the root below, so first we find the root. AttributeErorr is 
            #raised if self.tree is an element
            actualroot = self.tree.getroot()
        except AttributeError:
            actualroot = self.tree
        if (len(candidates) > 1) or (not candidates[0] is actualroot):
            self.log.debug('pattern matched, but could not find expectedTags or actualTags')
            return None, None, None
        parentTag = None
        expectedTags = ['dita']
        actualTags = [actualTag]
        self.log.debug('pattern matched')
        self.log.debug('\tparentTag: %s' % str(parentTag))
        self.log.debug('\tactualTags: %s' % str(actualTags))
        self.log.debug('\texpectedTags: %s' % str(expectedTags))
        #return None as parent because this is the root. 
        return None, expectedTags, actualTags
        
    def _parsePattern3(self):
        pattern = r'.*?\:\d*\:\d*\:ERROR:VALID\:DTD_CONTENT_MODEL\: Element (.*?) content does not follow the DTD, expecting (.*), got '
        self.log.debug('testing pattern: %s' % str(pattern))
        match = re.search(pattern, self.errorMessage)
        if not match: return None, None, None
        #if this matched then the error is caused by an element that
        #should have children, but doesn't. We've only got information about what 
        #children that element was expected, not what it's parent was expecting. So the
        #element in question should not be the targetElement because we can't build and 
        #acceptableTags list for it. 
        #Therefore, what do we do? We want the targetElement to be beneath the element in 
        #question, but it does not have any children. 
        #The solution is to append the unit element beneath the empty element. 
        #The unit element then becomes the targetElement
        expectedTags = match.group(2).split(',')
        parentTag = match.group(1)
        self.log.debug('pattern matched')
        self.log.debug('no actualTags found. Appending unit node.')
        unitnode = lxml.etree.Element('_')
        #this xpath returns nodes with parentTag that have no children, of 
        #which the element in question is the first. 
        self.tree.xpath('//%s[not(*)]' % parentTag)[0].append(unitnode)
        actualTags = ['_']
        self.log.debug('\tparentTag: %s' % parentTag)
        self.log.debug('\tactualTags: %s' % str(actualTags))
        self.log.debug('\texpectedTags: %s' % str(expectedTags))
        return parentTag, expectedTags, actualTags
    
    def _parsePattern4(self):
        pattern = r'.*?\:\d*\:\d*\:ERROR\:VALID\:DTD_INVALID_CHILD\: Element (.*?) is not declared in (.*?) list of possible children'
        self.log.debug('testing pattern: %s' % str(pattern))
        match = re.search(pattern, self.errorMessage)
        if not match: return None, None, None
        #If match, then it gets tricky. This pattern does not give any indication of what
        #element is expected, so we need to guess. For now, the only guess we make is that
        #if this is the root, it should be dita. 
        #The xpath below should match at least once, and the target element should be the first match
        element = self.tree.xpath('//%s/%s' % (match.group(2), match.group(1)))[0]
        if (self.tree.getroot() is element.getparent()) and (not element.getparent().tag in ['dita', 'topic', 'task']):
            parentTag = None
            expectedTags = ['dita']
            actualTags = [match.group(2)]
        else:
            parentTag = None
            expectedTags = None
            actualTags = None
        self.log.debug('\tparentTag: %s' % parentTag)
        self.log.debug('\tactualTags: %s' % str(actualTags))
        self.log.debug('\texpectedTags: %s' % str(expectedTags))
        return parentTag, expectedTags, actualTags
    
    
    
    
    
    
    