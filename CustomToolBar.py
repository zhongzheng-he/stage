from PyMca import PyMcaQt as qt
from  DoubleSlider import DoubleSlider
from LabelEditAndButton import LabelEditAndButton

class CustomToolBar(qt.QToolBar):

    def __init__(self, parent):
        '''
        Constructor
        '''
        qt.QToolBar.__init__(self, parent)
        self.setIconSize(qt.QSize(25, 25))

        self.zoomAutoAction = qt.QAction(qt.QIcon('Icones/autozoom.png'), '&Zoom', self)
        self.zoomAutoAction.setStatusTip('Fit window')
        self.zoomAutoAction.setCheckable(False)
        self.zoomAutoAction.setChecked(False)
        self.zoomActive = False
        qt.QObject.connect(self.zoomAutoAction, qt.SIGNAL("triggered()"), self.zoomAutoPushed)

        self.zone1Action = qt.QAction(qt.QIcon('Icones/zone.png'), '&ZoneSelection', self)
        self.zone1Action.setStatusTip('Select Zone')
        self.zone1Action.setCheckable(True)
        self.zone1Action.setChecked(False)
        qt.QObject.connect(self.zone1Action, qt.SIGNAL("triggered()"), self.zone1Selected)

        self.pointerAction = qt.QAction(qt.QIcon('Icones/cursor.png'), '&PointerSelection', self)
        self.pointerAction.setStatusTip('Select Pointer')
        self.pointerAction.setCheckable(True)
        self.pointerAction.setChecked(True)
        qt.QObject.connect(self.pointerAction, qt.SIGNAL("triggered()"), self.pointerSelected)

        self.drawingAction = qt.QAction(qt.QIcon('Icones/circle18.png'), '&DrawingSelection', self)
        self.drawingAction.setStatusTip('Select Drawing')
        self.drawingAction.setCheckable(True)
        self.drawingAction.setChecked(False)
        qt.QObject.connect(self.drawingAction, qt.SIGNAL("triggered()"), self.drawingSelected)

        self.polygonAction = qt.QAction(qt.QIcon('Icones/polygon.png'), '&PolygonSelection', self)
        self.polygonAction.setStatusTip('Select Polygone')
        self.polygonAction.setCheckable(True)
        self.polygonAction.setChecked(False)
        qt.QObject.connect(self.polygonAction, qt.SIGNAL("triggered()"), self.polygonSelected)

        self.pointRemoveAction = qt.QAction(qt.QIcon('Icones/remove.png'), '&DeletePoint', self)
        self.pointRemoveAction.setStatusTip('remove Point')
        self.pointRemoveAction.setCheckable(False)
        self.pointRemoveAction.setChecked(False)

        self.radius = LabelEditAndButton(True, "", True, str(100), False)

        self.doubleSlider = DoubleSlider(self)
        self.setMinAndMaxToolBar(0, 0)
        self.doubleSlider.setMaximumWidth(800)

        self.colorChoice = qt.QComboBox()
        self.colormapList = []
        colorMapDefault = "GrayLevel", range(256), range(256), range(256)
        self.colormapList.append(colorMapDefault)
        self.colorChoice.addItems([self.colormapList[0][0]])
        self.addColorMap('Jet', './jet_color.txt')

        self.addAction(self.zoomAutoAction)
        self.addSeparator()
        self.addAction(self.pointerAction)
        self.addAction(self.zone1Action)
        self.addAction(self.drawingAction)
        self.ActionRadius = self.addWidget(self.radius)
        self.ActionRadius.setVisible(False)
        self.addAction(self.polygonAction)
        self.addAction(self.pointRemoveAction)
        self.addWidget(self.doubleSlider)
        self.addWidget(self.colorChoice )

    def setMinAndMaxToolBar(self, min, max):
        self.doubleSlider.minSlider.setRange(min, max)
        self.doubleSlider.minSlider.setValue(min)
        self.doubleSlider.maxSlider.setRange(min, max)
        self.doubleSlider.maxSlider.setValue(max)
        self.doubleSlider.setMinMax(min, max)

    def zoomPushed(self):

        if (self.zoomAutoAction.isChecked() == True):
            self.zoomAutoAction.setChecked(False)
            self.zoomActive = False
        else:
            self.zoomAction.setChecked(True)
            self.zoomActive = True


    def zoomAutoPushed(self):
        self.zone1Action.setChecked(False)
        self.pointerAction.setChecked(False)


    def zone1Selected(self):
        self.ActionRadius.setVisible(0)

        if (self.pointerAction.isChecked() == True):
            self.pointerAction.setChecked(False)

        if (self.drawingAction.isChecked() == True):
            self.drawingAction.setChecked(False)

        if self.polygonAction.isChecked() == True:
            self.polygonAction.setChecked(False)

    def pointerSelected(self):
        self.ActionRadius.setVisible(0)

        if (self.zone1Action.isChecked() == True):
            self.zone1Action.setChecked(False)

        if (self.drawingAction.isChecked() == True):
            self.drawingAction.setChecked(False)

        if self.polygonAction.isChecked() == True:
            self.polygonAction.setChecked(False)

    def drawingSelected(self):

        self.ActionRadius.setVisible(1)

        if (self.pointerAction.isChecked() == True):
            self.pointerAction.setChecked(False)
        if (self.zone1Action.isChecked() == True):
            self.zone1Action.setChecked(False)

        if self.polygonAction.isChecked() == True:
            self.polygonAction.setChecked(False)

    def polygonSelected(self):

        self.ActionRadius.setVisible(0)

        if (self.pointerAction.isChecked() == True):
            self.pointerAction.setChecked(False)

        if (self.zone1Action.isChecked() == True):
            self.zone1Action.setChecked(False)

        if (self.drawingAction.isChecked() == True):
            self.drawingAction.setChecked(False)

    def addColorMap(self, name, path):

        f = open(path)
        R = []
        G = []
        B = []
        for line in f:

            listColor =  line.split(' ')
            R.append((float(listColor[0])*255))
            G.append((float(listColor[1])*255))
            B.append((float(listColor[2])*255))

        NewcolorMap = name, R, G, B
        self.colormapList.append(NewcolorMap)
        self.colorChoice.addItem(name)