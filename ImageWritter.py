# -*- coding: utf-8 -*-


from PyMca import EdfFile,TiffIO
import numpy as np
import scipy.io as sio
import scipy

class ImageWritter(object) : 

	def __init__(self,filename,data) : 
		
		self.fileName = filename

		self.data=data
		self.slice=None

	def writeData(self) : 
			
		if self.fileName.endswith('.edf')  : 
			fileEdf = EdfFile.EdfFile(self.fileName, access='wb')
			fileEdf.WriteImage({}, self.data)
			print fileEdf

		if self.fileName.endswith('.mat')  : 
			print 'fdkjfkds' 
			NameFile = self.fileName.split('/')[-1]
			NameFile = NameFile.split('.')[0]
			print self.fileName
			sio.savemat(self.fileName,{NameFile:self.data})

			
		if self.fileName.endswith('.tiff')  : 
			tifImage = TiffIO.TiffIO(self.fileName, 'wb+')
			tifImage.writeImage(self.data)
   
   		if self.fileName.endswith('.png')  : 
			scipy.misc.imsave(self.fileName, self.data)
			
		if self.fileName.endswith('.dcm')  : 
			print 'To Be Implemented' 
			
		if self.fileName.endswith('.npy')  : 
			np.save( self.fileName, self.data)
