from . import String


#text strings form a group by considering each character in the string to be a
#member of the cyclic group defined by the textdomain list, below. We form
#a group by imagining that strings have an infinite tail of space characters 
#(the unit in the character group. strings are then 
#added character by character, and since every character is a member of a cyclic
#group, the text as a whole forms a group. 

#The unit characted is the first element in the domain, ie textdomain[0]. For 
#text strings, this is whitespace, unlike the tags, where the unit is '_'

textdomain = [' '] + [i for i in map(chr, range(97, 123))] + ['-', '_'] + [i for i in map(chr, range(65, 91))]


def _addstrings(text1, text2):
    """Add two strings and return the result. The addition must be the operation 
    used by a cyclic group over the textdomain"""
    
    return String._addstrings(text1, text2, textdomain)


 
def _textinverse(text1):
    """Return the inverse of the text. This function closely follows string._stringinverse(), 
    but deals with whitespace that we do not want to invert in document text. Also deals with
    receiving None, which can happen with document text but not, for example, element tags."""
    if text1 is None: 
        return None
    
    result = ''
    for i in text1:
        if i == '\n':
            result += i
        else:
            result += String._characterinverse(i, textdomain)

    result = _cleantext(result)
    return result



def _cleantext(text1):
    return String.cleanstring(text1, textdomain)
    