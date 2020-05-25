# -*- coding: utf-8 -*-

from PyMca import PyMcaQt as qt
import numpy as np

from CustomToolBar import CustomToolBar
from SliderAndLabel import SliderAndLabel
from CustomGraphicsView import CustomGraphicsView


class SliceVisualizer(qt.QWidget):

    def __init__(self, planeSection, parent=None):
        qt.QWidget.__init__(self, parent)

        self.currentPlaneSection = planeSection

        self.scene = qt.QGraphicsScene()
        self.view = CustomGraphicsView(self.scene, self)

        self.sliceSlider = SliderAndLabel(self)
        self.sliceSlider._setRange(0,0)

        self.flagFirstCircle = True

        self.connect(self.view, qt.SIGNAL("CustomGraphicsViewEvent"), self.clickedOnView)
        self.connect(self.view,qt.SIGNAL("CustomGraphicsViewEvent"),self.mouseMoved)
        self.connect(self.sliceSlider.slider, qt.SIGNAL("valueChanged(int)"), self._changeSlice)

        self.Items = {}
        self.colortable = []
        self.posPolyPoints = []
        for i in range(256):
            self.colortable.append(qt.qRgb(i, i, i))

        layout = qt.QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.sliceSlider)
        self.setLayout(layout)

    def updateItems(self,items):
        self.Items = items

    def _changeSlice(self):
        self.scene.clear()

        if (self.currentPlaneSection == 0):

            if ('Circles' in self.Items):
                if len(self.Items['Circles']['Direction0']) != 0:
                    for circle in self.Items['Circles']['Direction0']:
                        if circle[2] == self.sliceSlider.value():
                            self.drawEllipse(circle[0],circle[1],circle[3])
                if len(self.Items['Zones']['Direction0']) != 0:

                    for zone in self.Items['Zones']['Direction0']:
                        if zone[2] == self.sliceSlider.value():
                            self.drawRect(zone[0] , zone[1] ,zone[3] ,zone[4] )

                if len(self.Items['Arrows']['Direction0']) != 0:

                    for arrow in self.Items['Arrows']['Direction0']:
                        if int(arrow[2]) == self.sliceSlider.value():
                            self.drawArrow(arrow[0] ,arrow[1] ,arrow[3] ,arrow[4] )

                if len(self.Items['Seeds']['Direction0']) != 0:
                    for Seed in self.Items['Seeds']['Direction0']:
                        if int(Seed[2]) == self.sliceSlider.value():
                            self.drawPoint(Seed[0],Seed[1])
                if len(self.Items['Poly']['Direction0'][0]) != 0:
                    for poly in self.Items['Poly']['Direction0']:
                        if len(poly) !=0:
                            if poly[-1][2] == self.sliceSlider.value():
                                listCoord = []
                                for coord in poly:
                                    listCoord.append([coord[0],coord[1]])
                                self.drawPoly(listCoord)

            self.slice = self.dataVolume[self.sliceSlider.value(), :, :]
            self.slice.squeeze()

        elif (self.currentPlaneSection == 1):

            if ('Circles' in self.Items):
                if len(self.Items['Circles']['Direction1']) != 0:
                    for circle in self.Items['Circles']['Direction1']:
                            if circle[1] == self.sliceSlider.value():
                                self.drawEllipse(circle[0],circle[2],circle[3])
                if len(self.Items['Zones']['Direction1']) != 0:
                    for zone in self.Items['Zones']['Direction1']:
                        if zone[1] == self.sliceSlider.value():
                            self.drawRect(zone[0] , zone[2] ,zone[3] ,zone[5] )

                if len(self.Items['Arrows']['Direction0']) != 0:
                    for arrow in self.Items['Arrows']['Direction0']:
                        if int(arrow[1]) == self.sliceSlider.value():
                            self.drawArrow(arrow[0] ,arrow[2] ,arrow[3] ,arrow[5] )

                if len(self.Items['Seeds']['Direction1']) != 0:
                    for seed in self.Items['Seeds']['Direction1']:
                        if int(seed[1]) == self.sliceSlider.value():
                            self.drawPoint(seed[0],seed[2])
                if len(self.Items['Poly']['Direction1'][0]) != 0:
                    for poly in self.Items['Poly']['Direction1']:
                        if len(poly) !=0:
                            if poly[-1][1] == self.sliceSlider.value():
                                listCoord = []
                                for coord in poly:
                                    listCoord.append([coord[0],coord[2]])
                                self.drawPoly(listCoord)
            self.slice = self.dataVolume[:, self.sliceSlider.value(), :]
            self.slice.squeeze()

        elif (self.currentPlaneSection == 2):
            if ('Circles' in self.Items):
                if len(self.Items['Circles']['Direction2']) != 0:
                    for circle in self.Items['Circles']['Direction2']:
                        if circle[0] == self.sliceSlider.value():
                            self.drawEllipse(circle[1],circle[2],circle[3])
                if len(self.Items['Zones']['Direction2']) != 0:
                    for zone in self.Items['Zones']['Direction2']:
                        if zone[0] == self.sliceSlider.value():
                            self.drawRect(zone[1] , zone[2] ,zone[4] ,zone[5] )

                if len(self.Items['Arrows']['Direction0']) != 0:

                    for arrow in self.Items['Arrows']['Direction0']:
                        if int(arrow[0]) == self.sliceSlider.value():
                            self.drawArrow(arrow[1] ,arrow[2] ,arrow[4] ,arrow[5] )

                if len(self.Items['Seeds']['Direction2']) != 0:
                    for seed in self.Items['Seeds']['Direction2']:
                        if int(seed[0]) == self.sliceSlider.value():
                            self.drawPoint(seed[1],seed[2])
                if len(self.Items['Poly']['Direction2'][0]) != 0:
                    for poly in self.Items['Poly']['Direction2']:
                        if len(poly) !=0:
                            if poly[-1][0] == self.sliceSlider.value():
                                listCoord = []
                                for coord in poly:
                                    listCoord.append([coord[1],coord[2]])
                                self.drawPoly(listCoord)

            self.slice = self.dataVolume[:, :, self.sliceSlider.value()]
            self.slice.squeeze()

        self.data = 255 * (self.slice - self.minimumValue) / (self.maximumValue - self.minimumValue)
        self.data[self.data >= 255] = 255
        self.data[self.data <= 0] = 0
        self.data = np.array(self.data, dtype=np.uint8)
        self.display_image()

    def _doubleSliderValueChanged(self, ddict):

        try:
            self.maximumValue = float(ddict['max'])
            self.minimumValue = float(ddict['min'])
        except:
            self.maximumValue = self.slice.max()
            self.maximumValue = self.slice.min()

        try:

            self.data = 255 * (self.slice - self.minimumValue) / (self.maximumValue - self.minimumValue)
            self.data[self.data >= 255] = 255
            self.data[self.data <= 0] = 0
            self.data = np.array(self.data, dtype=np.uint8)
            self.display_image()

        except:
            pass

    def _setDataVolume(self,dataVolume):
        self.dataShape = dataVolume.shape
        self.dataVolume = dataVolume

        self.maximumValue = self.dataVolume.max()
        self.minimumValue = self.dataVolume.min()

        if (self.currentPlaneSection == 0):
            self.sliceSlider._setRange(0, self.dataShape[0] - 1)
        elif (self.currentPlaneSection == 1):
            self.sliceSlider._setRange(0, self.dataShape[1] - 1)
        elif (self.currentPlaneSection == 2):
            self.sliceSlider._setRange(0, self.dataShape[2] - 1)

        self._changeSlice()
        self.scene.update

    def display_image(self):

        self.flagFirstCircle = True

        self.image = qt.QImage(self.data, self.data.shape[1], self.data.shape[0], self.data.shape[1],qt.QImage.Format_Indexed8)
        self.image.setColorTable(self.colortable)
        pixMap = qt.QPixmap.fromImage(self.image)
        pixItem = qt.QGraphicsPixmapItem(pixMap)
        pixItem.setZValue(-1)
        self.scene.addItem(pixItem)
        self.scene.setSceneRect(0, 0, self.image.width(), self.image.height())
        self.scene.update

    def clickedOnView(self, ddict):
        if ((ddict['event'] == 'MousePressed') or (ddict['event'] == 'RMousePressed')):
            if ddict['event'] == 'MousePressed':
                event = 'MousePressed'
            elif ddict['event'] == 'RMousePressed':
                event = 'RMousePressed'

            x = int(ddict['x'])
            y = int(ddict['y'])
            ddict = {}
            ddict['event'] = event
            if (self.currentPlaneSection == 0):
                z = self.sliceSlider.value()
                ddict['PlaneSection'] = 0
                ddict['x'] = x
                ddict['y'] = y
                ddict['z'] = z
                self.emit(qt.SIGNAL("clickedOnVizualizer"), ddict)

            if (self.currentPlaneSection == 1):
                z = self.sliceSlider.value()
                ddict['PlaneSection'] = 1
                ddict['x'] = x
                ddict['y'] = z
                ddict['z'] = y
                self.emit(qt.SIGNAL("clickedOnVizualizer"), ddict)

            if (self.currentPlaneSection == 2):
                z = self.sliceSlider.value()
                ddict['PlaneSection'] = 2
                ddict['x'] = z
                ddict['y'] = x
                ddict['z'] = y
                self.emit(qt.SIGNAL("clickedOnVizualizer"), ddict)

        if (ddict['event'] == 'MouseMoved'):
            x = int(ddict['x'])
            y = int(ddict['y'])
            ddict = {}
            ddict['event'] = "MouseMoved"

            if (self.currentPlaneSection == 0):
                z = self.sliceSlider.value()
                ddict['PlaneSection'] = 0
                ddict['x'] = x
                ddict['y'] = y
                ddict['z'] = z
                self.emit(qt.SIGNAL("MovedOnVizualizer"), ddict)

            if (self.currentPlaneSection == 1):
                z = self.sliceSlider.value()
                ddict['PlaneSection'] = 1
                ddict['x'] = x
                ddict['y'] = z
                ddict['z'] = y
                self.emit(qt.SIGNAL("MovedOnVizualizer"), ddict)

            if (self.currentPlaneSection == 2):
                z = self.sliceSlider.value()
                ddict['PlaneSection'] = 2
                ddict['x'] = z
                ddict['y'] = x
                ddict['z'] = y
                self.emit(qt.SIGNAL("MovedOnVizualizer"), ddict)


        if (ddict['event'] == 'MouseReleased'):
            x = int(ddict['x'])
            y = int(ddict['y'])
            ddict = {}
            ddict['event'] = "MouseReleased"

            if (self.currentPlaneSection == 0):
                z = self.sliceSlider.value()
                ddict['PlaneSection'] = 0
                ddict['x'] = x
                ddict['y'] = y
                ddict['z'] = z
                self.emit(qt.SIGNAL("releasedOnVizualizer"), ddict)

            if (self.currentPlaneSection == 1):
                z = self.sliceSlider.value()
                ddict['PlaneSection'] = 1
                ddict['x'] = x
                ddict['y'] = z
                ddict['z'] = y
                self.emit(qt.SIGNAL("releasedOnVizualizer"), ddict)

            if (self.currentPlaneSection == 2):
                z = self.sliceSlider.value()
                ddict['PlaneSection'] = 2
                ddict['x'] = z
                ddict['y'] = x
                ddict['z'] = y
                self.emit(qt.SIGNAL("releasedOnVizualizer"), ddict)

    def mouseMoved(self,ddict):
        if (ddict['event'] == 'MouseMoved'):
            x = int(ddict['x'])
            y = int(ddict['y'])
            ddict = {}
            ddict['event'] = "MouseMoved"


            if (self.currentPlaneSection == 0):
                z = self.sliceSlider.value()
                ddict['PlaneSection'] = 0
                ddict['x'] = x
                ddict['y'] = y
                ddict['z'] = z
                self.emit(qt.SIGNAL("movedOnVizualizer"), ddict)

            if (self.currentPlaneSection == 1):
                z = self.sliceSlider.value()
                ddict['PlaneSection'] = 1
                ddict['x'] = x
                ddict['y'] = z
                ddict['z'] = y
                self.emit(qt.SIGNAL("movedOnVizualizer"), ddict)

            if (self.currentPlaneSection == 2):
                z = self.sliceSlider.value()
                ddict['PlaneSection'] = 2
                ddict['x'] = z
                ddict['y'] = x
                ddict['z'] = y
                self.emit(qt.SIGNAL("movedOnVizualizer"), ddict)

    def drawEllipse(self,x,y,r):

        self.Item = qt.QGraphicsEllipseItem(x-r/2,y-r/2,r,r)
        self.Item.setFlag(qt.QGraphicsItem.ItemIsMovable)

        pen = qt.QPen(qt.Qt.blue)
        pen.setWidth( 3 )
        brush = qt.QBrush(qt.QColor(0xFF, 0, 0, 0x00))
        self.Item.setBrush(brush)
        self.Item.setPen(pen)
        self.scene.addItem(self.Item)


    def drawPoint(self, x, y):
        self.scene.addRect(x, y, 4, 4, qt.Qt.black, qt.QBrush(qt.Qt.red))
        self.scene.update

    def drawPoly(self,listCoord):

        pr_coord = listCoord[0]
        
        for i, coord in enumerate(listCoord):
            if i != 0:
                self.scene.addLine(coord[0], coord[1],pr_coord[0], pr_coord[1],qt.Qt.green)

            pr_coord = coord

        self.scene.addLine(listCoord[0][0], listCoord[0][1],listCoord[-1][0], listCoord[-1][1],qt.Qt.green)
        self.scene.update

    def drawPointPolygon(self,x,y,FlagEnd):
        
        if not FlagEnd:
            self.posPolyPoints.append([x,y])

            if len(self.posPolyPoints) > 1:

                self.scene.addLine(x, y, self.posPolyPoints[-2][0], self.posPolyPoints[-2][1],qt.Qt.green)
        else :
            self.scene.addLine(self.posPolyPoints[0][0], self.posPolyPoints[-0][1], self.posPolyPoints[-1][0], self.posPolyPoints[-1][1],qt.Qt.green)

        self.scene.update

    def drawArrow(self, x1, y1,x2,y2):
        self.scene.addLine(x1, y1, x2, y2,qt.Qt.yellow)
        self.scene.addRect(x2-0.5, y2-0.5, 1, 1,qt.Qt.yellow, qt.Qt.yellow)
        self.scene.update

    def drawRect(self, x1, y1,x2,y2):
        self.scene.addLine(x1, y1, x2, y1,qt.Qt.red)
        self.scene.addLine(x1, y1, x1, y2,qt.Qt.red)
        self.scene.addLine(x1, y2, x2, y2,qt.Qt.red)
        self.scene.addLine(x2, y1, x2, y2,qt.Qt.red)
        self.scene.update

    def changeSelectorToRuberband(self):
        self.view.setDragMode(qt.QGraphicsView.RubberBandDrag)
        self.view.FlagWheellEvent = True

    def changeSelectorToPointer(self):
        self.view.setDragMode(qt.QGraphicsView.NoDrag)
        self.view.FlagWheellEvent = True

    def changeSelectorToCircle(self):
        self.view.setDragMode(qt.QGraphicsView.NoDrag)
        self.view.FlagWheellEvent = False

    def changeSelectorToBrush(self):
        self.view.setDragMode(qt.QGraphicsView.NoDrag)


    def changeColorMap(self, R, G, B):
        if len(R) != 256 or len(G) != 256 or len(B) != 256:
            print "Wrong Color Array shape"
        else:
            self.colortable = []
            for i in range(256):
                self.colortable.append(qt.qRgb(R[i], G[i], B[i]))


class Interactor3D(qt.QWidget):
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)

        self.toolBar = CustomToolBar(self)

        self.axialWidget = SliceVisualizer(0)
        self.coronalWidget = SliceVisualizer(1)
        self.sagittalWidget = SliceVisualizer(2)

        self.Items = {'Seeds':{'Direction0':[],'Direction1':[],'Direction2':[]},\
        'Zones':{'Direction0':[],'Direction1':[],'Direction2':[]},\
        'Circles':{'Direction0':[],'Direction1':[],'Direction2':[]},\
        'Poly':{'Direction0':[],'Direction1':[],'Direction2':[]}}

        layoutTop = qt.QHBoxLayout()
        layoutTop.addWidget(self.toolBar)

        layout = qt.QVBoxLayout()
        layout.addLayout(layoutTop)

        splitterVertical = qt.QSplitter(self)
        splitterAxialCoronal = qt.QSplitter(0, self)

        splitterVertical.addWidget(self.axialWidget)
        splitterAxialCoronal.addWidget(self.sagittalWidget)
        splitterAxialCoronal.addWidget(self.coronalWidget)
        splitterVertical.addWidget(splitterAxialCoronal)
        layout.addWidget(splitterVertical)


        self.toolBar.doubleSlider.sigDoubleSliderValueChanged.connect( self.axialWidget._doubleSliderValueChanged)
        self.toolBar.doubleSlider.sigDoubleSliderValueChanged.connect( self.coronalWidget._doubleSliderValueChanged)
        self.toolBar.doubleSlider.sigDoubleSliderValueChanged.connect( self.sagittalWidget._doubleSliderValueChanged)

        qt.QObject.connect(self.toolBar.zoomAutoAction, qt.SIGNAL("triggered()"), self.axialWidget.view.autofit)
        qt.QObject.connect(self.toolBar.zoomAutoAction, qt.SIGNAL("triggered()"), self.coronalWidget.view.autofit)
        qt.QObject.connect(self.toolBar.zoomAutoAction, qt.SIGNAL("triggered()"), self.sagittalWidget.view.autofit)

        qt.QObject.connect(self.toolBar.zone1Action, qt.SIGNAL("triggered()"),self.axialWidget.changeSelectorToRuberband)
        qt.QObject.connect(self.toolBar.zone1Action, qt.SIGNAL("triggered()"),self.coronalWidget.changeSelectorToRuberband)
        qt.QObject.connect(self.toolBar.zone1Action, qt.SIGNAL("triggered()"),self.sagittalWidget.changeSelectorToRuberband)

        qt.QObject.connect(self.toolBar.drawingAction, qt.SIGNAL("triggered()"), self.axialWidget.changeSelectorToCircle)
        qt.QObject.connect(self.toolBar.drawingAction, qt.SIGNAL("triggered()"), self.coronalWidget.changeSelectorToCircle)
        qt.QObject.connect(self.toolBar.drawingAction, qt.SIGNAL("triggered()"), self.sagittalWidget.changeSelectorToCircle)

        qt.QObject.connect(self.toolBar.pointerAction, qt.SIGNAL("triggered()"),self.axialWidget.changeSelectorToPointer)
        qt.QObject.connect(self.toolBar.pointerAction, qt.SIGNAL("triggered()"), self.coronalWidget.changeSelectorToPointer)
        qt.QObject.connect(self.toolBar.pointerAction, qt.SIGNAL("triggered()"), self.sagittalWidget.changeSelectorToPointer)

        self.connect(self.toolBar.colorChoice, qt.SIGNAL("currentIndexChanged(int)"), self._colorMapChanged)

        self.setLayout(layout)

    def _setDataVolume(self, dataVolume):
        self.dataShape = dataVolume.shape
        self.dataVolume = dataVolume
        self.maximumValue = self.dataVolume.max()* 2.0

        self.minimumValue = self.dataVolume.min()
        maxValue3Char = '%3.3f' % self.maximumValue
        minValue3Char = '%3.3f' % self.minimumValue
        self.toolBar.setMinAndMaxToolBar(float(minValue3Char), float(maxValue3Char))
        self.axialWidget._setDataVolume(self.dataVolume)
        self.coronalWidget._setDataVolume(self.dataVolume)
        self.sagittalWidget._setDataVolume(self.dataVolume)

    def updateItems(self,items):

        self.Items = items

        self.axialWidget.updateItems(self.Items)
        self.coronalWidget.updateItems(self.Items)
        self.sagittalWidget.updateItems(self.Items)

        self.axialWidget._changeSlice()
        self.coronalWidget._changeSlice()
        self.sagittalWidget._changeSlice()

    def _axialViewClicked(self, ddict):
        x = int(ddict['x'])
        y = int(ddict['y'])
        ddict = {}
        z = self.axialWidget.sliceSlider.value()
        ddict['event'] = "MousePressed"
        ddict['x'] = x
        ddict['y'] = y
        ddict['z'] = z
        self.emit(qt.SIGNAL("CustomGraphicsViewEvent"), ddict)

    def drawRectangleOnThreePlanes(self,x1,x2,y1,y2,z1,z2):

        if (z1 == z2) and (self.axialWidget.sliceSlider.value() == z1):
            self.axialWidget.drawRect(x1,x2,y1,y2)

        if (y1 == y2)and (self.coronalWidget.sliceSlider.value() == y1):
            self.coronalWidget.drawRect(x1,x2,z1,z2)

        if (x1 == x2)and (self.sagittalWidget.sliceSlider.value() == x1):
            self.sagittalWidget.drawRect(y1,y2,z1,z2)

    def drawPointOnThreePlanes(self, x, y, z):
        if (self.axialWidget.sliceSlider.value() == z):
            self.axialWidget.drawPoint(x, y)

        if (self.coronalWidget.sliceSlider.value() == y):
            self.coronalWidget.drawPoint(x, z)

        if (self.sagittalWidget.sliceSlider.value() == x):
            self.sagittalWidget.drawPoint(y, z)

    def drawpolygonOnThreePlanes(self,x,y,z,FlagEnd):
        if (self.axialWidget.sliceSlider.value() == z):
            self.axialWidget.drawPointPolygon(x, y,FlagEnd)

        if (self.coronalWidget.sliceSlider.value() == y):
            self.coronalWidget.drawPointPolygon(x, z,FlagEnd)

        if (self.sagittalWidget.sliceSlider.value() == x):
            self.sagittalWidget.drawPointPolygon(y, z,FlagEnd)

    def drawEllipseOnThreePlanes(self,x,y,z):
        if (self.axialWidget.sliceSlider.value() == z):
            self.axialWidget.drawEllipse(x, y)

        if (self.coronalWidget.sliceSlider.value() == y):
            self.coronalWidget.drawEllipse(x, z)

        if (self.sagittalWidget.sliceSlider.value() == x):
            self.sagittalWidget.drawEllipse(y, z)

    def PaintOnThreePlanes(self,x, y, z):
        if (self.axialWidget.sliceSlider.value() == z):
            self.axialWidget.brush(x, y,self.toolBar.boxSizeBrush.value())

        if (self.coronalWidget.sliceSlider.value() == y):
            self.coronalWidget.brush(x, z,self.toolBar.boxSizeBrush.value())

        if (self.sagittalWidget.sliceSlider.value() == x):
            self.sagittalWidget.brush(y, z, self.toolBar.boxSizeBrush.value())

    def _autofit(self):
        self.axialWidget.view.autofit()
        self.sagittalWidget.view.autofit()
        self.coronalWidget.view.autofit()
    
    def _colorMapChanged(self):

        colorMapToDisplay = self.toolBar.colormapList[self.toolBar.colorChoice.currentIndex()]
        self.axialWidget.changeColorMap(colorMapToDisplay[1], colorMapToDisplay[2], colorMapToDisplay[3])
        self.coronalWidget.changeColorMap(colorMapToDisplay[1], colorMapToDisplay[2], colorMapToDisplay[3])
        self.sagittalWidget.changeColorMap(colorMapToDisplay[1], colorMapToDisplay[2], colorMapToDisplay[3])

        self.axialWidget._changeSlice()
        self.coronalWidget._changeSlice()
        self.sagittalWidget._changeSlice()