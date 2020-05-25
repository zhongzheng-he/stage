# -*- coding: utf-8 -*-

import os
from PyMca import EdfFile,TiffIO
import numpy as np
import matplotlib.image as mpimg
import dicom as dicom
import scipy.io as sio

import ImageProcessing as IP


class STLReader():

    def __init__(self,filename):

           self.fileName = filename

    def data(self):
         data = IP.importSTL(self.fileName)
         return data

class MatReader():
    def __init__(self,filename):
        self.fileName = filename
        self.info = {}

        self.seriesDescription = []
        self.seriesImageSize = {}

    def getListScan(self):
        self.dicmat = sio.loadmat(self.fileName)
        return self.dicmat.keys()

class DicomReader():
    def __init__(self,filesname):
        self.filesName = filesname
        self.info = {}

        self.seriesDescription = []
        self.seriesImageSize = {}
        self.pixel_size = [1,1,1]

    def getListScan(self):

        self.filesName.sort()
        if len(self.filesName) > 1:
            fieldsToTest = ['SeriesDescription','PixelSpacing', 'Columns','Rows']
            for fileName in self.filesName:
                image=dicom.read_file(fileName,stop_before_pixels=True )
                if all(keyTT in image for keyTT in fieldsToTest):
                    if  not image.SeriesDescription in self.seriesDescription:
                        self.seriesDescription.append(image.SeriesDescription)
                        self.pixel_size[0] = abs(float(image.SpacingBetweenSlices))
                        self.pixel_size[1] = abs(float(image.PixelSpacing[0]))
                        self.pixel_size[2] = abs(float(image.PixelSpacing[1]))
                        self.seriesImageSize[image.SeriesDescription] = [1,int(image.Rows),int(image.Columns)]
                    else:
                        self.seriesImageSize[image.SeriesDescription][0] +=1


        else:
            self.seriesDescription = []
            image=dicom.read_file(self.filesName[0])
            self.pixel_size[0] = abs(float(image.SpacingBetweenSlices))
            self.pixel_size[1] = abs(float(image.PixelSpacing[0]))
            self.pixel_size[2] = abs(float(image.PixelSpacing[1]))
            self.data = image.pixel_array
        return self.seriesDescription


    def importScan(self,scanToImport):
        self.scanToImport = scanToImport
        self.inputData = {}

        for scan in self.scanToImport:
            arrayToImport = np.zeros((self.seriesImageSize[scan][0],self.seriesImageSize[scan][1],self.seriesImageSize[scan][2]), np.float32)
            self.inputData[scan]  = arrayToImport

        for fileName in self.filesName:
            image=dicom.read_file(fileName,stop_before_pixels=True )
            
            if  not image.SeriesDescription in self.info:
                self.info[image.SeriesDescription] = image

            if image.SeriesDescription in self.scanToImport:
                image=dicom.read_file(fileName)
                self.inputData[image.SeriesDescription][image.InstanceNumber-1,:,:] = image.pixel_array


        for scan in self.scanToImport:
            while np.all(self.inputData[scan][0]==0):
                self.inputData[scan]=np.delete(self.inputData[scan],0,0)
            while np.all(self.inputData[scan][self.inputData[scan].shape[0]-1]==0) and self.inputData[scan].shape[0]>1:
                self.inputData[scan]=np.delete(self.inputData[scan],-1,0)
        return self.inputData


class ImageReader(object) :

    def __init__(self,filename,access=None,format='edf') :
        self.fileName = filename
        self.File = 0
        self.width=0
        self.height=0
        self.data=None
        self.slice=None
        self.File = open(self.fileName, access)
        self.dtype=np.float32

    def getData(self) :

        if(self.fileName.endswith('.raw') or self.fileName.endswith('.RAW') or self.fileName.endswith('.img')) :
            File = open(str(self.fileName),"rb")
            size = os.path.getsize(str(self.fileName)) / 4.
            self.width=int(size**.5)
            self.height=self.width
            self.currentSlice = np.fromfile(File,dtype='<f4')
            self.currentSlice.resize(self.height,self.width)

        elif(self.fileName.endswith('.edf') or self.fileName.endswith('.EDF') ) :
            fileEdf = EdfFile.EdfFile(str(self.fileName),access='rb')
            self.currentSlice = fileEdf.GetData(0)

        elif(self.fileName.endswith('.DOWN') or self.fileName.endswith('.UP') ) :
            fileEdf = EdfFile.EdfFile(str(self.fileName),access='rb')
            self.currentSlice = fileEdf.GetData(0)


        elif(self.fileName.endswith('.tif') or self.fileName.endswith('.TIF') or self.fileName.endswith('.TIFF') or self.fileName.endswith('.tiff')) :
            fileTif=TiffIO.TiffIO(str(self.fileName), mode ='rb')
            self.currentSlice =fileTif.getImage(0)

        elif(self.fileName.endswith('.png') or self.fileName.endswith('.PNG')):
            filePng= mpimg.imread(self.fileName)
            self.currentSlice = filePng

        elif(self.fileName.endswith('.dcm') or self.fileName.endswith('.DCM') ) :
            image=dicom.read_file(str(self.fileName))

            self.currentSlice =image.pixel_array

        elif(self.fileName.endswith('.mat') or self.fileName.endswith('.MAT') ) :
            image = sio.loadmat(self.fileName)
            self.currentSlice = image[image.keys()[0].keys()[0]]

        else:
            image=dicom.read_file(str(self.fileName))

            self.currentSlice =image

        return self.currentSlice
