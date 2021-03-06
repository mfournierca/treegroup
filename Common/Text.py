import logging

from . import String


#text strings form a group by considering each character in the string to be a
#member of the cyclic group defined by the textdomain list, below. We form
#a group by imagining that strings have an infinite tail of space characters 
#(the unit in the character group. strings are then 
#added character by character, and since every character is a member of a cyclic
#group, the text as a whole forms a group. 

#newlines are ignored here, or converted to the unit character. This is because newlines are 
#not significant in xml anyway, and make checking equality harder as they are often caused
#by line wrap functions in editors and therefore have nothing to do with the actual content. 
#there should be some standards compliant way of dealing with this . . . 
#should we require that every character we can encounter be part of the group? For consistency? 
#it should be safe to completely ignore newlines, if we are consistent. 

#The unit characted is the first element in the domain, ie textdomain[0]. For 
#text strings, this is whitespace, unlike the tags, where the unit is '_'

textdomain = [' '] + ['\t', '‘', '’', '“', '”'] + [i for i in map(chr, range(33, 127))] #[i for i in map(chr, range(97, 123))] + ['-', '_'] + [i for i in map(chr, range(65, 91))]


def isUnitText(text):
    if text == textdomain[0]:
        return True
    else:
        return False
    
    
def getTextDomain():
    return textdomain


def equal(text1, text2):
    return String.equal(text1.replace('\n', ''), text2.replace('/n', ''), textdomain)


def addText(text1, text2):
    """Add two strings and return the result. The addition must be the operation 
    used by a cyclic group over the textdomain"""
    if text1 is None and text2 is None:
        return None
    if text1 is None:
        text1 = ''
    if text2 is None: 
        text2 = ''
    
    #whitespace is sometimes significantWe don't want to remove whitespace, 
    #it is significant in some contexts in some documentation
#    text1 = text1.rstrip()
#    text2 = text2.rstrip()
    
    #first make them the same length
    if len(text1) == len(text2):
        pass
    elif len(text1) > len(text2):
        for i in range(0, len(text1) - len(text2)): text2 += textdomain[0]
    elif len(text1) < len(text2):
        for i in range(0, len(text2) - len(text1)): text1 += textdomain[0]
                
    #then iterate over the characters in text1
    result = ''
    for index, char1 in enumerate(text1):
        if char1 == '\n':
            char1 = textdomain[0]
        char2 = text2[index]
        if char2 == '\n':
            char2 = textdomain[0]
            
        result += String._addchars(char1, char2, textdomain)
        
    result = _cleantext(result)
        
    #add the corresponding character in string 2
    return result.rstrip()


 
def textInverse(text1):
    """Return the inverse of the text. This function closely follows string._stringinverse(), 
    but deals with whitespace that we do not want to invert in document text. Also deals with
    receiving None, which can happen with document text but not, for example, element tags."""
    log = logging.getLogger()
    
    if text1 is None: 
        return None
    
    if text1 == '':
        text1 = textdomain[0]

#    log.debug('inverting: "%s"' % text1)

    #whitespace is significant sometimes. We don't want to remove whitespace, 
    #it is significant in some contexts in some documentation
#    text1 = text1.rstrip()
#    log.debug('rstrip: "%s"' % text1)
    
    result = ''
    for i in text1:
        if i == '\n':
            result += textdomain[0]
        else:
            result += String._characterinverse(i, textdomain)
#        log.debug('"%s"' % result)
#        log.debug('"%s"' % text1)
        
    result = _cleantext(result)
#    log.debug('result: "%s"' % result)
    return result



def _cleantext(text1):
    return String.cleanstring(text1, textdomain)
    