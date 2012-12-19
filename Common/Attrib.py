
#attributes are dictionaries of key - value pairs. 
#We form a group of attributes by imagining every attribute dictionary to 
#contain every possible key. Addition is then simply adding the values of
#corresponding keys according to the same rules that tags are added with. 

#When writing a dictionary, keys with blank values (the vast majority) are
#not written. 
    
from . import Tag
from . import String
import copy, logging


#strings form a group by considering each character in the strings to be a
#member of the cyclic group defined by the stringdomain list, below. We form
#a group by imagining that strings have an infinite tail of space characters 
#(the unit in the character group. Tags are then 
#added character by character, and since every character is a member of a cyclic
#group, the string as a whole forms a group. 

#the unit is the first element in the domain, ie attrdomain[0]
#it would be better to use ' ' as the unitchar, but lxml does not allow blank strings. 
#So we are using '_'. This is ok, the artihmetic does not particularly care what the
#unit node is because this is a cyclic group. But keep in mind that several operations, 
#eg cleanstring() remove trailing units in a string, which may cause problems if the '_' is
#significant in some context. 
attrdomain = ['_'] + [i for i in map(chr, range(97, 123))] + [i for i in map(chr, range(32, 48))] + [i for i in map(chr, range(58, 65))] + ['\\'] + [i for i in map(chr, range(65, 91))] + [i for i in map(chr, range(48, 58))] 

def cleanKeys(attr):
    deletekeys = []
    for key in attr.keys():
        if (attr[key] == attrdomain[0]) or (attr[key] == '') or (attr[key] is False) or (attr[key] is None): 
            deletekeys.append(key)
    for key in deletekeys:
        del attr[key]
    
    
    
def addAttribs(attrib1, attrib2):
    """Add two attribute dictionaries and return the result"""
    log = logging.getLogger()
    #log.debug('adding attributes: %s\t%s' % (str(attrib1), str(attrib2)))
    result = copy.copy(attrib1)
    for key in attrib2.keys():
        #log.debug('attrib2: key: %s\tvalue: %s' % (key, attrib2[key]))
        if key not in result.keys():
            result[key] = attrib2[key]
        else:
            #log.debug('result key: %s\tvalue: %s' % (key, result[key]))
            result[key] = String._addstrings(result[key], attrib2[key], attrdomain)
    
    cleanKeys(result)        
#    log.debug('result: %s' % str(result))
    return result



def attribInverse(attrib):
    """Return the inverse of the attributes"""
    result = {}
    cleanKeys(attrib)
    for key in attrib.keys():
        result[key] = String._stringinverse(attrib[key], attrdomain)
    return result    