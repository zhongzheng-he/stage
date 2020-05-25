# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 17:55:36 2017

@author: broche
"""

from PyMca import PyMcaQt as qt



class TitleAndIcones(qt.QWidget) :

    def __init__(self,boolTitle=True,textTitle="text1", boolIcons=True, pathIcon1 = '',pathIcon2 = '',pathIcon3 = '',parent=None) :
        qt.QWidget.__init__(self, parent)
        self.textTitle=textTitle
        self.boolTitle=boolTitle
        self.boolIcons=boolIcons
        self.pathIcon1 = pathIcon1
        self.pathIcon2 = pathIcon2
        self.pathIcon3 = pathIcon3
        self._build()

    def _build(self) :
        self.layout=qt.QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.label = None
        self.button =None
        if(self.boolTitle) :
            self.label=qt.QLabel(self.textTitle,self)
            self.label.setMinimumWidth(200)
            self.layout.addWidget(self.label)
        if(self.boolIcons) :
            self.save=qt.QPushButton()
            self.saveas=qt.QPushButton()
            self.load=qt.QPushButton()

            self.save.setMaximumWidth(30)
            self.saveas.setMaximumWidth(30)
            self.load.setMaximumWidth(30)
            self.save.setMaximumHeight(30)
            self.saveas.setMaximumHeight(30)
            self.load.setMaximumHeight(30)


            self.save.setFlat(True)
            self.saveas.setFlat(True)
            self.load.setFlat(True)

            if self.pathIcon1 != '':
                self.save.setIcon(qt.QIcon(qt.QPixmap(self.pathIcon1)))

            if self.pathIcon2 != '':
                self.saveas.setIcon(qt.QIcon(qt.QPixmap(self.pathIcon2)))

            if self.pathIcon3 != '':
                self.load.setIcon(qt.QIcon(qt.QPixmap(self.pathIcon3)))

            self.layout.addWidget(self.save)
            self.layout.addWidget(self.saveas)
            self.layout.addWidget(self.load)


        self.setLayout(self.layout)

    def changeLabel(self,textTitle):
        self.textTitle=textTitle
        self.label.setText(self.textTitle)



