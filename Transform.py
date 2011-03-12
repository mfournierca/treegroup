"""Transform a tree into dita using the functions in this module"""

import logging, lxml.etree, sys, optparse, re

import Tree

import DitaTools.Tree.File.Dita


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
    def __init__(self):
        self._dict = {
                    'element':          None, 
                    'error':            None, 
                    'operation tree':   None,
                    'cost':             None, 
                    'operation index':  None
                     }
        self.log = logging.getLogger()
        
    def setError(self, error):
        if not isinstance(error, str):
            self.log.warning('attempted to assign non-string object to error key: %s' % str(error))
            return False
        elif not re.search(r'.*', error):
            #regex tests to make sure this is what we expect?
            pass
        self._dict['error'] = error
        
    def getError(self):
        return self._dict['error']
    
    def setElement(self, element):
        if not isinstance(element, lxml.etree._Element):
            self.log.warning('attempted to assign non-element object to element key: %s' % str(element))
            return False
        self._dict['element'] = element 
    
    def getElement(self):
        return self._dict['element']
    
    def setOperationTree(self, operationtree):
        #store as lxml.etree._ElementTree, or string?
        self._dict['operation tree'] = operationtree
    
    def getOperationTree(self):
        return self._dict['operation tree']
    
    
    
    
    
    
    


class DitaTransformer():
    
    def __init__(self, file):
        """Initialize"""
        self.log = logging.getLogger()
        self.log.debug('Initializing')
        self.file = file
        self.tree = lxml.etree.parse(file)

        self.attemptorder = [self._attemptRename, self._attemptAppendUp, self._attemptAppendDown, self._attemptUnwrap, self._attemptInsert]
        
        self.unittree = "<_/>"
        
        #operation stack
        #[
            #{element: None, 
            #error: None, 
            #operation tree: None,
            #cost: None, 
            #operation index: None
            #}
        #]
        self.operationstack = []
        
        self.validationerrors = DitaTools.Tree.File.Dita.v11_validate(self.tree) 




        
    def Transform(self):
        """Run the transformation"""
        self.log.debug('running transformation')
        
        #master loop
        #loop the transformation routine until the tree is transformed, or failure. 
        #the only failure conditions are:
        #    - an empty stack.
        #    - an error does not match any pattern
        #    - an element that cannot be found
        #the only success condition is no validation errors
        while len(self.validationerrors) > 0:# and len(self.operationstack) > 0:
            
            #initialize next stack item
            if not self._initializeNextStackItem():
                self.log.error('transformation failed')
                return False
            
            #attempt operation. this runs through all the possible operations, takes 
            #the first one that works and remembers where it left off for future reference. 
            
            #if operation failed, move up stack and try again
            
            #if operation passed, continue 
    
    
    
    
    
    
    def _initializeNextStackItem(self):
        """Append the next entry onto the operation stack. This means get the error message
        that the operation will try to fix and the element it applies to. 
        
        The operation tree and tree are set to None and will be set by other functions. The
        operation index is set to 0 no operations have been tried on this element yet"""
        
        #get the first invalid element and the error message 
        element, error = self._getFirstInvalidElement()
        if element is None: return None
        
        #add to stack with no tree, cost None and first operation index
        newstackitem = OperationStackItem()
        
        return newstackitem
    
    
    
    
    
    
    def _getFirstInvalidElement(self):
        #return the first element in the tree that has a validation error, and return it with its error
        self.log.debug('finding first invalid element')
        self.validationerrors = DitaTools.Tree.File.Dita.v11_validate(self.tree)
        if len(self.validationerrors) == 0:
            #this will stop the main loop in Transform()
            raise StopIteration
        firsterror = self.validationerrors[0]
        
        #there are several patterns that an error can follow, all of which need to be
        #interpreted differently in order to find the correct element. 
        self.log.debug('first error: %s' % firsterror)
        pattern = r'.*?\:\d*\:\d*:ERROR:VALID:DTD_UNKNOWN_ELEM: No declaration for element (.*)'
        match = re.search(pattern, firsterror)
        if match:
            self.log.debug('\tmatched pattern: %s' % pattern)
            #in this case, "no declaration for element $1 means that this element should not 
            #appear in the tree at all, so every instance of this element will create an error, 
            #so the first instance of this element created first error. Therefore, we only need to 
            #find the first instance of this element
            try: 
                element = self.tree.xpath('//%s' % match.group(1))[0]
            except IndexError:
                self.log.error('element not found')
                return None, None
            return element, firsterror
        else:
            self.log.error('first error did not match any patterns, aborting')
            return None, None
        
    
    
    
    
    def _attemptOperation(self):
        

        #while true
    
            #build attempt
            
            #if false, no more operations available. Return false. 
            
            #apply the operation
    
            #"getting closer" test
   
            #if getting closer test failed, reverse and continue
            
            #if successful, return True
        
        pass
        
        
        
        
        
    def _buildAttempt(self):
        
        #look at the last entry of the stack
        #get the current element and error message and operation index. 
        
        #build tree for current operation
        
        #if no more operations, attempt failed, return false
        
        #return the operation tree
        pass
        
        
        
        
        
    def _moveUpStack(self):
        #if stack is empty, transform failed
        pass
    
    
    def _attemptRename(self):
        pass
    
    
    def _attemptAppendUp(self):
        pass
    
    
    def _attemptAppendDown(self):
        pass
    
    
    def _attemptUnwrap(self):
        pass
    
    
    def _attemptInsert(self):
        pass
    
    



#function attempt order: [rename, appendDown, appendUp . . .]


#initialize operations stack
    #[target element, operand tree, cost, operation that created this operand (rename, append, etc)]





#parse the tree

#initialize stack, first entry is first invalid element


#while True?
    
    #all operations are applied to last entry in stack
       
    #attemptOperations()
    
    #if operation successful, append next element to stack and continue
    
    #if operation unsuccessful, take last element off stack and continue





if __name__ == "__main__":
    #called from a command line
    optparser=optparse.OptionParser()
    
    optparser.add_option("-i", "--input", type="string", dest="input", default='', 
    help="Path to the input file")
    optparser.add_option("--debug", action="store_true", dest="debug",
    help="Turn this on to activate debug logging.")
    #optparser.add_option( "-t", "--tempdir", type="string", dest="tempdir", default=None, 
    #help="path to the tempdir")
    
    (options, args) = optparser.parse_args()
    input = options.input
    debug = options.debug
    
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
    
    pass
    
    
    
    
    