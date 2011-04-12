#!/usr/bin/env python3

"""Classes to handle errors - parse error message, get target element, etc."""

import logging, lxml.etree, re

import DitaTools.Tree.File.Dita

class ErrorParser:
    """Find and parse the errors of a tree"""
    
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
        
        #start testing patterns. Each parsing function must return a parent tag, an expectedTags and 
        #an actualTags list, or None if the pattern did not match. 
        for f in [self._parsePattern1, self._parsePattern2]: 
            self._parentTag, self._expectedTags, self._actualTags = f()
            if (not self._expectedTags is None) and (not self._actualTags is None):
                break
        else:
            #no matches
            self.log.debug('no matches found')
            self.targetElement = None
            self.acceptableTags = None
            return False
        
        #parse the actualTags and the expectedTags and get the targetElement and the acceptableTags. 
        #build links between actual and expected.
        #Turn the lists into n x 2 arrays. The second entry will contain the index of the corresponding
        #entry in the other list, if any. 
        self._expectedTags = [[i, None] for i in self._expectedTags]
        self._actualTags = [[i, None] for i in self._actualTags]
        
        #build the links between the two tags lists
        self._buildLinks()
                               
        #the links between the two lists are built. Now we can use this information to get the
        #targetElement and to build the acceptableTags list. We do this by iterating over the 
        #actualTags list and expectedTags lists separately and comparing the results. 
        
        #search the the actualTags list to get the targetElement and acceptableTags list. 
        self.log.debug('finding targetElement')
        self._getTargetAndAcceptableTagsFromActualTags()
#        self._getTargetAndAcceptableTagsFromExpectedTags()







    #===========================================================================
    # functions
    #===========================================================================
    
    def _getTargetAndAcceptableTagsFromActualTags(self):
        targetTag, targetActualIndex = self._actualTagsFindTargetTag()
        targetCandidate = self._actualTagsFindTargetElement(targetActualIndex)
#        self.acceptableTags = self._actualTagsFindAcceptableTags()
        return targetCandidate
    
                
    def _actualTagsFindTargetElement(self, targetActualIndex):
        #now we need to find the targetElement in the tree, which can be tricky. 
        #there may be many elements with the targetTag, not all of which are invalid. 
        #We need to build an xpath expression that will get the targetElement precisely. 
        #To do this, we use that fact that it is the particular arrangement of siblings 
        #and the parent around the targetElement that makes it invalid. So we create an 
        #xpath to find that particular arrangement. 
        #If the parentTag is None, we know that the targetElement is the root. 
        self.log.debug('finding targetElement')
        if self._parentTag is None:   # and len(actualTags) == 0: 
            self.log.debug('\tparentTag is None, targetElement is root')
            self.targetElement = self.tree.getroot()
        else:
            xpath = self._buildXpathFromActualIndex(targetActualIndex)
            self.targetElement = self.tree.xpath(xpath)[0]
            
                
    def _buildXpathFromActualIndex(self, targetActualIndex):
        #build the xpath expression
        self.log.debug('\tbuilding xpath expression')
        xpath = '//%s/%s' % (self._parentTag, self._actualTags[targetActualIndex][0])
        self.log.debug('\txpath: %s' % xpath)
        #to build the xpath expression, we take each of the siblings in order and
        #add them to the appropriate spot in the expression
      
        #add previous siblings first.
        self.log.debug('\tbuilding expression for preceding siblings')
        index = targetActualIndex - 1
        bracketCount = 0
        precedingXpath = ''
        while index >= 0:
            self.log.debug('\t\tindex: %s\ttag: %s' % (str(index), self._actualTags[index][0]))
            precedingXpath = precedingXpath + '[preceding-sibling::*[1][self::%s]' % self._actualTags[index][0]
            index = index - 1
            bracketCount += 1
        for i in range(0, bracketCount): precedingXpath += ']'
        self.log.debug('\t\tpreviousXpath: %s' % precedingXpath)
            
        self.log.debug('\tbuildingexpression for following siblings')
        index = targetActualIndex + 1
        bracketCount = 0
        followingXpath = ''
        while index < len(self._actualTags) - 1:
            self.log.debug('\t\tindex: %s\ttag: %s' % (str(index), self._actualTags[index][0]))
            followingXpath = followingXpath + '[following-sibling::*[1][self::%s]' % self._actualTags[index][0]
            index = index + 1
            bracketCount += 1
        for i in range(0, bracketCount): followingXpath += ']'
        self.log.debug('\t\tfollowingXpath: %s' % followingXpath)
        
        xpath = xpath + precedingXpath + followingXpath
        self.log.debug('xpath: %s' % xpath)
        return xpath
            
            
    def _actualTagsFindTargetTag(self):
        """search the actualTags list for the targetTag, the tag of the targetElement"""
        targetTag = None
        self.log.debug('searching actualTags')
        for index, actual in enumerate(self._actualTags):
            self.log.debug('\ttesting: %s' % str(actual)) 
            if actual[1] is None: 
                self.log.debug('\ttargetTag found: %s' % actual[0])
                #this is the targetElement
                targetTag = actual[0]
                return targetTag, index
            else:
                continue
        else:
            self.log.debug('target not found in actualTags')
            pass
                
        
    def _buildLinks(self):
        #build the links. Iterate over the actualTags array and find what entry in the 
        #expectedTags list it corresponds to, and then write the correspondence into the arrays. 
        #Keep moving up the expectedTags list, so that you do not search through the same section
        #twice. 
        #This is where the *, + and ? characters in the expectedTags list are dealt with. These 
        #these characters follow a tag name or list of names and denote that said tag(s) can be repeated
        #0 -> any number of times, 1 -> any number of times, or 0 -> 1 times, respectively. 
        #This complicates the parsing, since multiple entries in the actualTags list may be linked 
        #to a single entry in the expectedTags list. 
        #To deal with this, repeat the * and + entries when encountered. We don't need to remove the 
        #unused entries because they are relevant to any unlinked actual entries near them. 
        expectedCutoff = 0
        self.log.debug('building links')
        for actualIndex, actual in enumerate(self._actualTags):
            self.log.debug('\tactualIndex: %i\tactual: %s' % (actualIndex, actual))
            self.log.debug('\texpectedCutoff: %i\tlen(self._expectedTags): %i' % (expectedCutoff, len(self._expectedTags)))
            if expectedCutoff > len(self._expectedTags) + 1: break
            
            pattern = r'[\s\(]%s[^\w]' % actual[0]
            self.log.debug('\tattempting to match expected, pattern: %s' % pattern)
            for expectedIndex, expected in enumerate(self._expectedTags):
                #we could use a slice of the expectedTags above, but that would not give us the
                #correct index, which is useful for logging. The line below deals with this. 
                if expectedIndex < expectedCutoff: continue
                self.log.debug('\t\texpectedIndex: %i\texpected: %s' % (expectedIndex, expected[0]))
                if re.search(pattern, expected[0]): 
                    self.log.debug('\t\tmatched actual')
                    self._actualTags[actualIndex][1] = expectedIndex
                    self._expectedTags[expectedIndex][1] = actualIndex
                    #if expected[0] ends with ?, * or +, take the appropriate action
                    if expected[0].endswith('?'): 
                        pass
                    elif expected[0].endswith('*'):
                        self._expectedTags.insert(expectedIndex + 1, [expected[0], None])
                    elif expected[0].endswith('+'):
                        self._expectedTags.insert(expectedIndex + 1, [expected[0], None])
                    expectedCutoff = expectedIndex + 1
                    break
            else:
                self.log.debug('\tno match found')
        
        #debug output
        self.log.debug('links built.')
        self.log.debug('actualTags links:')
        for entry in self._actualTags: 
            if entry[1] is not None: 
                self.log.debug('\t%s -> %s: %s' % (entry[0], entry[1], self._expectedTags[entry[1]][0]))
            else:
                self.log.debug('\t%s -> %s: %s' % (entry[0], str(None), str(None)))
        self.log.debug('expectedTags links:')
        for entry in self._expectedTags: 
            if entry[1] is not None: 
                self.log.debug('\t%s -> %s: %s' % (entry[0], entry[1], self._actualTags[entry[1]][0]))
            else:
                self.log.debug('\t%s -> %s: %s' % (entry[0], str(None), str(None)))   






    #===========================================================================
    # pattern parsers. Each pattern parser must parse the error and return the parentTag, 
    # the tag of the parent of the targetElement; the expectedTags, the order list of tags that
    # the validator expected for the children of the parent; and the actualTags, a list of tags
    # that the validator actually found under the parent.
    #===========================================================================
    
    def _parsePattern1(self):
        pattern = r'.*?\:\d*\:\d*:ERROR:VALID:DTD_CONTENT_MODEL: Element (.*?) content does not follow the DTD, expecting (.*), got \((.*?)\)'
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
        pattern = r'.*?\:\d*:\d*:ERROR:VALID:DTD_UNKNOWN_ELEM: No declaration for element (.*)'
        self.log.debug('testing pattern: %s' % str(pattern))
        match = re.search(pattern, self.errorMessage)
        if not match: return None, None, None
        actualTag = match.group(1)
        candidates = self.tree.xpath('//%s' % actualTag)
        if (len(candidates) > 1) or (not candidates[0] is self.tree.getroot()):
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
        return None, expectedTags, self._actualTags
        
                
     