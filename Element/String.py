import logging

#strings form a group by considering each character in the strings to be a
#member of the cyclic group defined by the stringdomain list, which should be passed. We form
#a group by imagining that strings have an infinite tail of space characters 
#(the unit in the character group. Tags are then 
#added character by character, and since every character is a member of a cyclic
#group, the string as a whole forms a group. 

#the unit of the group is the first element in the domain, ie stringdomain[0]

def _addstrings(string1, string2, stringdomain):
    """Add two strings and return the result. The addition must be the operation 
    used by a cyclic group over the stringdomain"""
    log = logging.getLogger()
    if string1 == '' or string2 == '':
        return False
    
    #first make them the same length
    if len(string1) == len(string2):
        pass
    elif len(string1) > len(string2):
        for i in range(0, len(string1) - len(string2)): string2 += stringdomain[0]
    elif len(string1) < len(string2):
        for i in range(0, len(string2) - len(string1)): string1 += stringdomain[0]
                
    #then iterate over the characters in string1
    result = ''
    for index, char in enumerate(string1):
        result += _addchars(string1[index], string2[index], stringdomain)
        
    result = cleanstring(result, stringdomain)
    log.debug('result: %s' % result)
    #add the corresponding character in string 2
    return result



def _addchars(char1, char2, stringdomain):
    """Add two characters, treating them as a elements of a cyclic group 
    defined by the stringdomain list"""
    try:
        index1 = stringdomain.index(char1)
    except ValueError:
        log = logging.getLogger()
        log.error('%s not found in stringdomain' % char1)
        raise
    
    try:
        index2 = stringdomain.index(char2)
    except ValueError:
        log = logging.getLogger()
        log.error('%s not found in stringdomain' % char2)
        raise
    
    newchar = stringdomain[(index1 + index2) % len(stringdomain)]
    return newchar
    

def _stringinverse(string1, stringdomain):
    """Return the inverse of the string"""
    result = ''
    for i in string1:
        result += _characterinverse(i, stringdomain)

    result = cleanstring(result, stringdomain)
    
    return result


def _characterinverse(char1, stringdomain):
    """Return the inverse of the character"""
    
    try:
        index = stringdomain.index(char1)
    except ValueError:
        log = logging.getLogger()
        log.error('character "%s" not found in string domain' % char1)
        raise
    return stringdomain[(len(stringdomain) - index) % len(stringdomain)]
    



def cleanstring(string1, stringdomain):
    result = string1[:]
    while result.endswith(stringdomain[0]) and len(result) > 1:
        result = result[:-1]
    return result
    
    