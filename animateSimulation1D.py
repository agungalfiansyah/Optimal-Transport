#!/usr/bin/env python

#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

from OT.utils.sys.run                                import runCommand
from OT.utils.sys.argv                               import extractArgv
from OT.OTObjects1D.animating.animatingConfiguration import AnimatingConfiguration

# Extract Arguments
arguments   = extractArgv()
configFile  = arguments['CONFIG_FILE']

try:
    printIO = ( arguments['PRINT_IO'] == 'True' )
except:
    printIO = False

# Builds configuration
config      = AnimatingConfiguration(configFile)

# Creates figDir
runCommand('mkdir -p '+config.figDir, printIO)

# Animates
animator    = config.animator()
animator.animate()
