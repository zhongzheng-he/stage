
from PyMca import PyMcaQt as qt

class OutputDialog(qt.QDialog) :
    def __init__(self, parent=None):
        qt.QDialog.__init__(self, parent)
        self.label = qt.QLabel('Please Select Output File Format : ')
        self.outputImageFormat = qt.QComboBox(self)
        self.outputImageFormat.addItem("EDF")
        self.outputImageFormat.addItem("Tiff")
        self.outputImageFormat.addItem("Dicom")
        self.outputImageFormat.addItem("Numpy")
        self.outputImageFormat.addItem("Matlab")
        self.outputImageFormat.addItem("PNG")
  
        buttonBox = qt.QDialogButtonBox(qt.QDialogButtonBox.Ok | qt.QDialogButtonBox.Cancel);

        qt.QObject.connect(buttonBox, qt.SIGNAL('accepted()'), self.accept);
        qt.QObject.connect(buttonBox, qt.SIGNAL('rejected()'), self.reject);
        self.mainLayout = qt.QGridLayout()
        self.mainLayout.addWidget(self.label, 0, 0)
        self.mainLayout.addWidget(self.outputImageFormat, 0, 1)
        self.mainLayout.addWidget(buttonBox, 1, 1)
        self.setLayout(self.mainLayout)

