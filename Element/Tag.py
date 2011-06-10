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
#eg cleantag() remove trailing units in a tag, which may cause problems if the '_' is
#significant in some context. 
#Also, note that although numbers (0, 1, 2, 3 . . . ) are valid as part of a tag name, a
#sole number is not considered a valid tag name by lxml. This means that they cannot be
#included in the tag domain, since excluding a node from being named any character in the
#tag domain would render the arithmetic inconsistent. Inconsistent arithmetic will break 
#everything, therefore we must exclude numbers from the domain. 
tagdomain = ['_'] + [i for i in map(chr, range(97, 123))] + ['-'] + [i for i in map(chr, range(65, 91))]# + [i for i in map(chr, range(48, 58))]


def _addtags(tag1, tag2):
    """Add two tags and return the result. The addition must be the operation 
    used by a cyclic group over the tagdomain"""
    
    return String._addstrings(tag1, tag2, tagdomain)


 
def _taginverse(tag1):
    """Return the inverse of the tag"""
     
    return String._stringinverse(tag1, tagdomain)


def _cleantag(tag1):
    return String.cleanstring(tag1, tagdomain)
    