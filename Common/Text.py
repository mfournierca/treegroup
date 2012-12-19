import logging

from . import String


#text strings form a group by considering each character in the string to be a
#member of the cyclic group defined by the textdomain list, below. We form
#a group by imagining that strings have an infinite tail of space characters 
#(the unit in the character group. strings are then 
#added character by character, and since every character is a member of a cyclic
#group, the text as a whole forms a group. 

#The unit characted is the first element in the domain, ie textdomain[0]. For 
#text strings, this is whitespace, unlike the tags, where the unit is '_'

textdomain = [' '] + ['\t', '‘', '’', '“', '”'] + [i for i in map(chr, range(33, 127))] #[i for i in map(chr, range(97, 123))] + ['-', '_'] + [i for i in map(chr, range(65, 91))]


def getTextDomain():
    return textdomain




def _addtext(text1, text2):
    """Add two strings and return the result. The addition must be the operation 
    used by a cyclic group over the textdomain"""
    if text1 is None and text2 is None:
        return None
    if text1 is None:
        text1 = ''
    if text2 is None: 
        text2 = ''
    
    #whitespace is sometimes significant
#    #we are not interested in trailing whitespace. 
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


 
def _textinverse(text1):
    """Return the inverse of the text. This function closely follows string._stringinverse(), 
    but deals with whitespace that we do not want to invert in document text. Also deals with
    receiving None, which can happen with document text but not, for example, element tags."""
    if text1 is None: 
        return None
    log = logging.getLogger()
#    log.debug('inverting: "%s"' % text1)

    #whitespace is significant sometimes. 
#    text1 = text1.rstrip()
#    log.debug('rstrip: "%s"' % text1)
    
    result = ''
    for i in text1:
        if i == '\n':
            result += i
        else:
            result += String._characterinverse(i, textdomain)
#        log.debug('"%s"' % result)
#        log.debug('"%s"' % text1)
        
    result = _cleantext(result)
#    log.debug('result: "%s"' % result)
    return result



def _cleantext(text1):
    return String.cleanstring(text1, textdomain)
    