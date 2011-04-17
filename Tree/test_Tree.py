import unittest, os.path, sys, logging

import lxml.etree, copy

from . import Tree    

import Element.Element

class test_equal(unittest.TestCase):
    """Test the equal() function"""
            
    def setUp(self):
        """set up data used in the tests, called before each test function execution"""
        
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'Tree', 'Equal')
        self.testtree = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_reference.xml'))
        self.log = logging.getLogger()
    
    def test_SameTree(self):
        testtreecopy = copy.deepcopy(self.testtree)
        result = Tree.equal(self.testtree, testtreecopy)
        self.assertTrue(result, "equal() failed: expected %s, got %s" % (str(True), str(result)))
        #test elements
        result = Tree.equal(self.testtree.getroot(), testtreecopy.getroot())
        self.assertTrue(result, "equal() failed: expected %s, got %s" % (str(True), str(result)))
        
    
    def test_SeparateTrees(self):
        comparetree = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_equal1.xml'))
        result = Tree.equal(self.testtree, comparetree)
        self.assertTrue(result, "equal() failed: expected %s, got %s" % (str(True), str(result)))
        #test elements
        result = Tree.equal(self.testtree.getroot(), comparetree.getroot())
        self.assertTrue(result, "equal() failed: expected %s, got %s" % (str(True), str(result)))
        
    
    def test_NotEqual_NoChildrenOfRoot(self):
        comparetree = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_notequal1.xml'))
        result = Tree.equal(self.testtree, comparetree)
        self.assertIs(result, False, "equal() failed: expected %s, got %s" % (str(False), str(result)))
        #test as elements
        result = Tree.equal(self.testtree.getroot(), comparetree.getroot())
        self.assertIs(result, False, "equal() failed: expected %s, got %s" % (str(False), str(result)))
        
        
    def test_NotEqual_NotNested(self):
        comparetree = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_notequal2.xml'))
        result = Tree.equal(self.testtree, comparetree)
        self.assertIs(result, False, "equal() failed: expected %s, got %s" % (str(False), str(result)))
        #test as elements
        result = Tree.equal(self.testtree.getroot(), comparetree.getroot())
        self.assertIs(result, False, "equal() failed: expected %s, got %s" % (str(False), str(result)))
    
    def test_NotEqual_IdsDiffer(self):
        comparetree = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_notequal3.xml'))
        result = Tree.equal(self.testtree, comparetree)
        self.assertIs(result, False, "equal() failed: expected %s, got %s" % (str(False), str(result)))
        #test as elements
        result = Tree.equal(self.testtree.getroot(), comparetree.getroot())
        self.assertIs(result, False, "equal() failed: expected %s, got %s" % (str(False), str(result)))
    
    def test_NotEqual_TagsDiffer(self):
        comparetree = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_notequal4.xml'))
        result = Tree.equal(self.testtree, comparetree)
        self.assertIs(result, False, "equal() failed: expected %s, got %s" % (str(False), str(result)))
        #test as elements
        result = Tree.equal(self.testtree.getroot(), comparetree.getroot())
        self.assertIs(result, False, "equal() failed: expected %s, got %s" % (str(False), str(result)))
        
    def test_NotATree(self):
        result = Tree.equal(None, None)
        self.assertIs(result, False, "equal() failed: expected %s, got %s" % (str(False), str(result)))
        
    def test_EqualSubtrees(self):
        #TreeTestFile_equal2.xml is a subtree of TreeTestFile_reference.xml, ie self.testtree
        #The matching subtree is at self.testtree.getroot()[1]
        comparetree = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_equal2.xml'))
        result = Tree.equal(self.testtree.getroot()[1], comparetree)
        self.assertIs(result, True, "equal() failed: expected %s, got %s" % (str(True), str(result)))
        #test as elements
        result = Tree.equal(self.testtree.getroot()[1], comparetree.getroot())
        self.assertIs(result, True, "equal() failed: expected %s, got %s" % (str(True), str(result)))
        
    def test_UnequalSubtrees(self):
        #TreeTestFile_equal2.xml is a subtree of TreeTestFile_reference.xml, ie self.testtree
        #The matching subtree is at self.testtree.getroot()[1]. This test, however, uses [0]
        comparetree = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_equal2.xml'))
        result = Tree.equal(self.testtree.getroot()[0], comparetree)
        self.assertIs(result, False, "equal() failed: expected %s, got %s" % (str(False), str(result)))
        #test as elements
        result = Tree.equal(self.testtree.getroot()[0], comparetree.getroot())
        self.assertIs(result, False, "equal() failed: expected %s, got %s" % (str(False), str(result)))
        




class test_ordering(unittest.TestCase):
    """Test the ordering() function"""
    
    def setUp(self):
        self.log = logging.getLogger()
        self.testfile = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'Tree', 'Ordering', 'TreeTestFile_reference.xml')
        self.testtree = lxml.etree.parse(self.testfile)
        
        self.treeOrdering = Tree.ordering(self.testtree)
        self.expectedTreeOrdering = [
                                 [1],
                                 [1, 1],
                                 [1, 1, 1], 
                                 [1, 2],
                                 [1, 2, 1], 
                                 [1, 2, 2], 
                                 [1, 2, 3], 
                                 [1, 2, 3, 1],
                                 [1, 2, 3, 1, 1],
                                ]  
        
        self.subtreeOrdering = Tree.ordering(self.testtree.getroot()[1])
        self.expectedSubtreeOrdering =  [
                                         [1],
                                         [1, 1],
                                         [1, 2], 
                                         [1, 3], 
                                         [1, 3, 1],
                                         [1, 3, 1, 1]
                                        ]
        
        
    
    def test_Length(self):
        self.assertEqual(len(self.treeOrdering), len(self.expectedTreeOrdering), 'ordering() returned an ordering with the wrong length: expected %i, got %i' \
                         % (len(self.expectedTreeOrdering), len(self.treeOrdering)))
    
    def test_SubtreeLength(self):
        self.assertEqual(len(self.expectedSubtreeOrdering), len(self.subtreeOrdering), 'ordering() returned an ordering with the wrong length: expected %i, got %i' \
                         % (len(self.expectedSubtreeOrdering), len(self.subtreeOrdering)))
    
    
    def test_Positions(self):
        for index, p in enumerate(self.treeOrdering):
            self.assertEqual(p, self.expectedTreeOrdering[index], "ordering() returned a list with incorrect entry at index %i: expected %s, got %s" \
                              % (index, str(self.expectedTreeOrdering[index]), str(p)))
    
    def test_SubtreePositions(self):
        for index, p in enumerate(self.subtreeOrdering):
            self.assertEqual(self.expectedSubtreeOrdering[index], p, "ordering() returned a list with incorrect entry at index %i: expected %s, got %s" \
                              % (index, str(self.expectedSubtreeOrdering[index]), str(p)))
    
    
    def test_Nodes(self):
        expectednodes = [
                         lxml.etree.Element('xml'),
                         lxml.etree.Element('node', {'id': '1'}),
                         lxml.etree.Element('child', {'id': '2'}),
                         lxml.etree.Element('node', {'id': '3'}),
                         lxml.etree.Element('child1', {'id': '4'}),
                         lxml.etree.Element('child2', {'id': '5'}),
                         lxml.etree.Element('child3', {'id': '6'}),
                         lxml.etree.Element('grandchild', {'id': '7'}),
                         lxml.etree.Element('newborn', {'id': '8'}),
                        ]
        
        for index, p in enumerate(self.treeOrdering):
            result = Tree.getNode(self.testtree, p)
            self.assertTrue(Element.Element.equal(result, expectednodes[index]), 'ordering returned a list with incorrect node position at index %i: expected %s %s, got %s %s,' \
                            % (index, expectednodes[index].tag, str(expectednodes[index].attrib), result.tag, str(result.attrib)))


    def test_SubtreeNodes(self):
        expectednodes = [
                         lxml.etree.Element('node', {'id': '3'}),
                         lxml.etree.Element('child1', {'id': '4'}),
                         lxml.etree.Element('child2', {'id': '5'}),
                         lxml.etree.Element('child3', {'id': '6'}),
                         lxml.etree.Element('grandchild', {'id': '7'}),
                         lxml.etree.Element('newborn', {'id': '8'}),
                        ]
        
        for index, p in enumerate(self.subtreeOrdering):
            result = Tree.getNode(self.testtree.getroot()[1], p)
            self.assertTrue(Element.Element.equal(result, expectednodes[index]), 'ordering returned a list with incorrect node position at index %i: expected %s %s, got %s %s,' \
                            % (index, expectednodes[index].tag, str(expectednodes[index].attrib), result.tag, str(result.attrib)))






class test_getNode(unittest.TestCase):
    
    def setUp(self):
        self.testfile = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'Tree', 'GetNode', 'TreeTestFile_reference.xml')
        self.testtree = lxml.etree.parse(self.testfile)
    
    
    def test_RootNode(self):
        position = [1, 0, 0, 0, 0]
        result = Tree.getNode(self.testtree, position)
        expected = lxml.etree.Element('xml')
        
        self.assertTrue(Element.Element.equal(result, expected), 'getNode() returned the wrong node: expected %s %s, got %s %s' \
                        % (expected.tag, str(expected.attrib), result.tag, str(result.attrib)))
    
    
    def test_NestedOneLevel(self):
        position = [1, 1, 0, 0, 0]
        result = Tree.getNode(self.testtree, position)
        expected = lxml.etree.Element('node', {'id': '1'})
        
        self.assertTrue(Element.Element.equal(result, expected), 'getNode() returned the wrong node: expected %s %s, got %s %s' \
                        % (expected.tag, str(expected.attrib), result.tag, str(result.attrib)))
    
    
    def test_LowestLevel(self):
        position = [1, 2, 3, 1, 1]
        result = Tree.getNode(self.testtree, position)
        expected = lxml.etree.Element('newborn', {'id': '8'})
        
        self.assertTrue(Element.Element.equal(result, expected), 'getNode() returned the wrong node: expected %s %s, got %s %s' \
                        % (expected.tag, str(expected.attrib), result.tag, str(result.attrib)))
    
    
    def test_NotLastSibling(self):
        position = [1, 2, 2]
        result = Tree.getNode(self.testtree, position)
        expected = lxml.etree.Element('child2', {'id': '5'})
        
        self.assertTrue(Element.Element.equal(result, expected), 'getNode() returned the wrong node: expected %s %s, got %s %s' \
                        % (expected.tag, str(expected.attrib), result.tag, str(result.attrib)))
        
        
    def test_SecondChildOfRoot(self):
        position = [1, 2]
        result = Tree.getNode(self.testtree, position)
        expected = lxml.etree.Element('node', {'id': '3'})
        
        self.assertTrue(Element.Element.equal(result, expected), 'getNode() returned the wrong node: expected %s %s, got %s %s' \
                        % (expected.tag, str(expected.attrib), result.tag, str(result.attrib)))
    
    
    def test_NodeFromSubtree(self):
        position = [1, 3, 1, 1]
        result = Tree.getNode(self.testtree.getroot()[1], position)
        expected = lxml.etree.Element('newborn', {'id': '8'})
        
        self.assertTrue(Element.Element.equal(expected, result), 'getNode() returned the wrong node: expected %s %s, got %s %s' \
                        % (expected.tag, str(expected.attrib), result.tag, str(result.attrib)))
    
    
    def test_RootOfSubtree(self):
        position = [1]
        result = Tree.getNode(self.testtree.getroot()[1], position)
        expected = lxml.etree.Element('node', {'id': '3'})
        
        self.assertTrue(Element.Element.equal(expected, result), 'getNode() returned the wrong node: expected %s %s, got %s %s' \
                        % (expected.tag, str(expected.attrib), result.tag, str(result.attrib)))
        
    
    
    
    
    
class test_add(unittest.TestCase):
    
    
    def setUp(self):
        self.log = logging.getLogger()
        self.testfilesdir = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'Tree', 'Add')
    
    
    def test_SimpleTrees_EqualStructures(self):
        
        self.log.debug('')
        self.log.debug('')
        self.log.debug('starting %s' % __name__)
        
        expectedtree = lxml.etree.fromstring('<e> <g id="2"/> </e>')
        
        tree1 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add1.xml'))
        tree2 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add2.xml'))
        Tree.add(tree1, tree2)
        self.assertTrue(Tree.equal(tree1, expectedtree), "Add failed, created incorrect tree")
         
        #test adding elements
        tree1 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add1.xml'))
        tree2 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add2.xml'))
        Tree.add(tree1.getroot(), tree2.getroot())
        self.assertTrue(Tree.equal(tree1, expectedtree), "Add failed, created incorrect tree")
                                       
    
    
    
    def test_ComplexTrees_EqualStructures(self):
        
        self.log.debug('')
        self.log.debug('')
        self.log.debug('starting %s' % __name__)
        
        expectedtree = lxml.etree.fromstring("""
                                        <c>
                                            <e id='2'/>
                                            <e id='3'>
                                                <g id='4'>
                                                    <i id='5'/>
                                                </g>
                                                <g id="6"/>
                                            </e>
                                        </c>
                                        """)
        
        tree1 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add3.xml'))
        tree2 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add4.xml'))
        Tree.add(tree1, tree2)
        self.assertTrue(Tree.equal(tree1, expectedtree), "Add failed, created incorrect tree")
        
        #test adding elements, which in the tree group theory are the same as trees
        tree1 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add3.xml'))
        tree2 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add4.xml'))
        Tree.add(tree1.getroot(), tree2.getroot())
        self.assertTrue(Tree.equal(tree1, expectedtree), "Add failed, created incorrect tree")
        
        
    
    def test_AddUnit(self):
        
        self.log.debug('')
        self.log.debug('')
        self.log.debug('starting %s' % __name__)
        
        expectedtree = lxml.etree.fromstring("""
                                            <a>
                                                <b id='1'/>
                                                <b id='2'>
                                                    <c id='3'>
                                                        <d id='4'/>
                                                    </c>
                                                    <c id="5"/>
                                                </b>
                                            </a>
                                            """)
        
        tree1 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add3.xml'))
        tree2 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_unit.xml'))
        Tree.add(tree1, tree2)
        self.assertTrue(Tree.equal(tree1, expectedtree), "Add failed, created incorrect tree")
 
        #test element addition
        tree1 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add3.xml'))
        tree2 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_unit.xml'))
        Tree.add(tree1.getroot(), tree2.getroot())
        self.assertTrue(Tree.equal(tree1, expectedtree), "Add failed, created incorrect tree")
 
    
    
    
    def test_SimpleTrees_UnequalStructures(self):
        
        self.log.debug('')
        self.log.debug('')
        self.log.debug('starting %s' % __name__)
        
        expectedtree = lxml.etree.fromstring("""<b> 
                                                    <d id="2"/> 
                                                    <g id="1"/>
                                                </b>""")
        
        tree1 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add5.xml'))
        tree2 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add6.xml'))
        Tree.add(tree1, tree2)
        self.assertTrue(Tree.equal(tree1, expectedtree), "Add failed, created incorrect tree")
        
        #test element addition
        tree1 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add5.xml'))
        tree2 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add6.xml'))
        Tree.add(tree1.getroot(), tree2.getroot())
        self.assertTrue(Tree.equal(tree1, expectedtree), "Add failed, created incorrect tree")
        
        
        
    def test_ComplexTrees_UnequalStructures(self):
        
        self.log.debug('')
        self.log.debug('')
        self.log.debug('starting %s' % __name__)
        
        expectedtree = lxml.etree.fromstring("""<c>
                                                    <c id='a'/>
                                                    <e id='3'>
                                                        <g id='4'>
                                                            <d id='4'/>
                                                        </g>
                                                        <g id="6"/>
                                                    </e>
                                                    <e id='6'>
                                                        <f id="7">
                                                            <g id='8'/>
                                                        </f>
                                                        <f id="8"/>
                                                    </e>
                                                </c>
                                            """)
        
        tree1 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add7.xml'))
        tree2 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add8.xml'))
        Tree.add(tree1, tree2)
        self.assertTrue(Tree.equal(tree1, expectedtree), "Add failed, created incorrect tree. Expected %s, got %s" \
                        % (lxml.etree.tostring(expectedtree, pretty_print=True), lxml.etree.tostring(tree1, pretty_print=True)))
        
        #test elements
        tree1 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add7.xml'))
        tree2 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add8.xml'))
        Tree.add(tree1.getroot(), tree2.getroot())
        self.assertTrue(Tree.equal(tree1, expectedtree), "Add failed, created incorrect tree. Expected %s, got %s" \
                        % (lxml.etree.tostring(expectedtree, pretty_print=True), lxml.etree.tostring(tree1, pretty_print=True)))
         
        
        
        
    def test_ComplexTrees_SeveralUnitsInOperand(self):
                    
        self.log.debug('')
        self.log.debug('')
        self.log.debug('starting %s' % __name__)
        
        expectedtree = lxml.etree.fromstring("""
                                                <c>
                                                    <b id='2'>
                                                        <c id='3'>
                                                            <d id="4"/>
                                                        </c>
                                                        <c id="5"/>
                                                    </b>
                                                    <b id="4"/>
                                                </c>
                                            """)
        
        tree1 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add9.xml'))
        tree2 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add10.xml'))
        Tree.add(tree1, tree2)
        self.assertTrue(Tree.equal(tree1, expectedtree), "Add failed, created incorrect tree. Expected %s, got %s" \
                        % (lxml.etree.tostring(expectedtree, pretty_print=True), lxml.etree.tostring(tree1, pretty_print=True)))
    
        #test elements    
        tree1 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add9.xml'))
        tree2 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add10.xml'))
        Tree.add(tree1.getroot(), tree2.getroot())
        self.assertTrue(Tree.equal(tree1, expectedtree), "Add failed, created incorrect tree. Expected %s, got %s" \
                        % (lxml.etree.tostring(expectedtree, pretty_print=True), lxml.etree.tostring(tree1, pretty_print=True)))
    
    
    
    
    def test_ComplexTrees_TrailingUnitsInResult(self):
                
        self.log.debug('')
        self.log.debug('')
        self.log.debug('starting %s' % __name__)
        
        expectedtree = lxml.etree.fromstring("""    
                                            <c>
                                                <_>
                                                    <c id='3'>
                                                        <d id="4"/>
                                                    </c>
                                                    <c id="5"/>
                                                </_>
                                            </c>
                                            """)
                                                
        tree1 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add11.xml'))
        tree2 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add12.xml'))
        Tree.add(tree1, tree2)
        self.assertTrue(Tree.equal(tree1, expectedtree), "Add failed, created incorrect tree. Expected %s, got %s" \
                        % (lxml.etree.tostring(expectedtree, pretty_print=True), lxml.etree.tostring(tree1, pretty_print=True)))
        
        #test elements
        tree1 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add11.xml'))
        tree2 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add12.xml'))
        Tree.add(tree1.getroot(), tree2.getroot())
        self.assertTrue(Tree.equal(tree1, expectedtree), "Add failed, created incorrect tree. Expected %s, got %s" \
                        % (lxml.etree.tostring(expectedtree, pretty_print=True), lxml.etree.tostring(tree1, pretty_print=True)))
        
        
    def test_Subtrees(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('starting test_Subtrees')
        
        expectedtree = lxml.etree.fromstring("""
                                            <_>
                                                <c id='3'>
                                                    <d id="4"/>
                                                </c>
                                                <c id="5"/>
                                            </_>
                                            """)
                                                
        tree1 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add11.xml'))
        tree2 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add12.xml'))
        Tree.add(tree1.getroot()[0], tree2.getroot()[0])
        self.assertTrue(Tree.equal(tree1.getroot()[0], expectedtree), "Add failed, created incorrect tree. Expected %s, got %s" \
                        % (lxml.etree.tostring(expectedtree, pretty_print=True), lxml.etree.tostring(tree1.getroot()[0], pretty_print=True)))
            
        
        
    def test_SubtreeToTree(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('starting test_SubtreeToTree')
        
        expectedtree = lxml.etree.fromstring("""
                                            <_ id="a">
                                                <b id='9'>
                                                    <g id="X"/>
                                                </b>
                                                <h id='1'>
                                                    <f id="7">
                                                        <g id='8'/>
                                                    </f>
                                                    <f id="8"/>
                                                </h>
                                            </_>
                                            """)
                                                
        tree1 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add11.xml'))
        tree2 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add12.xml'))
        Tree.add(tree1, tree2.getroot()[0])
        self.assertTrue(Tree.equal(tree1, expectedtree), "Add failed, created incorrect tree. Expected %s, got %s" \
                        % (lxml.etree.tostring(expectedtree, pretty_print=True), lxml.etree.tostring(tree1, pretty_print=True)))
            
        
        
        
    def test_TreeToSubtree(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('starting test_TreeToSubtree')
        
        expectedtree = lxml.etree.fromstring("""
                                            <_ id="a">
                                                <b id='9'>
                                                    <g id="X"/>
                                                </b>
                                                <h id='1'>
                                                    <f id="7">
                                                        <g id='8'/>
                                                    </f>
                                                    <f id="8"/>
                                                </h>
                                            </_>
                                            """)
                                                
        tree1 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add11.xml'))
        tree2 = lxml.etree.parse(os.path.join(self.testfilesdir, 'TreeTestFile_add12.xml'))
        Tree.add(tree2.getroot()[0], tree1)
        self.assertTrue(Tree.equal(tree2.getroot()[0], expectedtree), "Add failed, created incorrect tree. Expected %s, got %s" \
                        % (lxml.etree.tostring(expectedtree, pretty_print=True), lxml.etree.tostring(tree2.getroot()[0], pretty_print=True)))
            
            
            
            
            
        
        
        
class test_invert(unittest.TestCase):
    """Test the invert() function"""
    
    def setUp(self):
        self.log = logging.getLogger()
    
    
    
    def test_SimpleTree(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('starting %s' % __name__)
        
        expectedtree = lxml.etree.fromstring("""    
                                            <Z>
                                                <Y id='i'/>
                                            </Z>
                                            """)
                                                
        tree = lxml.etree.parse(os.path.join(os.path.dirname(__file__),  '..', 'testfiles', 'Tree', 'Invert', 'TreeTestFile_invert1.xml'))
        Tree.invert(tree)
        self.assertTrue(Tree.equal(tree, expectedtree), "invert() failed, created incorrect tree. Expected %s, got %s" \
                        % (lxml.etree.tostring(expectedtree, pretty_print=True), lxml.etree.tostring(tree, pretty_print=True)))
    
    
    
    
    
    def test_ComplexTree(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('starting %s' % __name__)
        
        expectedtree = lxml.etree.fromstring("""    
                                            <Z>
                                                <_/>
                                                <Y id='i'/>
                                                <Y id='h'>
                                                    <X id='g'>
                                                        <W id='f'/>
                                                    </X>
                                                    <X id="e"/>
                                                </Y>
                                            </Z>
                                            """)
                                                
        tree = lxml.etree.parse(os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'Tree', 'Invert', 'TreeTestFile_invert2.xml'))
        Tree.invert(tree)
        self.assertTrue(Tree.equal(tree, expectedtree), "invert() failed, created incorrect tree. Expected %s, got %s" \
                        % (lxml.etree.tostring(expectedtree, pretty_print=True), lxml.etree.tostring(tree, pretty_print=True)))
    
    
    
    
    
    def test_UnitTree(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('starting %s' % __name__)
        
        expectedtree = lxml.etree.fromstring("""    
                                            <_/>
                                            """)
                                                
        tree = lxml.etree.parse(os.path.join(os.path.dirname(__file__),  '..', 'testfiles', 'Tree', 'Invert', 'TreeTestFile_invert3.xml'))
    
        Tree.invert(tree)
        self.assertTrue(Tree.equal(tree, expectedtree), "invert() failed, created incorrect tree. Expected %s, got %s" \
                        % (lxml.etree.tostring(expectedtree, pretty_print=True), lxml.etree.tostring(tree, pretty_print=True)))
    
    
    
    
    
    def test_InverseAddition(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('starting %s' % __name__)
        
        unittree = lxml.etree.fromstring("""    
                                        <_/>
                                        """)
                                                
        tree1 = lxml.etree.parse(os.path.join(os.path.dirname(__file__),  '..', 'testfiles', 'Tree', 'Invert', 'TreeTestFile_invert2.xml'))
        tree2 = copy.deepcopy(tree1)
        Tree.invert(tree1)
        Tree.add(tree1, tree2)
        self.assertTrue(Tree.equal(tree1, unittree), "invert() failed, created incorrect tree, did not add to unit")
    
    
    
    
    def test_Subtree(self):
        self.log.debug('')
        self.log.debug('')
        self.log.debug('starting %s' % __name__)
        
        expectedtree = lxml.etree.fromstring("""
                                            <Y id='h'>
                                                <X id='g'>
                                                    <W id='f'/>
                                                </X>
                                                <X id="e"/>
                                            </Y>
                                            """)
                                                
        tree = lxml.etree.parse(os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'Tree', 'Invert', 'TreeTestFile_invert2.xml'))
        Tree.invert(tree.getroot()[2])
        self.assertTrue(Tree.equal(tree.getroot()[2], expectedtree), "invert() failed, created incorrect tree. Expected %s, got %s" \
                        % (lxml.etree.tostring(expectedtree, pretty_print=True), lxml.etree.tostring(tree.getroot()[2], pretty_print=True)))
    
    
    