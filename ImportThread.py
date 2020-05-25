# -*- coding: utf-8 -*-
from PyMca import PyMcaQt as qt
import os
import numpy as np


from ImageReader import ImageReader



class ImportThread(qt.QThread):

    def __init__(self,files,parent):

        qt.QThread.__init__(self, parent)

        self.daddy=parent
        self.inputFiles=files
    def run(self):
        self.FileReference = str(self.inputFiles[0])
        self.inputDir = os.path.dirname(self.FileReference)

        image = ImageReader(self.FileReference, 'rb')

        data = image.getData()
        self.shapeReference = data.shape
        typeImage = data.dtype
        self.inputData = np.zeros((len(self.inputFiles), self.shapeReference[0], self.shapeReference[1]), dtype= typeImage)

        i = 0
        for filename in self.inputFiles :
            filename = str(filename)
            image = ImageReader(filename, 'rb')
            data = image.getData()

            if (data.ndim == 2):
                self.inputData[i, :, :] = data
            else:
                self.inputData[i, :, :] = data[:,:,0]

            i += 1
            self.emit(qt.SIGNAL("Progress"), i)


class ImportNo():

    def __init__(self,files):

        self.inputFiles=files
        self.FileReference = str(self.inputFiles[0])
        self.inputDir = os.path.dirname(self.FileReference)

        image = ImageReader(self.FileReference, 'rb')

        data = image.getData()
        self.shapeReference = data.shape
        typeImage = data.dtype
        self.inputData = np.zeros((len(self.inputFiles), self.shapeReference[0], self.shapeReference[1]), dtype= typeImage)

        i = 0
        for filename in self.inputFiles :
            filename = str(filename)
            image = ImageReader(filename, 'rb')
            data = image.getData()
            self.inputData[i, :, :] = data
            i += 1
