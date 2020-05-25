# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from ImageWritter import ImageWritter
from PyMca import PyMcaQt as qt




class ExportThread(qt.QThread):

    def __init__(self,files,imageStack,extension,parent):

        qt.QThread.__init__(self, parent)

        self.daddy=parent
        self.outputFiles=files
        self.dataToSave = imageStack
        self.extension = extension

    def run(self):


        if self.extension == '.mat':
            filename = self.outputFiles +  self.extension
            writter = ImageWritter(filename, self.dataToSave)
            writter.writeData()
        else:
            for i in range(0,self.dataToSave.shape[0]-1) :

                image = self.dataToSave[i,:,:]
                filename = self.outputFiles + '%4.4d' % i + self.extension
                writter = ImageWritter(filename, image)
                writter.writeData()
                self.emit(qt.SIGNAL("Progress"), i)
#

