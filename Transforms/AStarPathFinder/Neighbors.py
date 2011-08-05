"""Functions to find the neighbors of a tree. Allowed operations are defined here"""

import logging, lxml.etree, re, sys, os.path, copy

import Element.Element
import Tree.Tree

import Errors, Filter

sys.path.insert(0, os.path.dirname(__file__))

class Neighbor:
    def __init__(self, tree):
        self._gscore = None
        self._hscore = None
        self._fscore = None
        self._camefrom = None
        
        #cost is used to control the performance of the path finder - 
        #make some neighbors less "expensive" so that they will be chosen over 
        #others. Cost can be set by considering the score from the tag filter, 
        #or by putting in our own values to make certain operations more expensive.         
        self._cost = 0

#        self.dist = None
        
        self._tree = None
        self.setTree(tree)
        self._operand = None
        
        #used for debugging. 
        self._id = None
        self._operandType = None
        self._targetElementStr = None
        
        
        
        #metric reduction factor
#        self.metricadjustmentfactor = float(1) / float(10)
    
    #===========================================================================
    # accessor methods
    #===========================================================================
    
    #note: since the AStarPathFinder will be used to transform trees, 
    #we have to be able to handle large trees. Some documents get up to 
    #5 MB, with hundreds of elements - if we stored the full tree of each neighbor
    #in memory, we would reach GB quickly. Therefore, it will be necessary at some 
    #point to do something more clever, ie only store the operand and only
    #calculate the full neighbor tree when needed, or write the trees to disk 
    #and retrieve them when needed. 
    #If in the future it is necessary to do this, it should be done here by changing
    #the accessor methods to write or read to disk, or calculate the neighbor 
    #tree as needed. These accessor methods are already created, although rather 
    #simple at this point. But changing them in the future will not require changes
    #in any other part of the program. 
        
#    def getOperandTree(self):
#        """Return the operand tree of this neighbor, ie the operand that when added to the
#        camefrom tree creates this neighbor tree. There is no guarantee that any changes
#        made on the return tree will persist, to guarantee that, use the setOperandTree() method."""
#        return self._operand
#    
#    def setOperandTree(self, tree):
#        """Set the operand tree"""
#        self._operand = tree
    
    
    def getTree(self):
        """Return the tree of this neighbor. There is no guarantee that any changes made on the 
        returned tree will persist - to guarantee that, use the setTree() method"""
        return self._tree
    
    def setTree(self, tree):
        """Set the neighbor tree."""
        self._tree = tree
        
        
    def setCameFrom(self, x):
        self._camefrom = x
        
    def getCameFrom(self):
        return self._camefrom
    
    
    def setGScore(self, g):
        self._gscore = g
    
    def getGScore(self):
        return self._gscore
    
    
    def setHScore(self, h):
        self._hscore = h
        
    def getHScore(self):
        return self._hscore
    
    
    def setFScore(self, f):
        self._fscore = f
        
    def getFScore(self):
        return self._fscore
    
    
    def setCameFrom(self, c):
        self._camefrom = c 
    
    def getCameFrom(self):
        return self._camefrom
    
    
    def setOperand(self, o):
        self._operand = o
        
    def getOperand(self):
        return self._operand
    
    
    def setId(self, i):
        self._id = i
        
    def getId(self):
        return self._id
    
    
    def setOperandType(self, t):
        self._operandType = t
        
    def getOperandType(self):
        return self._operandType
    
    
    def setTargetElementStr(self, t):
        self._targetElementStr = t
        
    def getTargetElementStr(self):
        return self._targetElementStr
    
    def setCost(self, filterscore, metric, metricnormalizationdenomiator, manualscore):
        #three factors in cost (or there should be): filter score, metric, and manually set.
        #should normalize these factors, ie force them all to be 0 < x < 1, so that none dominate
        #normalize metric
        metric = float(metric) / float(metricnormalizationfactor) #* self.metricadjustmentfactor
        
        #filterscore and manualscore are already normalized. 
        
        #the filter returns scores that are higher when better - we want the opposite
        filterscore = 1 - filterscore
        
        self._cost = filterscore + metric + manualscore
        
    
    def getCost(self):
        return self._cost
    
    
    
    
    
def findNeighbors_FirstValidationError(t):
    """Find Neighbors by fixing the first validation error. 
    
    Neighbors are defined as a tree that can be reached by some operation
    on the source tree. (this means any tree, in effect). 
    
    The first validation error is the first error in the list created by a 
    validator. By fixing this first error, we find neighbors that are the 
    result of fixing the first invalid element in the tree. """
    
    import Generators.Rename
    import Generators.Unwrap
    import Generators.Wrap
    import Generators.RenameAttribute
    import Generators.AddAttribute
    import Generators.InsertBefore
    import Generators.AppendBefore
    import Generators.WrapText
    
    log = logging.getLogger()
    
    def getTreeSize(tree):
        """used to get the tree size, which is used to normalize the metric"""
        count = 0
        for i in tree:
            count = 1 + getTreeSize(i)
        return count
    
    treeSize = getTreeSize(t.getroot())
       
#    log.debug('creating neighbors')
    neighbors = []
    
    
    #===========================================================================
    # #element errors
    #===========================================================================
    
    #Error parser
    errorParser = Errors.ElementErrorParser(t.getTree()())
    parsed = errorParser.parse()
    
    if parsed:
        #generate operands using the result of this error parser
        
        #filter acceptable tags
        filter = Filter.ElementTagFilter()
        filteredtags, filteredscores = filter.filter(errorParser.targetElement, errorParser.acceptableTags)
    
        renameGenerator = Generators.Rename.Generator()
        wrapGenerator = Generators.Wrap.Generator()
        unwrapGenerator = Generators.Unwrap.Generator()
        insertBeforeGenerator = Generators.InsertBefore.Generator()
        appendBeforeGenerator = Generators.AppendBefore.Generator()
        tag = '_'    
        for tag in filteredtags:
            
            #rename operator
            renameOperand = renameGenerator.generateOperand(errorParser.targetElement, tag)
            renameNeighbor = Neighbor(Tree.Tree.add(copy.deepcopy(renameOperand.getTree()), t.getTree()()))
            renameNeighbor.setOperand(renameOperand.getTree())
            renameNeighbor.setOperandType('rename')
            renameNeighbor.setTargetElementStr(str(errorParser.targetElement))
            
            renameNeighbor.setCost(filteredscores[tag], 
                                   Tree.Tree.metric(t.getTree(), renameNeighbor.getTree()),
                                   treeSize,
                                   getManualCost(renameNeighbor, 'rename', tag)
                                   )
            neighbors.append(renameNeighbor)
        
            #wrap operator
            wrapOperand = wrapGenerator.generateOperand(errorParser.targetElement, tag)
            wrapNeighbor = Neighbor(Tree.Tree.add(copy.deepcopy(wrapOperand.getTree()), t.getTree()()))
            wrapNeighbor.setOperand(wrapOperand.getTree())
            wrapNeighbor.setOperandType('wrap')
            wrapNeighbor.setTargetElementStr(str(errorParser.targetElement))
            wrapNeighbor.setCost(filteredscores[tag], 
                               Tree.Tree.metric(t.getTree(), wrapNeighbor.getTree()),
                               treeSize,
                               getManualCost(wrapNeighbor, 'wrap', tag)
                               )
            neighbors.append(wrapNeighbor)
            
            #InsertBefore operator
            insertBeforeOperand = insertBeforeGenerator.generateOperand(errorParser.targetElement, tag)
            if not insertBeforeOperand:
                pass
            else:
                insertBeforeNeighbor = Neighbor(Tree.Tree.add(copy.deepcopy(insertBeforeOperand.getTree()), t.getTree()()))
                insertBeforeNeighbor.setOperand(insertBeforeOperand.getTree())
                insertBeforeNeighbor.setOperandType('insertBefore')
                insertBeforeNeighbor.setTargetElementStr(str(errorParser.targetElement))
                insertBeforeNeighbor.setCost(filteredscores[tag],
                                             Tree.Tree.metric(t.getTree(), insertBeforeNeighbore.getTree()),
                                             treeSize,
                                             getManualCost(insertBeforeNeighbor, 'insertBefore', tag),
                                             )
                neighbors.append(insertBeforeNeighbor)
            
        #unwrap operator. There is only one result of the unwrap operator, so it comes outside
        #the loop
        unwrapOperand = unwrapGenerator.generateOperand(errorParser.targetElement)
        if not unwrapOperand: 
            #happens when trying to unwrap the root
            pass
        else:
            unwrapNeighbor = Neighbor(Tree.Tree.add(copy.deepcopy(unwrapOperand.getTree()), t.getTree()()))
            unwrapNeighbor.setOperand(unwrapOperand.getTree())
            unwrapNeighbor.setOperandType('unwrap')
            unwrapNeighbor.setTargetElementStr(str(errorParser.targetElement))
            unwrapNeighbor.setCost(0.5,
                                 Tree.Tree.metric(t.getTree(), unwrapNeighbors.getTree()),
                                 treeSize,
                                 getManualCost(unwrapNeighbor, 'unwrap', tag),
                                 )
            neighbors.append(unwrapNeighbor)
        
        #appendBefore operator. There is only one result of the appendBefore operator, so it comes outside
        #the loop
        appendBeforeOperand = appendBeforeGenerator.generateOperand(errorParser.targetElement)
        if not appendBeforeOperand: 
            #happens when trying to appendBefore the root
            pass
        else:
            appendBeforeNeighbor = Neighbor(Tree.Tree.add(copy.deepcopy(appendBeforeOperand.getTree()), t.getTree()()))
            appendBeforeNeighbor.setOperand(appendBeforeOperand.getTree())
            appendBeforeNeighbor.setOperandType('appendBefore')
            appendBeforeNeighbor.setTargetElementStr(str(errorParser.targetElement))
            appendBeforeNeighbor.setCost(0.5,
                                         Tree.Tree.metric(t.getTree(), unwrapNeighbors.getTree()),
                                         treeSize,
                                         getManualCost(appendBeforeNeighbor, 'appendBefore', tag),
                                         )
            neighbors.append(appendBeforeNeighbor)
        
        #return neighbors.
        return neighbors


    #===========================================================================
    # attribute errors
    #===========================================================================
    errorParser = Errors.AttributeErrorParser(t.getTree()())
    parsed = errorParser.parse()
    
    if parsed:
        #generate operands using the result of this error parser
        
        renameAttributeGenerator = Generators.RenameAttribute.Generator()
        for attributeName in errorParser.acceptableAttributes:
            renameAttributeOperand = renameAttributeGenerator.generateOperand(errorParser.targetElement, errorParser.actualAttribute, attributeName)
            if not renameAttributeOperand:
                continue
            renameAttributeNeighbor = Neighbor(Tree.Tree.add(copy.deepcopy(renameAttributeOperand.getTree()), t.getTree()()))
            renameAttributeNeighbor.setOperand(renameAttributeOperand.getTree())
            renameAttributeNeighbor.setOperandType('renameAttribute')
            renameAttributeNeighbor.setTargetElementStr(str(errorParser.targetElement))
            renameAttributeNeighbor.setCost(0.5,
                                         Tree.Tree.metric(t.getTree(), renameAttributeNeighbor.getTree()),
                                         treeSize,
                                         getManualCost(renameAttributeNeighbor, 'renameAttribute', None),
                                         )
            neighbors.append(renameAttributeNeighbor)


        addAttributeGenerator = Generators.AddAttribute.Generator()
        for attributeName in errorParser.acceptableAttributes:
            addAttributeOperand = addAttributeGenerator.generateOperand(errorParser.targetElement, attributeName)
            addAttributeNeighbor = Neighbor(Tree.Tree.add(copy.deepcopy(addAttributeOperand.getTree()), t.getTree()()))
            addAttributeNeighbor.setOperand(addAttributeOperand.getTree())
            addAttributeNeighbor.setOperandType('addAttribute')
            addAttributeNeighbor.setTargetElementStr(str(errorParser.targetElement))
            addAttributeNeighbor.setCost(0.5,
                                         Tree.Tree.metric(t.getTree(), addAttributeNeighbor.getTree()),
                                         treeSize,
                                         getManualCost(addAttributeNeighbor, 'addAttribute', None),
                                         )
            neighbors.append(addAttributeNeighbor)

        return neighbors
            
    
    #===========================================================================
    # text errors
    #===========================================================================
    errorParser = Errors.TextErrorParser(t.getTree()())
    parsed = errorParser.parse()
    
    if parsed and errorParser.text:
        #generate operands using the result of this error parser
        wrapTextGenerator = Generators.WrapText.Generator()

        #filter acceptable tags
        filter = Filter.ElementTagFilter()
        filteredtags, filteredscores = filter.filter(errorParser.targetElement, errorParser.acceptableTags)
        
        for tag in filteredtags:
            wrapTextOperand = wrapTextGenerator.generateOperand(errorParser.targetElement, tag)
            if not wrapTextOperand:
                continue
            wrapTextNeighbor = Neighbor(Tree.Tree.add(copy.deepcopy(wrapTextOperand.getTree()), t.getTree()()))
            wrapTextNeighbor.setOperand(wrapTextOperand.getTree())
            wrapTextNeighbor.setOperandType('wrapText')
            wrapTextNeighbor.setTargetElementStr(str(errorParser.targetElement))
            wrapTextNeighbor.setCost(filteredscores[tag],
                                     Tree.Tree.metric(t.getTree(), wrapTextNeighbor.getTree()),
                                     treeSize,
                                     getManualCost(wrapTextNeighbor, 'wrapText', tag),
                                     )
            neighbors.append(wrapTextNeighbor)

        return neighbors
    
    if parsed and errorParser.tail:
        pass
        #get wrap tail operand
    
    #===========================================================================
    # error parsers failed
    #===========================================================================
    log.error('all error parsers failed')
    sys.exit(-1)
    
    










def getManaulCost(neighbor, operandtype, desttag):
    """A placeholder function. Get a 'cost' of the neighbor based on some 
    criteria. The 'cost' should reflect the 'cost' of using this neighbor - 
    better or more desirable neighbors should receive a lower score. 
    
    Eventually, this should be done using more sofisticated methods, ie, 
    bayesian filters that learn the desired cost based on the tag, target, 
    elements surrounding the target, etc. That is difficult, however, and 
    for now in the proof of concept stage we are simply going to hard code 
    everything with if statements."""
    
    #result must be between 0 and 1
    
    cost = 0
    
    #account for operandtype
    if operandtype == 'rename': cost += .25
    elif operandtype == 'renameAttribute': cost += .25
    elif operandtype == 'wrap': cost += .5
    elif operandtype == 'unwrap': cost += .75
    elif operandtype == 'insertBefore': cost += .5
    elif operandtype == 'appendBefore': cost += 0
    else: cost += 1
    
    return cost
    
    
    