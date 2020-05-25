from PyMca import PyMcaQt as qt


class SliderAndLabel(qt.QWidget):
    def __init__(self,parent=None, Orientation=1) :
        qt.QWidget.__init__(self, parent)
        self.slider=qt.QSlider(1)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.Label=qt.QLabel("0")
        self.Label.setFixedSize(45,45)
        self.layout=qt.QHBoxLayout()
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.Label)
        self._changeLabel()
        self.connect(self.slider,qt.SIGNAL("valueChanged(int)"),self._changeLabel)
        self.setLayout(self.layout)

    def _changeLabel(self):
        self.Label.setText(str(self.slider.value()))

    def _setOrientation(self):
        self.slider.setOrientation(1)

    def _setRange(self,mini,maxi):
        self.slider.setMinimum(mini)
        self.slider.setValue(mini)
        self.slider.setMaximum(maxi)
        self._changeLabel();

    def value(self):
        return self.slider.value()

class SliderAndLabelSpecificScale(qt.QWidget):
    def __init__(self,parent=None, Orientation=1) :
        qt.QWidget.__init__(self, parent)
        self.slider=qt.QSlider(1)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.Coef = 1.0
        self.Label=qt.QLabel("0")
        self.Label.setFixedSize(45,10)
        self.layout=qt.QHBoxLayout()
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.Label)
        self._changeLabel()
        self.connect(self.slider,qt.SIGNAL("valueChanged(int)"),self._changeLabel)
        self.setLayout(self.layout)

    def _changeLabel(self):
        self.Label.setText(str(self.slider.value()/self.Coef))

    def _setStepPrecision(self,Pres):
        self.Coef = 1.0/Pres

    def _defaultValue(self,Value):
        self.slider.setValue(Value*self.Coef)
        self._changeLabel()

    def _setOrientation(self):
        self.slider.setOrientation(1)

    def _setRange(self,mini,maxi):
        self.slider.setMinimum(mini*self.Coef)
        self.slider.setMaximum(maxi*self.Coef)
        self._changeLabel()

    def value(self):
        return self.slider.value() / self.Coef