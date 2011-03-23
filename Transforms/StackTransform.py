"""Transform a tree into dita using the functions in this module"""

import logging, lxml.etree, sys, optparse, re, copy

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import Tree.Tree, Element.Element

import DitaTools.Tree.File.Dita


class NoErrorMatchException(Exception):
    def __init__(self, message):
        self.text = "No matches found for: %s" % message
    def __str__(self):
        return repr(self.text)





class DitaTransformer():
    
    def __init__(self, file):
        """Initialize"""
        self.log = logging.getLogger()
        self.log.debug('Initializing')
        self.file = file
        self.tree = lxml.etree.parse(file)
        self.operationstack = OperationStack()
        self.validationerrors = DitaTools.Tree.File.Dita.v11_validate(self.tree) 
        self.operandbuilder = OperandBuilder()

    def Transform(self):
        """Run the transformation"""
        self.log.debug('running transformation')
        
        #master loop. 
        #loop the transformation routine until the tree is transformed, or failure. 
        #the only failure conditions are:
        #    - an empty stack.
        #    - an error does not match any pattern
        #    - an element that cannot be found
        #the only success condition is no validation errors
        while len(self.validationerrors) > 0:# and len(self.operationstack) > 0:
            
            try:
                stackitem = OperationStackItem(self.tree)
            except NoErrorMatchException as e:
                self.log.error(str(e))
                self.log.error('aborting transformation')
                return False
            self.operationstack.insert(0, stackitem)
            
            #build operand
            check = self.operandbuilder.buildOperand(stackitem)
            if not check:
                #no operand found, go back up the stack
                pass
            
            #try operand
            self.log.debug('trying operand: %s' % lxml.etree.tostring(stackitem.operand.tree))
            Tree.add(self.tree, stackitem.operand.tree)
            
            #test distance
        
    def _moveUpStack(self):
        #if stack is empty, transform failed
        pass
    
    









class OperationStack(list):
    def __init__(self):
        self.log = logging.getLogger()
    
    def append(self, x):
        #make sure to check with isinstance
        if not isinstance(x, OperationStackItem):
            self.log.warning('tried to append invalid object to OperationStack: %s' % str(x))
            return False
        super(OperationStack, self).append(x)
    
    def remove(self):
        pass
        #??
    
    def addOperationTrees(self):
        #add all the operation trees together to get the net operation
        pass
    
    
    
class OperationStackItem():
    """The OperationStackItem contains all the information about the operation - 
    it's operand, the cost, the error it address and the element it targets"""
    def __init__(self, tree):
        self.log = logging.getLogger()
        self.element = None
        self.error = None
        self.operand = None
        self.operationindex = None

        #get first error, initialize error object. Any errors in initialization get passed back to 
        #Transform()
        error = ValidationError(tree)
        self.element = tree.xpath(error.xpath)[0]
        self.error = error
        self.setOperationIndex(0)
        
    #accessor methods
    def setError(self, error):
        if not isinstance(error, ValidationError):
            self.log.warning('attempted to assign ValidationError object to error key: %s' % str(error))
            return False
        elif not re.search(r'.*', error.message):
            #regex tests to make sure this is what we expect?
            pass
        self.error = error

    def setElement(self, element):
        if not isinstance(element, lxml.etree._Element):
            self.log.warning('attempted to assign non-element object to element key: %s' % str(element))
            return False
        self.element = element 

    def setOperationTree(self, operationtree):
        #store as lxml.etree._ElementTree, or string?
        self.operationtree = operationtree

    def setOperationIndex(self, index):
        if not isinstance(index, int):
            self.log.warning('attempted to assign non-integer to operation index key: %s' % str(index))
            return False
        self.operationindex = index

    
    
    
    
    
        
    
    
    
    
    
    
    
    
    
    
class ValidationError():
    """The validation error object contains all the information about 
    the validation error being addressed - the message, the element 
    being addressed, the xpath to find that element and some hints for 
    the Operand Builder"""
    
    def __init__(self, tree):
        self.log = logging.getLogger()
        self.log.debug('getting validation error and element')
        #the following attributes can be retrieved by any other object
        #and are mainly used by OperandBuilder as hints as to what it
        #should do
        self._suggestedrename = None
        
        #retrieve the first validation error message
        validationerrors = DitaTools.Tree.File.Dita.v11_validate(tree)
        if len(validationerrors) == 0:
            #this will stop the main loop in Transform()
            self.log.debug('no errors found')
            raise StopIteration
        self.message = validationerrors[0]
        self.log.debug('message: %s' % self.message)    
        
        #try to parse the message, return if successful
        if self._noDeclarationParser(): pass
        elif self._ditaElementDoesNotFollowDTDParser(): pass
        else:
            self.log.error('message did not match any known errors, cannot initialize')
            raise NoErrorMatchException(self.message)
    
    #there are several patterns that an error can follow, all of which need to be
    #interpreted differently in order to find the correct element. 
    #Every validation error message must match a parser here. 
        
    def _noDeclarationParser(self):
        pattern = r'.*?\:\d*\:\d*:ERROR:VALID:DTD_UNKNOWN_ELEM: No declaration for element (.*)'
        match = re.search(pattern, self.message)
        if match:
            self.log.debug('\tmatched pattern: "%s"' % pattern)
            #in this case, "no declaration for element $1 means that this element should not 
            #appear in the tree at all, so every instance of this element will create an error, 
            #so the first instance of this element created first error. Therefore, we only need to 
            #find the first instance of this element
            self.xpath = '//%s' % match.group(1)
            self.suggestedrename = 'dita'
            return True
        else: 
            return False

    def _ditaElementDoesNotFollowDTDParser(self):
        pattern = r'.*?\:\d*\:\d*:ERROR:VALID:DTD_CONTENT_MODEL: Element dita content does not follow the DTD, expecting \(topic \| concept \| task \| reference \| glossentry\)\+, got \((.*?)\)'
        match = re.search(pattern, self.message)
        if match:
            self.log.debug('\tmatched pattern: "%s"' % pattern)
            tags = match.group(1).split(' ')
            self.log.debug('found tags: %s' % str(tags))
            for i in tags: 
                if i in ['topic', 'task', 'concept', 'reference']:
                    continue
                else:
                    tag = i
                    break
            self.xpath = '//%s' % tag
            self.suggestedrename = 'topic'
            return True
        else: 
            return False
    
    def _emptyTopicParser(self):
        pattern = r'.*?\:\d*\:\d*:ERROR:VALID:DTD_CONTENT_MODEL: Element topic content does not follow the DTD, expecting \(topic \| concept \| task \| reference \| glossentry\)\+, got '
        match = re.search(pattern, self.message)
        if match:
            self.log.debug('\tmatched pattern: "%s"' % pattern)
            self.xpath = '//%s' % 'topic'
            return True
        else: 
            return False
    
    
    
    
    
    
class OperandBuilder():
    def __init__(self):
        #define costs
        self.log = logging.getLogger()
        self.attemptorder = [self._buildRename, self._buildAppendUp, self._buildAppendDown, self._buildUnwrap, self._buildInsert]
        pass
    
    def buildOperand(self, stackitem):
        self.log.debug('building operand')
        for i in self.attemptorder[stackitem.operationindex:]:
            operand = i(stackitem.error, stackitem.element)
            if operand:
                stackitem.operand = operand
                break
            
    #The various operand building routines. Every movement to be performed on the tree must 
    #be built here. 
    
    def _buildRename(self, error, element):
        """Build an operand used to rename the element. This requires building
        a tree of units down to the position of the element in its tree, and then
        putting the correct rename node at the correct position in the operand tree"""
        self.log.debug('building rename operand')
        operand = Operand()
        #set the cost of Rename
        operand.cost = 1
        
        position = Element.Element.position(element)
        if not position[0] == 1:
            self.log.warning('invalid position received')
            return False
        current = operand.tree
        #build a tree of units down to the position of element
        for p in position[1:]:
            for i in range(0, p):
                new = lxml.etree.Element('_')
                current.append(new)
            current = new
        if error.suggestedrename: 
            #current is the unit node right now. 
            #make current the node that will rename element
            Element.Element.add(current, lxml.etree.Element(error.suggestedrename))
            Element.Element.add(current, Element.Element.invert(lxml.etree.Element(element.tag)))
            return operand
        else:
            #no idea where to start, no dice. 
            return None
            
    
    def _buildAppendUp(self):
        self.log.warning('this function is not yet written')
        pass
    
    def _buildAppendDown(self):
        self.log.warning('this function is not yet written')
        pass
    
    def _buildUnwrap(self):
        self.log.warning('this function is not yet written')
        pass
    
    def _buildInsert(self):
        self.log.warning('this function is not yet written')
        pass
    
    
    
    
class Operand():
    def __init__(self):
        #unit tree by defaul
        self.tree = lxml.etree.fromstring('<_/>')
        self.cost = None
    
    




    
    
    








if __name__ == "__main__":
    #called from a command line
    optparser=optparse.OptionParser()
    
    optparser.add_option("-i", "--input", type="string", dest="input", default='', 
    help="Path to the input file")
    optparser.add_option("-o", "--output", type="string", dest="output", default='', 
    help="Path to the input file")
    optparser.add_option("--debug", action="store_true", dest="debug",
    help="Turn this on to activate debug logging.")
    #optparser.add_option( "-t", "--tempdir", type="string", dest="tempdir", default=None, 
    #help="path to the tempdir")
    
    (options, args) = optparser.parse_args()
    input = options.input
    debug = options.debug
    output = options.output
    
    #this next block ensures that the user can pass the input as a positional
    #argument, without the -i
    try:
        input = args[0]
    except:
        pass
    
    
    #===============================================================================
    # #prepare logging
    #===============================================================================
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
     
    warninghandler = logging.StreamHandler(sys.stdout)
    warninghandler.setLevel(logging.WARNING)
    warningformatter = logging.Formatter("%(module)8.8s.%(funcName)20.20s%(levelname)10.10s\t%(message)s")
    warninghandler.setFormatter(warningformatter)
    log.addHandler(warninghandler)
    
    if debug:
#        debughandler = logging.FileHandler(os.path.basename(__file__).replace('.py', '-debug.txt'), 'w', encoding='utf-8')
        debughandler = logging.StreamHandler(sys.stdout)
        debughandler.setLevel(logging.DEBUG)
        debugformatter = logging.Formatter("%(module)8.8s.%(funcName)20.20s%(levelname)10.10s\t%(message)s")
        debughandler.setFormatter(debugformatter)
        log.addHandler(debughandler)
    else:
        pass

    log.debug("input file: %s" % input)
        
    #initialize transformation object
    transformer = DitaTransformer(input)
    
    #perform transformation
    transformer.Transform()
    
    DitaTools.Tree.File.Dita.write_tree_to_file(transformer.tree, output)
    
    
    