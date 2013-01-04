from . import String


#tags form a group by considering each character in the tags to be a
#member of the cyclic group defined by the tagdomain list, below. We form
#a group by imagining that tags have an infinite tail of space characters 
#(the unit in the character group. Tags are then 
#added character by character, and since every character is a member of a cyclic
#group, the tag as a whole forms a group. 

#The unit characted is the first element in the domain, ie tagdomain[0]
#it would be better to use ' ' as the unitchar, but lxml does not allow blank tags. 
#So we are using '_'. This is ok, the artihmetic does not particularly care what the
#unit node is because this is a cyclic group. But keep in mind that several operations, 
#eg cleantag() remove leading units in a tag, which may cause problems if the '_' is
#significant in some context. 
#Also, note that although numbers (0, 1, 2, 3 . . . ) are valid as part of a tag name, a
#sole number is not considered a valid tag name by lxml. This means that they cannot be
#included in the tag domain, since excluding a node from being named any character in the
#tag domain would render the arithmetic inconsistent. Inconsistent arithmetic will break 
#everything, therefore we must exclude numbers from the domain. 
tagdomain = ['_'] + [i for i in map(chr, range(97, 123))] + ['-'] + [i for i in map(chr, range(48, 58))] + [i for i in map(chr, range(65, 91))]


#2011-09-15: inconsistent arithmetic appeared, and I should have caught it before. 
#lxml does not allow '-' as a tag name, '-' must be preceded by some other character to be 
#considered valid. This was fixed by considering strings in reverse order. 
#In other contexts (text, attributes, tail) strings are considered cyclic groups over each 
#character, and the strings are combined by adding each character starting at the beginning. 
#The tag functions now simply reverse this, and start iterating at the end of the string, 
#instead of the beginning. This means that _leading_ units must be removed, not trailing
#as in other contexts. 
#Leading units are left in if the tag starts with '-' (or a digit, in the future). This allows the 
#arithmetic to remain consistent, and to work around this little quirk of lxml. 



def isUnitTag(tag):
    if tag == tagdomain[0]:
        return True
    else:
        return False
    

def equal(tag1, tag2):
    if _cleantag(tag1) == _cleantag(tag2):
        return True
    else:
        return False


def addTags(tag1, tag2):
    """Add two tags and return the result. The addition must be the operation 
    used by a cyclic group over the tagdomain"""
    import logging
    
    log = logging.getLogger()
    
    if tag1 == '' or tag2 == '':
        return False
    
    #first make them the same length
    if len(tag1) == len(tag2):
        pass
    elif len(tag1) > len(tag2):
        for i in range(0, len(tag1) - len(tag2)): 
            tag2 = ''.join((tagdomain[0], tag2))
    elif len(tag1) < len(tag2):
        for i in range(0, len(tag2) - len(tag1)): 
            tag1 = ''.join((tagdomain[0], tag1))
                
    #then iterate over the characters in tag1
    result = ''
    for index, char in enumerate(tag1):
        result += String._addchars(tag1[index], tag2[index], tagdomain)
        
    result = _cleantag(result)
#    log.debug('result: %s' % result)
    return result





 
def tagInverse(tag1):
    """Return the inverse of the tag"""
     
    result = String._stringinverse(tag1, tagdomain)
    #no empty tags allowed as explained above, lxml does not allow it. 
    if result == '': result = tagdomain[0]
    
    return _cleantag(result)
    



def _cleantag(tag1):
    result = tag1[:]
    while result.startswith(tagdomain[0]) and len(result) > 1:
        result = result[1:]
    
    if (result.startswith('-')) or (result[0] in [i for i in map(chr, range(48, 58))]):
        result = ''.join(('_', result))
        
    return result
    
    