import param
import numpy as np

from ...element import Polygons, Contours, Distribution, Bivariate
from ...operation.stats import univariate_kde, bivariate_kde

from .chart import AreaPlot
from .path import PolygonPlot


class DistributionPlot(AreaPlot):
    """
    DistributionPlot visualizes a distribution of values as a KDE.
    """

    bw = param.Number(default=None)

    def __init__(self, element, **params):
        element = element.map(self._convert_element, Distribution)
        super(DistributionPlot, self).__init__(element, **params)

    def _convert_element(self, element):
        plot_opts = self.lookup_options(element, 'plot').options
        style_opts = self.lookup_options(element, 'style').options
        return univariate_kde(element, bandwidth=plot_opts.get('bw')).opts(plot=plot_opts, style=style_opts)



class BivariatePlot(PolygonPlot):
    """
    Bivariate plot visualizes two-dimensional kernel density
    estimates. Additionally, by enabling the joint option, the
    marginals distributions can be plotted alongside each axis (does
    not animate or compose).
    """

    bw = param.Number(default=None)

    filled = param.Boolean(default=False)

    def __init__(self, element, **params):
        element = element.map(self._convert_element, Bivariate)
        super(BivariatePlot, self).__init__(element, **params)

    def _convert_element(self, element):
        plot_opts = self.lookup_options(element, 'plot').options
        style_opts = self.lookup_options(element, 'style').options
        return bivariate_kde(element, contours=True, filled=plot_opts.get('filled', self.filled),
                             bandwidth=plot_opts.get('bw')).opts(plot=plot_opts, style=style_opts)
