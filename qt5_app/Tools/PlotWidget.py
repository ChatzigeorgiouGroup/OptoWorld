

from PyQt5 import QtWidgets, QtGui, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

plt.rcParams['figure.constrained_layout.use'] = True

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=4, height=3, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # self.axes = self.fig.add_subplot(111)

        # self.fig, self.axes = plt.subplots(figsize = (15,5), constrained_layout = True, sharex = True)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    #        self.plot()

    # def plot(self):
    #     data = np.sin(np.linspace(0, 6 * np.pi, 1000)) * np.random.normal(1, 0.1, 1000)
    #     ax = self.figure.add_subplot(111)
    #     ax.plot(data, 'r-')
    #     ax.set_title('PyQt Matplotlib Example')
    #     self.draw()
    #     self.show()
    #
    # def boxplot(self):
    #     group1 = np.random.normal(10, 4, 1000)
    #     group2 = np.random.normal(15, 3, 1000)
    #     ax = self.figure.add_subplot(111)
    #     ax.set_title("Boxplot Example")
    #     ax.violinplot([group1, group2])
    #     self.draw()
    #     self.show()
    #
    # def clear(self):
    #     self.axes.cla()
    #     self.draw()


class PlotWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)
        self.canvas = PlotCanvas(parent=self)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.toggle_toolbar_action = QtWidgets.QAction("&Toggle Toolbar", self, triggered = self.toggle_toolbar)
        self.customContextMenuRequested.connect(self.contextMenuEvent_PlotWidget)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)
        self.toolbar.setVisible(False)

    def contextMenuEvent_PlotWidget(self, event):
        menu = QtWidgets.QMenu(self)
        menu.addAction(self.toggle_toolbar_action)
        menu.popup(self.mapToGlobal(event))

    def toggle_toolbar(self):
        if self.toolbar.isVisible() == False:
            self.toolbar.setVisible(True)
        else:
            self.toolbar.setVisible(False)


    def draw(self):
        self.canvas.draw()

    def plot(self, x, y, xname="X", yname="Y", plot_title=False, color="b", linewidth=2, alpha=1, clear_axis=True):
        if clear_axis:
            self.canvas.clear()
            ax = self.canvas.figure.add_subplot(111)
        else:
            ax = self.canvas.figure.gca()
        ax.plot(x, y, color=color, lw=linewidth, alpha=alpha)
        ax.set_xlabel(xname)
        ax.set_ylabel(yname)
        if not plot_title:
            ax.set_title(yname + " vs " + xname)
        else:
            ax.set_title(plot_title)
        self.canvas.figure.tight_layout()
        self.draw()
