from PyMca import PyMcaQt as qt


class CustomGraphicsView(qt.QGraphicsView):
    def __init__(self, scene, parent):
        
        '''
        Constructor
        '''
        self.scene = scene
        qt.QGraphicsView.__init__(self, scene, parent)
        self.setMouseTracking(True)
        self.setBackgroundBrush(qt.Qt.black);
        self.setAcceptDrops(True)
        self.setRenderHints(qt.QPainter.Antialiasing | qt.QPainter.SmoothPixmapTransform);
        self.zoomScale = 1
        self.FlagWheellEvent = True

    def mousePressEvent(self, event):

        if (event.button() == qt.Qt.LeftButton):
            dx = event.pos().x()
            dy = event.pos().y()
            clickPosition = self.mapToScene(dx, dy)
 
            ddict = {}
            ddict['event'] = "MousePressed"
            ddict['x'] = clickPosition.x()
            ddict['y'] = clickPosition.y()

        if (event.button() == qt.Qt.RightButton):
            dx = event.pos().x()
            dy = event.pos().y()

            clickPosition = self.mapToScene(dx, dy)
            ddict = {}
            ddict['event'] = "RMousePressed"
            ddict['x'] = clickPosition.x()
            ddict['y'] = clickPosition.y()

        self.emit(qt.SIGNAL("CustomGraphicsViewEvent"), ddict)

        return qt.QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if (event.button() == qt.Qt.NoButton):
            dx = event.pos().x()
            dy = event.pos().y()

            clickPosition = self.mapToScene(dx, dy)
            ddict = {}
            ddict['event'] = "MouseMoved"
            ddict['x'] = clickPosition.x()
            ddict['y'] = clickPosition.y()

            self.emit(qt.SIGNAL("CustomGraphicsViewEvent"), ddict)

        return qt.QGraphicsView.mouseMoveEvent(self, event) # <-- added this line.


    def mouseReleaseEvent(self, event):

        if (event.button() == qt.Qt.LeftButton):
            dx = event.pos().x()
            dy = event.pos().y()

            clickPosition = self.mapToScene(dx, dy)
            ddict = {}
            ddict['event'] = "MouseReleased"
            ddict['x'] = clickPosition.x()
            ddict['y'] = clickPosition.y()

            self.emit(qt.SIGNAL("CustomGraphicsViewEvent"), ddict)

        return qt.QGraphicsView.mouseReleaseEvent(self, event)

    def wheelEvent(self, event):

        delta = event.delta()

        if (delta < 0):
            factor = 2. ** (float(event.delta()) / 440.)
        else:
            factor = 2. ** (float(event.delta()) / 440.)

        self.zoomScale *= factor
        self.setTransformationAnchor(qt.QGraphicsView.AnchorUnderMouse)
        self.scale(factor, factor)

    def autofit(self):
        self.zoomScale = 1
        self.fitInView(self.scene.sceneRect(), qt.Qt.KeepAspectRatio)
