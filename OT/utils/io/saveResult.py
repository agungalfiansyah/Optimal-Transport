#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
###############
# saveResult.py
###############

import cPickle as pck

from files import fileResult

def saveResult(outputDir, result):
    f = open(fileResult(outputDir), 'wb')
    p = pck.Pickler(f, protocol=-1)
    p.dump(result)
    f.close()

