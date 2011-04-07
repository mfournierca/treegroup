Welcome to Tree Group. 

This module defines operations that allow all document trees to be thought of
as elements of a group under addition. The addition, inverse, unit and equality
are all defined and proven to be valid. 

Details of proofs here? 

This theory allows you to think of trees as member of a group, or space. You can
add, subtract and invert trees, which can be used to move the trees through the 
space, i.e. convert trees from one to another. 

Metrics can also be defined, but as of 2011-04-07 this has not been done. 

This TreeGroup module is divided into Tree/, Element/ and Transforms/ folders. 

Elements/ contains basic definitions and operations individual elements of a tree. 
An element here is defined as an object that has a tag, attributes, but no children. 

Tree/ contains tree definitions and operations. A tree is defined, roughly, as a collection
of elements with parent-child relationships defined. 

Transforms/ contains tools and scripts which can be used to transform trees, i.e. move 
them. The transforms use the definitions and operations defined in the other folders. 


This module uses lxml.etree for parsing of documents, representation of trees and
as the foundation for all the operations. It should be noted that there may be some
confusion between the words "Tree" and "Element" as they are used in this TreeGroup 
module and in lxml.etree. 

In lxml.etree, both Elements and ElementTrees have child-parent relationships defined. 
This means that for the purposes of TreeGroup, they are both trees. The TreeGroup concept of
an Element that has no child relationships defined is not found in lxml.etree. 

The table below sums it up: 

Tree Group Term			lxml.etree term

Tree	--------------> Tree
	\
	  \---------------> Element				
						
						
Element --------------> No equivalent in lxml.etree.