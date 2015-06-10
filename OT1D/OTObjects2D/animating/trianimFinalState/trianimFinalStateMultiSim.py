#_____________________________
# trianimFinalStateMultiSim.py
#_____________________________
#
# util to plot the final state for multiple simulations 
#

import numpy                as np
import matplotlib.pyplot    as plt

from matplotlib.animation           import FuncAnimation

from ....utils.io.io                import fileNameSuffix
from ....utils.io.extractFinalState import extractFinalStateMultiSim
from ....utils.plotting.positions   import figureRect
from ....utils.plotting.positions   import xylims2d
from ....utils.plotting.plotting    import makeAxesGridTriplot
from ....utils.plotting.plotting    import adaptAxesExtent
from ....utils.plotting.plot        import addTitleLabelsGrid
from ....utils.plotting.plot        import addTimeTextPBar
from ....utils.plotting.plot        import plotTimeTextPBar
from ....utils.plotting.plotMatrix  import addColorBar
from ....utils.plotting.plotMatrix  import plotMatrix

#__________________________________________________ 

def makeTrianimFinalStateMultiSim(kwargsFuncAnim,
                                  outputDirList,
                                  figDir,
                                  labelList,
                                  plotter,
                                  kwargs,
                                  colorBar,
                                  cmapName,
                                  timeTextPBar,
                                  xLabel,
                                  yLabel,
                                  cLabel,
                                  extendX,
                                  extendY,
                                  nbrXTicks,
                                  nbrYTicks,
                                  nbrCTicks,
                                  xTicksDecimals,
                                  yTicksDecimals,
                                  cticksDecimals,
                                  order,
                                  extendDirection,
                                  extendDirectionTriplot,
                                  EPSILON):

    (fs, finits, ffinals, mini, maxi, Pmax) = extractFinalStateMultiSim(outputDirList)
    (xmin, xmax, ymin, ymax)                = xylims2d()

    figure = plt.figure()
    plt.clf()

    (gs, axes, axesInit, axesFinal) = makeAxesGridTriplot(plt, len(outputDirList), order, extendDirection, extendDirectionTriplot)

    for (f, finit, ffinal, label, ax, axInit, axFinal) in zip(fs, finits, ffinals, labelList, axes, axesInit, axesFinal):

        imC = plotMatrix(ax,
                         f[:,:,0],
                         plotter=plotter,
                         xmin=xmin,
                         xmax=xmax,
                         ymin=ymin,
                         ymax=ymax,
                         cmapName=cmapName,
                         vmin=mini,
                         vmax=maxi,
                         **kwargs)
        imI = plotMatrix(axInit,
                         finit,
                         plotter=plotter,
                         xmin=xmin,
                         xmax=xmax,
                         ymin=ymin,
                         ymax=ymax,
                         cmapName=cmapName,
                         vmin=mini,
                         vmax=maxi,
                         **kwargs)
        imF = plotMatrix(axFinal,
                         ffinal,
                         plotter=plotter,
                         xmin=xmin,
                         xmax=xmax,
                         ymin=ymin,
                         ymax=ymax,
                         cmapName=cmapName,
                         vmin=mini,
                         vmax=maxi,
                         **kwargs)

        adaptAxesExtent(ax, xmin, xmax, ymin, ymax, extendX, extendY, nbrXTicks, nbrYTicks, xTicksDecimals, yTicksDecimals, EPSILON)
        addTitleLabelsGrid(ax, title=label, xLabel=xLabel, yLabel=yLabel, grid=False)
        adaptAxesExtent(axInit, xmin, xmax, ymin, ymax, extendX, extendY, nbrXTicks, nbrYTicks, xTicksDecimals, yTicksDecimals, EPSILON)
        addTitleLabelsGrid(axInit, title=label+', init', xLabel=xLabel, yLabel=yLabel, grid=False)
        adaptAxesExtent(axFinal, xmin, xmax, ymin, ymax, extendX, extendY, nbrXTicks, nbrYTicks, xTicksDecimals, yTicksDecimals, EPSILON)
        addTitleLabelsGrid(axFinal, title=label+', final', xLabel=xLabel, yLabel=yLabel, grid=False)


    gs.tight_layout(figure, rect=figureRect(colorBar, timeTextPBar))
    if colorBar:
        (cax, cbar)   = addColorBar(plt, timeTextPBar, cmapName, mini, maxi, nbrCTicks, cticksDecimals, cLabel)

    if timeTextPBar:
        (TTPBax, ret) = addTimeTextPBar(plt, 0, Pmax+1)

    def animate(t):
        ret = []

        for (f, finit, ffinal, label, ax, axInit, axFinal) in zip(fs, finits, ffinals, labelList, axes, axesInit, axesFinal):
            ax.cla()
            imC = plotMatrix(ax,
                             f[:,:,t],
                             plotter=plotter,
                             xmin=xmin,
                             xmax=xmax,
                             ymin=ymin,
                             ymax=ymax,
                             cmapName=cmapName,
                             vmin=mini,
                             vmax=maxi,
                             **kwargs)
            imI = plotMatrix(axInit,
                             finit,
                             plotter=plotter,
                             xmin=xmin,
                             xmax=xmax,
                             ymin=ymin,
                             ymax=ymax,
                             cmapName=cmapName,
                             vmin=mini,
                             vmax=maxi,
                             **kwargs)
            imF = plotMatrix(axFinal,
                             ffinal,
                             plotter=plotter,
                             xmin=xmin,
                             xmax=xmax,
                             ymin=ymin,
                             ymax=ymax,
                             cmapName=cmapName,
                             vmin=mini,
                             vmax=maxi,
                             **kwargs)
            ret.extend([imC,imI,imF])

            adaptAxesExtent(ax, xmin, xmax, ymin, ymax, extendX, extendY, nbrXTicks, nbrYTicks, xTicksDecimals, yTicksDecimals, EPSILON)
            addTitleLabelsGrid(ax, title=label, xLabel=xLabel, yLabel=yLabel, grid=False)
            adaptAxesExtent(axInit, xmin, xmax, ymin, ymax, extendX, extendY, nbrXTicks, nbrYTicks, xTicksDecimals, yTicksDecimals, EPSILON)
            addTitleLabelsGrid(axInit, title=label+', init', xLabel=xLabel, yLabel=yLabel, grid=False)
            adaptAxesExtent(axFinal, xmin, xmax, ymin, ymax, extendX, extendY, nbrXTicks, nbrYTicks, xTicksDecimals, yTicksDecimals, EPSILON)
            addTitleLabelsGrid(axFinal, title=label+', final', xLabel=xLabel, yLabel=yLabel, grid=False)

        if timeTextPBar:
            TTPBax.cla()
            ret.extend(plotTimeTextPBar(TTPBax, t, Pmax+1))

        return tuple(ret)

    def init():
        return animate(0)

    frames = np.arange(Pmax+2)
    print('Making animation ...')
    return FuncAnimation(figure, animate, frames, init_func=init, **kwargsFuncAnim)

#__________________________________________________ 
