"""Transform a tree into dita using an adapted A* pathfinding algorithm"""


import logging, lxml.etree, sys, optparse, re, copy

import DitaTools.Tree.File.Dita

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import Tree.Tree, Element.Element










#===============================================================================
# main
#===============================================================================

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
    pathfinder = AStarPathfinder(input)
    
    #perform transformation
    path = pathfinder.findPath()
    
    #add path to input
    
#    DitaTools.Tree.File.Dita.write_tree_to_file(transformer.tree, output)
    