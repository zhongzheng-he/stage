# -*- coding: utf-8 -*-
from PyMca import PyMcaQt as qt

class LabelEditAndButton(qt.QWidget) :

    def __init__(self,boolLabel=True,textLabel="text1",booltextEdit=True,textEdit="text2", boolButton=True,textButton="Browse...", parent=None) :
        qt.QWidget.__init__(self, parent)
        self.textLabel=textLabel
        self.textEdit=textEdit
        self.textButton=textButton;
        self.boolLabel=boolLabel
        self.booltextEdit=booltextEdit
        self.boolButton=boolButton

        self._build()

    def _build(self) :
        self.layout=qt.QHBoxLayout()
        self.label =None
        self.lineEdit =None
        self.button =None
        if(self.boolLabel) :
            self.label=qt.QLabel(self.textLabel,self)
            self.layout.addWidget(self.label)
        if(self.booltextEdit) :
            self.lineEdit= qt.QLineEdit(self.textEdit,self)
            self.layout.addWidget(self.lineEdit)

        if(self.boolButton) :
            self.button=qt.QPushButton(self.textButton,self)
            self.layout.addWidget(self.button)
            self.connect(self.button,qt.SIGNAL("clicked()"),self.buttonPushed)

        self.setLayout(self.layout)

    def changeLabel(self,textLabel):
        self.textLabel=textLabel
        self.label.setText(self.textLabel)

    def changeLineEdit(self,textLineEit):
        self.textEdit=textLineEit
        self.lineEdit.setText(self.textEdit)

    def valueLineEdit(self):
        self.textEdit=self.lineEdit.text()
        return self.textEdit

    def buttonPushed(self):
        self.resultFileName = str(qt.QFileDialog.getSaveFileName(self, "Save 3D volume snapshots ", self.textEdit))
        self.lineEdit.setText(self.resultFileName)
        self.textEdit = self.resultFileName
        return self.textEdit
