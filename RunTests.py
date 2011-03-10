#!/usr/bin/env python3

#Copyright 2010 DOMESTIC CHURCH COMMUNICATIONS ltd. (Samalander, a legal trade name of DOMESTIC CHURCH COMMUNICATIONS ltd.)    
#See the file "copyright.txt" at the root level of this module for full copyright notice.   

"""Run all the unittests"""

#have to use nose from here, instead of the standard nosetests script that come 
#with the nose package because of version conflicts between Python 2.5 and 3.1 that 
#I didn't manage to resolve. 

import sys
import nose, logging, os, os.path

log = logging.getLogger()
log.setLevel(logging.DEBUG)
 
warninghandler = logging.StreamHandler(sys.stdout)
warninghandler.setLevel(logging.WARNING)
warningformatter = logging.Formatter("%(module)8.8s.%(funcName)20.20s%(levelname)10.10s\t%(message)s")
warninghandler.setFormatter(warningformatter)
log.addHandler(warninghandler)

debughandler = logging.FileHandler(os.path.basename(__file__).replace('.py', '-debug.txt'), 'w', encoding='utf-8')
#debughandler = logging.StreamHandler(sys.stdout)
debughandler.setLevel(logging.DEBUG)
debugformatter = logging.Formatter("%(module)8.8s.%(funcName)20.20s%(levelname)10.10s\t\t%(message)s")
debughandler.setFormatter(debugformatter)
log.addHandler(debughandler)


nose.main()