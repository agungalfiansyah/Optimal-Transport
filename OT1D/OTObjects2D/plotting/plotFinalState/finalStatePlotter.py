######################
# finalStatePlotter.py
######################

from ....utils.plotting.defaultTransparency import defaultTransparency
from ....utils.plotting.defaultTransparency import fastVanishingTransparency
from ....utils.plotting.defaultTransparency import customTransparency

from plotFinalStateMultiSim                 import plotFinalStateMultiSim

class FinalStatePlotter:

    def __init__(self, plottingConfig):
        self.plottingConfig = plottingConfig

    def plot(self):
        if not self.plottingConfig.plotFinalState == 1:
            return

        if self.plottingConfig.plotFinalState_transparencyFunction == 'defaultTransparency':
            transparencyFunction = defaultTransparency
        elif self.plottingConfig.plotFinalState_transparencyFunction == 'fastVanishingTransparency':
            transparencyFunction = fastVanishingTransparency
        elif self.plottingConfig.plotFinalState_transparencyFunction == 'customTransparency':
            transparencyFunction = customTransparency

        if self.plottingConfig.singleOrMulti == 0:
            outputDirList = [self.plottingConfig.outputDir[0]]
            labelList     = [self.plottingConfig.label[0]]
        elif self.plottingConfig.singleOrMulti == 1:
            outputDirList = self.plottingConfig.outputDir
            labelList     = self.plottingConfig.label

        cmapName = 'jet'
        if self.plottingConfig.plotFinalState_colorBar == 1:
            cmapName = self.plottingConfig.plotFinalState_cmapName

        plotFinalStateMultiSim(outputDirList,
                               self.plottingConfig.figDir,
                               self.plottingConfig.plotFinalState_prefixFigName,
                               labelList,
                               transparencyFunction,
                               self.plottingConfig.plotFinalState_plotter,
                               self.plottingConfig.plotFinalState_args,
                               self.plottingConfig.plotFinalState_argsInit,
                               self.plottingConfig.plotFinalState_argsFinal,
                               self.plottingConfig.plotFinalState_colorBar,
                               cmapName,
                               self.plottingConfig.plotFinalState_timeTextPBar,
                               self.plottingConfig.plotFinalState_xLabel,
                               self.plottingConfig.plotFinalState_yLabel,
                               self.plottingConfig.plotFinalState_cLabel,
                               self.plottingConfig.plotFinalState_extendX,
                               self.plottingConfig.plotFinalState_extendY,
                               self.plottingConfig.plotFinalState_nbrXTicks,
                               self.plottingConfig.plotFinalState_nbrYTicks,
                               self.plottingConfig.plotFinalState_nbrCTicks,
                               self.plottingConfig.plotFinalState_xTicksDecimals,
                               self.plottingConfig.plotFinalState_yTicksDecimals,
                               self.plottingConfig.plotFinalState_cTicksDecimals,
                               self.plottingConfig.plotFinalState_order,
                               self.plottingConfig.plotFinalState_extendDirection,
                               self.plottingConfig.extension,
                               self.plottingConfig.EPSILON)

