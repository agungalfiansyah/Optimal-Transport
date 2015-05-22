#########################
# Class anamorphAlgorithm
#########################
#
# defines the compute the anamorphose
#

import numpy   as np
import time    as tm
import cPickle as pck

from scipy.interpolate import interp1d
from scipy.integrate   import cumtrapz

from ...OTObject import OTObject
from ...grid     import grid

class AnamorphAlgorithm( OTObject ):
    '''
    class to handle an anamorphose Algorithm
    '''

    def __init__(self, config):
        self.config = config
        OTObject.__init__(self, config.N , config.P)
        self.state = None
        
    def __repr__(self):
        return ( 'Anamorphose Algorithm' )

    def saveState(self):
        fileConfig   = self.config.outputDir + 'config.bin'
        fileState    = self.config.outputDir + 'finalState.bin'
        fileRunCount = self.config.outputDir + 'runCount.bin'
        fileTmap     = self.config.outputDir + 'Tmap.npy'

        try:
            f = open(fileConfig, 'ab')
            p = pck.Pickler(f,protocol=-1)
            p.dump(self.config)
            f.close()

            f = open(fileState, 'wb')
            p = pck.Pickler(f,protocol=-1)
            p.dump(self.state)
            f.close()

            try:
                f = open(fileRunCount, 'rb')
                p = pck.Unpickler(f)
                runCount = p.load()
                runCount += 1
                f.close()
            except:
                runCount = 1
                
            f = open(fileRunCount, 'wb')
            p = pck.Pickler(f,protocol=-1)
            p.dump(runCount)
            f.close()

            self.config.iterCount = 0
            self.config.iterTarget = 0

            print('__________________________________________________')
            print('Files written...')
            print(fileConfig)
            print(fileState)
            print(fileRunCount)
            print(fileTmap)
            print('__________________________________________________')

        except:
            print('__________________________________________________')
            print('WARNING : could not write output files')
            print('__________________________________________________')

    def run(self):
        self.config.iterTarget = 1
        fileCurrentState = self.config.outputDir + 'states.bin'
        fileTmap         = self.config.outputDir + 'Tmap.npy'    

        f = open(fileCurrentState, 'ab')
        p = pck.Pickler(f,protocol=-1)

        print('__________________________________________________')
        print('Starting algorithm...')
        print('__________________________________________________')
        self.config.printConfig()
        print('__________________________________________________')
        timeStart = tm.time()

        # Computing CDF for initial and final states
        N = self.config.N
        P = self.config.P

        fInitPP         = np.zeros(N+3)
        fInitPP[1:N+2]  = self.config.boundaries.temporalBoundaries.bt0[:]
        fFinalPP        = np.zeros(N+3)
        fFinalPP[1:N+2] = self.config.boundaries.temporalBoundaries.bt1[:]

        X               = np.zeros(N+3)
        X[1:N+2]        = np.linspace(0.5/(N+1.), 1.0-0.5/(N+1.), N+1)
        X[N+2]          = 1.0

        FInitMap        = interp1d(X, fInitPP)
        FFinalMap       = interp1d(X, fFinalPP)

        NN              = self.config.fineResolution
        XI              = np.linspace(0.0, 1.0, NN)
        FInitFine       = FInitMap(XI)
        FFinalFine      = FFinalMap(XI)

        NZmin           = min( ( FInitFine * ( FInitFine > 0 ) +
                                 FInitFine.max() * ( FInitFine <=0 ) ).min() ,
                               ( FFinalFine * ( FFinalFine > 0 ) +
                                 FFinalFine.max() * ( FFinalFine <=0 ) ).min() )


        tolerance         = 0.01
        FInitFine         = np.maximum(FInitFine,  tolerance*NZmin/NN)
        FFinalFine        = np.maximum(FFinalFine, tolerance*NZmin/NN)

        CDFInit           = cumtrapz(FInitFine, XI, initial=0.)
        CDFFinal          = cumtrapz(FFinalFine, XI, initial=0.)

        CDFFinal         *= CDFInit[NN-1] / CDFFinal[NN-1]

        CDFFinalMap       = interp1d(XI, CDFFinal)

        CDFInitPP         = np.zeros(NN+2)
        CDFInitPP[1:NN+1] = CDFInit[:]
        CDFInitPP[0]      = CDFInit[0] - 1.
        CDFInitPP[NN+1]   = CDFInit[NN-1] + 1.
        XIPP              = np.zeros(NN+2)
        XIPP[1:NN+1]      = XI[:]
        XIPP[0]           = XI[0]
        XIPP[NN+1]        = XI[NN-1]
        iCDFInitMap       = interp1d(CDFInitPP, XIPP)

        # T = CDFInit^(-1) o CDFFinal
        def Tmap(x):
            return iCDFInitMap( CDFFinalMap( x ) )

        # Computes the derivative of T by finate differences
        # on a finer grid (to try and avoid infinite derivative)
        # result is stored in partialXTarray
        Tarray               = Tmap(XI)

        partialXTarray       = np.zeros(NN+1)
        partialXTarray[1:NN] = NN * ( Tarray[1:] - Tarray[:NN-1] )
        partialXTarray[0]    = partialXTarray[1]
        partialXTarray[NN]   = partialXTarray[NN-1]

        Xpartial             = np.zeros(NN+1)
        Xpartial[1:NN]       = 0.5 * ( XI[1:] + XI[:NN-1] )
        Xpartial[NN]         = 1.0

        # avoid extremal values of partialXTarray
        partialXTarray       = np.minimum(10*partialXTarray.mean(), partialXTarray)

        # Computes maps associated to the derivative of T by interpolating         
        partialXTmap         = interp1d(Xpartial, partialXTarray)

        # Approximate solution of the optimal transport
        def func(x,t):
            return ( FInitMap( ( 1. - t ) * x + t * Tmap(x) ) *
                     abs( ( 1. - t ) + t * partialXTmap(x) ) )

        # Storing solution in a staggered grid
        x   = np.linspace(0.5/(N+1.), 1.0-0.5/(N+1.), N+1 )
        t   = np.linspace(0.0, 1.0, P+2)

        X,T = np.meshgrid(x,t,indexing='ij')
        fu  = func(X, T)

        # Now computes m to complete the solution of the optimal transport
        # We have df/dt + dm/dx = 0
        partialTfu         = P * ( fu[:,1:P+2] - fu[:,0:P+1] )

        # Computes mu = - int( partialTfu , x )
        mu                 = np.zeros(shape=(N+2,P+1))

        XpartialTfu        = np.zeros(N+3)
        XpartialTfu[1:N+2] = np.linspace(0.5/(N+1.), 1.0-0.5/(N+1.), N+1)
        XpartialTfu[N+2]   = 1.0

        Xmu                = np.linspace(0.0, 1.0, N+2)

        for t in xrange(P+1):
            ptfu           = interp1d(XpartialTfu, -partialTfu[:,t])
            ptfut          = ptfu(Xmu)
            mu[:,t]        = cumtrapz(ptfut, Xmu, initial=0.0)

            # Corrects boundary condition
            # this produce non zero divergence to the results
            # it could be appropriate to apply proxCdivb after this algorithm

            divError       = mu[N+1,t]
            mu[:,t]       -= divError / ( N + 2. )

        # Stores the whole solution in a StaggeredField
        self.state = grid.StaggeredField( N , P , mu , fu )

        self.config.iterCount = 1
        self.config.iterTarget = 1

        p.dump(self.state)
        p.dump(tm.time()-timeStart)

        timeAlgo = tm.time() - timeStart
        f.close()

        finalJ = self.state.interpolation().functionalJ()
        finalDiv = self.state.divergence().LInftyNorm()

        timeAlgo = tm.time() - timeStart
        print('__________________________________________________')
        print('Algorithm finished')
        print('J          = '+str(finalJ))
        print('div        = '+str(finalDiv))
        print('Time taken : '+str(timeAlgo))
        print('__________________________________________________')

        # Saves Tmap
        f = open(fileTmap, 'wb')
        np.save(f, XI)
        np.save(f, Tarray)
        f.close()
        
        self.saveState()
        return finalJ
